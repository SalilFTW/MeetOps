from app.models.action import (
    Action,
    ActionOwnership,
    ActionType,
)
from app.services.qa_service import (
    build_action_context,
    answer_question,
)


def make_action() -> Action:
    return Action(
        id="action_vendor_list",
        title="Send updated vendor list",
        action_type=ActionType.COMMITMENT,
        owner="Arjun Malhotra",
        recipient="Raghav Sethi",
        ownership=ActionOwnership.MY_ACTION,
        deadline_text="by end of day tomorrow",
        notes=[
            "Arjun explicitly committed to sending the list."
        ],
    )


def test_action_context_contains_action_details():
    action = make_action()

    context = build_action_context(
        [action]
    )

    assert "action_vendor_list" in context
    assert "Send updated vendor list" in context
    assert "Raghav Sethi" in context
    assert "by end of day tomorrow" in context


def test_unanswerable_question_does_not_call_llm():
    result = answer_question(
        question="What is the weather?",
        actions=[
            make_action()
        ],
    )

    assert result.confidence == 0.0
    assert result.action_ids == []
    assert "does not establish" in result.answer