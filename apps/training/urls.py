from django.urls import path
from . import views

app_name = 'training'

urlpatterns = [
    path('',                              views.course_list,          name='course_list'),
    path('<slug:slug>/',                  views.course_detail,        name='course_detail'),
    path('my-courses/',                   views.my_courses,           name='my_courses'),
    path('enrollment/<uuid:pk>/payment/', views.payment_instructions, name='payment_instructions'),
    path('enrollment/<uuid:pk>/confirm/', views.confirm_payment,      name='confirm_payment'),
    path('enrollment/<uuid:pk>/progress/',views.course_progress,      name='course_progress'),
]
