
const API = {
    fetchUserInfo: async function() {
        const res = await fetch('/api/user/');
        return await res.json();
    },

    fetchCourses: async function(search = '') {
        const res = await fetch('/api/courses/?search=' + search);
        return await res.json();
    },

    fetchCourseDetail: async function(courseId) {
        const res = await fetch('/api/courses/' + courseId + '/');
        return await res.json();
    },

    fetchLessonDetail: async function(lessonId) {
        const res = await fetch('/api/lessons/' + lessonId + '/');
        return await res.json();
    },

    enrollInCourse: async function(courseId) {
        const res = await fetch('/api/courses/' + courseId + '/enroll/', {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCookie('csrftoken'),
                'Content-Type': 'application/json',
            },
        });
        return await res.json();
    },

    submitQuiz: async function(quizId, answers) {
        const res = await fetch('/api/quiz/' + quizId + '/submit/', {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCookie('csrftoken'),
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ answers: answers }),
        });
        return await res.json();
    }
};