function Header({
  backendHealthy,
  aiServiceConnected,
  onRefresh,
  onRunPipeline,
  pipelineRunning,
}) {
  // Determine the label and dot class for the combined status
  let statusLabel;
  let dotClass;

  if (!backendHealthy) {
    statusLabel = "Backend unavailable";
    dotClass = "status-dot";
  } else if (!aiServiceConnected) {
    statusLabel = "Backend connected · AI offline";
    dotClass = "status-dot degraded";
  } else {
    statusLabel = "All systems connected";
    dotClass = "status-dot healthy";
  }

  return (
    <header className="app-header">
      <div>
        <div className="brand">
          MeetOps
        </div>

        <div className="subtitle">
          Executive Productivity Agent
        </div>
      </div>

      <div className="header-actions">
        <div className="health-indicator">
          <span className={dotClass} />
          {statusLabel}
        </div>

        <button
          className="secondary-button"
          onClick={onRefresh}
        >
          Refresh
        </button>

        <button
          className="primary-button"
          onClick={onRunPipeline}
          disabled={pipelineRunning || !backendHealthy}
          title={
            !backendHealthy
              ? "Backend is not available"
              : !aiServiceConnected
              ? "AI service is offline — start it with: python ai_service/run.py --server"
              : "Run the MeetOps pipeline"
          }
        >
          {pipelineRunning
            ? "Running..."
            : "Run Pipeline"}
        </button>
      </div>
    </header>
  );
}

export default Header;