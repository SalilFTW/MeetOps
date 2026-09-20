import pytest

from app.models.llm_output import (
    ExtractedAction,
    ExtractedActions,
)

from app.services.llm_to_action import (
    determine_action_ownership,
)

from app.models.action import ActionOwnership


def test_extracted_action_schema():

    action = ExtractedAction(
        title="Send updated vendor list",
        action_type="commitment",
        owner="Arjun Malhotra",
        recipient="Raghav Sethi",
        deadline_text="Wednesday morning",
        ownership_reason=(
            "Arjun explicitly committed to send it."
        ),
        evidence_excerpt=(
            "I told Raghav I’d send him the updated vendor list."
        ),
        confidence=0.98,
    )

    assert action.title == "Send updated vendor list"
    assert action.owner == "Arjun Malhotra"
    assert action.confidence == 0.98


def test_extracted_actions_container():

    result = ExtractedActions(
        actions=[]
    )

    assert result.actions == []


def test_confidence_must_be_between_zero_and_one():

    with pytest.raises(Exception):
        ExtractedAction(
            title="Test",
            action_type="task",
            owner="Arjun Malhotra",
            recipient=None,
            deadline_text=None,
            ownership_reason="Test",
            evidence_excerpt="Test",
            confidence=1.5,
        )


def test_arjun_is_my_action():

    ownership = determine_action_ownership(
        "Arjun Malhotra"
    )

    assert ownership == ActionOwnership.MY_ACTION


def test_other_person_is_waiting_on_other():

    ownership = determine_action_ownership(
        "Divya Rao"
    )

    assert ownership == ActionOwnership.WAITING_ON_OTHER


def test_missing_owner_is_unclear():

    ownership = determine_action_ownership(
        None
    )

    assert ownership == ActionOwnership.UNCLEAR