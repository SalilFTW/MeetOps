# Error Resolution: AI Service Connection Failure

## The Error

The backend Node.js terminal (`node`, ProcessId: 6300) was logging this repeatedly:

```text
Pipeline run error: AIServiceError: Could not communicate with AI Service at http://127.0.0.1:8000: fetch failed
    at request (file:///.../backend/src/services/aiClient.js:50:11)
    ...
    status: 503,
    details: { originalError: 'fetch failed' }
```

And the frontend was showing **"Backend unavailable"** (grey dot) with the error toast:

```text
Could not communicate with AI Service at http://127.0.0.1:8000: fetch failed
```

---

## Root Cause

This is **not a code bug** — it is a **process management issue**.

MeetOps is a two-service architecture:

| Service | Language | Port | Purpose |
|---------|----------|------|---------|
| JavaScript Backend | Node.js + Express | 3000 | REST API, SQLite, data layer |
| Python AI Service | FastAPI + LangGraph | 8000 | AI extraction, reasoning, Q&A |

The **Python AI Service was simply not running** on port 8000. When the Node.js backend tried to call `http://127.0.0.1:8000/ai/pipeline/run`, there was nothing listening on that port, so `fetch` threw `ECONNREFUSED` → surfaced as `fetch failed`.

### Why the frontend showed "Backend unavailable" (incorrectly)

The original `/api/health` endpoint in [backend/src/server.js](file:///c:/Users/Salil%20Chauhan%20FTW/OneDrive/Desktop/PROJECT/MEETOPS/backend/src/server.js) was:

```javascript
// BEFORE — wrong: requires BOTH services to be "healthy"
const healthy = dbStatus === "connected" && aiStatus === "connected";
return res.status(healthy ? 200 : 207).json({
  status: healthy ? "healthy" : "degraded",
  ...
});
```

This made the health endpoint return `status: "degraded"` whenever the AI service was offline — even though the Node.js backend and SQLite were perfectly functional. The frontend's `App.jsx` then read `health?.status === "healthy"` and set `backendHealthy = false`, causing the **"Backend unavailable"** message despite the backend being up.

---

## Changes Made

### 1. Fixed `backend/src/server.js` — Correct Health Check Logic

The health endpoint now correctly reports `status: "healthy"` when the **SQLite DB is connected**, regardless of whether the AI service is reachable. AI service status is exposed as its own separate field.

```diff
- const healthy = dbStatus === "connected" && aiStatus === "connected";
- return res.status(healthy ? 200 : 207).json({
-   status: healthy ? "healthy" : "degraded",
-   ai_service: { url: config.aiServiceUrl, status: aiStatus },
- });

+ const backendHealthy = dbStatus === "connected";
+ const aiConnected = aiStatus === "connected";
+ return res.status(backendHealthy ? 200 : 503).json({
+   status: backendHealthy ? "healthy" : "unavailable",
+   ai_service: {
+     url: config.aiServiceUrl,
+     status: aiConnected ? "connected" : "disconnected",
+     message: aiConnected
+       ? "AI service is reachable"
+       : "Start the AI service: .venv\\Scripts\\python ai_service\\run.py --server",
+   },
+ });
```

### 2. Updated `frontend/src/App.jsx` — Track Services Separately

Added a new `aiServiceConnected` state variable, populated from `health?.ai_service?.status === "connected"`, so the backend and AI service are tracked independently.

### 3. Updated `frontend/src/components/Header.jsx` — Nuanced Status Indicator

The header now shows three distinct states instead of just two:

| Condition | Dot Colour | Label |
|-----------|-----------|-------|
| Backend DB unreachable | 🔴 Red/Grey | Backend unavailable |
| Backend OK, AI offline | 🟡 Amber | Backend connected · AI offline |
| Both services connected | 🟢 Green | All systems connected |

The **Run Pipeline** button now shows an explanatory tooltip when AI service is offline.

### 4. Added `status-dot.degraded` CSS Rule in `frontend/src/index.css`

```css
/* NEW — amber dot for partial connectivity */
.status-dot.degraded {
  background: #e8a020;
}
```

### 5. Created `start-ai-service.bat` — Quick Start Script

Created [start-ai-service.bat](file:///c:/Users/Salil%20Chauhan%20FTW/OneDrive/Desktop/PROJECT/MEETOPS/start-ai-service.bat) at the project root for easy AI service startup:

```bat
.\.venv\Scripts\python.exe ai_service\run.py --server
```

---

## How to Start All Services

You need **three separate terminals**:

```powershell
# Terminal 1 – Python AI Service (port 8000)
.\.venv\Scripts\python.exe ai_service\run.py --server
# OR double-click start-ai-service.bat

# Terminal 2 – Node.js Backend (port 3000)
cd backend
npm start

# Terminal 3 – Vite Frontend Dev Server (port 5173)
cd frontend
npm run dev
```

---

## Verification

**Frontend build** — ✅ clean, 0 errors, built in 1.05s:
```text
vite v6.4.3 building for production...
✓ 35 modules transformed.
dist/assets/index-D5LlVxVa.css    4.75 kB │ gzip:  1.52 kB
dist/assets/index-CADNrdlc.js   233.25 kB │ gzip: 72.36 kB
✓ built in 1.05s
```

**Backend tests** — ✅ all 6 passing:
```text
✔ MeetOps JavaScript Backend - Database & Model Tests (18.1324ms)
ℹ pass 6  ℹ fail 0
```

> **Note**: Per your instructions, no automatic `git push` was performed.
