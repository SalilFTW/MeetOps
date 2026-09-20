import express from "express";
import cors from "cors";
import { config } from "./config.js";
import { initDatabase, db } from "./database/db.js";
import { aiClient } from "./services/aiClient.js";
import { pipelineRouter } from "./routes/pipeline.js";
import { actionsRouter } from "./routes/actions.js";
import { briefsRouter } from "./routes/briefs.js";
import { conflictsRouter } from "./routes/conflicts.js";

const app = express();

app.use(cors());
app.use(express.json());

// Initialize SQLite database tables and indices
initDatabase();

// Mount API routes
app.use("/api/pipeline", pipelineRouter);
app.use("/api/actions", actionsRouter);
app.use("/api/briefs", briefsRouter);
app.use("/api/conflicts", conflictsRouter);

// Health check endpoint
app.get("/api/health", async (req, res) => {
  let dbStatus = "unknown";
  try {
    const row = db.prepare("SELECT 1 AS ok").get();
    dbStatus = row && row.ok === 1 ? "connected" : "error";
  } catch (err) {
    dbStatus = `error: ${err.message}`;
  }

  let aiStatus = "unknown";
  try {
    const aiHealth = await aiClient.checkHealth();
    aiStatus = aiHealth?.status === "healthy" ? "connected" : "unhealthy";
  } catch (err) {
    aiStatus = `disconnected (${err.message})`;
  }

  const healthy = dbStatus === "connected" && aiStatus === "connected";

  return res.status(healthy ? 200 : 207).json({
    status: healthy ? "healthy" : "degraded",
    backend: "running",
    database: {
      type: "sqlite",
      path: config.dbPath,
      status: dbStatus,
    },
    ai_service: {
      url: config.aiServiceUrl,
      status: aiStatus,
    },
    timestamp: new Date().toISOString(),
  });
});

app.get("/", (req, res) => {
  res.json({
    app: config.appName,
    tier: "JavaScript Backend",
    version: "1.0.0",
    executive: config.executiveName,
    endpoints: {
      health: "/api/health",
      run_pipeline: "POST /api/pipeline/run",
      actions: "GET /api/actions",
      latest_brief: "GET /api/briefs/latest",
      conflicts: "GET /api/conflicts",
    },
  });
});

// Error handling middleware
app.use((err, req, res, next) => {
  console.error("Unhandled error:", err);
  res.status(500).json({
    error: err.message || "Internal server error",
  });
});

// Start listening if executed directly
if (process.env.NODE_ENV !== "test") {
  app.listen(config.port, () => {
    console.log(`=============================================================`);
    console.log(` MEETOPS JAVASCRIPT BACKEND RUNNING ON http://127.0.0.1:${config.port}`);
    console.log(` SQLite Database connected at: ${config.dbPath}`);
    console.log(` AI Microservice expected at: ${config.aiServiceUrl}`);
    console.log(` Health check: http://127.0.0.1:${config.port}/api/health`);
    console.log(`=============================================================`);
  });
}

export default app;
