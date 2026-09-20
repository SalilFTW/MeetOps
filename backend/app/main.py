from fastapi import FastAPI
from app.config import APP_NAME
from app.services.action_engine import extract_actions, group_actions

app = FastAPI(
    title=APP_NAME,
    description="MeetOps - Executive Productivity Agent",
    version="0.1.0",
)


@app.get("/")
def root():
    return {
        "message": "Welcome to MeetOps",
        "status": "running",
    }


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "app": APP_NAME,
    }


@app.get("/actions")
def get_actions(use_llm: bool = False):
    actions = extract_actions(use_llm=use_llm)
    groups = group_actions(actions)
    return {
        "total": len(actions),
        "actions": actions,
        "grouped": groups,
    }