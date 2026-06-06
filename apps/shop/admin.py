from django.contrib import admin
from django.contrib import messages as admin_messages
from django.core.mail import send_mail
from django.conf import settings
from .models import ProductCategory, Product, Order, OrderItem


@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


class OrderItemInline(admin.TabularInline):
    model       = OrderItem
    extra       = 0
    fields      = ('product', 'name', 'price', 'quantity')
    readonly_fields = ('product',)


def _send_order_status_email(order, old_status):
    """Send customer an email when their order status changes."""
    status_messages = {
        'confirmed':  (
            "Your Payment Has Been Confirmed!",
            f"Great news! We have confirmed your payment for Order #{order.order_number}.\n\n"
            f"Your order is now being processed and will be delivered to you soon.\n\n"
            f"Track your order at: http://127.0.0.1:8000/shop/track/\n"
            f"Use Order Number: #{order.order_number}\n"
        ),
        'processing': (
            "Your Order is Being Processed",
            f"Your Order #{order.order_number} is now being prepared for delivery.\n\n"
            f"We will notify you once it is dispatched.\n\n"
            f"Track your order at: http://127.0.0.1:8000/shop/track/\n"
        ),
        'delivered':  (
            "Your Order Has Been Delivered!",
            f"Your Order #{order.order_number} has been delivered successfully.\n\n"
            f"Thank you for shopping with SIBRAH Computers & Technology Hub!\n\n"
            f"If you have any issues, please contact us:\n"
            f"WhatsApp: +234 808 110 1992\n"
            f"Email: info@sibrahtech.com.ng\n"
        ),
        'cancelled':  (
            "Your Order Has Been Cancelled",
            f"We're sorry, but Order #{order.order_number} has been cancelled.\n\n"
            f"If you believe this is a mistake, please contact us immediately:\n"
            f"WhatsApp: +234 808 110 1992\n"
        ),
    }

    if order.status in status_messages:
        subject_suffix, body = status_messages[order.status]
        subject = f"Order #{order.order_number} — {subject_suffix} | SIBRAH"
        message = (
            f"Dear {order.customer_name},\n\n"
            f"{body}\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"Order Number : #{order.order_number}\n"
            f"Total Amount : \u20A6{order.total_amount:,.0f}\n"
            f"Current Status: {order.get_status_display()}\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            f"SIBRAH Computers & Technology Hub\n"
            f"Phone: +234 808 110 1992 | info@sibrahtech.com.ng\n"
        )
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


# ── ADMIN ACTIONS ─────────────────────────────────────────────────────

def confirm_orders(modeladmin, request, queryset):
    count = 0
    for order in queryset.filter(status='pending'):
        old_status = order.status
        order.status = 'confirmed'
        order.save()
        _send_order_status_email(order, old_status)
        count += 1
    admin_messages.success(
        request,
        f"{count} order(s) confirmed. Customers have been emailed automatically."
    )
confirm_orders.short_description = "✅ Confirm selected orders & email customers"


def mark_processing(modeladmin, request, queryset):
    count = 0
    for order in queryset.exclude(status__in=['delivered', 'cancelled']):
        old_status = order.status
        order.status = 'processing'
        order.save()
        _send_order_status_email(order, old_status)
        count += 1
    admin_messages.success(request, f"{count} order(s) marked as processing.")
mark_processing.short_description = "⚙️ Mark as Processing & email customers"


def mark_delivered(modeladmin, request, queryset):
    count = 0
    for order in queryset.exclude(status='cancelled'):
        old_status = order.status
        order.status = 'delivered'
        order.save()
        _send_order_status_email(order, old_status)
        count += 1
    admin_messages.success(request, f"{count} order(s) marked as delivered.")
mark_delivered.short_description = "🚚 Mark as Delivered & email customers"


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display        = ('name', 'category', 'price', 'stock',
                           'is_active', 'is_featured', 'badge')
    list_filter         = ('category', 'is_active', 'is_featured')
    search_fields       = ('name',)
    prepopulated_fields = {'slug': ('name',)}
    list_editable       = ('is_active', 'is_featured', 'stock')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display    = ('order_number', 'customer_name', 'customer_phone',
                       'total_amount', 'status', 'created_at')
    list_filter     = ('status',)
    search_fields   = ('order_number', 'customer_name',
                       'customer_email', 'customer_phone')
    list_editable   = ('status',)
    inlines         = [OrderItemInline]
    readonly_fields = ('order_number', 'created_at')
    actions         = [confirm_orders, mark_processing, mark_delivered]

    def save_model(self, request, obj, form, change):
        """Auto-send status email when order status changes via admin save."""
        if change:
            try:
                old = Order.objects.get(pk=obj.pk)
                if old.status != obj.status:
                    _send_order_status_email(obj, old.status)
                    admin_messages.info(
                        request,
                        f"Status update email sent to {obj.customer_email}"
                    )
            except Order.DoesNotExist:
                pass
        super().save_model(request, obj, form, change)
