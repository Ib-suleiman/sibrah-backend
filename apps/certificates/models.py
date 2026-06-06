"""
SIBRAH Certificates App — Models
apps/certificates/models.py
"""

from django.db import models
from django.conf import settings
import uuid, random, string


def generate_cert_code():
    import datetime
    year   = datetime.datetime.now().year
    rnd    = "".join(random.choices(string.digits, k=3))
    prefix = "".join(random.choices(string.ascii_uppercase, k=2))
    return f"SIBRAH-{year}-{prefix}-{rnd}"


class Certificate(models.Model):
    GRADE_CHOICES = [
        ('distinction', 'Distinction'),
        ('credit',      'Credit'),
        ('merit',       'Merit'),
        ('pass',        'Pass'),
    ]

    id         = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    code       = models.CharField(max_length=30, unique=True, default=generate_cert_code)
    student    = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='certificates'
    )
    course     = models.ForeignKey(
        'training.Course', on_delete=models.CASCADE, related_name='certificates'
    )
    enrollment = models.OneToOneField(
        'training.Enrollment', on_delete=models.SET_NULL,
        null=True, blank=True, related_name='certificate'
    )
    grade      = models.CharField(max_length=20, choices=GRADE_CHOICES, default='pass')
    issued_by  = models.CharField(max_length=100, default='SIBRAH Computers & Technology Hub')
    instructor = models.CharField(max_length=100, blank=True)
    issued_at  = models.DateField(auto_now_add=True)
    is_valid   = models.BooleanField(default=True)
    notes      = models.TextField(blank=True)

    def __str__(self):
        return f"{self.code} — {self.student.full_name} — {self.course.title}"

    class Meta:
        ordering = ['-issued_at']
