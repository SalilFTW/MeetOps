from datetime import date
from typing import Optional
from app.models.qa import QuestionRequest
from app.graph.runner import run_meetops_agent
from app.services.qa_service import answer_question
from fastapi import FastAPI
from pydantic import BaseModel, Field

from app.config import APP_NAME
from app.graph.runner import run_meetops_agent
from app.models.action import Action
from app.models.daily_brief import DailyBrief
from app.models.deduplication import ActionConflict, DeduplicationResult
from app.services.action_engine import extract_actions, group_actions
from app.services.action_resolution import resolve_actions
from app.services.daily_brief_service import build_daily_brief


app = FastAPI(
    title=f"{APP_NAME} AI Service",
    description="Stateless AI microservice for action extraction, deduplication, conflict detection, and executive brief reasoning.",
    version="1.0.0",
)


class PipelineRunRequest(BaseModel):
    use_llm: bool = Field(default=False, description="Whether to use LangChain + Groq LLM extraction")
    brief_date: Optional[date] = Field(default=None, description="Reference date for daily brief and deadline calculation")


class ResolveActionsRequest(BaseModel):
    actions: list[Action] = Field(default_factory=list)


class BuildBriefRequest(BaseModel):
    actions: list[Action] = Field(default_factory=list)
    brief_date: Optional[date] = None


@app.get("/")
def root():
    return {
        "service": "MeetOps AI Service",
        "status": "running",
        "docs": "/docs",
    }


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "service": "MeetOps AI Service",
    }


@app.post("/ai/pipeline/run")
def run_pipeline(request: PipelineRunRequest = PipelineRunRequest()):
    """
    Execute the full LangGraph pipeline:
    extract -> resolve & detect conflicts -> group -> build daily brief
    """
    result = run_meetops_agent(
        use_llm=request.use_llm,
        brief_date=request.brief_date,
    )

    return {
        "success": True,
        "use_llm": result.get("use_llm", request.use_llm),
        "brief_date": result.get("brief_date"),
        "raw_actions": result.get("raw_actions", []),
        "canonical_actions": result.get("canonical_actions", []),
        "conflicts": result.get("conflicts", []),
        "my_actions": result.get("my_actions", []),
        "waiting_on_others": result.get("waiting_on_others", []),
        "unclear_actions": result.get("unclear_actions", []),
        "daily_brief": result.get("daily_brief"),
        "error": result.get("error"),
    }


@app.get("/ai/actions")
def get_actions(use_llm: bool = False, resolve_duplicates: bool = True):
    """
    Direct extraction endpoint.
    """
    actions = extract_actions(
        use_llm=use_llm,
        resolve_duplicates=resolve_duplicates,
    )
    groups = group_actions(actions)
    return {
        "total": len(actions),
        "actions": actions,
        "grouped": groups,
    }


@app.post("/ai/resolve")
def resolve_action_list(request: ResolveActionsRequest):
    """
    Deduplicate actions, merge evidence, and detect conflicts.
    """
    result = resolve_actions(request.actions)
    return {
        "canonical_actions": result.canonical_actions,
        "merged_action_ids": result.merged_action_ids,
        "conflicts": result.conflicts,
    }


@app.post("/ai/brief")
def create_brief(request: BuildBriefRequest):
    """
    Construct daily brief and resolve deadlines.
    """
    ref_date = request.brief_date or date(2026, 9, 21)
    brief = build_daily_brief(
        actions=request.actions,
        reference_date=ref_date,
    )
    return brief
@app.post("/ai/ask")
def ask_question(request: QuestionRequest):
    result = run_meetops_agent(
        use_llm=False,
    )

    actions = result.get(
        "canonical_actions",
        [],
    )

    return answer_question(
        question=request.question,
        actions=actions,
    )