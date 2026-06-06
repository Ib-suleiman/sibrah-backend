"""
SIBRAH Payments — Views
apps/payments/views.py
"""

import json
import logging
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.conf import settings
from django.utils import timezone

from .models import PaystackTransaction
from .paystack import (
    initialize_transaction,
    verify_transaction,
    verify_webhook_signature,
    generate_reference,
)

logger = logging.getLogger(__name__)


# ── COURSE PAYMENT ─────────────────────────────────────────────────────

@login_required
def pay_for_course(request, enrollment_id):
    """
    Initiate Paystack payment for a course enrollment.
    Called instead of the bank-transfer payment instructions page.
    """
    from apps.training.models import Enrollment

    enrollment = get_object_or_404(
        Enrollment, pk=enrollment_id, student=request.user
    )

    if enrollment.status == 'active':
        messages.info(request, "This enrollment is already active.")
        return redirect('accounts:dashboard')

    # Build reference and callback URL
    reference    = generate_reference('SIBRAH-ENR')
    callback_url = request.build_absolute_uri(f'/payments/verify/course/{enrollment_id}/?ref={reference}')

    result = initialize_transaction(
        email        = request.user.email,
        amount_naira = float(enrollment.course.fee),
        reference    = reference,
        callback_url = callback_url,
        metadata     = {
            'enrollment_id': str(enrollment.pk),
            'course':        enrollment.course.title,
            'student':       request.user.get_full_name() or request.user.username,
            'student_id':    request.user.student_id or '',
            'purpose':       'course_enrollment',
        },
        channels = ['card', 'bank', 'ussd', 'bank_transfer', 'mobile_money'],
    )

    if not result['status']:
        messages.error(request,
            f"Could not initiate payment: {result.get('message')}. "
            "Please try again or pay by bank transfer.")
        return redirect('training:payment_instructions', pk=enrollment_id)

    # Save transaction record
    PaystackTransaction.objects.create(
        reference     = reference,
        user          = request.user,
        email         = request.user.email,
        amount        = enrollment.course.fee,
        amount_kobo   = result['amount_kobo'],
        purpose       = 'course',
        status        = 'initiated',
        enrollment_id = enrollment.pk,
    )

    # Redirect to Paystack checkout page
    return redirect(result['authorization_url'])


@login_required
def verify_course_payment(request, enrollment_id):
    """
    Paystack redirects here after course payment.
    Verifies the transaction and activates the enrollment.
    """
    from apps.training.models import Enrollment

    reference  = request.GET.get('ref') or request.GET.get('reference', '')
    enrollment = get_object_or_404(
        Enrollment, pk=enrollment_id, student=request.user
    )

    if not reference:
        messages.error(request, "Payment reference missing. Please contact support.")
        return redirect('accounts:dashboard')

    # Verify with Paystack API
    result = verify_transaction(reference)

    # Update our transaction record
    txn = PaystackTransaction.objects.filter(reference=reference).first()

    if result['status'] and result['transaction_status'] == 'success':
        # ✅ Payment confirmed
        enrollment.status       = 'active'
        enrollment.amount_paid  = result['amount_naira']
        enrollment.payment_ref  = reference
        enrollment.save()

        if txn:
            txn.status           = 'success'
            txn.paystack_id      = result.get('paystack_id', '')
            txn.channel          = result.get('channel', '')
            txn.gateway_response = result.get('gateway_response', '')
            txn.paid_at          = timezone.now()
            txn.save()

        messages.success(request,
            f"Payment confirmed! ₦{result['amount_naira']:,.0f} received. "
            f"Your enrollment for {enrollment.course.title} is now ACTIVE. "
            "Welcome to SIBRAH Academy!")

        return render(request, 'payments/payment_success.html', {
            'enrollment': enrollment,
            'transaction': txn,
            'purpose': 'course',
        })

    else:
        # ❌ Payment failed or not verified
        if txn:
            txn.status = 'failed'
            txn.gateway_response = result.get('message', 'Verification failed')
            txn.save()

        messages.error(request,
            "Payment could not be verified. If you were charged, "
            "please contact us at +234 808 110 1992 with your reference: "
            f"{reference}")

        return render(request, 'payments/payment_failed.html', {
            'reference':  reference,
            'enrollment': enrollment,
            'purpose':    'course',
        })


# ── ORDER PAYMENT ──────────────────────────────────────────────────────

def pay_for_order(request, order_id):
    """
    Initiate Paystack payment for a shop order.
    Works for both logged-in and guest users.
    """
    from apps.shop.models import Order

    order = get_object_or_404(Order, pk=order_id)

    if order.status == 'confirmed':
        messages.info(request, "This order has already been paid for.")
        return redirect('shop:order_success', pk=order_id)

    email = order.customer_email
    if not email and request.user.is_authenticated:
        email = request.user.email

    reference    = generate_reference('SIBRAH-ORD')
    callback_url = request.build_absolute_uri(f'/payments/verify/order/{order_id}/?ref={reference}')

    result = initialize_transaction(
        email        = email,
        amount_naira = float(order.total_amount),
        reference    = reference,
        callback_url = callback_url,
        metadata     = {
            'order_id':      str(order.pk),
            'order_number':  order.order_number,
            'customer':      order.customer_name,
            'phone':         order.customer_phone,
            'purpose':       'shop_order',
        },
        channels = ['card', 'bank', 'ussd', 'bank_transfer', 'mobile_money'],
    )

    if not result['status']:
        messages.error(request,
            f"Could not initiate payment: {result.get('message')}. "
            "Please try bank transfer instead.")
        return redirect('shop:order_payment', pk=order_id)

    # Save transaction record
    PaystackTransaction.objects.create(
        reference   = reference,
        user        = request.user if request.user.is_authenticated else None,
        email       = email,
        amount      = order.total_amount,
        amount_kobo = result['amount_kobo'],
        purpose     = 'order',
        status      = 'initiated',
        order_id    = order.pk,
    )

    return redirect(result['authorization_url'])


