"""
SIBRAH Training App — Views
apps/training/views.py
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .models import Course, Enrollment, CourseSession
from .forms import EnrollmentForm


def course_list(request):
    courses      = Course.objects.filter(is_active=True)
    beginners    = courses.filter(level='beginner')
    intermediate = courses.filter(level='intermediate')
    advanced     = courses.filter(level='advanced')
    return render(request, 'training/course_list.html', {
        'beginners':    beginners,
        'intermediate': intermediate,
        'advanced':     advanced,
        'company':      settings.SIBRAH_COMPANY,
    })


def course_detail(request, slug):
    course = get_object_or_404(Course, slug=slug, is_active=True)
    already_enrolled = False
    if request.user.is_authenticated:
        already_enrolled = Enrollment.objects.filter(
            student=request.user, course=course
        ).exists()

    if request.method == 'POST':
        if not request.user.is_authenticated:
            messages.warning(request,
                "Please log in or register to enroll in this course.")
            return redirect(f"/portal/login/?next=/training/{slug}/")
        if already_enrolled:
            existing = Enrollment.objects.filter(
                student=request.user, course=course
            ).first()
            if existing:
                if existing.status == 'completed':
                    messages.info(request,
                        f"You have already completed {course.title}. "
                        "Check your certificates in your dashboard.")
                elif existing.status == 'active':
                    messages.info(request,
                        f"You are currently enrolled in {course.title}. "
                        "Check your dashboard to track your progress.")
                elif existing.status == 'pending':
                    messages.warning(request,
                        f"You already have a pending enrollment for {course.title}. "
                        "Please complete your payment to activate it.")
                    return redirect('training:payment_instructions', pk=existing.pk)
                else:
                    messages.info(request, "You are already enrolled in this course.")
            return redirect('accounts:dashboard')
        form = EnrollmentForm(request.POST)
        if form.is_valid():
            enrollment = form.save(commit=False)
            enrollment.student = request.user
            enrollment.course  = course
            enrollment.status  = 'pending'
            enrollment.progress = 0
            enrollment.save()

            # Send confirmation email to student
            _send_enrollment_confirmation(enrollment)

            # Notify admin
            _notify_admin_new_enrollment(enrollment)

            messages.success(request,
                f"Enrollment submitted for {course.title}! "
                f"A confirmation email has been sent to {request.user.email}. "
                f"Please complete payment of \u20A6{course.fee:,.0f} to activate your spot.")
            return redirect('training:payment_instructions', pk=enrollment.pk)
    else:
        form = EnrollmentForm()

    # Pass enrollment object for status display
    enrollment_status = None
    if request.user.is_authenticated:
        enrollment_status = Enrollment.objects.filter(
            student=request.user, course=course
        ).first()

    return render(request, 'training/course_detail.html', {
        'course':            course,
        'form':              form,
        'already_enrolled':  already_enrolled,
        'enrollment_status': enrollment_status,
        'company':           settings.SIBRAH_COMPANY,
    })


@login_required
def payment_instructions(request, pk):
    enrollment = get_object_or_404(Enrollment, pk=pk, student=request.user)
    ref = f"SIBRAH-ENR-{str(enrollment.id)[:8].upper()}"
    return render(request, 'training/payment_instructions.html', {
        'enrollment': enrollment,
        'ref':        ref,
        'company':    settings.SIBRAH_COMPANY,
    })


@login_required
def confirm_payment(request, pk):
    enrollment = get_object_or_404(Enrollment, pk=pk, student=request.user)
    if request.method == 'POST':
        proof = request.FILES.get('payment_proof')
        ref   = request.POST.get('payment_ref', '').strip()
        if proof:
            enrollment.payment_proof = proof
            enrollment.payment_ref   = ref
            enrollment.save()

            # Notify admin
            _notify_admin_enrollment_proof(enrollment)

            messages.success(request,
                "Payment proof submitted! We will verify and activate your "
                "enrollment within 2 hours. You will receive a confirmation email "
                "once activated. You can also send your receipt to "
                "+234 808 110 1992 on WhatsApp.")
            return redirect('accounts:dashboard')
        messages.error(request, "Please upload your payment proof screenshot.")
    return render(request, 'training/confirm_payment.html', {
        'enrollment': enrollment,
        'company':    settings.SIBRAH_COMPANY,
    })


@login_required
def my_courses(request):
    enrollments = Enrollment.objects.filter(
        student=request.user
    ).select_related('course').order_by('-enrolled_at')
    return render(request, 'training/my_courses.html', {'enrollments': enrollments})


@login_required
def course_progress(request, pk):
    enrollment = get_object_or_404(Enrollment, pk=pk, student=request.user)
    sessions   = enrollment.sessions.all()
    return render(request, 'training/course_progress.html', {
        'enrollment': enrollment,
        'sessions':   sessions,
    })


# ── EMAIL HELPERS ─────────────────────────────────────────────────────

def _send_enrollment_confirmation(enrollment):
    """Email student when they submit enrollment."""
    ref = f"SIBRAH-ENR-{str(enrollment.id)[:8].upper()}"
    subject = f"Enrollment Confirmation — {enrollment.course.title} | SIBRAH Academy"
    message = f"""
Dear {enrollment.student.first_name},

Thank you for enrolling at SIBRAH Academy! Your enrollment has been received.

