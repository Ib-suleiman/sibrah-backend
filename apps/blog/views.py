"""
SIBRAH Blog App — Views
apps/blog/views.py
"""
from django.shortcuts import render, get_object_or_404
from .models import Post, PostCategory


def post_list(request):
    posts      = Post.objects.filter(is_published=True)
    categories = PostCategory.objects.all()
    cat_slug   = request.GET.get('category', '')
    if cat_slug:
        posts = posts.filter(category__slug=cat_slug)
    return render(request, 'blog/post_list.html', {
        'posts': posts, 'categories': categories, 'active_cat': cat_slug
    })


def post_detail(request, slug):
    post    = get_object_or_404(Post, slug=slug, is_published=True)
    related = Post.objects.filter(
        category=post.category, is_published=True
    ).exclude(pk=post.pk)[:3]
    return render(request, 'blog/post_detail.html', {'post': post, 'related': related})
