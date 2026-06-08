from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('',            views.home,       name='home'),
    path('about/',      views.about,      name='about'),
    path('services/',   views.services,   name='services'),
    path('portfolio/',  views.portfolio,  name='portfolio'),
    path('gallery/',    views.gallery,    name='gallery'),
    path('faq/',        views.faq,        name='faq'),
    path('contact/',    views.contact,    name='contact'),

    # SEO
    path('sitemap.xml', views.sitemap,    name='sitemap'),
    path('robots.txt',  views.robots_txt, name='robots_txt'),
]
