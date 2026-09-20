from app.models.action import (
    Action,
    ActionOwnership,
    ActionType,
)
from app.services.qa_retriever import (
    retrieve_relevant_actions,
)


def make_action(
    action_id: str,
    title: str,
    owner: str | None,
    recipient: str | None,
    ownership: ActionOwnership,
    action_type: ActionType = ActionType.TASK,
) -> Action:
    return Action(
        id=action_id,
        title=title,
        action_type=action_type,
        owner=owner,
        recipient=recipient,
        ownership=ownership,
    )


def test_retriever_finds_raghav_action():
    actions = [
        make_action(
            action_id="vendor",
            title="Send updated vendor list",
            owner="Arjun Malhotra",
            recipient="Raghav Sethi",
            ownership=ActionOwnership.MY_ACTION,
            action_type=ActionType.COMMITMENT,
        ),
        make_action(
            action_id="expense",
            title="Receive expense variance report",
            owner="Divya Rao",
            recipient="Arjun Malhotra",
            ownership=ActionOwnership.WAITING_ON_OTHER,
        ),
    ]

    results = retrieve_relevant_actions(
        "What did I promise Raghav?",
        actions,
    )

    assert len(results) > 0
    assert results[0].id == "vendor"


def test_retriever_finds_waiting_actions():
    actions = [
        make_action(
            action_id="expense",
            title="Receive July expense variance report",
            owner="Divya Rao",
            recipient="Arjun Malhotra",
            ownership=ActionOwnership.WAITING_ON_OTHER,
        ),
    ]

    results = retrieve_relevant_actions(
        "What am I waiting on?",
        actions,
    )

    assert len(results) == 1
    assert results[0].id == "expense"


def test_retriever_finds_unclear_actions():
    actions = [
        make_action(
            action_id="lease",
            title="Confirm ownership of Mumbai office lease",
            owner=None,
            recipient=None,
            ownership=ActionOwnership.UNCLEAR,
        ),
    ]

    results = retrieve_relevant_actions(
        "What is unclear?",
        actions,
    )

    assert len(results) == 1
    assert results[0].id == "lease"


def test_retriever_returns_empty_for_unrelated_question():
    actions = [
        make_action(
            action_id="vendor",
            title="Send updated vendor list",
            owner="Arjun Malhotra",
            recipient="Raghav Sethi",
            ownership=ActionOwnership.MY_ACTION,
        ),
    ]

    results = retrieve_relevant_actions(
        "What is the weather?",
        actions,
    )

    assert results == []