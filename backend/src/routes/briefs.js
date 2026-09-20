import { Router } from "express";
import {
  getLatestDailyBrief,
  getDailyBriefByDate,
} from "../database/db.js";

export const briefsRouter = Router();

/**
 * GET /api/briefs/latest
 * Return the most recent persisted executive daily brief
 */
briefsRouter.get("/latest", (req, res) => {
  try {
    const brief = getLatestDailyBrief();
    if (!brief) {
      return res.status(404).json({ error: "No daily brief found in database" });
    }
    return res.json(brief);
  } catch (err) {
    return res.status(500).json({ error: err.message });
  }
});

/**
 * GET /api/briefs/:date
 * Return daily brief for a given ISO date (YYYY-MM-DD)
 */
briefsRouter.get("/:date", (req, res) => {
  try {
    const brief = getDailyBriefByDate(req.params.date);
    if (!brief) {
      return res.status(404).json({ error: `No daily brief found for date ${req.params.date}` });
    }
    return res.json(brief);
  } catch (err) {
    return res.status(500).json({ error: err.message });
  }
});
