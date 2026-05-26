from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegisterForm, UserProfileForm, UserEditForm, CourseForm, LessonForm, QuizForm, QuestionForm
from .models import UserProfile, Course, Lesson, Quiz, Question, Enrollment, Submission


def register_view(request):
    form = RegisterForm()
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            role = form.cleaned_data.get('role')
            profile = user.profile
            profile.role = role
            profile.save()
            login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('dashboard')
    return render(request, 'courses/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'courses/login.html')


@login_required
def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('login')


# UPDATED — now shows stats for both roles
@login_required
def dashboard_view(request):
    if request.user.profile.role == 'instructor':
        courses = Course.objects.filter(instructor=request.user)
        total_students = Enrollment.objects.filter(course__instructor=request.user).count()
        total_lessons = Lesson.objects.filter(course__instructor=request.user).count()
        total_quizzes = Quiz.objects.filter(lesson__course__instructor=request.user).count()
        context = {
            'courses': courses,
            'total_students': total_students,
            'total_lessons': total_lessons,
            'total_quizzes': total_quizzes,
        }
    else:
        enrolled_courses = Enrollment.objects.filter(student=request.user).values_list('course', flat=True)
        courses = Course.objects.filter(id__in=enrolled_courses)
        all_courses = Course.objects.all()
        total_submissions = Submission.objects.filter(student=request.user).count()
        correct_submissions = Submission.objects.filter(student=request.user, is_correct=True).count()
        score_percentage = 0
        if total_submissions > 0:
            score_percentage = round((correct_submissions / total_submissions) * 100)
        context = {
            'courses': courses,
            'all_courses': all_courses,
            'total_submissions': total_submissions,
            'correct_submissions': correct_submissions,
            'score_percentage': score_percentage,
        }
    return render(request, 'courses/dashboard.html', context)


# NEW — profile editing view
@login_required
def profile_view(request):
    if request.method == 'POST':
        user_form = UserEditForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = UserProfileForm(instance=request.user.profile)

    if request.user.profile.role == 'instructor':
        courses = Course.objects.filter(instructor=request.user)
    else:
        enrolled_ids = Enrollment.objects.filter(student=request.user).values_list('course', flat=True)
        courses = Course.objects.filter(id__in=enrolled_ids)

    total_submissions = Submission.objects.filter(student=request.user).count()
    correct_submissions = Submission.objects.filter(student=request.user, is_correct=True).count()

    return render(request, 'courses/profile.html', {
        'user_form': user_form,
        'profile_form': profile_form,
        'courses': courses,
        'total_submissions': total_submissions,
        'correct_submissions': correct_submissions,
    })


@login_required
def create_course_view(request):
    if request.user.profile.role != 'instructor':
        messages.error(request, 'Only instructors can create courses.')
        return redirect('dashboard')
    form = CourseForm()
    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES)
        if form.is_valid():
            course = form.save(commit=False)
            course.instructor = request.user
            course.save()
            messages.success(request, 'Course created successfully!')
            return redirect('course_detail', course_id=course.id)
    return render(request, 'courses/create_course.html', {'form': form})


