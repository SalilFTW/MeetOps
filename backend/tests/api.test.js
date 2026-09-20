import { test, describe, before, after } from "node:test";
import assert from "node:assert/strict";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));

// Point test to in-memory/temp database
const testDbPath = path.resolve(__dirname, "../../data/test_meetops.db");
process.env.DB_PATH = testDbPath;
process.env.NODE_ENV = "test";

const { initDatabase, db, saveAction, getActions, getActionById, updateActionStatus, saveDailyBrief, getLatestDailyBrief, saveConflictsBatch, getConflicts } = await import("../src/database/db.js");

describe("MeetOps JavaScript Backend - Database & Model Tests", () => {
  before(() => {
    initDatabase();
  });

  after(() => {
    try {
      db.close();
      if (fs.existsSync(testDbPath)) {
        fs.unlinkSync(testDbPath);
      }
    } catch {
      // ignore
    }
  });

  test("Database initializes and creates tables", () => {
    const tables = db.prepare("SELECT name FROM sqlite_master WHERE type='table';").all().map(t => t.name);
    assert.ok(tables.includes("actions"));
    assert.ok(tables.includes("source_evidence"));
    assert.ok(tables.includes("conflicts"));
    assert.ok(tables.includes("daily_briefs"));
  });

  test("saveAction inserts and retrieves canonical action with evidence", () => {
    const action = {
      id: "test_action_001",
      title: "Send updated vendor list",
      action_type: "commitment",
      owner: "Arjun Malhotra",
      recipient: "Raghav Sethi",
      ownership: "my_action",
      deadline: "2026-09-22T17:00:00.000Z",
      deadline_text: "by end of day tomorrow",
      status: "open",
      confidence: 0.98,
      notes: ["High priority"],
      source_evidence: [
        {
          source_type: "meeting_transcript",
          source_id: "leadership_sync",
          reference_id: "sec_1",
          timestamp: "2026-09-21T10:00:00.000Z",
          excerpt: "I will send Raghav the updated vendor list tomorrow."
        }
      ]
    };

    saveAction(action);

    const retrieved = getActionById("test_action_001");
    assert.ok(retrieved);
    assert.equal(retrieved.title, "Send updated vendor list");
    assert.equal(retrieved.owner, "Arjun Malhotra");
    assert.equal(retrieved.ownership, "my_action");
    assert.equal(retrieved.source_evidence.length, 1);
    assert.equal(retrieved.source_evidence[0].source_id, "leadership_sync");
    assert.deepEqual(retrieved.notes, ["High priority"]);
  });

  test("updateActionStatus updates status and appends note", () => {
    const updated = updateActionStatus("test_action_001", "completed", "Sent to Raghav at 4pm");
    assert.equal(updated.status, "completed");
    assert.ok(updated.notes.includes("Sent to Raghav at 4pm"));
  });

  test("getActions filters by ownership and status", () => {
    const myActions = getActions({ ownership: "my_action" });
    assert.equal(myActions.length, 1);

    const openActions = getActions({ status: "open" });
    assert.equal(openActions.length, 0);

    const completedActions = getActions({ status: "completed" });
    assert.equal(completedActions.length, 1);
  });

  test("saveConflictsBatch and getConflicts store detected conflicts", () => {
    saveConflictsBatch([
      {
        conflict_type: "ownership",
        description: "Different owners Divya vs Arjun",
        severity: "high",
        action_ids: ["act_1", "act_2"]
      }
    ]);

    const conflicts = getConflicts();
    assert.equal(conflicts.length, 1);
    assert.equal(conflicts[0].conflict_type, "ownership");
    assert.deepEqual(conflicts[0].action_ids, ["act_1", "act_2"]);
  });

  test("saveDailyBrief and getLatestDailyBrief persist brief", () => {
    const brief = {
      executive: "Arjun Malhotra",
      brief_date: "2026-09-21",
      summary: "3 actions, 1 due today",
      my_actions: [],
      due_today: [],
      overdue: [],
      waiting_on_others: [],
      unclear_actions: []
    };

    saveDailyBrief(brief);

    const retrieved = getLatestDailyBrief();
    assert.ok(retrieved);
    assert.equal(retrieved.executive, "Arjun Malhotra");
    assert.equal(retrieved.summary, "3 actions, 1 due today");
  });
});
