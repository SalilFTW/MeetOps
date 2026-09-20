from app.models.action import (
    ActionOwnership,
    ActionStatus,
    ActionType,
)
from app.services.action_engine import extract_actions, group_actions
from app.services.assignment1_extractor import extract_assignment1_actions


def test_assignment1_actions_are_extracted():
    actions = extract_assignment1_actions()

    assert len(actions) == 5


def test_vendor_list_commitment():
    actions = extract_assignment1_actions()

    action = next(
        action
        for action in actions
        if action.id == "action_vendor_list"
    )

    assert action.title == "Send updated vendor list"
    assert action.owner == "Arjun Malhotra"
    assert action.recipient == "Raghav Sethi"
    assert action.ownership == ActionOwnership.MY_ACTION
    assert action.action_type == ActionType.COMMITMENT
    assert action.status == ActionStatus.OPEN
    assert action.deadline_text == "by end of day tomorrow"


def test_meridian_call_is_my_action():
    actions = extract_assignment1_actions()

    action = next(
        action
        for action in actions
        if action.id == "action_meridian_call"
    )

    assert action.owner == "Arjun Malhotra"
    assert action.recipient == "Priya Nair"
    assert action.ownership == ActionOwnership.MY_ACTION


def test_expense_report_is_waiting_on_other():
    actions = extract_assignment1_actions()

    action = next(
        action
        for action in actions
        if action.id == "action_expense_variance"
    )

    assert action.owner == "Divya Rao"
    assert action.ownership == ActionOwnership.WAITING_ON_OTHER
    assert action.deadline_text == "Wednesday evening"


def test_mumbai_lease_has_unclear_ownership():
    actions = extract_assignment1_actions()

    action = next(
        action
        for action in actions
        if action.id == "action_mumbai_lease"
    )

    assert action.owner is None
    assert action.ownership == ActionOwnership.UNCLEAR
    assert action.deadline_text == "this week"


def test_every_action_has_evidence():
    actions = extract_assignment1_actions()

    for action in actions:
        assert len(action.source_evidence) >= 1
        assert action.source_evidence[0].source_id


def test_action_grouping():
    actions = extract_actions()
    groups = group_actions(actions)

    assert len(groups["my_actions"]) == 3
    assert len(groups["waiting_on_others"]) == 1
    assert len(groups["unclear"]) == 1