import { Router } from "express";
import { aiClient } from "../services/aiClient.js";
import {
  saveActionsBatch,
  saveConflictsBatch,
  saveDailyBrief,
  getActions,
} from "../database/db.js";

export const pipelineRouter = Router();

/**
 * Trigger the end-to-end AI extraction and reasoning pipeline,
 * persist all generated actions, conflicts, and briefs into SQLite,
 * and return the synchronized data.
 */
pipelineRouter.post("/run", async (req, res) => {
  try {
    const { use_llm = false, brief_date = null } = req.body || {};

    // 1. Call Python AI Service
    const aiResult = await aiClient.runPipeline({ use_llm, brief_date });

    if (!aiResult.success) {
      return res.status(500).json({
        success: false,
        error: aiResult.error || "AI pipeline failed without error details",
      });
    }

    const {
      canonical_actions = [],
      conflicts = [],
      daily_brief = null,
      my_actions = [],
      waiting_on_others = [],
      unclear_actions = [],
    } = aiResult;

    // 2. Persist to Database exclusively in JavaScript Backend
    if (canonical_actions.length > 0) {
      saveActionsBatch(canonical_actions);
    }

    if (conflicts.length > 0) {
      saveConflictsBatch(conflicts);
    }

    if (daily_brief) {
      saveDailyBrief(daily_brief);
    }

    // 3. Return persisted payload
    return res.json({
      success: true,
      persisted: {
        actions_count: canonical_actions.length,
        conflicts_count: conflicts.length,
        brief_saved: Boolean(daily_brief),
      },
      data: {
        daily_brief,
        canonical_actions,
        conflicts,
        grouped: {
          my_actions,
          waiting_on_others,
          unclear_actions,
        },
      },
    });
  } catch (err) {
    console.error("Pipeline run error:", err);
    return res.status(err.status || 500).json({
      success: false,
      error: err.message,
      details: err.details || null,
    });
  }
});
