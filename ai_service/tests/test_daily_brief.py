from datetime import date

from app.models.action import (
    Action,
    ActionOwnership,
    ActionType,
)
from app.services.daily_brief_service import build_daily_brief


def make_action(
    action_id: str,
    title: str,
    owner: str | None,
    ownership: ActionOwnership,
    deadline_text: str | None = None,
) -> Action:

    return Action(
        id=action_id,
        title=title,
        action_type=ActionType.TASK,
        owner=owner,
        recipient=None,
        ownership=ownership,
        deadline_text=deadline_text,
    )


def test_daily_brief_separates_action_groups():

    actions = [
        make_action(
            action_id="a1",
            title="Send vendor list",
            owner="Arjun Malhotra",
            ownership=ActionOwnership.MY_ACTION,
            deadline_text="tomorrow",
        ),
        make_action(
            action_id="a2",
            title="Receive expense report",
            owner="Divya Rao",
            ownership=ActionOwnership.WAITING_ON_OTHER,
            deadline_text="Wednesday evening",
        ),
        make_action(
            action_id="a3",
            title="Resolve lease ownership",
            owner=None,
            ownership=ActionOwnership.UNCLEAR,
            deadline_text="this week",
        ),
    ]

    brief = build_daily_brief(
        actions=actions,
        reference_date=date(2026, 9, 21),
    )

    assert len(brief.my_actions) == 1
    assert len(brief.waiting_on_others) == 1
    assert len(brief.unclear_actions) == 1


def test_daily_brief_identifies_due_today():

    actions = [
        make_action(
            action_id="a1",
            title="Send vendor list",
            owner="Arjun Malhotra",
            ownership=ActionOwnership.MY_ACTION,
            deadline_text="today",
        ),
    ]

    brief = build_daily_brief(
        actions=actions,
        reference_date=date(2026, 9, 21),
    )

    assert len(brief.due_today) == 1
    assert brief.due_today[0].title == "Send vendor list"


def test_daily_brief_identifies_overdue_action():

    actions = [
        make_action(
            action_id="a1",
            title="Send vendor list",
            owner="Arjun Malhotra",
            ownership=ActionOwnership.MY_ACTION,
            deadline_text="Wednesday",
        ),
    ]

    brief = build_daily_brief(
        actions=actions,
        reference_date=date(2026, 9, 24),
    )

    assert len(brief.overdue) == 1
    assert brief.overdue[0].status.value == "overdue"


def test_daily_brief_has_summary():

    actions = [
        make_action(
            action_id="a1",
            title="Send vendor list",
            owner="Arjun Malhotra",
            ownership=ActionOwnership.MY_ACTION,
        ),
    ]

    brief = build_daily_brief(
        actions=actions,
        reference_date=date(2026, 9, 21),
    )

    assert brief.summary != ""
    assert "1 executive actions" in brief.summary