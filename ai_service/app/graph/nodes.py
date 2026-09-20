from datetime import date

from app.graph.state import MeetOpsState
from app.services.action_engine import extract_actions, group_actions
from app.services.action_resolution import resolve_actions
from app.services.daily_brief_service import build_daily_brief


def extract_actions_node(state: MeetOpsState) -> MeetOpsState:
    use_llm = state.get("use_llm", True)

    actions = extract_actions(
        use_llm=use_llm,
        resolve_duplicates=False,
    )

    return {
        "raw_actions": actions,
        "error": None,
    }


def resolve_actions_node(state: MeetOpsState) -> MeetOpsState:
    raw_actions = state.get("raw_actions", [])

    result = resolve_actions(raw_actions)

    return {
        "canonical_actions": result.canonical_actions,
        "conflicts": result.conflicts,
    }


def group_actions_node(state: MeetOpsState) -> MeetOpsState:
    canonical_actions = state.get("canonical_actions", [])

    groups = group_actions(canonical_actions)

    return {
        "my_actions": groups["my_actions"],
        "waiting_on_others": groups["waiting_on_others"],
        "unclear_actions": groups["unclear"],
    }


def build_daily_brief_node(state: MeetOpsState) -> MeetOpsState:
    canonical_actions = state.get("canonical_actions", [])

    brief_date = state.get(
        "brief_date",
        date(2026, 9, 21),
    )

    daily_brief = build_daily_brief(
        actions=canonical_actions,
        reference_date=brief_date,
    )

    return {
        "daily_brief": daily_brief,
    }


def error_node(state: MeetOpsState) -> MeetOpsState:
    if "error" not in state:
        return {
            "error": None,
        }

    return state