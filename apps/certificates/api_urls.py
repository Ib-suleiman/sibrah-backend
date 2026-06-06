from django.urls import path
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from .models import Certificate

@api_view(['GET'])
@permission_classes([AllowAny])
def verify_api(request):
    code = request.GET.get('code', '').strip().upper()
    if not code:
        return Response({'error': 'Please provide a certificate code.'}, status=400)
    try:
        cert = Certificate.objects.select_related('student', 'course').get(code=code)
        if not cert.is_valid:
            return Response({'valid': False, 'message': 'This certificate has been revoked.'})
        return Response({
            'valid':      True,
            'code':       cert.code,
            'student':    cert.student.full_name,
            'course':     cert.course.title,
            'grade':      cert.get_grade_display(),
            'issued_at':  cert.issued_at,
            'issued_by':  cert.issued_by,
            'instructor': cert.instructor,
        })
    except Certificate.DoesNotExist:
        return Response({'valid': False, 'message': 'Certificate not found.'}, status=404)

urlpatterns = [
    path('verify/', verify_api, name='verify_api'),
]
