"""
SIBRAH Shop App — Models
apps/shop/models.py
"""

from django.db import models
from django.conf import settings
import uuid


class ProductCategory(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    icon = models.CharField(max_length=10, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Product Categories'


class Product(models.Model):
    id            = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name          = models.CharField(max_length=200)
    slug          = models.SlugField(unique=True)
    category      = models.ForeignKey(ProductCategory, on_delete=models.SET_NULL,
                                      null=True, related_name='products')
    description   = models.TextField()
    specs         = models.TextField(blank=True, help_text='Technical specifications')
    price         = models.DecimalField(max_digits=12, decimal_places=2)
    old_price     = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    image         = models.ImageField(upload_to='products/', blank=True, null=True)
    icon          = models.CharField(max_length=10, blank=True, help_text='Fallback emoji')
    stock         = models.PositiveIntegerField(default=0)
    is_active     = models.BooleanField(default=True)
    is_featured   = models.BooleanField(default=False)
    badge         = models.CharField(max_length=20, blank=True, help_text='e.g. New, Hot, Sale')
    created_at    = models.DateTimeField(auto_now_add=True)

    @property
    def in_stock(self):
        return self.stock > 0

    @property
    def discount_percent(self):
        if self.old_price and self.old_price > self.price:
            return round((1 - self.price / self.old_price) * 100)
        return 0

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-is_featured', 'name']


class Order(models.Model):
    STATUS_CHOICES = [
        ('pending',    'Pending Payment'),
        ('confirmed',  'Payment Confirmed'),
        ('processing', 'Processing'),
        ('delivered',  'Delivered'),
        ('cancelled',  'Cancelled'),
    ]

    id             = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order_number   = models.CharField(max_length=20, unique=True, blank=True)
    customer       = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
                                       null=True, blank=True, related_name='orders')
    # For guest orders
    customer_name  = models.CharField(max_length=100)
    customer_email = models.EmailField()
    customer_phone = models.CharField(max_length=20)
    delivery_address = models.TextField(blank=True)

    status         = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    total_amount   = models.DecimalField(max_digits=12, decimal_places=2)
    payment_ref    = models.CharField(max_length=50, blank=True)
    payment_proof  = models.ImageField(upload_to='order_proofs/', blank=True, null=True)
    notes          = models.TextField(blank=True)
    created_at     = models.DateTimeField(auto_now_add=True)
    updated_at     = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.order_number:
            import datetime, random, string
            yr  = datetime.datetime.now().year
            rnd = ''.join(random.choices(string.digits, k=4))
            self.order_number = f"ORD-{yr}-{rnd}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"#{self.order_number} — {self.customer_name}"

    class Meta:
        ordering = ['-created_at']


class OrderItem(models.Model):
    order    = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product  = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    name     = models.CharField(max_length=200)   # snapshot at order time
    price    = models.DecimalField(max_digits=12, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    @property
    def subtotal(self):
        return self.price * self.quantity

    def __str__(self):
        return f"{self.quantity}x {self.name}"
