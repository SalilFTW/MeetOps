import Database from "better-sqlite3";
import fs from "node:fs";
import path from "node:path";
import { config } from "../config.js";

// Ensure database directory exists
const dbDir = path.dirname(config.dbPath);
if (!fs.existsSync(dbDir)) {
  fs.mkdirSync(dbDir, { recursive: true });
}

export const db = new Database(config.dbPath);

// Enable WAL mode for high performance concurrency
db.pragma("journal_mode = WAL");
db.pragma("foreign_keys = ON");

// Initialize Database Tables
export function initDatabase() {
  db.exec(`
    CREATE TABLE IF NOT EXISTS actions (
      id TEXT PRIMARY KEY,
      title TEXT NOT NULL,
      action_type TEXT NOT NULL,
      owner TEXT,
      recipient TEXT,
      ownership TEXT NOT NULL,
      deadline TEXT,
      deadline_text TEXT,
      status TEXT NOT NULL DEFAULT 'open',
      confidence REAL,
      notes TEXT DEFAULT '[]',
      updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
      created_at TEXT DEFAULT CURRENT_TIMESTAMP
    );

    CREATE TABLE IF NOT EXISTS source_evidence (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      action_id TEXT NOT NULL,
      source_type TEXT NOT NULL,
      source_id TEXT NOT NULL,
      reference_id TEXT,
      timestamp TEXT,
      excerpt TEXT NOT NULL,
      FOREIGN KEY (action_id) REFERENCES actions(id) ON DELETE CASCADE
    );

    CREATE TABLE IF NOT EXISTS conflicts (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      conflict_type TEXT NOT NULL,
      description TEXT NOT NULL,
      severity TEXT NOT NULL,
      action_ids TEXT NOT NULL,
      resolved INTEGER DEFAULT 0,
      created_at TEXT DEFAULT CURRENT_TIMESTAMP
    );

    CREATE TABLE IF NOT EXISTS daily_briefs (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      executive TEXT NOT NULL,
      brief_date TEXT NOT NULL UNIQUE,
      summary TEXT NOT NULL,
      payload TEXT NOT NULL,
      created_at TEXT DEFAULT CURRENT_TIMESTAMP
    );

    CREATE INDEX IF NOT EXISTS idx_actions_ownership ON actions(ownership);
    CREATE INDEX IF NOT EXISTS idx_actions_status ON actions(status);
    CREATE INDEX IF NOT EXISTS idx_actions_owner ON actions(owner);
    CREATE INDEX IF NOT EXISTS idx_evidence_action ON source_evidence(action_id);
    CREATE INDEX IF NOT EXISTS idx_briefs_date ON daily_briefs(brief_date);
  `);
}

// -------------------------------------------------------------
// Action Repositories
// -------------------------------------------------------------

export function saveAction(action) {
  const insertAction = db.prepare(`
    INSERT INTO actions (
      id, title, action_type, owner, recipient, ownership,
      deadline, deadline_text, status, confidence, notes, updated_at
    ) VALUES (
      @id, @title, @action_type, @owner, @recipient, @ownership,
      @deadline, @deadline_text, @status, @confidence, @notes, CURRENT_TIMESTAMP
    )
    ON CONFLICT(id) DO UPDATE SET
      title = excluded.title,
      action_type = excluded.action_type,
      owner = excluded.owner,
      recipient = excluded.recipient,
      ownership = excluded.ownership,
      deadline = excluded.deadline,
      deadline_text = excluded.deadline_text,
      status = excluded.status,
      confidence = excluded.confidence,
      notes = excluded.notes,
      updated_at = CURRENT_TIMESTAMP;
  `);

  const deleteEvidence = db.prepare(`DELETE FROM source_evidence WHERE action_id = ?;`);
  const insertEvidence = db.prepare(`
    INSERT INTO source_evidence (action_id, source_type, source_id, reference_id, timestamp, excerpt)
    VALUES (?, ?, ?, ?, ?, ?);
  `);

  insertAction.run({
    id: action.id,
    title: action.title,
    action_type: action.action_type,
    owner: action.owner || null,
    recipient: action.recipient || null,
    ownership: action.ownership,
    deadline: action.deadline ? new Date(action.deadline).toISOString() : null,
    deadline_text: action.deadline_text || null,
    status: action.status || "open",
    confidence: action.confidence ?? null,
    notes: JSON.stringify(action.notes || []),
  });

  if (action.source_evidence && action.source_evidence.length > 0) {
    deleteEvidence.run(action.id);
    for (const ev of action.source_evidence) {
      insertEvidence.run(
        action.id,
        ev.source_type,
        ev.source_id,
        ev.reference_id || null,
        ev.timestamp ? new Date(ev.timestamp).toISOString() : null,
        ev.excerpt
      );
    }
  }
}

