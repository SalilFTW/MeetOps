import { Router } from "express";
import {
  getActions,
  getActionById,
  updateActionStatus,
  saveAction,
} from "../database/db.js";

export const actionsRouter = Router();

/**
 * GET /api/actions
 * Query actions with optional filters: ?ownership=my_action&status=open&owner=Arjun
 */
actionsRouter.get("/", (req, res) => {
  try {
    const { ownership, status, owner } = req.query;
    const actions = getActions({ ownership, status, owner });

    const grouped = {
      my_actions: actions.filter((a) => a.ownership === "my_action"),
      waiting_on_others: actions.filter((a) => a.ownership === "waiting_on_other"),
      unclear: actions.filter((a) => a.ownership === "unclear"),
    };

    return res.json({
      total: actions.length,
      actions,
      grouped,
    });
  } catch (err) {
    return res.status(500).json({ error: err.message });
  }
});

/**
 * GET /api/actions/:id
 * Retrieve single action with attached source evidence
 */
actionsRouter.get("/:id", (req, res) => {
  try {
    const action = getActionById(req.params.id);
    if (!action) {
      return res.status(404).json({ error: "Action not found" });
    }
    return res.json(action);
  } catch (err) {
    return res.status(500).json({ error: err.message });
  }
});

/**
 * PATCH /api/actions/:id
 * Update action status ('open', 'completed', 'overdue') or append note
 */
actionsRouter.patch("/:id", (req, res) => {
  try {
    const { status, note, notes } = req.body;
    if (!status && !note && !notes) {
      return res.status(400).json({ error: "Provide at least status or note to update" });
    }

    const action = getActionById(req.params.id);
    if (!action) {
      return res.status(404).json({ error: "Action not found" });
    }

    const newStatus = status || action.status;
    const notesToAdd = note || notes;

    const updated = updateActionStatus(req.params.id, newStatus, notesToAdd);
    return res.json({
      success: true,
      action: updated,
    });
  } catch (err) {
    return res.status(500).json({ error: err.message });
  }
});
