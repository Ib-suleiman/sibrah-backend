from django.contrib import admin
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms
from .models import Post, PostCategory


class PostAdminForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model  = Post
        fields = '__all__'


@admin.register(PostCategory)
class PostCategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    form            = PostAdminForm
    list_display    = ('title', 'category', 'author', 'is_published',
                       'is_featured', 'published_at')
    list_filter     = ('is_published', 'is_featured', 'category')
    search_fields   = ('title', 'excerpt', 'content')
    prepopulated_fields = {'slug': ('title',)}
    list_editable   = ('is_published', 'is_featured')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Post Info', {
            'fields': ('title', 'slug', 'category', 'author', 'icon', 'read_time')
        }),
        ('Content', {
            'fields': ('excerpt', 'content', 'thumbnail'),
            'description': 'Use the editor toolbar to format your content — bold, italic, headings, images, lists etc.'
        }),
        ('Publishing', {
            'fields': ('is_published', 'is_featured', 'published_at')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
