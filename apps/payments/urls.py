"""
SIBRAH Payments — URLs
apps/payments/urls.py
"""

from django.urls import path
from . import views

app_name = 'payments'

urlpatterns = [
    # ── Course payments ──────────────────────────────────────────
    path('pay/course/<uuid:enrollment_id>/',
         views.pay_for_course,
         name='pay_course'),

    path('verify/course/<uuid:enrollment_id>/',
         views.verify_course_payment,
         name='verify_course'),

    path('choose/course/<uuid:enrollment_id>/',
         views.choose_payment_method_course,
         name='choose_course'),

    # ── Order payments ───────────────────────────────────────────
    path('pay/order/<uuid:order_id>/',
         views.pay_for_order,
         name='pay_order'),

    path('verify/order/<uuid:order_id>/',
         views.verify_order_payment,
         name='verify_order'),

    path('choose/order/<uuid:order_id>/',
         views.choose_payment_method_order,
         name='choose_order'),

    # ── Paystack webhook (no CSRF) ───────────────────────────────
    path('webhook/paystack/',
         views.webhook,
         name='webhook'),
]
