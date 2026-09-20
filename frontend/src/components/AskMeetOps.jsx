import { useState } from "react";

function AskMeetOps({
  onAsk,
}) {
  const [question, setQuestion] =
    useState("");

  const [answer, setAnswer] =
    useState(null);

  const [loading, setLoading] =
    useState(false);

  const [error, setError] =
    useState(null);

  async function handleSubmit(event) {
    event.preventDefault();

    const trimmedQuestion =
      question.trim();

    if (!trimmedQuestion) {
      return;
    }

    setLoading(true);
    setError(null);
    setAnswer(null);

    try {
      const result = await onAsk(
        trimmedQuestion
      );

      setAnswer(result);
    } catch (err) {
      setError(
        err.message ||
        "Failed to get an answer"
      );
    } finally {
      setLoading(false);
    }
  }

  return (
    <section className="card">
      <div className="card-header">
        <h2>Ask MeetOps</h2>
      </div>

      <form
        className="question-form"
        onSubmit={handleSubmit}
      >
        <input
          type="text"
          value={question}
          onChange={(event) =>
            setQuestion(event.target.value)
          }
          placeholder="What did I promise Raghav?"
        />

        <button
          type="submit"
          disabled={
            loading ||
            !question.trim()
          }
          className="primary-button"
        >
          {loading
            ? "Thinking..."
            : "Ask"}
        </button>
      </form>

      {error && (
        <div className="error-message">
          {error}
        </div>
      )}

      {answer && (
        <div className="answer-box">
          <h3>Answer</h3>

          <p>
            {answer.answer}
          </p>

          {answer.confidence !== undefined && (
            <p className="answer-confidence">
              Confidence: {answer.confidence}
            </p>
          )}

          {answer.evidence?.length > 0 && (
            <>
              <h4>Evidence</h4>

              <ul>
                {answer.evidence.map(
                  (item, index) => (
                    <li key={index}>
                      {typeof item === "string"
                        ? item
                        : item.excerpt ||
                          JSON.stringify(item)}
                    </li>
                  )
                )}
              </ul>
            </>
          )}
        </div>
      )}
    </section>
  );
}

export default AskMeetOps;