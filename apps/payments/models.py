"""
SIBRAH Payments App — Models
apps/payments/models.py

Tracks every Paystack transaction for courses and shop orders.
"""

from django.db import models
from django.conf import settings
import uuid


class PaystackTransaction(models.Model):

    PURPOSE_CHOICES = [
        ('course',  'Course Enrollment'),
        ('order',   'Shop Order'),
    ]

    STATUS_CHOICES = [
        ('initiated',  'Initiated'),
        ('pending',    'Pending'),
        ('success',    'Success'),
        ('failed',     'Failed'),
        ('abandoned',  'Abandoned'),
    ]

    id              = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    reference       = models.CharField(max_length=100, unique=True)
    user            = models.ForeignKey(
                        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
                        null=True, blank=True, related_name='transactions'
                      )
    email           = models.EmailField()
    amount          = models.DecimalField(max_digits=12, decimal_places=2)   # in Naira
    amount_kobo     = models.PositiveIntegerField()                           # Paystack uses kobo
    purpose         = models.CharField(max_length=20, choices=PURPOSE_CHOICES)
    status          = models.CharField(max_length=20, choices=STATUS_CHOICES, default='initiated')

    # Links to what was paid for
    enrollment_id   = models.UUIDField(null=True, blank=True)
    order_id        = models.UUIDField(null=True, blank=True)

    # Paystack response data
    paystack_id     = models.CharField(max_length=100, blank=True)
    channel         = models.CharField(max_length=50, blank=True)   # card, bank, ussd, etc.
    currency        = models.CharField(max_length=10, default='NGN')
    gateway_response= models.CharField(max_length=200, blank=True)
    paid_at         = models.DateTimeField(null=True, blank=True)

    created_at      = models.DateTimeField(auto_now_add=True)
    updated_at      = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.reference} — {self.email} — ₦{self.amount} ({self.status})"

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Paystack Transaction'
        verbose_name_plural = 'Paystack Transactions'