def verify_order_payment(request, order_id):
    """
    Paystack redirects here after order payment.
    Verifies and confirms the order.
    """
    from apps.shop.models import Order

    reference = request.GET.get('ref') or request.GET.get('reference', '')
    order     = get_object_or_404(Order, pk=order_id)

    if not reference:
        messages.error(request, "Payment reference missing. Please contact support.")
        return redirect('shop:shop_home')

    result = verify_transaction(reference)
    txn    = PaystackTransaction.objects.filter(reference=reference).first()

    if result['status'] and result['transaction_status'] == 'success':
        order.status      = 'confirmed'
        order.payment_ref = reference
        order.save()

        if txn:
            txn.status           = 'success'
            txn.paystack_id      = result.get('paystack_id', '')
            txn.channel          = result.get('channel', '')
            txn.gateway_response = result.get('gateway_response', '')
            txn.paid_at          = timezone.now()
            txn.save()

        messages.success(request,
            f"Payment confirmed! ₦{result['amount_naira']:,.0f} received for "
            f"Order #{order.order_number}. We will process your order shortly.")

        return render(request, 'payments/payment_success.html', {
            'order':       order,
            'transaction': txn,
            'purpose':     'order',
        })

    else:
        if txn:
            txn.status           = 'failed'
            txn.gateway_response = result.get('message', 'Verification failed')
            txn.save()

        messages.error(request,
            f"Payment could not be verified. Reference: {reference}. "
            "Please contact +234 808 110 1992.")

        return render(request, 'payments/payment_failed.html', {
            'reference': reference,
            'order':     order,
            'purpose':   'order',
        })


# ── PAYSTACK WEBHOOK ───────────────────────────────────────────────────

@csrf_exempt
@require_POST
def webhook(request):
    """
    Paystack sends event notifications here.
    Handles: charge.success, charge.failed, transfer.success
    """
    signature = request.headers.get('X-Paystack-Signature', '')
    payload   = request.body

    # Verify webhook signature
    if not verify_webhook_signature(payload, signature):
        logger.warning("Invalid Paystack webhook signature received")
        return HttpResponse(status=400)

    try:
        event = json.loads(payload.decode('utf-8'))
    except json.JSONDecodeError:
        return HttpResponse(status=400)

    event_type = event.get('event', '')
    data       = event.get('data', {})
    reference  = data.get('reference', '')

    logger.info(f"Paystack webhook: {event_type} | ref: {reference}")

    if event_type == 'charge.success':
        _handle_successful_charge(data, reference)
    elif event_type == 'charge.failed':
        _handle_failed_charge(data, reference)

    return HttpResponse(status=200)


def _handle_successful_charge(data, reference):
    """Process a successful payment from webhook."""
    from apps.training.models import Enrollment
    from apps.shop.models import Order

    txn = PaystackTransaction.objects.filter(reference=reference).first()
    if not txn:
        return

    if txn.status == 'success':
        return   # Already processed

    txn.status           = 'success'
    txn.paystack_id      = str(data.get('id', ''))
    txn.channel          = data.get('channel', '')
    txn.gateway_response = data.get('gateway_response', '')
    txn.paid_at          = timezone.now()
    txn.save()

    # Activate enrollment
    if txn.purpose == 'course' and txn.enrollment_id:
        Enrollment.objects.filter(pk=txn.enrollment_id).update(
            status='active',
            amount_paid=txn.amount,
            payment_ref=reference,
        )

    # Confirm order
    elif txn.purpose == 'order' and txn.order_id:
        Order.objects.filter(pk=txn.order_id).update(
            status='confirmed',
            payment_ref=reference,
        )


def _handle_failed_charge(data, reference):
    """Mark a failed payment in our database."""
    PaystackTransaction.objects.filter(reference=reference).update(
        status='failed',
        gateway_response=data.get('gateway_response', 'Payment failed'),
    )


# ── CHOOSE PAYMENT METHOD ──────────────────────────────────────────────

@login_required
def choose_payment_method_course(request, enrollment_id):
    """Let student choose between Paystack or bank transfer for a course."""
    from apps.training.models import Enrollment
    enrollment = get_object_or_404(Enrollment, pk=enrollment_id, student=request.user)
    return render(request, 'payments/choose_method.html', {
        'enrollment': enrollment,
        'purpose':    'course',
        'amount':     enrollment.course.fee,
        'item_name':  enrollment.course.title,
        'pay_url':    f'/payments/pay/course/{enrollment_id}/',
        'bank_url':   f'/training/enrollment/{enrollment_id}/payment/',
        'company':    settings.SIBRAH_COMPANY,
    })


def choose_payment_method_order(request, order_id):
    """Let customer choose between Paystack or bank transfer for an order."""
    from apps.shop.models import Order
    order = get_object_or_404(Order, pk=order_id)
    return render(request, 'payments/choose_method.html', {
        'order':     order,
        'purpose':   'order',
        'amount':    order.total_amount,
        'item_name': f"Order #{order.order_number}",
        'pay_url':   f'/payments/pay/order/{order_id}/',
        'bank_url':  f'/shop/payment/{order_id}/',
        'company':   settings.SIBRAH_COMPANY,
    })
