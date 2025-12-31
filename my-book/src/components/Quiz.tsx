import React from 'react';
import styles from './Quiz.module.css';

interface QuizQuestion {
  id: number;
  question: string;
  options: string[];
  correctAnswer: number;
  explanation: string;
}

interface QuizProps {
  title: string;
  questions: QuizQuestion[];
  passingScore?: number;
}

/**
 * Quiz Component
 * Interactive quiz with immediate feedback and score tracking
 */
export default function Quiz({
  title,
  questions,
  passingScore = 80,
}: QuizProps): JSX.Element {
  const [currentQuestion, setCurrentQuestion] = React.useState(0);
  const [selectedAnswers, setSelectedAnswers] = React.useState<
    (number | null)[]
  >(new Array(questions.length).fill(null));
  const [showResults, setShowResults] = React.useState(false);

  const handleSelectAnswer = (answerIndex: number) => {
    const newAnswers = [...selectedAnswers];
    newAnswers[currentQuestion] = answerIndex;
    setSelectedAnswers(newAnswers);
  };

  const handleNext = () => {
    if (currentQuestion < questions.length - 1) {
      setCurrentQuestion(currentQuestion + 1);
    }
  };

  const handlePrevious = () => {
    if (currentQuestion > 0) {
      setCurrentQuestion(currentQuestion - 1);
    }
  };

  const handleSubmit = () => {
    setShowResults(true);
  };

  const handleReset = () => {
    setCurrentQuestion(0);
    setSelectedAnswers(new Array(questions.length).fill(null));
    setShowResults(false);
  };

  const correctCount = selectedAnswers.filter(
    (answer, index) =>
      answer !== null && answer === questions[index].correctAnswer
  ).length;

  const score = Math.round((correctCount / questions.length) * 100);
  const isPassing = score >= passingScore;
  const question = questions[currentQuestion];
  const isAnswered = selectedAnswers[currentQuestion] !== null;

  if (showResults) {
    return (
      <div className={styles.quiz}>
        <div className={styles.resultsContainer}>
          <div className={`${styles.scoreDisplay} ${isPassing ? styles.passing : styles.failing}`}>
            <div className={styles.scoreNumber}>{score}%</div>
            <div className={styles.scoreLabel}>
              {isPassing ? '✅ Passed!' : '❌ Needs Review'}
            </div>
          </div>

          <div className={styles.resultsStats}>
            <p className={styles.statsText}>
              You answered <strong>{correctCount} out of {questions.length}</strong> questions
              correctly.
            </p>
            {isPassing ? (
              <p className={styles.successMessage}>
                Great job! You have a solid understanding of this material.
              </p>
            ) : (
              <p className={styles.reviewMessage}>
                Review the material and try again. You're almost there!
              </p>
            )}
          </div>

          <div className={styles.resultsList}>
            {questions.map((q, idx) => (
              <div
                key={idx}
                className={`${styles.resultItem} ${
                  selectedAnswers[idx] === q.correctAnswer
                    ? styles.correct
                    : styles.incorrect
                }`}
              >
                <div className={styles.resultHeader}>
                  <span className={styles.resultNumber}>Q{idx + 1}</span>
                  <span className={styles.resultIcon}>
                    {selectedAnswers[idx] === q.correctAnswer ? '✓' : '✗'}
                  </span>
                </div>
                <p className={styles.resultQuestion}>{q.question}</p>
                <p className={styles.resultCorrect}>
                  Correct: {q.options[q.correctAnswer]}
                </p>
              </div>
            ))}
          </div>

          <button className={styles.retakeBtn} onClick={handleReset}>
            🔄 Retake Quiz
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className={styles.quiz}>
      <div className={styles.header}>
        <h3 className={styles.title}>{title}</h3>
        <div className={styles.progress}>
          {currentQuestion + 1} / {questions.length}
        </div>
      </div>

      <div className={styles.progressBar}>
        <div
          className={styles.progressFill}
          style={{ width: `${((currentQuestion + 1) / questions.length) * 100}%` }}
        />
      </div>

      <div className={styles.questionContainer}>
        <h4 className={styles.questionText}>{question.question}</h4>

        <div className={styles.optionsContainer}>
          {question.options.map((option, idx) => (
            <label
              key={idx}
              className={`${styles.option} ${
                selectedAnswers[currentQuestion] === idx ? styles.selected : ''
              }`}
            >
              <input
                type="radio"
                name={`question-${currentQuestion}`}
                value={idx}
                checked={selectedAnswers[currentQuestion] === idx}
                onChange={() => handleSelectAnswer(idx)}
                className={styles.radioInput}
              />
              <span className={styles.optionLabel}>{option}</span>
            </label>
          ))}
        </div>
      </div>

      <div className={styles.navigationButtons}>
        <button
          className={styles.navBtn}
          onClick={handlePrevious}
          disabled={currentQuestion === 0}
        >
          ← Previous
        </button>

        {currentQuestion === questions.length - 1 ? (
          <button
            className={`${styles.submitBtn} ${!isAnswered ? styles.disabled : ''}`}
            onClick={handleSubmit}
            disabled={selectedAnswers.some((a) => a === null)}
          >
            Submit Quiz
          </button>
        ) : (
          <button
            className={`${styles.navBtn} ${!isAnswered ? styles.disabled : ''}`}
            onClick={handleNext}
            disabled={!isAnswered}
          >
            Next →
          </button>
        )}
      </div>

      <div className={styles.answerStatus}>
        <span className={styles.statusText}>
          {isAnswered ? '✓ Answered' : '○ Not answered'}
        </span>
      </div>
    </div>
  );
}
