# Architecture Separation: JavaScript Backend & Python AI Service

## 1. Overview of the Architecture

MeetOps has been restructured into two dedicated, decoupled services:

1. **JavaScript Backend (`backend/`)**:
   - Built with **Node.js, Express.js, and SQLite** (`better-sqlite3`).
   - **Exclusive Database Owner**: Holds sole access to the SQLite database (`data/meetops.db`).
   - Serves client API endpoints for action retrieval, status updates, conflict resolution, and daily briefs.
   - Orchestrates the AI pipeline by making HTTP calls to the Python AI service.

2. **Python AI Microservice (`ai_service/`)**:
   - Built with **Python, FastAPI, LangChain, LangGraph, and Groq**.
   - **Stateless & Database-Free**: Holds zero database connections.
   - Responsible for action extraction, LLM deduplication, conflict detection, and executive daily brief reasoning.
   - Communicates exclusively over HTTP with the JavaScript backend.

```
                    ┌───────────────────────────┐
                    │    Frontend / Client      │
                    └─────────────┬─────────────┘
                                  │ HTTP REST
                                  ▼
                    ┌───────────────────────────┐
                    │    JavaScript Backend     │
                    │   (Node.js + Express)     │
                    └──────┬─────────────┬──────┘
       Exclusive Access    │             │ HTTP REST
                           ▼             ▼
             ┌──────────────────┐  ┌──────────────────┐
             │ SQLite Database  │  │  Python AI Svc   │
             │ (data/meetops.db)│  │ (FastAPI + Graph)│
             └──────────────────┘  └─────────┬────────┘
                                             │ Groq API
                                             ▼
                                   ┌──────────────────┐
                                   │  Groq Cloud LLM  │
                                   └──────────────────┘
```

---

## 2. Changes Made by Component

### A. Python AI Microservice (`ai_service/`)
- **Code Relocation**:
  - Moved Python modules from `backend/app/` to `ai_service/app/`.
  - Moved tests from `backend/tests/` to `ai_service/tests/`.
  - Moved `requirements.txt` to `ai_service/requirements.txt`.
- **FastAPI Endpoints (`ai_service/app/main.py`)**:
  - `GET /health`: Health check endpoint.
  - `POST /ai/pipeline/run`: Executes the complete LangGraph agent workflow (`extract_actions` ➔ `resolve_actions` ➔ `group_actions` ➔ `build_daily_brief`) and returns canonical actions, conflicts, and the daily brief.
  - `GET /ai/actions`: Direct extraction endpoint.
  - `POST /ai/resolve`: Deduplicates an action list and detects conflicts.
  - `POST /ai/brief`: Builds a daily brief with deadline resolutions.

---

### B. JavaScript Backend (`backend/`)
- **Package Configuration (`backend/package.json`)**:
  - Initialized ES module Node.js project.
  - Dependencies: `express`, `cors`, `dotenv`, `better-sqlite3`.
  - Scripts: `start`, `dev` (with `--watch`), and `test` (`node:test`).
