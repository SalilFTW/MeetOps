from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class ActionType(str, Enum):
    COMMITMENT = "commitment"
    TASK = "task"
    FOLLOW_UP = "follow_up"


class ActionOwnership(str, Enum):
    MY_ACTION = "my_action"
    WAITING_ON_OTHER = "waiting_on_other"
    UNCLEAR = "unclear"


class ActionStatus(str, Enum):
    OPEN = "open"
    COMPLETED = "completed"
    OVERDUE = "overdue"
    UNCLEAR = "unclear"


class SourceEvidence(BaseModel):
    source_type: str
    source_id: str
    reference_id: Optional[str] = None
    timestamp: Optional[datetime] = None
    excerpt: str


class Action(BaseModel):
    id: str

    title: str

    action_type: ActionType

    owner: Optional[str] = None

    recipient: Optional[str] = None

    ownership: ActionOwnership

    deadline: Optional[datetime] = None

    deadline_text: Optional[str] = None

    status: ActionStatus = ActionStatus.OPEN

    source_evidence: list[SourceEvidence] = Field(default_factory=list)

    confidence: Optional[float] = None

    notes: list[str] = Field(default_factory=list)