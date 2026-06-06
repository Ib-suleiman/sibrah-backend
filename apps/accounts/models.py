"""
SIBRAH Accounts App — Models
apps/accounts/models.py
"""

from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid


class SibrahUser(AbstractUser):
    """Extended user model for students, staff, and admins."""

    ROLE_CHOICES = [
        ('student',  'Student'),
        ('staff',    'Staff'),
        ('admin',    'Administrator'),
    ]

    id          = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    role        = models.CharField(max_length=20, choices=ROLE_CHOICES, default='student')
    phone       = models.CharField(max_length=20, blank=True)
    profile_pic = models.ImageField(upload_to='profiles/', blank=True, null=True)
    address     = models.TextField(blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)

    # Student ID (auto-generated)
    student_id  = models.CharField(max_length=20, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.student_id and self.role == 'student':
            import datetime
            year = datetime.datetime.now().year
            count = SibrahUser.objects.filter(role='student').count() + 1
            self.student_id = f"STU-{year}-{count:03d}"
        super().save(*args, **kwargs)

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}".strip() or self.username

    @property
    def is_student(self):
        return self.role == 'student'

    @property
    def is_admin_user(self):
        return self.role in ('admin', 'staff') or self.is_staff

    def __str__(self):
        return f"{self.full_name} ({self.student_id or self.role})"

    class Meta:
        verbose_name = 'SIBRAH User'
        verbose_name_plural = 'SIBRAH Users'
        ordering = ['-created_at']
