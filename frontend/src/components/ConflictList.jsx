function ConflictList({
  conflicts,
  onResolve,
}) {
  return (
    <section className="card">
      <div className="card-header">
        <h2>Conflicts</h2>

        <span className="count-badge">
          {conflicts.length}
        </span>
      </div>

      {conflicts.length === 0 ? (
        <div className="empty-state">
          No unresolved conflicts.
        </div>
      ) : (
        <div className="conflict-list">
          {conflicts.map((conflict) => (
            <div
              className="conflict-item"
              key={
                conflict.id ||
                conflict.action_ids?.join("-")
              }
            >
              <div>
                <strong>
                  {conflict.conflict_type}
                </strong>

                <p>
                  {conflict.description}
                </p>
              </div>

              <div className="conflict-side">
                <span
                  className={`severity severity-${conflict.severity}`}
                >
                  {conflict.severity}
                </span>

                {conflict.id && (
                  <button
                    className="secondary-button"
                    onClick={() =>
                      onResolve(conflict.id)
                    }
                  >
                    Resolve
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

export default ConflictList;