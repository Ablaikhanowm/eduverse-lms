function QuizCard({ quiz, onSubmit }) {
    const [selected, setSelected] = React.useState('');
    const [submitted, setSubmitted] = React.useState(false);

    const handleSubmit = () => {
        if (selected) {
            onSubmit(quiz.id, selected);
            setSubmitted(true);
        }
    };

    return (
        <div className="card mb-3">
            <div className="card-body">
                <h5>{quiz.question}</h5>
                {['A', 'B', 'C', 'D'].map(option => (
                    <div key={option} className="form-check mb-2">
                        <input
                            className="form-check-input"
                            type="radio"
                            name={'quiz-' + quiz.id}
                            value={option}
                            id={'q' + quiz.id + '-' + option}
                            onChange={() => setSelected(option)}
                            disabled={submitted}
                        />
                        <label className="form-check-label" htmlFor={'q' + quiz.id + '-' + option}>
                            {option}) {quiz['option_' + option.toLowerCase()]}
                        </label>
                    </div>
                ))}
                {!submitted && (
                    <button className="btn btn-primary mt-2" onClick={handleSubmit} disabled={!selected}>
                        Submit Answer
                    </button>
                )}
                {submitted && <span className="badge bg-info mt-2">Answer submitted!</span>}
            </div>
        </div>
    );
}