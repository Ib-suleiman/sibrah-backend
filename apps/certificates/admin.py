from django.contrib import admin
from .models import Certificate

@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    list_display  = ('code', 'student', 'course', 'grade', 'issued_at', 'is_valid')
    list_filter   = ('grade', 'is_valid', 'course')
    search_fields = ('code', 'student__first_name', 'student__last_name', 'student__email')
    list_editable = ('is_valid',)
    readonly_fields = ('code', 'issued_at')
