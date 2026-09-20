import { useEffect, useState } from "react";

import Header from "./components/Header";
import DailyBrief from "./components/DailyBrief";
import ActionList from "./components/ActionList";
import ConflictList from "./components/ConflictList";
import AskMeetOps from "./components/AskMeetOps";

import { api } from "./services/api";

function App() {
  const [actions, setActions] = useState([]);
  const [brief, setBrief] = useState(null);
  const [conflicts, setConflicts] = useState([]);

  const [backendHealthy, setBackendHealthy] =
    useState(false);

  const [aiServiceConnected, setAiServiceConnected] =
    useState(false);

  const [loading, setLoading] =
    useState(true);

  const [pipelineRunning, setPipelineRunning] =
    useState(false);

  const [error, setError] =
    useState("");

  async function loadHealth() {
    try {
      const health =
        await api.getHealth();

      // Backend is healthy when DB is connected (status === "healthy")
      setBackendHealthy(
        health?.status === "healthy"
      );

      // AI service is a separate concern
      setAiServiceConnected(
        health?.ai_service?.status === "connected"
      );
    } catch (err) {
      console.error(
        "Health check failed:",
        err
      );

      setBackendHealthy(false);
      setAiServiceConnected(false);
    }
  }

  async function loadDashboard() {
    try {
      setLoading(true);
      setError("");

      const [
        actionsResponse,
        briefResponse,
        conflictsResponse,
      ] = await Promise.all([
        api.getActions(),
        api.getLatestBrief(),
        api.getConflicts(false),
      ]);

      setActions(
        actionsResponse.actions || []
      );

      setBrief(
        briefResponse || null
      );

      setConflicts(
        conflictsResponse.conflicts || []
      );

      await loadHealth();
    } catch (err) {
      console.error(
        "Dashboard loading error:",
        err
      );

      setError(
        err.message ||
        "Failed to load dashboard"
      );

      await loadHealth();
    } finally {
      setLoading(false);
    }
  }

  async function runPipeline() {
    try {
      setPipelineRunning(true);
      setError("");

      await api.runPipeline({
        use_llm: false,
      });

      await loadDashboard();
    } catch (err) {
      console.error(
        "Pipeline error:",
        err
      );

      setError(
        err.message ||
        "Pipeline failed"
      );
    } finally {
      setPipelineRunning(false);
    }
  }

  async function completeAction(
    actionId
  ) {
    try {
      await api.updateActionStatus(
        actionId,
        "completed"
      );

      await loadDashboard();
    } catch (err) {
      console.error(
        "Action update error:",
        err
      );

      setError(
        err.message ||
        "Failed to update action"
      );
    }
  }

  async function resolveConflict(
    conflictId
  ) {
    try {
      await api.resolveConflict(
        conflictId
      );

      await loadDashboard();
    } catch (err) {
      console.error(
        "Conflict resolution error:",
        err
      );

      setError(
        err.message ||
        "Failed to resolve conflict"
      );
    }
  }

  async function askMeetOps(
    question
  ) {
    return api.askMeetOps(question);
  }

  useEffect(() => {
    loadDashboard();
  }, []);

  return (
    <div className="app">
      <Header
        backendHealthy={backendHealthy}
        aiServiceConnected={aiServiceConnected}
        onRefresh={loadDashboard}
        onRunPipeline={runPipeline}
        pipelineRunning={pipelineRunning}
      />

      <main className="dashboard">
        {error && (
          <div className="error-banner">
            {error}
          </div>
        )}

        {loading ? (
          <div className="loading">
            Loading MeetOps...
          </div>
        ) : (
          <>
            <DailyBrief
              brief={brief}
            />

            <div className="dashboard-grid">
              <ActionList
                title="My Actions"
                actions={actions.filter(
                  (action) =>
                    action.ownership ===
                    "my_action"
                )}
                onComplete={
                  completeAction
                }
              />

              <ActionList
                title="Waiting on Others"
                actions={actions.filter(
                  (action) =>
                    action.ownership ===
                    "waiting_on_other"
                )}
              />

              <ActionList
                title="Unclear Ownership"
                actions={actions.filter(
                  (action) =>
                    action.ownership ===
                    "unclear"
                )}
              />

              <ConflictList
                conflicts={conflicts}
                onResolve={
                  resolveConflict
                }
              />
            </div>

            <AskMeetOps
              onAsk={askMeetOps}
            />
          </>
        )}
      </main>
    </div>
  );
}

export default App;