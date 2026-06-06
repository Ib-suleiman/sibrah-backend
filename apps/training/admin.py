from django.contrib import admin
from django.contrib import messages as admin_messages
from .models import Course, CourseCategory, Enrollment, CourseSession


@admin.register(CourseCategory)
class CourseCategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display        = ('title', 'level', 'fee', 'duration', 'is_active', 'is_featured', 'order')
    list_filter         = ('level', 'is_active', 'is_featured')
    search_fields       = ('title',)
    prepopulated_fields = {'slug': ('title',)}
    list_editable       = ('is_active', 'is_featured', 'order')


class CourseSessionInline(admin.TabularInline):
    model  = CourseSession
    extra  = 0
    fields = ('session_no', 'title', 'scheduled_at', 'zoom_link', 'is_completed')


def activate_enrollments(modeladmin, request, queryset):
    """
    Admin action: Activate selected enrollments and email each student.
    Use this after verifying student payment.
    """
    from apps.training.views import send_enrollment_activated_email
    activated = 0
    for enrollment in queryset:
        if enrollment.status != 'active':
            enrollment.status = 'active'
            enrollment.save()
            send_enrollment_activated_email(enrollment)
            activated += 1
    admin_messages.success(
        request,
        f"{activated} enrollment(s) activated. Students have been emailed automatically."
    )
activate_enrollments.short_description = "✅ Activate selected enrollments & email students"


def mark_completed(modeladmin, request, queryset):
    """Admin action: Mark selected enrollments as completed."""
    queryset.update(status='completed', progress=100)
    admin_messages.success(request, f"{queryset.count()} enrollment(s) marked as completed.")
mark_completed.short_description = "🏆 Mark selected enrollments as completed"


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display    = ('student', 'course', 'status', 'schedule', 'progress',
                       'payment_ref', 'enrolled_at')
    list_filter     = ('status', 'schedule', 'course')
    search_fields   = ('student__first_name', 'student__last_name',
                       'student__email', 'student__student_id')
    list_editable   = ('status', 'progress')
    inlines         = [CourseSessionInline]
    readonly_fields = ('enrolled_at',)
    actions         = [activate_enrollments, mark_completed]

    def save_model(self, request, obj, form, change):
        """
        Auto-send activation email when status changed to active.
        Auto-set progress to 100 when status changed to completed.
        """
        if change:
            try:
                old = Enrollment.objects.get(pk=obj.pk)

                # Status changed to active — send activation email
                if old.status != 'active' and obj.status == 'active':
                    from apps.training.views import send_enrollment_activated_email
                    send_enrollment_activated_email(obj)
                    admin_messages.info(
                        request,
                        f"Activation email sent to {obj.student.email}"
                    )

                # Status changed to completed — auto set progress to 100
                if old.status != 'completed' and obj.status == 'completed':
                    obj.progress = 100
                    admin_messages.info(
                        request,
                        f"Progress automatically set to 100% for {obj.student.get_full_name()}"
                    )

            except Enrollment.DoesNotExist:
                pass

        super().save_model(request, obj, form, change)
