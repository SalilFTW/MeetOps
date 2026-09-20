from app.models.action import (
    ActionOwnership,
    ActionType,
)

from app.models.deduplication import (
    ConflictType,
)

from app.services.action_extractor import (
    create_action,
)

from app.services.conflict_detector import (
    detect_conflicts,
)


def make_action(
    action_id: str,
    title: str,
    owner: str | None,
    deadline_text: str | None = None,
):
    if owner == "Arjun Malhotra":
        ownership = ActionOwnership.MY_ACTION
    elif owner:
        ownership = (
            ActionOwnership.WAITING_ON_OTHER
        )
    else:
        ownership = ActionOwnership.UNCLEAR

    return create_action(
        action_id=action_id,
        title=title,
        owner=owner,
        ownership=ownership,
        action_type=ActionType.TASK,
        source_type="test",
        source_id=action_id,
        excerpt=title,
        deadline_text=deadline_text,
    )


def test_no_conflict_for_same_owner():

    first = make_action(
        "a1",
        "Send vendor list",
        "Arjun Malhotra",
    )

    second = make_action(
        "a2",
        "Send vendor list",
        "Arjun Malhotra",
    )

    conflicts = detect_conflicts(
        first,
        second,
    )

    ownership_conflicts = [
        conflict
        for conflict in conflicts
        if conflict.conflict_type
        == ConflictType.OWNERSHIP
    ]

    assert ownership_conflicts == []


def test_conflict_for_different_owners():

    first = make_action(
        "a1",
        "Prepare report",
        "Divya Rao",
    )

    second = make_action(
        "a2",
        "Prepare report",
        "Arjun Malhotra",
    )

    conflicts = detect_conflicts(
        first,
        second,
    )

    assert any(
        conflict.conflict_type
        == ConflictType.OWNERSHIP
        for conflict in conflicts
    )


def test_conflict_for_different_deadlines():

    first = make_action(
        "a1",
        "Send vendor list",
        "Arjun Malhotra",
        "Wednesday morning",
    )

    second = make_action(
        "a2",
        "Send vendor list",
        "Arjun Malhotra",
        "Thursday morning",
    )

    conflicts = detect_conflicts(
        first,
        second,
    )

    assert any(
        conflict.conflict_type
        == ConflictType.DEADLINE
        for conflict in conflicts
    )