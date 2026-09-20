from datetime import date

from pydantic import BaseModel, Field

from app.models.action import Action


class DailyBrief(BaseModel):
    executive: str
    brief_date: date

    my_actions: list[Action] = Field(default_factory=list)
    due_today: list[Action] = Field(default_factory=list)
    overdue: list[Action] = Field(default_factory=list)

    waiting_on_others: list[Action] = Field(default_factory=list)
    unclear_actions: list[Action] = Field(default_factory=list)

    summary: str = ""