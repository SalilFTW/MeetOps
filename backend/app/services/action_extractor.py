from datetime import datetime
from typing import Optional

from app.models.action import (
    Action,
    ActionOwnership,
    ActionStatus,
    ActionType,
    SourceEvidence,
)


def create_action(
    action_id: str,
    title: str,
    owner: Optional[str] = None,
    recipient: Optional[str] = None,
    ownership: ActionOwnership = ActionOwnership.UNCLEAR,
    action_type: ActionType = ActionType.TASK,
    source_type: str = "",
    source_id: str = "",
    excerpt: str = "",
    deadline_text: Optional[str] = None,
    deadline: Optional[datetime] = None,
    status: ActionStatus = ActionStatus.OPEN,
    confidence: Optional[float] = None,
    notes: Optional[list[str]] = None,
    reference_id: Optional[str] = None,
    timestamp: Optional[datetime] = None,
) -> Action:
    """
    Factory helper to create a canonical Action instance with SourceEvidence attached.
    """
    source_evidence: list[SourceEvidence] = []
    if source_type or source_id or excerpt:
        source_evidence.append(
            SourceEvidence(
                source_type=source_type,
                source_id=source_id,
                reference_id=reference_id,
                timestamp=timestamp,
                excerpt=excerpt,
            )
        )

    return Action(
        id=action_id,
        title=title,
        action_type=action_type,
        owner=owner,
        recipient=recipient,
        ownership=ownership,
        deadline=deadline,
        deadline_text=deadline_text,
        status=status,
        source_evidence=source_evidence,
        confidence=confidence,
        notes=notes or [],
    )
