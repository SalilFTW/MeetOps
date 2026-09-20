from enum import Enum

from pydantic import BaseModel, Field


class ConflictType(str, Enum):
    OWNERSHIP = "ownership"
    DEADLINE = "deadline"
    ACTION_TYPE = "action_type"


class ActionConflict(BaseModel):
    action_ids: list[str] = Field(
        min_length=2,
        description="Actions involved in the conflict.",
    )

    conflict_type: ConflictType

    description: str

    severity: str = "medium"


class DeduplicationResult(BaseModel):
    canonical_actions: list
    merged_action_ids: dict[str, list[str]] = Field(
        default_factory=dict
    )
    conflicts: list[ActionConflict] = Field(
        default_factory=list
    )