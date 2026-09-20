from typing import TypedDict
from datetime import date

from app.models.action import Action
from app.models.daily_brief import DailyBrief
from app.models.deduplication import ActionConflict


class MeetOpsState(TypedDict, total=False):
    use_llm: bool
    brief_date: date

    raw_actions: list[Action]
    canonical_actions: list[Action]

    conflicts: list[ActionConflict]

    my_actions: list[Action]
    waiting_on_others: list[Action]
    unclear_actions: list[Action]

    daily_brief: DailyBrief

    error: str | None