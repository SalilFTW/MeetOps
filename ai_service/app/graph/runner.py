from datetime import date

from app.graph.state import MeetOpsState
from app.graph.workflow import build_meetops_graph


def run_meetops_agent(
    use_llm: bool = True,
    brief_date: date | None = None,
) -> MeetOpsState:

    graph = build_meetops_graph()

    initial_state: MeetOpsState = {
        "use_llm": use_llm,
        "brief_date": brief_date or date(2026, 9, 21),
        "raw_actions": [],
        "canonical_actions": [],
        "conflicts": [],
        "my_actions": [],
        "waiting_on_others": [],
        "unclear_actions": [],
        "error": None,
    }

    result = graph.invoke(initial_state)

    return result