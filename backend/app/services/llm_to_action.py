from app.models.action import (
    Action,
    ActionOwnership,
    ActionType,
)

from app.models.llm_output import ExtractedAction

from app.services.action_extractor import create_action


def determine_action_ownership(
    owner: str | None,
) -> ActionOwnership:
    """
    Determine MeetOps ownership from the explicitly
    extracted owner.
    """

    if owner is None:
        return ActionOwnership.UNCLEAR

    if owner.strip().lower() == "arjun malhotra":
        return ActionOwnership.MY_ACTION

    return ActionOwnership.WAITING_ON_OTHER


def convert_extracted_action(
    extracted: ExtractedAction,
    action_id: str,
    source_type: str,
    source_id: str,
) -> Action:
    """
    Convert the LLM representation into the application's
    canonical Action model.
    """

    ownership = determine_action_ownership(
        extracted.owner
    )

    try:
        action_type = ActionType(
            extracted.action_type
        )
    except ValueError:
        action_type = ActionType.TASK

    return create_action(
        action_id=action_id,
        title=extracted.title,
        owner=extracted.owner,
        recipient=extracted.recipient,
        ownership=ownership,
        action_type=action_type,
        source_type=source_type,
        source_id=source_id,
        excerpt=extracted.evidence_excerpt,
        deadline_text=extracted.deadline_text,
        confidence=extracted.confidence,
        notes=[
            extracted.ownership_reason
        ],
    )