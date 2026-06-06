from django.contrib import admin
from .models import Post, PostCategory

@admin.register(PostCategory)
class PostCategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display  = ('title', 'category', 'author', 'is_published', 'is_featured', 'published_at')
    list_filter   = ('is_published', 'is_featured', 'category')
    search_fields = ('title', 'excerpt', 'content')
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ('is_published', 'is_featured')