export function saveActionsBatch(actions) {
  const runTransaction = db.transaction((actionList) => {
    for (const action of actionList) {
      saveAction(action);
    }
  });

  runTransaction(actions);
}

export function getActions({ ownership, status, owner } = {}) {
  let query = "SELECT * FROM actions WHERE 1=1";
  const params = [];

  if (ownership) {
    query += " AND ownership = ?";
    params.push(ownership);
  }
  if (status) {
    query += " AND status = ?";
    params.push(status);
  }
  if (owner) {
    query += " AND LOWER(owner) = LOWER(?)";
    params.push(owner);
  }

  query += " ORDER BY created_at DESC;";

  const actions = db.prepare(query).all(...params);

  const getEvidence = db.prepare("SELECT source_type, source_id, reference_id, timestamp, excerpt FROM source_evidence WHERE action_id = ?;");

  return actions.map((act) => ({
    ...act,
    notes: JSON.parse(act.notes || "[]"),
    source_evidence: getEvidence.all(act.id),
  }));
}

export function getActionById(id) {
  const action = db.prepare("SELECT * FROM actions WHERE id = ?;").get(id);
  if (!action) return null;

  const evidence = db.prepare("SELECT source_type, source_id, reference_id, timestamp, excerpt FROM source_evidence WHERE action_id = ?;").all(id);

  return {
    ...action,
    notes: JSON.parse(action.notes || "[]"),
    source_evidence: evidence,
  };
}

export function updateActionStatus(id, status, notes = null) {
  if (notes !== null) {
    const existing = getActionById(id);
    const updatedNotes = Array.isArray(notes) ? notes : [...(existing?.notes || []), notes];
    db.prepare("UPDATE actions SET status = ?, notes = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?;").run(status, JSON.stringify(updatedNotes), id);
  } else {
    db.prepare("UPDATE actions SET status = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?;").run(status, id);
  }
  return getActionById(id);
}

// -------------------------------------------------------------
// Conflicts Repositories
// -------------------------------------------------------------

export function saveConflictsBatch(conflicts) {
  const insertConflict = db.prepare(`
    INSERT INTO conflicts (conflict_type, description, severity, action_ids)
    VALUES (?, ?, ?, ?);
  `);

  const tx = db.transaction((conflictList) => {
    for (const c of conflictList) {
      insertConflict.run(
        c.conflict_type,
        c.description,
        c.severity || "medium",
        JSON.stringify(c.action_ids || [])
      );
    }
  });

  tx(conflicts);
}

export function getConflicts({ resolved } = {}) {
  let query = "SELECT * FROM conflicts";
  const params = [];

  if (resolved !== undefined) {
    query += " WHERE resolved = ?";
    params.push(resolved ? 1 : 0);
  }

  query += " ORDER BY id DESC;";

  const rows = db.prepare(query).all(...params);
  return rows.map((r) => ({
    ...r,
    action_ids: JSON.parse(r.action_ids || "[]"),
    resolved: Boolean(r.resolved),
  }));
}

export function resolveConflict(id) {
  db.prepare("UPDATE conflicts SET resolved = 1 WHERE id = ?;").run(id);
}

// -------------------------------------------------------------
// Daily Brief Repositories
// -------------------------------------------------------------

export function saveDailyBrief(brief) {
  const insertBrief = db.prepare(`
    INSERT INTO daily_briefs (executive, brief_date, summary, payload)
    VALUES (@executive, @brief_date, @summary, @payload)
    ON CONFLICT(brief_date) DO UPDATE SET
      executive = excluded.executive,
      summary = excluded.summary,
      payload = excluded.payload,
      created_at = CURRENT_TIMESTAMP;
  `);

  insertBrief.run({
    executive: brief.executive,
    brief_date: typeof brief.brief_date === "string" ? brief.brief_date : new Date(brief.brief_date).toISOString().split("T")[0],
    summary: brief.summary,
    payload: JSON.stringify(brief),
  });
}

export function getLatestDailyBrief() {
  const row = db.prepare("SELECT * FROM daily_briefs ORDER BY brief_date DESC LIMIT 1;").get();
  if (!row) return null;
  return JSON.parse(row.payload);
}

export function getDailyBriefByDate(dateStr) {
  const row = db.prepare("SELECT * FROM daily_briefs WHERE brief_date = ?;").get(dateStr);
  if (!row) return null;
  return JSON.parse(row.payload);
}
