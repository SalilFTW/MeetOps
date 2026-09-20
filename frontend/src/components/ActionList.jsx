function ActionList({
  title,
  actions,
  onComplete,
}) {
  return (
    <section className="card">
      <div className="card-header">
        <h2>{title}</h2>

        <span className="count-badge">
          {actions.length}
        </span>
      </div>

      {actions.length === 0 ? (
        <div className="empty-state">
          No actions in this category.
        </div>
      ) : (
        <div className="action-list">
          {actions.map((action) => (
            <div
              className="action-item"
              key={action.id}
            >
              <div className="action-main">
                <h3>{action.title}</h3>

                <div className="action-meta">
                  {action.recipient && (
                    <span>
                      Recipient: {action.recipient}
                    </span>
                  )}

                  {action.deadline_text && (
                    <span>
                      Deadline: {action.deadline_text}
                    </span>
                  )}
                </div>

                {action.notes?.length > 0 && (
                  <div className="action-note">
                    {action.notes[0]}
                  </div>
                )}
              </div>

              <div className="action-side">
                <span
                  className={`status-pill status-${action.status}`}
                >
                  {action.status}
                </span>

                {action.status !== "completed" && (
                  <button
                    className="complete-button"
                    onClick={() =>
                      onComplete(action.id)
                    }
                  >
                    Complete
                  </button>
                )}
              </div>
            </div>
          ))}
        </div>
      )}
    </section>
  );
}

export default ActionList;