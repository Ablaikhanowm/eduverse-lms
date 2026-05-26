from django.urls import path
from django.shortcuts import redirect
from . import views
from . import api_views

urlpatterns = [
    path('', lambda request: redirect('login'), name='home'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('profile/', views.profile_view, name='profile'),
    path('progress/', views.progress_view, name='progress'),
    path('course/create/', views.create_course_view, name='create_course'),
    path('course/<int:course_id>/', views.course_detail_view, name='course_detail'),
    path('course/<int:course_id>/enroll/', views.enroll_view, name='enroll'),
    path('course/<int:course_id>/add-lesson/', views.add_lesson_view, name='add_lesson'),
    path('lesson/<int:lesson_id>/', views.lesson_detail_view, name='lesson_detail'),
    path('lesson/<int:lesson_id>/create-quiz/', views.create_quiz_view, name='create_quiz'),
    path('quiz/<int:quiz_id>/add-question/', views.add_question_view, name='add_question'),
    path('quiz/<int:quiz_id>/take/', views.take_quiz_view, name='take_quiz'),
    path('quiz/<int:quiz_id>/results/', views.quiz_results_view, name='quiz_results'),
    path('browse/', views.browse_view, name='browse'),

    # API endpoints
    path('api/courses/', api_views.api_courses, name='api_courses'),
    path('api/courses/<int:course_id>/', api_views.api_course_detail, name='api_course_detail'),
    path('api/courses/<int:course_id>/enroll/', api_views.api_enroll, name='api_enroll'),
    path('api/lessons/<int:lesson_id>/', api_views.api_lesson_detail, name='api_lesson_detail'),
    path('api/quiz/<int:quiz_id>/submit/', api_views.api_submit_quiz, name='api_submit_quiz'),
    path('api/user/', api_views.api_user_info, name='api_user_info'),
]