"""
SIBRAH Certificates App — Views
apps/certificates/views.py
"""

from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import Certificate


def verify(request):
    """Public certificate verification page."""
    result = None
    code   = ''
    if request.method == 'POST' or request.GET.get('code'):
        code = (request.POST.get('code') or request.GET.get('code', '')).strip().upper()
        if code:
            try:
                cert   = Certificate.objects.select_related('student', 'course').get(code=code)
                result = {'found': True, 'cert': cert}
            except Certificate.DoesNotExist:
                result = {'found': False}

    return render(request, 'certificates/verify.html', {
        'result': result,
        'code':   code,
    })


def certificate_detail(request, code):
    """Display a single certificate (printable view)."""
    cert = get_object_or_404(Certificate, code=code.upper(), is_valid=True)
    return render(request, 'certificates/detail.html', {'cert': cert})
