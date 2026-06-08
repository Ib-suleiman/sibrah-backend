"""
SIBRAH Blog App — Models
apps/blog/models.py
"""

from django.db import models
from django.conf import settings
from ckeditor_uploader.fields import RichTextUploadingField
import uuid


class PostCategory(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Post Categories'


class Post(models.Model):
    id           = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title        = models.CharField(max_length=250)
    slug         = models.SlugField(unique=True)
    category     = models.ForeignKey(PostCategory, on_delete=models.SET_NULL,
                                     null=True, blank=True)
    author       = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
                                     null=True, blank=True)
    excerpt      = models.TextField(max_length=300,
                                    help_text='Short summary shown on listing page')
    # RichTextUploadingField replaces plain TextField
    # This gives you bold, italic, headings, images, tables etc.
    content      = RichTextUploadingField(
                        help_text='Write your full article here. Use the toolbar to format text.')
    thumbnail    = models.ImageField(upload_to='blog/', blank=True, null=True)
    icon         = models.CharField(max_length=10, blank=True, help_text='Emoji icon')
    read_time    = models.PositiveIntegerField(default=5, help_text='Minutes to read')
    is_published = models.BooleanField(default=False)
    is_featured  = models.BooleanField(default=False)
    published_at = models.DateTimeField(null=True, blank=True)
    created_at   = models.DateTimeField(auto_now_add=True)
    updated_at   = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-published_at', '-created_at']
