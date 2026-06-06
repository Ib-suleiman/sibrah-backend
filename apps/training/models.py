"""
SIBRAH Training App — Models
apps/training/models.py
"""

from django.db import models
from django.conf import settings
import uuid


class CourseCategory(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Course Categories'


class Course(models.Model):
    LEVEL_CHOICES = [
        ('beginner',     'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced',     'Advanced'),
    ]

    id           = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title        = models.CharField(max_length=200)
    slug         = models.SlugField(unique=True)
    category     = models.ForeignKey(CourseCategory, on_delete=models.SET_NULL, null=True, blank=True)
    level        = models.CharField(max_length=20, choices=LEVEL_CHOICES)
    description  = models.TextField()
    duration     = models.CharField(max_length=50, help_text='e.g. 8 Weeks')
    fee          = models.DecimalField(max_digits=10, decimal_places=2)
    icon         = models.CharField(max_length=10, blank=True, help_text='Emoji icon')
    tools        = models.CharField(max_length=200, blank=True, help_text='e.g. Python, Django')
    schedule     = models.CharField(max_length=100, blank=True, help_text='e.g. Weekdays / Weekend')
    is_active    = models.BooleanField(default=True)
    is_featured  = models.BooleanField(default=False)
    order        = models.PositiveIntegerField(default=0)
    created_at   = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.get_level_display()})"

    class Meta:
        ordering = ['order', 'title']


class Enrollment(models.Model):
    STATUS_CHOICES = [
        ('pending',    'Pending Payment'),
        ('active',     'Active'),
        ('completed',  'Completed'),
        ('cancelled',  'Cancelled'),
    ]

    SCHEDULE_CHOICES = [
        ('weekdays', 'Weekdays (Mon–Fri)'),
        ('weekends', 'Weekends (Sat–Sun)'),
        ('online',   'Online / Virtual'),
    ]

    id             = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    student        = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                       related_name='enrollments')
    course         = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments')
    status         = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    schedule       = models.CharField(max_length=20, choices=SCHEDULE_CHOICES, default='weekdays')
    progress       = models.PositiveIntegerField(default=0, help_text='Progress percentage 0-100')
    amount_paid    = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    payment_proof  = models.ImageField(upload_to='payment_proofs/', blank=True, null=True)
    payment_ref    = models.CharField(max_length=50, blank=True)
    enrolled_at    = models.DateTimeField(auto_now_add=True)
    completed_at   = models.DateTimeField(null=True, blank=True)
    notes          = models.TextField(blank=True)

    def __str__(self):
        return f"{self.student.full_name} → {self.course.title}"

    class Meta:
        ordering = ['-enrolled_at']
        unique_together = ('student', 'course')


class CourseSession(models.Model):
    """Scheduled class sessions for a course enrollment."""
    enrollment   = models.ForeignKey(Enrollment, on_delete=models.CASCADE, related_name='sessions')
    session_no   = models.PositiveIntegerField()
    title        = models.CharField(max_length=200)
    scheduled_at = models.DateTimeField()
    zoom_link    = models.URLField(blank=True)
    is_completed = models.BooleanField(default=False)
    notes        = models.TextField(blank=True)

    def __str__(self):
        return f"Session {self.session_no}: {self.title}"

    class Meta:
        ordering = ['scheduled_at']