@login_required
def course_detail_view(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    lessons = course.lessons.all()
    is_enrolled = Enrollment.objects.filter(student=request.user, course=course).exists()
    is_instructor = course.instructor == request.user
    student_count = Enrollment.objects.filter(course=course).count()
    return render(request, 'courses/course_detail.html', {
        'course': course,
        'lessons': lessons,
        'is_enrolled': is_enrolled,
        'is_instructor': is_instructor,
        'student_count': student_count,
    })


@login_required
def enroll_view(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    if request.user.profile.role == 'student':
        Enrollment.objects.get_or_create(student=request.user, course=course)
        messages.success(request, f'Enrolled in {course.title}!')
    return redirect('course_detail', course_id=course.id)


@login_required
def add_lesson_view(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    if course.instructor != request.user:
        messages.error(request, 'Only the course instructor can add lessons.')
        return redirect('course_detail', course_id=course.id)
    form = LessonForm()
    if request.method == 'POST':
        form = LessonForm(request.POST, request.FILES)
        if form.is_valid():
            lesson = form.save(commit=False)
            lesson.course = course
            lesson.save()
            messages.success(request, 'Lesson added!')
            return redirect('course_detail', course_id=course.id)
    return render(request, 'courses/add_lesson.html', {'form': form, 'course': course})


@login_required
def lesson_detail_view(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)
    quizzes = lesson.quizzes.all()
    is_enrolled = Enrollment.objects.filter(student=request.user, course=lesson.course).exists()
    is_instructor = lesson.course.instructor == request.user
    if not is_enrolled and not is_instructor:
        messages.error(request, 'You must enroll to view lessons.')
        return redirect('course_detail', course_id=lesson.course.id)
    return render(request, 'courses/lesson_detail.html', {
        'lesson': lesson,
        'quizzes': quizzes,
        'is_instructor': is_instructor,
    })


# NEW — create a quiz (just the title)
@login_required
def create_quiz_view(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)
    if lesson.course.instructor != request.user:
        messages.error(request, 'Only the course instructor can create quizzes.')
        return redirect('lesson_detail', lesson_id=lesson.id)
    form = QuizForm()
    if request.method == 'POST':
        form = QuizForm(request.POST)
        if form.is_valid():
            quiz = form.save(commit=False)
            quiz.lesson = lesson
            quiz.save()
            messages.success(request, 'Quiz created! Now add questions.')
            return redirect('add_question', quiz_id=quiz.id)
    return render(request, 'courses/create_quiz.html', {'form': form, 'lesson': lesson})


# NEW — add questions to a quiz one by one
@login_required
def add_question_view(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    if quiz.lesson.course.instructor != request.user:
        messages.error(request, 'Only the course instructor can add questions.')
        return redirect('lesson_detail', lesson_id=quiz.lesson.id)
    questions = quiz.questions.all()
    form = QuestionForm()
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.quiz = quiz
            if not question.order:
                question.order = questions.count() + 1
            question.save()
            messages.success(request, 'Question added!')
            return redirect('add_question', quiz_id=quiz.id)
    return render(request, 'courses/add_question.html', {
        'form': form,
        'quiz': quiz,
        'questions': questions,
    })


# NEW — take a quiz (all questions at once, submit together)
@login_required
def take_quiz_view(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    questions = quiz.questions.all()
    is_enrolled = Enrollment.objects.filter(student=request.user, course=quiz.lesson.course).exists()
    is_instructor = quiz.lesson.course.instructor == request.user

    if not is_enrolled and not is_instructor:
        messages.error(request, 'You must enroll to take quizzes.')
        return redirect('course_detail', course_id=quiz.lesson.course.id)

    already_taken = Submission.objects.filter(student=request.user, quiz=quiz).exists()

    if request.method == 'POST' and not already_taken:
        correct = 0
        total = questions.count()
        for question in questions:
            selected = request.POST.get(f'question_{question.id}')
            if selected:
                is_correct = selected == question.correct_answer
                if is_correct:
                    correct += 1
                Submission.objects.create(
                    student=request.user,
                    question=question,
                    quiz=quiz,
                    selected_answer=selected,
                    is_correct=is_correct,
                )
        if total > 0:
            pct = round(correct / total * 100)
        else:
            pct = 0
        messages.success(request, f'Quiz completed! You got {correct}/{total} correct ({pct}%).')
        return redirect('quiz_results', quiz_id=quiz.id)

    return render(request, 'courses/take_quiz.html', {
        'quiz': quiz,
        'questions': questions,
        'already_taken': already_taken,
    })


# NEW — show quiz results with correct/wrong answers
@login_required
def quiz_results_view(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    questions = quiz.questions.all()
    submissions = Submission.objects.filter(student=request.user, quiz=quiz)
    submission_map = {}
    for s in submissions:
        submission_map[s.question_id] = s
    results = []
    for question in questions:
        sub = submission_map.get(question.id)
        results.append({
            'question': question,
            'selected': sub.selected_answer if sub else None,
            'is_correct': sub.is_correct if sub else False,
        })
    correct_count = submissions.filter(is_correct=True).count()
    total_count = questions.count()
    if total_count > 0:
        percentage = round(correct_count / total_count * 100)
    else:
        percentage = 0
    return render(request, 'courses/quiz_results.html', {
        'quiz': quiz,
        'results': results,
        'correct_count': correct_count,
        'total_count': total_count,
        'percentage': percentage,
    })


# React browse page
@login_required
def browse_view(request):
    return render(request, 'courses/browse.html')


# NEW — student progress tracking page
@login_required
def progress_view(request):
    enrollments = Enrollment.objects.filter(student=request.user).select_related('course')
    course_progress = []
    for enrollment in enrollments:
        course = enrollment.course
        total_questions = Question.objects.filter(quiz__lesson__course=course).count()
        answered = Submission.objects.filter(student=request.user, quiz__lesson__course=course).count()
        correct = Submission.objects.filter(student=request.user, quiz__lesson__course=course, is_correct=True).count()
        if answered > 0:
            percentage = round(correct / answered * 100)
        else:
            percentage = 0
        course_progress.append({
            'course': course,
            'total_questions': total_questions,
            'answered': answered,
            'correct': correct,
            'percentage': percentage,
        })
    return render(request, 'courses/progress.html', {'course_progress': course_progress})