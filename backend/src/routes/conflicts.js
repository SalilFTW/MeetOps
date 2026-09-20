import { Router } from "express";
import { getConflicts, resolveConflict } from "../database/db.js";

export const conflictsRouter = Router();

/**
 * GET /api/conflicts
 * List conflicts, optionally filtered by ?resolved=true/false
 */
conflictsRouter.get("/", (req, res) => {
  try {
    const { resolved } = req.query;
    const isResolved = resolved !== undefined ? resolved === "true" : undefined;
    const conflicts = getConflicts({ resolved: isResolved });

    return res.json({
      total: conflicts.length,
      conflicts,
    });
  } catch (err) {
    return res.status(500).json({ error: err.message });
  }
});

/**
 * POST /api/conflicts/:id/resolve
 * Mark a conflict as resolved
 */
conflictsRouter.post("/:id/resolve", (req, res) => {
  try {
    resolveConflict(parseInt(req.params.id, 10));
    return res.json({ success: true, message: `Conflict ${req.params.id} marked as resolved` });
  } catch (err) {
    return res.status(500).json({ error: err.message });
  }
});
