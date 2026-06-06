"""
SIBRAH Accounts App — Views
apps/accounts/views.py
"""

from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView, UpdateView
from django.urls import reverse_lazy
from .models import SibrahUser
from .forms import StudentRegistrationForm, StudentProfileForm
from apps.training.models import Enrollment
from apps.certificates.models import Certificate


def register_student(request):
    """Public student registration page."""
    if request.user.is_authenticated:
        return redirect('accounts:dashboard')
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = 'student'
            user.save()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            messages.success(request,
                f"Welcome {user.first_name}! Your student account has been created. "
                f"Your Student ID is: {user.student_id}")
            return redirect('accounts:dashboard')
    else:
        form = StudentRegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})


def student_login(request):
    """Student login page."""
    if request.user.is_authenticated:
        return redirect('accounts:dashboard')
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()
        user = authenticate(request, username=username, password=password)
        if user is None:
            # Try login by student_id
            try:
                u = SibrahUser.objects.get(student_id=username)
                user = authenticate(request, username=u.username, password=password)
            except SibrahUser.DoesNotExist:
                pass
        if user is not None:
            login(request, user)
            messages.success(request, f"Welcome back, {user.first_name}!")
            return redirect(request.GET.get('next', 'accounts:dashboard'))
        else:
            messages.error(request, "Invalid credentials. Please try again.")
    return render(request, 'accounts/login.html')


@login_required
def student_logout(request):
    logout(request)
    messages.info(request, "You have been logged out successfully.")
    return redirect('core:home')


@login_required
def dashboard(request):
    """Student dashboard."""
    user = request.user
    enrollments = Enrollment.objects.filter(student=user).select_related('course')
    certificates = Certificate.objects.filter(student=user)
    context = {
        'user': user,
        'enrollments': enrollments,
        'certificates': certificates,
        'total_courses': enrollments.count(),
        'completed_courses': enrollments.filter(status='completed').count(),
        'total_certificates': certificates.count(),
    }
    return render(request, 'accounts/dashboard.html', context)


@login_required
def edit_profile(request):
    """Edit student profile."""
    if request.method == 'POST':
        form = StudentProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect('accounts:dashboard')
    else:
        form = StudentProfileForm(instance=request.user)
    return render(request, 'accounts/edit_profile.html', {'form': form})


# ── ADMIN VIEWS ──

def admin_required(view_func):
    """Decorator: restrict to admin/staff users only."""
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_admin_user:
            messages.error(request, "You do not have permission to access the admin area.")
            return redirect('core:home')
        return view_func(request, *args, **kwargs)
    return wrapper


@admin_required
def admin_dashboard(request):
    """Admin overview dashboard."""
    from apps.shop.models import Order
    from apps.training.models import Course
    context = {
        'total_students':    SibrahUser.objects.filter(role='student').count(),
        'total_orders':      Order.objects.count(),
        'pending_orders':    Order.objects.filter(status='pending').count(),
        'total_courses':     Course.objects.count(),
        'total_enrollments': Enrollment.objects.count(),
        'total_certs':       Certificate.objects.count(),
        'recent_students':   SibrahUser.objects.filter(role='student').order_by('-created_at')[:5],
        'recent_orders':     Order.objects.order_by('-created_at')[:5],
    }
    return render(request, 'accounts/admin_dashboard.html', context)


@admin_required
def admin_students(request):
    students = SibrahUser.objects.filter(role='student').order_by('-created_at')
    return render(request, 'accounts/admin_students.html', {'students': students})


@admin_required
def admin_orders(request):
    from apps.shop.models import Order
    orders = Order.objects.all().order_by('-created_at')
    return render(request, 'accounts/admin_orders.html', {'orders': orders})


# ── PASSWORD MANAGEMENT ───────────────────────────────────────────────

