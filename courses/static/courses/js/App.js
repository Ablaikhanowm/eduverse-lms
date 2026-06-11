function App() {
    const [view, setView] = React.useState('courses');
    const [courses, setCourses] = React.useState([]);
    const [selectedCourse, setSelectedCourse] = React.useState(null);
    const [selectedLesson, setSelectedLesson] = React.useState(null);
    const [searchTerm, setSearchTerm] = React.useState('');
    const [loading, setLoading] = React.useState(true);
    const [message, setMessage] = React.useState('');
    const [userInfo, setUserInfo] = React.useState(null);

    React.useEffect(() => {
        loadCourses();
        loadUserInfo();
    }, []);

    const loadUserInfo = async () => {
        const data = await API.fetchUserInfo();
        setUserInfo(data);
    };

    const loadCourses = async (search) => {
        setLoading(true);
        const data = await API.fetchCourses(search || '');
        setCourses(data);
        setLoading(false);
    };

    const loadCourseDetail = async (courseId) => {
        setLoading(true);
        const data = await API.fetchCourseDetail(courseId);
        setSelectedCourse(data);
        setView('courseDetail');
        setLoading(false);
    };

    const loadLessonDetail = async (lessonId) => {
        setLoading(true);
        const data = await API.fetchLessonDetail(lessonId);
        setSelectedLesson(data);
        setView('lessonDetail');
        setLoading(false);
    };

    const handleEnroll = async (courseId) => {
        const data = await API.enrollInCourse(courseId);
        setMessage(data.message);
        loadCourseDetail(courseId);
        setTimeout(() => setMessage(''), 3000);
    };

    const handleQuizSubmit = async (quizId, answer) => {
        const data = await API.submitQuiz(quizId, answer);
        setMessage(data.message);
        setTimeout(() => setMessage(''), 3000);
    };

    const handleSearch = (e) => {
        e.preventDefault();
        loadCourses(searchTerm);
    };

    if (loading && view === 'courses') {
        return (
            <div className="text-center mt-5">
                <div className="spinner-border" role="status"></div>
            </div>
        );
    }

    return (
        <div>
            {/* Flash message banner */}
            {message && (
                <div className={'alert ' + (message.includes('Correct') || message.includes('Enrolled') ? 'alert-success' : 'alert-warning')}>
                    {message}
                </div>
            )}

            {/* VIEW: Course List */}
            {view === 'courses' && (
                <div>
                    <div className="d-flex justify-content-between align-items-center mb-4">
                        <h2 style={{fontWeight: 800}}>Browse Courses</h2>
                        {userInfo && <span className="badge bg-primary">{userInfo.role}</span>}
                    </div>

                    {/* Search bar */}
                    <form onSubmit={handleSearch} className="mb-4">
                        <div className="input-group">
                            <input
                                type="text"
                                className="form-control"
                                placeholder="Search courses..."
                                value={searchTerm}
                                onChange={(e) => setSearchTerm(e.target.value)}
                            />
                            <button className="btn btn-primary" type="submit">Search</button>
                            {searchTerm && (
                                <button
                                    className="btn btn-outline-secondary"
                                    type="button"
                                    onClick={() => { setSearchTerm(''); loadCourses(); }}
                                >
                                    Clear
                                </button>
                            )}
                        </div>
                    </form>

                    {/* Course grid */}
                    <div className="row">
                        {courses.map(course => (
                            <div key={course.id} className="col-md-4 mb-4">
                                <div className="card h-100 shadow-sm">
                                    {course.thumbnail && (
                                        <img
                                            src={course.thumbnail}
                                            className="card-img-top"
                                            alt={course.title}
                                            style={{height: '200px', objectFit: 'cover'}}
                                        />
                                    )}
                                    <div className="card-body d-flex flex-column">
                                        <h5 className="card-title">{course.title}</h5>
                                        <p className="text-muted small">by {course.instructor_name}</p>
                                        <p className="card-text">
                                            {course.description.substring(0, 100)}...
                                        </p>
                                        <div className="mt-auto d-flex justify-content-between align-items-center">
                                            <span className="badge bg-secondary">
                                                {course.lesson_count} lessons
                                            </span>
                                            <button
                                                className="btn btn-primary btn-sm"
                                                onClick={() => loadCourseDetail(course.id)}
                                            >
                                                View Course
                                            </button>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        ))}
                        {courses.length === 0 && (
                            <p className="text-muted">No courses found.</p>
                        )}
                    </div>
                </div>
            )}

            {/* VIEW: Course Detail */}
            {view === 'courseDetail' && selectedCourse && (
                <div>
                    <button
                        className="btn btn-outline-secondary mb-3"
                        onClick={() => { setView('courses'); loadCourses(); }}
                    >
                        &larr; Back to Courses
                    </button>

                    <div className="row">
                        <div className="col-md-8">
                            <h2>{selectedCourse.title}</h2>
                            <p className="text-muted">by {selectedCourse.instructor_name}</p>
                            <p>{selectedCourse.description}</p>

                            {selectedCourse.thumbnail && (
                                <img
                                    src={selectedCourse.thumbnail}
                                    className="img-fluid rounded mb-3"
                                    style={{maxHeight: '300px'}}
                                    alt={selectedCourse.title}
                                />
                            )}

                            {!selectedCourse.is_enrolled && userInfo && userInfo.role === 'student' && (
                                <button
                                    className="btn btn-success mb-3"
                                    onClick={() => handleEnroll(selectedCourse.id)}
                                >
                                    Enroll in this Course
                                </button>
                            )}
                            {selectedCourse.is_enrolled && (
                                <span className="badge bg-success mb-3 d-inline-block">Enrolled</span>
                            )}

                            <h4 className="mt-4">
                                Lessons ({selectedCourse.lessons.length})
                            </h4>
                            <div className="list-group">
                                {selectedCourse.lessons.map(lesson => (
                                    <button
                                        key={lesson.id}
                                        className="list-group-item list-group-item-action"
                                        onClick={() => loadLessonDetail(lesson.id)}
                                    >
                                        <strong>{lesson.order}.</strong> {lesson.title}
                                    </button>
                                ))}
                                {selectedCourse.lessons.length === 0 && (
                                    <p className="text-muted mt-2">No lessons yet.</p>
                                )}
                            </div>
                        </div>
                    </div>
                </div>
            )}

            {/* VIEW: Lesson Detail */}
            {view === 'lessonDetail' && selectedLesson && (
                <div>
                    <button
                        className="btn btn-outline-secondary mb-3"
                        onClick={() => loadCourseDetail(selectedLesson.course_id)}
                    >
                        &larr; Back to {selectedLesson.course_title}
                    </button>

                    <h2>{selectedLesson.title}</h2>
                    <div className="card mb-4">
                        <div className="card-body">
                            <p>{selectedLesson.content}</p>
                            {selectedLesson.file && (

                                    href={selectedLesson.file}
                                    className="btn btn-sm btn-outline-secondary"
                                    download
                                >
                                    Download Attachment
                                </a>
                            )}
                        </div>
                    </div>

                    <h4>Quizzes</h4>
                    {selectedLesson.quizzes.map(quiz => (
                        <QuizCard
                            key={quiz.id}
                            quiz={quiz}
                            onSubmit={handleQuizSubmit}
                        />
                    ))}
                    {selectedLesson.quizzes.length === 0 && (
                        <p className="text-muted">No quizzes for this lesson.</p>
                    )}
                </div>
            )}
        </div>
    );
}