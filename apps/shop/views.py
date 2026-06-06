"""
SIBRAH Shop App — Views
apps/shop/views.py
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.conf import settings
from django.core.mail import send_mail
from urllib.parse import quote
from .models import Product, ProductCategory, Order, OrderItem
from .forms import OrderForm


def shop_home(request):
    categories = ProductCategory.objects.all()
    products   = Product.objects.filter(is_active=True)
    cat_slug   = request.GET.get('category', '')
    if cat_slug:
        products = products.filter(category__slug=cat_slug)
    return render(request, 'shop/shop_home.html', {
        'products':   products,
        'categories': categories,
        'active_cat': cat_slug,
        'company':    settings.SIBRAH_COMPANY,
    })


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, is_active=True)
    related = Product.objects.filter(
        category=product.category, is_active=True
    ).exclude(pk=product.pk)[:4]
    return render(request, 'shop/product_detail.html', {
        'product': product,
        'related': related,
        'company': settings.SIBRAH_COMPANY,
    })


def place_order(request, slug):
    product = get_object_or_404(Product, slug=slug, is_active=True)
    if not product.in_stock:
        messages.error(request, "Sorry, this product is currently out of stock.")
        return redirect('shop:shop_home')

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = Order(
                customer_name    = form.cleaned_data['customer_name'],
                customer_email   = form.cleaned_data['customer_email'],
                customer_phone   = form.cleaned_data['customer_phone'],
                delivery_address = form.cleaned_data.get('delivery_address', ''),
                notes            = form.cleaned_data.get('notes', ''),
                total_amount     = product.price,
                status           = 'pending',
            )
            if request.user.is_authenticated:
                order.customer = request.user
            order.save()

            OrderItem.objects.create(
                order    = order,
                product  = product,
                name     = product.name,
                price    = product.price,
                quantity = 1,
            )

            # Send order confirmation email to customer
            _send_order_confirmation_email(order)

            # Notify SIBRAH admin
            _notify_admin_new_order(order)

            messages.success(request,
                f"Order #{order.order_number} placed! "
                "A confirmation email has been sent to you. "
                "Please complete payment to confirm your order.")
            return redirect('shop:order_payment', pk=order.pk)
        else:
            messages.error(request, "Please fill in all required fields.")
    else:
        form = OrderForm()
        if request.user.is_authenticated:
            form.initial = {
                'customer_name':  request.user.get_full_name() or request.user.username,
                'customer_email': request.user.email,
                'customer_phone': getattr(request.user, 'phone', ''),
            }

    return render(request, 'shop/place_order.html', {
        'product': product,
        'form':    form,
        'company': settings.SIBRAH_COMPANY,
    })


def order_payment(request, pk):
    order = get_object_or_404(Order, pk=pk)
    ref   = f"SIBRAH-{order.order_number}"

    if request.method == 'POST':
        proof     = request.FILES.get('payment_proof')
        ref_input = request.POST.get('payment_ref', '').strip()
        if proof:
            order.payment_proof = proof
            order.payment_ref   = ref_input
            order.save()

            # Notify admin that proof was submitted
            _notify_admin_payment_proof(order)

            messages.success(request,
                "Payment proof received! We will confirm your order within 2 hours. "
                "You can track your order status at the Order Tracking page.")
            return redirect('shop:order_success', pk=order.pk)
        messages.error(request, "Please upload your payment proof screenshot.")

    wa_text = (
        f"Hello SIBRAH,\n\n"
        f"I would like to confirm payment for:\n"
        f"Order: #{order.order_number}\n"
        f"Amount: \u20A6{order.total_amount:,.0f}\n"
        f"Reference: {ref}\n\n"
        f"Please confirm my order. Thank you!"
    )
    whatsapp_msg = quote(wa_text)

    return render(request, 'shop/order_payment.html', {
        'order':        order,
        'ref':          ref,
        'whatsapp_msg': whatsapp_msg,
        'company':      settings.SIBRAH_COMPANY,
    })


def order_success(request, pk):
    order = get_object_or_404(Order, pk=pk)
    return render(request, 'shop/order_success.html', {
        'order':   order,
        'company': settings.SIBRAH_COMPANY,
    })


def track_order(request):
    """Public order tracking — no login required."""
    order                  = None
    cancelled              = False
    searched               = False
    searched_order_number  = ''
    searched_identifier    = ''

    if request.method == 'POST':
        searched              = True
        searched_order_number = request.POST.get('order_number', '').strip().upper()
        searched_identifier   = request.POST.get('identifier', '').strip().lower()

        if searched_order_number and searched_identifier:
            try:
                found = Order.objects.get(order_number=searched_order_number)
                # Verify identity — match email OR phone
                email_match = found.customer_email.lower() == searched_identifier
                phone_match = found.customer_phone.replace(' ', '') == searched_identifier.replace(' ', '')

                if email_match or phone_match:
                    if found.status == 'cancelled':
                        cancelled = True
                    else:
                        order = found
                # If no match, order stays None → "not found" shown
            except Order.DoesNotExist:
                pass  # order stays None

    return render(request, 'shop/order_tracking.html', {
        'order':                 order,
        'cancelled':             cancelled,
        'searched':              searched,
        'searched_order_number': searched_order_number,
        'searched_identifier':   searched_identifier,
        'company':               settings.SIBRAH_COMPANY,
    })


# ── EMAIL HELPERS ─────────────────────────────────────────────────────

def _send_order_confirmation_email(order):
    """Send order confirmation to customer after placing order."""
    items_text = "\n".join(
        [f"  - {item.quantity}x {item.name} — \u20A6{item.subtotal:,.0f}"
         for item in order.items.all()]
    )
    subject = f"Order Confirmation — #{order.order_number} | SIBRAH Technology Hub"
    message = f"""