- **Configuration (`backend/src/config.js`)**:
  - Resolves `PORT` (default: 3000), `AI_SERVICE_URL` (default: http://127.0.0.1:8000), and `DB_PATH` (`data/meetops.db`).
- **Database Layer (`backend/src/database/db.js`)**:
  - Connects to SQLite with WAL mode (`journal_mode = WAL`) and foreign key enforcement.
  - Creates tables and indices:
    - `actions`: Canonical actions, owners, recipients, status, deadlines, notes.
    - `source_evidence`: Evidence snippets with source IDs and excerpts attached to actions.
    - `conflicts`: Detected ownership, deadline, and action-type contradictions.
    - `daily_briefs`: Persisted daily executive brief records with summary and JSON payload.
  - Exposes repository functions: `saveAction`, `saveActionsBatch`, `getActions`, `getActionById`, `updateActionStatus`, `saveConflictsBatch`, `getConflicts`, `saveDailyBrief`, `getLatestDailyBrief`.
- **AI Service Client (`backend/src/services/aiClient.js`)**:
  - Encapsulates HTTP calls to the Python AI service with error handling and health checking.
- **API Routes**:
  - `backend/src/routes/pipeline.js` (`POST /api/pipeline/run`): Calls AI service, transactionally writes canonical actions, conflicts, and daily briefs into SQLite, and returns the result.
  - `backend/src/routes/actions.js` (`GET /api/actions`, `GET /api/actions/:id`, `PATCH /api/actions/:id`): Reads and updates actions directly in SQLite.
  - `backend/src/routes/briefs.js` (`GET /api/briefs/latest`, `GET /api/briefs/:date`): Retrieves saved daily briefs from SQLite.
  - `backend/src/routes/conflicts.js` (`GET /api/conflicts`, `POST /api/conflicts/:id/resolve`): Views and resolves detected conflicts.
- **Server Entrypoint (`backend/src/server.js`)**:
  - Configures Express, CORS, JSON body parser, route mounting, and `/api/health`.
- **Database Tests (`backend/tests/api.test.js`)**:
  - Built-in `node:test` suite testing table creation, action persistence, status updates, conflict saving, and brief retrieval.

---

### C. Environment & Orchestration
- **`.env` & `.env.example`**:
  - Added `PORT=3000`, `AI_SERVICE_URL=http://127.0.0.1:8000`, `DB_PATH=data/meetops.db`.
- **`.gitignore`**:
  - Added SQLite write-ahead log files (`*.db-wal`, `*.db-shm`).
- **Root Orchestrator (`run.py`)**:
  - `--ai`: Launches Python AI microservice on port 8000.
  - `--backend`: Launches JavaScript backend on port 3000.
  - `--test`: Executes both Python `pytest` and JavaScript `node:test` test suites.
  - `--llm`: Runs LLM extraction brief.

---

## 3. Verification & Test Results

### 1. Python AI Service Tests
```powershell
python -m pytest ai_service/tests -q
45 passed in 0.72s
```

### 2. JavaScript Backend Tests
```powershell
npm test --prefix backend
▶ MeetOps JavaScript Backend - Database & Model Tests
  ✔ Database initializes and creates tables (0.9197ms)
  ✔ saveAction inserts and retrieves canonical action with evidence (2.3743ms)
  ✔ updateActionStatus updates status and appends note (0.6542ms)
  ✔ getActions filters by ownership and status (0.6096ms)
  ✔ saveConflictsBatch and getConflicts store detected conflicts (0.9641ms)
  ✔ saveDailyBrief and getLatestDailyBrief persist brief (0.514ms)
✔ MeetOps JavaScript Backend - Database & Model Tests (13.3906ms)
ℹ pass 6, fail 0
```

### 3. Live End-to-End Inter-Service Verification
1. `GET http://127.0.0.1:3000/api/health` returned:
   ```json
   {
     "status": "healthy",
     "backend": "running",
     "database": { "type": "sqlite", "status": "connected" },
     "ai_service": { "url": "http://127.0.0.1:8000", "status": "connected" }
   }
   ```
2. `POST http://127.0.0.1:3000/api/pipeline/run` executed the LangGraph pipeline via the Python service and persisted 5 actions and 1 daily brief into SQLite.
3. `GET http://127.0.0.1:3000/api/actions` retrieved the actions directly from SQLite.
4. `PATCH http://127.0.0.1:3000/api/actions/action_vendor_list` updated action status to `completed` in SQLite.
5. `GET http://127.0.0.1:3000/api/briefs/latest` returned the executive brief from SQLite.

---

## 4. How to Run the Services

### To run tests:
```powershell
# Run Python AI service tests (45 tests)
python -m pytest ai_service/tests -q

# Run JavaScript backend tests (6 tests)
npm test --prefix backend

# Run both suites together
python run.py --test
```

### To run services:
```powershell
# Start Python AI Microservice (port 8000)
python run.py --ai

# Start JavaScript Backend (port 3000)
python run.py --backend
```
