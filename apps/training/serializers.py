from rest_framework import serializers
from .models import Course, Enrollment

class CourseSerializer(serializers.ModelSerializer):
    level_display = serializers.CharField(source='get_level_display', read_only=True)
    class Meta:
        model  = Course
        fields = ['id','title','slug','level','level_display','description',
                  'duration','fee','icon','tools','schedule']

class EnrollmentSerializer(serializers.ModelSerializer):
    course_title = serializers.CharField(source='course.title', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    class Meta:
        model  = Enrollment
        fields = ['id','course','course_title','status','status_display',
                  'schedule','progress','enrolled_at']
