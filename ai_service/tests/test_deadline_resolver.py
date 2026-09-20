from app.models.action import Action
from datetime import date

from app.models.action import ActionStatus
from app.services.deadline_resolver import (
    apply_deadline_status,
    resolve_deadline,
)


REFERENCE_DATE = date(2026, 9, 21)


def test_tomorrow_resolves_correctly():
    result = resolve_deadline(
        "by end of day tomorrow",
        REFERENCE_DATE,
    )

    assert result == date(2026, 9, 22)


def test_wednesday_resolves_correctly():
    result = resolve_deadline(
        "Wednesday evening",
        REFERENCE_DATE,
    )

    assert result == date(2026, 9, 23)


def test_thursday_resolves_correctly():
    result = resolve_deadline(
        "Thursday morning",
        REFERENCE_DATE,
    )

    assert result == date(2026, 9, 24)


def test_this_week_does_not_invent_exact_date():
    result = resolve_deadline(
        "this week",
        REFERENCE_DATE,
    )

    assert result is None


def test_past_deadline_becomes_overdue():
    action = Action(
        id="test_action",
        title="Test action",
        action_type="task",
        owner="Arjun Malhotra",
        recipient=None,
        ownership="my_action",
        deadline_text="Wednesday",
    )

    updated = apply_deadline_status(
        action=action,
        reference_date=date(2026, 9, 24),
    )

    assert updated.status == ActionStatus.OVERDUE