from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import SibrahUser


@admin.register(SibrahUser)
class SibrahUserAdmin(UserAdmin):
    list_display  = ('student_id', 'username', 'full_name', 'email', 'phone', 'role', 'is_active', 'created_at')
    list_filter   = ('role', 'is_active', 'is_staff')
    search_fields = ('username', 'email', 'first_name', 'last_name', 'student_id', 'phone')
    ordering      = ('-created_at',)

    fieldsets = UserAdmin.fieldsets + (
        ('SIBRAH Info', {'fields': ('role', 'phone', 'student_id', 'address', 'date_of_birth', 'profile_pic')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('SIBRAH Info', {'fields': ('role', 'email', 'phone', 'first_name', 'last_name')}),
    )
