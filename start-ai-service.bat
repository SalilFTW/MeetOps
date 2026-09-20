@echo off
REM Start the MeetOps AI Service (Python FastAPI on port 8000)
REM Run this in a separate terminal before or after starting the backend.

echo ============================================================
echo  Starting MeetOps AI Service on http://127.0.0.1:8000
echo  Swagger docs: http://127.0.0.1:8000/docs
echo ============================================================

.\.venv\Scripts\python.exe ai_service\run.py --server
