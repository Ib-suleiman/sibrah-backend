from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    # Auth
    path('register/',    views.register_student, name='register'),
    path('login/',       views.student_login,    name='login'),
    path('logout/',      views.student_logout,   name='logout'),

    # Student portal
    path('dashboard/',   views.dashboard,        name='dashboard'),
    path('profile/',     views.edit_profile,     name='edit_profile'),

    # Password management
    path('change-password/',         views.change_password,        name='change_password'),
    path('change-password/success/', views.password_change_success, name='password_change_success'),
    path('forgot-password/',         views.forgot_password,         name='forgot_password'),
    path('reset-password/<str:token>/', views.reset_password,       name='reset_password'),

    # Admin
    path('admin-panel/',          views.admin_dashboard, name='admin_dashboard'),
    path('admin-panel/students/', views.admin_students,  name='admin_students'),
    path('admin-panel/orders/',   views.admin_orders,    name='admin_orders'),
]
