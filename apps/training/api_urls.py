from django.urls import path
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .models import Course
from .serializers import CourseSerializer

@api_view(['GET'])
@permission_classes([AllowAny])
def courses_api(request):
    courses = Course.objects.filter(is_active=True)
    return Response(CourseSerializer(courses, many=True).data)

urlpatterns = [
    path('courses/', courses_api, name='courses_api'),
]
