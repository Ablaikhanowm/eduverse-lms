from rest_framework import serializers
from .models import Course, Lesson, Quiz, Enrollment, Submission


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ['id', 'title', 'content', 'file', 'order', 'created_at']


class QuizSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quiz
        fields = ['id', 'question', 'option_a', 'option_b', 'option_c', 'option_d']


class CourseSerializer(serializers.ModelSerializer):
    instructor_name = serializers.CharField(source='instructor.username', read_only=True)
    lesson_count = serializers.SerializerMethodField()
    is_enrolled = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = ['id', 'title', 'description', 'thumbnail', 'instructor_name', 'lesson_count', 'is_enrolled', 'created_at']

    def get_lesson_count(self, obj):
        return obj.lessons.count()

    def get_is_enrolled(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return Enrollment.objects.filter(student=request.user, course=obj).exists()
        return False