━━━━━━━━━━━━━━━━━━━━━━━━
ENROLLMENT DETAILS
━━━━━━━━━━━━━━━━━━━━━━━━
Student ID   : {enrollment.student.student_id}
Course       : {enrollment.course.title}
Level        : {enrollment.course.get_level_display()}
Duration     : {enrollment.course.duration}
Schedule     : {enrollment.get_schedule_display()}
Course Fee   : \u20A6{enrollment.course.fee:,.0f}
Status       : Pending Payment

━━━━━━━━━━━━━━━━━━━━━━━━
PAYMENT INSTRUCTIONS
━━━━━━━━━━━━━━━━━━━━━━━━
Bank         : ACCESS BANK
Account Name : IBRAHIM BABA SULEIMAN
Account No   : 1227425306
Amount       : \u20A6{enrollment.course.fee:,.0f}
Reference    : {ref}

After payment, send your receipt to:
WhatsApp: +234 808 110 1992

Your enrollment will be ACTIVATED within 2 hours of payment confirmation.

━━━━━━━━━━━━━━━━━━━━━━━━
STUDENT PORTAL
━━━━━━━━━━━━━━━━━━━━━━━━
Track your enrollment status anytime at:
http://127.0.0.1:8000/portal/dashboard/

Username: {enrollment.student.username}

━━━━━━━━━━━━━━━━━━━━━━━━

Questions? Contact us:
Phone/WhatsApp : +234 808 110 1992
Email          : info@sibrahtech.com.ng

We look forward to having you in class!

Best regards,
SIBRAH Academy Team
SIBRAH Computers & Technology Hub
Abuja, Nigeria
"""
    try:
        send_mail(
            subject        = subject,
            message        = message,
            from_email     = settings.DEFAULT_FROM_EMAIL,
            recipient_list = [enrollment.student.email],
            fail_silently  = True,
        )
    except Exception:
        pass


def _notify_admin_new_enrollment(enrollment):
    """Notify admin of a new course enrollment."""
    subject = f"[NEW ENROLLMENT] {enrollment.course.title} — {enrollment.student.get_full_name()}"
    message = f"""
NEW COURSE ENROLLMENT!

Student    : {enrollment.student.get_full_name()}
Student ID : {enrollment.student.student_id}
Email      : {enrollment.student.email}
Phone      : {enrollment.student.phone}
Course     : {enrollment.course.title}
Fee        : \u20A6{enrollment.course.fee:,.0f}
Schedule   : {enrollment.get_schedule_display()}

Manage at:
http://127.0.0.1:8000/admin/training/enrollment/
"""
    try:
        send_mail(
            subject        = subject,
            message        = message,
            from_email     = settings.DEFAULT_FROM_EMAIL,
            recipient_list = [settings.SIBRAH_COMPANY['email']],
            fail_silently  = True,
        )
    except Exception:
        pass


def _notify_admin_enrollment_proof(enrollment):
    """Notify admin that payment proof was submitted for enrollment."""
    subject = f"[PAYMENT PROOF] {enrollment.course.title} — {enrollment.student.get_full_name()}"
    message = f"""
Payment proof submitted for course enrollment.

Student    : {enrollment.student.get_full_name()}
Student ID : {enrollment.student.student_id}
Phone      : {enrollment.student.phone}
Course     : {enrollment.course.title}
Fee        : \u20A6{enrollment.course.fee:,.0f}
Reference  : {enrollment.payment_ref}

Please verify payment and activate this enrollment:
http://127.0.0.1:8000/admin/training/enrollment/

IMPORTANT: After verifying, change Status to "Active" to notify the student.
"""
    try:
        send_mail(
            subject        = subject,
            message        = message,
            from_email     = settings.DEFAULT_FROM_EMAIL,
            recipient_list = [settings.SIBRAH_COMPANY['email']],
            fail_silently  = True,
        )
    except Exception:
        pass


def send_enrollment_activated_email(enrollment):
    """
    Call this from Django Admin (or a signal) when enrollment is activated.
    Usage: from apps.training.views import send_enrollment_activated_email
    """
    subject = f"Enrollment Activated — {enrollment.course.title} | SIBRAH Academy"
    message = f"""
Dear {enrollment.student.first_name},

Great news! Your payment has been confirmed and your enrollment is now ACTIVE!

━━━━━━━━━━━━━━━━━━━━━━━━
ENROLLMENT ACTIVATED
━━━━━━━━━━━━━━━━━━━━━━━━
Course     : {enrollment.course.title}
Student ID : {enrollment.student.student_id}
Schedule   : {enrollment.get_schedule_display()}
Status     : ACTIVE ✓

You can now access your course materials and class schedule
by logging into your student portal:
http://127.0.0.1:8000/portal/dashboard/

Your trainer will contact you shortly with the first class details.

━━━━━━━━━━━━━━━━━━━━━━━━

Questions? WhatsApp: +234 808 110 1992

Welcome to SIBRAH Academy!

Best regards,
SIBRAH Academy Team
"""
    try:
        send_mail(
            subject        = subject,
            message        = message,
            from_email     = settings.DEFAULT_FROM_EMAIL,
            recipient_list = [enrollment.student.email],
            fail_silently  = True,
        )
    except Exception:
        pass