@login_required
def change_password(request):
    """Allow logged-in student to change their own password."""
    if request.method == 'POST':
        old_password  = request.POST.get('old_password', '').strip()
        new_password1 = request.POST.get('new_password1', '').strip()
        new_password2 = request.POST.get('new_password2', '').strip()

        # Validate current password
        if not request.user.check_password(old_password):
            messages.error(request, "Your current password is incorrect. Please try again.")
            return redirect('accounts:change_password')

        # Check new passwords match
        if new_password1 != new_password2:
            messages.error(request, "Your new passwords do not match. Please try again.")
            return redirect('accounts:change_password')

        # Check minimum length
        if len(new_password1) < 8:
            messages.error(request, "Your new password must be at least 8 characters long.")
            return redirect('accounts:change_password')

        # All good — update password
        request.user.set_password(new_password1)
        request.user.save()

        # Keep user logged in after password change
        from django.contrib.auth import update_session_auth_hash
        update_session_auth_hash(request, request.user)

        messages.success(request, "Password changed successfully!")
        return redirect('accounts:password_change_success')

    return render(request, 'accounts/change_password.html')


def password_change_success(request):
    return render(request, 'accounts/password_change_success.html')


def forgot_password(request):
    """Send password reset link to student email."""
    if request.method == 'POST':
        email = request.POST.get('email', '').strip().lower()
        try:
            user = SibrahUser.objects.get(email=email)
            # Generate a simple reset token
            import hashlib, time
            token = hashlib.sha256(
                f"{user.pk}{user.email}{time.time()}".encode()
            ).hexdigest()[:32]

            # Store token temporarily in session
            request.session[f'reset_token_{token}'] = str(user.pk)
            request.session.set_expiry(3600)  # 1 hour

            # Send reset email
            from django.core.mail import send_mail
            from django.conf import settings
            reset_url = f"http://127.0.0.1:8000/portal/reset-password/{token}/"
            try:
                send_mail(
                    subject    = "Password Reset — SIBRAH Student Portal",
                    message    = f"""
Dear {user.first_name},

You requested a password reset for your SIBRAH student account.

Click the link below to reset your password (valid for 1 hour):
{reset_url}

If you did not request this, please ignore this email.
Your password will not change until you click the link above.

SIBRAH Technology Hub
+234 808 110 1992 | info@sibrahtech.com.ng
""",
                    from_email     = settings.DEFAULT_FROM_EMAIL,
                    recipient_list = [user.email],
                    fail_silently  = True,
                )
            except Exception:
                pass

            messages.success(request,
                f"A password reset link has been sent to {email}. "
                "Please check your inbox and spam folder.")
        except SibrahUser.DoesNotExist:
            # Don't reveal if email exists or not — security best practice
            messages.success(request,
                f"If an account exists for {email}, "
                "a reset link has been sent.")
        return redirect('accounts:forgot_password')

    return render(request, 'accounts/forgot_password.html')


def reset_password(request, token):
    """Handle password reset from email link."""
    user_id = request.session.get(f'reset_token_{token}')
    if not user_id:
        messages.error(request, "This password reset link is invalid or has expired.")
        return redirect('accounts:forgot_password')

    try:
        user = SibrahUser.objects.get(pk=user_id)
    except SibrahUser.DoesNotExist:
        messages.error(request, "Invalid reset link.")
        return redirect('accounts:forgot_password')

    if request.method == 'POST':
        new_password1 = request.POST.get('new_password1', '').strip()
        new_password2 = request.POST.get('new_password2', '').strip()

        if new_password1 != new_password2:
            messages.error(request, "Passwords do not match.")
            return redirect('accounts:reset_password', token=token)

        if len(new_password1) < 8:
            messages.error(request, "Password must be at least 8 characters.")
            return redirect('accounts:reset_password', token=token)

        user.set_password(new_password1)
        user.save()

        # Clear the token
        del request.session[f'reset_token_{token}']

        messages.success(request, "Password reset successfully! Please log in with your new password.")
        return redirect('accounts:login')

    return render(request, 'accounts/reset_password.html', {'token': token, 'user': user})
