function DailyBrief({
  brief,
}) {
  if (!brief) {
    return (
      <section className="card">
        <div className="empty-state">
          No daily brief available.
        </div>
      </section>
    );
  }

  return (
    <section className="brief-card">
      <div className="brief-heading">
        <div>
          <p className="eyebrow">
            DAILY BRIEF
          </p>

          <h1>
            Good morning, {brief.executive}
          </h1>

          <p className="brief-date">
            {brief.brief_date}
          </p>
        </div>
      </div>

      <p className="brief-summary">
        {brief.summary}
      </p>

      <div className="metrics">
        <div className="metric">
          <span className="metric-value">
            {brief.my_actions?.length || 0}
          </span>

          <span className="metric-label">
            My actions
          </span>
        </div>

        <div className="metric">
          <span className="metric-value">
            {brief.due_today?.length || 0}
          </span>

          <span className="metric-label">
            Due today
          </span>
        </div>

        <div className="metric">
          <span className="metric-value">
            {brief.overdue?.length || 0}
          </span>

          <span className="metric-label">
            Overdue
          </span>
        </div>

        <div className="metric">
          <span className="metric-value">
            {brief.waiting_on_others?.length || 0}
          </span>

          <span className="metric-label">
            Waiting
          </span>
        </div>

        <div className="metric">
          <span className="metric-value">
            {brief.unclear_actions?.length || 0}
          </span>

          <span className="metric-label">
            Unclear
          </span>
        </div>
      </div>
    </section>
  );
}

export default DailyBrief;