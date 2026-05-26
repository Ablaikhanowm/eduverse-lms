from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Course, Lesson, Quiz, Enrollment, Submission
from .serializers import CourseSerializer, LessonSerializer, QuizSerializer


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def api_courses(request):
    search = request.GET.get('search', '')
    courses = Course.objects.all()
    if search:
        courses = courses.filter(title__icontains=search)
    serializer = CourseSerializer(courses, many=True, context={'request': request})
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def api_course_detail(request, course_id):
    course = Course.objects.get(id=course_id)
    lessons = course.lessons.all()
    course_data = CourseSerializer(course, context={'request': request}).data
    course_data['lessons'] = LessonSerializer(lessons, many=True).data
    return Response(course_data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def api_enroll(request, course_id):
    course = Course.objects.get(id=course_id)
    enrollment, created = Enrollment.objects.get_or_create(student=request.user, course=course)
    if created:
        return Response({'status': 'enrolled', 'message': f'Enrolled in {course.title}!'})
    return Response({'status': 'already_enrolled', 'message': 'Already enrolled.'})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def api_lesson_detail(request, lesson_id):
    lesson = Lesson.objects.get(id=lesson_id)
    quizzes = lesson.quizzes.all()
    lesson_data = LessonSerializer(lesson).data
    lesson_data['quizzes'] = QuizSerializer(quizzes, many=True).data
    lesson_data['course_title'] = lesson.course.title
    lesson_data['course_id'] = lesson.course.id
    return Response(lesson_data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def api_submit_quiz(request, quiz_id):
    quiz = Quiz.objects.get(id=quiz_id)
    selected = request.data.get('answer')
    is_correct = selected == quiz.correct_answer
    Submission.objects.create(
        student=request.user,
        quiz=quiz,
        selected_answer=selected,
        is_correct=is_correct,
    )
    return Response({
        'is_correct': is_correct,
        'correct_answer': quiz.correct_answer,
        'message': 'Correct!' if is_correct else f'Wrong! The correct answer was {quiz.correct_answer}.'
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def api_user_info(request):
    return Response({
        'username': request.user.username,
        'role': request.user.profile.role,
    })