Dear {order.customer_name},

Thank you for your order! We have received it and are awaiting your payment.

━━━━━━━━━━━━━━━━━━━━━━━━
ORDER DETAILS
━━━━━━━━━━━━━━━━━━━━━━━━
Order Number : #{order.order_number}
Date         : {order.created_at.strftime('%B %d, %Y')}

Items:
{items_text}

Total Amount : \u20A6{order.total_amount:,.0f}

━━━━━━━━━━━━━━━━━━━━━━━━
PAYMENT INSTRUCTIONS
━━━━━━━━━━━━━━━━━━━━━━━━
Bank         : ACCESS BANK
Account Name : IBRAHIM BABA SULEIMAN
Account No   : 1227425306
Amount       : \u20A6{order.total_amount:,.0f}
Reference    : SIBRAH-{order.order_number}

After payment, send your receipt to:
WhatsApp: +234 808 110 1992

━━━━━━━━━━━━━━━━━━━━━━━━
TRACK YOUR ORDER
━━━━━━━━━━━━━━━━━━━━━━━━
You can check your order status anytime at:
http://127.0.0.1:8000/shop/track/

Use your Order Number: #{order.order_number}
And your email: {order.customer_email}

━━━━━━━━━━━━━━━━━━━━━━━━

If you have any questions, contact us:
Phone/WhatsApp : +234 808 110 1992
Email          : info@sibrahtech.com.ng

Thank you for choosing SIBRAH Computers & Technology Hub!

Best regards,
SIBRAH Technology Hub Team
Abuja, Nigeria
"""
    try:
        send_mail(
            subject        = subject,
            message        = message,
            from_email     = settings.DEFAULT_FROM_EMAIL,
            recipient_list = [order.customer_email],
            fail_silently  = True,
        )
    except Exception:
        pass


def _notify_admin_new_order(order):
    """Notify SIBRAH admin when a new order is placed."""
    items_text = "\n".join(
        [f"  - {item.quantity}x {item.name} — \u20A6{item.subtotal:,.0f}"
         for item in order.items.all()]
    )
    subject = f"[NEW ORDER] #{order.order_number} — {order.customer_name}"
    message = f"""
NEW ORDER RECEIVED!

━━━━━━━━━━━━━━━━━━━━━━━━
Customer   : {order.customer_name}
Phone      : {order.customer_phone}
Email      : {order.customer_email}
Address    : {order.delivery_address or 'Not provided'}

Items:
{items_text}

Total      : \u20A6{order.total_amount:,.0f}
Order No   : #{order.order_number}
Reference  : SIBRAH-{order.order_number}
━━━━━━━━━━━━━━━━━━━━━━━━

Manage this order at:
http://127.0.0.1:8000/admin/shop/order/
"""
    try:
        send_mail(
            subject        = subject,
            message        = message,
            from_email     = settings.DEFAULT_FROM_EMAIL,
            recipient_list = [settings.SIBRAH_COMPANY['email']],
            fail_silently  = True,
        )
    except Exception:
        pass


def _notify_admin_payment_proof(order):
    """Notify admin that a customer submitted payment proof."""
    subject = f"[PAYMENT PROOF] Order #{order.order_number} — {order.customer_name}"
    message = f"""
Payment proof submitted for Order #{order.order_number}

Customer : {order.customer_name}
Phone    : {order.customer_phone}
Email    : {order.customer_email}
Amount   : \u20A6{order.total_amount:,.0f}

Please verify and update the order status to "Confirmed":
http://127.0.0.1:8000/admin/shop/order/
"""
    try:
        send_mail(
            subject        = subject,
            message        = message,
            from_email     = settings.DEFAULT_FROM_EMAIL,
            recipient_list = [settings.SIBRAH_COMPANY['email']],
            fail_silently  = True,
        )
    except Exception:
        pass
