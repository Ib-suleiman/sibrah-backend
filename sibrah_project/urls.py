"""
SIBRAH - Main URL Configuration
sibrah_project/urls.py
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

admin.site.site_header  = "SIBRAH Technology Hub — Admin"
admin.site.site_title   = "SIBRAH Admin Portal"
admin.site.index_title  = "Welcome to SIBRAH Admin"

urlpatterns = [
    # CKEditor
    path('ckeditor/', include('ckeditor_uploader.urls')),

    # Django admin
    path('admin/', admin.site.urls),

    # Allauth authentication
    path('accounts/', include('allauth.urls')),

    # SIBRAH apps
    path('',               include('apps.core.urls',         namespace='core')),
    path('portal/',        include('apps.accounts.urls',     namespace='accounts')),
    path('training/',      include('apps.training.urls',     namespace='training')),
    path('shop/',          include('apps.shop.urls',         namespace='shop')),
    path('certificates/',  include('apps.certificates.urls', namespace='certificates')),
    path('blog/',          include('apps.blog.urls',         namespace='blog')),

    # REST API
    path('api/training/',      include('apps.training.api_urls')),
    path('api/shop/',          include('apps.shop.api_urls')),
    path('api/certificates/',  include('apps.certificates.api_urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,  document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
