# EduVerse — Online Learning Platform

A full-stack web application where instructors create courses with lessons and quizzes, and students enroll, learn, and track their progress.

Built with **Django**, **React.js**, and **SQLite**.

![Python](https://img.shields.io/badge/Python-3.13-blue)
![Django](https://img.shields.io/badge/Django-6.0-green)
![React](https://img.shields.io/badge/React-18-blue)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3-purple)
![License](https://img.shields.io/badge/License-MIT-yellow)

---

## Features

### Two User Roles

**Instructors can:**
- Create courses with thumbnail images
- Add lessons with file attachments (PDFs, documents, images)
- Create quizzes with multiple questions (A/B/C/D format)
- View enrollment statistics on their dashboard

**Students can:**
- Browse and search courses
- Enroll in courses
- View lesson content and download attachments
- Take multi-question quizzes
- View quiz results with correct/wrong answer feedback
- Track progress across all enrolled courses

### Core Functionality
- User registration and login with session-based authentication
- Role-based access control (instructors and students see different content)
- File uploads for profile pictures, course thumbnails, and lesson materials
- Automatic quiz grading with score percentage
- Color-coded quiz results (green for correct, red for wrong)
- Progress tracking with progress bars per course
- Dynamic React-powered course browser with live search
- REST API connecting the React frontend to the Django backend
- Responsive design (desktop and mobile)
- Django admin panel for database management

---

## Tech Stack

### Backend
- **Python 3.13** — programming language
- **Django 6.0** — web framework (routing, authentication, ORM, file uploads)
- **Django REST Framework** — REST API for the React frontend
- **SQLite** — relational database (built into Python)
- **Pillow** — image processing library

### Frontend
- **HTML5** — page structure
- **CSS3** — custom styling (CSS variables, gradients, transitions, animations)
- **Bootstrap 5** — responsive layout framework
- **Bootstrap Icons** — icon library
- **React.js 18** — dynamic course browser (single-page application)
- **Babel** — JSX to JavaScript compiler

---

## Database Schema

The application uses 7 custom models plus Django's built-in User model:

```
User (built-in) ←→ UserProfile (one-to-one)
User → Course (one-to-many: one instructor creates many courses)
Course → Lesson (one-to-many)
Lesson → Quiz (one-to-many)
Quiz → Question (one-to-many)
User ↔ Course through Enrollment (many-to-many)
User → Submission → Question (quiz answers with grading)
```

---

## Project Structure

```
online_education_site/
├── manage.py                  # Django management commands
├── db.sqlite3                 # SQLite database
├── media/                     # Uploaded files (images, PDFs)
├── lms_project/               # Project configuration
│   ├── settings.py            # App settings, database config
│   ├── urls.py                # Main URL router
│   ├── wsgi.py                # Production server interface
│   └── asgi.py                # Async server interface
└── courses/                   # Main application
    ├── models.py              # Database models (7 models)
    ├── forms.py               # Django forms (7 forms)
    ├── views.py               # View functions (16 views)
    ├── urls.py                # URL patterns (18 routes)
    ├── api_views.py           # REST API views (6 endpoints)
    ├── serializers.py         # JSON serializers
    ├── admin.py               # Admin panel registration
    └── templates/courses/     # HTML templates (15 templates)
        ├── base.html          # Master template (navbar, CSS, footer)
        ├── login.html         # Login page
        ├── register.html      # Registration page
        ├── dashboard.html     # Dashboard with stats
        ├── profile.html       # Profile editing
        ├── browse.html        # React-powered course browser
        ├── create_course.html # Course creation form
        ├── course_detail.html # Course detail page
        ├── add_lesson.html    # Lesson creation form
        ├── lesson_detail.html # Lesson detail with quizzes
        ├── create_quiz.html   # Quiz creation form
        ├── add_question.html  # Add questions to quiz
        ├── take_quiz.html     # Take quiz (all questions)
        ├── quiz_results.html  # Quiz results with feedback
        └── progress.html      # Student progress tracking
```

---

## Installation

### Prerequisites
- Python 3.10 or higher
- pip (Python package manager)

### Setup

1. **Clone the repository:**
```bash
git clone https://github.com/YOUR_USERNAME/eduverse-lms.git
cd eduverse-lms
```

2. **Create a virtual environment:**
```bash
python3 -m venv .venv
source .venv/bin/activate        # macOS/Linux
# .venv\Scripts\activate         # Windows
```

3. **Install dependencies:**
```bash
pip install django pillow djangorestframework
```

4. **Run database migrations:**
```bash
python manage.py makemigrations courses
python manage.py migrate
```

5. **Create a superuser (admin account):**
```bash
python manage.py createsuperuser
```

6. **Start the development server:**
```bash
python manage.py runserver
```

7. **Open in browser:**
```
http://127.0.0.1:8000/
```

---

## Usage

1. **Register** as an Instructor at `/register/`
2. **Create a course** with a title, description, and thumbnail image
3. **Add lessons** with content and file attachments
4. **Create quizzes** and add multiple-choice questions
5. **Log out** and register a Student account
6. **Browse courses** at `/browse/` and enroll
7. **Take quizzes** and view your results
8. **Track progress** at `/progress/`

### Admin Panel
Visit `/admin/` and log in with your superuser credentials to manage all data.

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/courses/` | List all courses (supports `?search=` parameter) |
| GET | `/api/courses/<id>/` | Get course details with lessons |
| POST | `/api/courses/<id>/enroll/` | Enroll in a course |
| GET | `/api/lessons/<id>/` | Get lesson details with quizzes |
| POST | `/api/quiz/<id>/submit/` | Submit quiz answers |
| GET | `/api/user/` | Get current user info |

---

## Screenshots

### Login Page
Clean centered login form with gradient navbar.

### Instructor Dashboard
Shows created courses, total students, total lessons in stat cards.

### Student Dashboard
Shows enrolled courses, questions answered, overall score percentage.

### Course Detail
Course info with thumbnail, enrollment button, lesson list with attachment indicators.

### Take Quiz
Multi-question quiz with radio buttons, color-coded answer options.

### Quiz Results
Score percentage with progress bar, each question marked correct (green) or wrong (red) with the right answer shown.

### Progress Tracking
Per-course progress bars with total questions, answered count, and correct count.

---

## Architecture

The project follows Django's **MVT (Model-View-Template)** pattern:

- **Models** — define database structure using Django ORM (Python → SQL automatically)
- **Views** — handle HTTP requests, business logic, and database queries
- **Templates** — generate HTML with Django template tags (`{% %}`, `{{ }}`)

The browse page additionally uses **REST API architecture**:
- Django serves JSON through API endpoints
- React fetches data with `fetch()` and renders the UI dynamically
- No page reloads — single-page application experience

---

## Author

**Abylaikhan** — Full-stack development, design, and implementation.

---

## License

This project is open source and available under the [MIT License](LICENSE).
