from django.urls import path
from . import views

app_name = 'shop'

urlpatterns = [
    path('',                        views.shop_home,      name='shop_home'),
    path('track/',                  views.track_order,    name='track_order'),
    path('product/<slug:slug>/',    views.product_detail, name='product_detail'),
    path('order/<slug:slug>/',      views.place_order,    name='place_order'),
    path('payment/<uuid:pk>/',      views.order_payment,  name='order_payment'),
    path('success/<uuid:pk>/',      views.order_success,  name='order_success'),
]
