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

from app.services.action_resolution import (
    resolve_actions,
)


def build_action(
    action_id: str,
    title: str,
    owner: str | None,
    recipient: str | None = None,
    deadline_text: str | None = None,
    action_type: ActionType = ActionType.TASK,
):
    ownership = (
        ActionOwnership.MY_ACTION
        if owner == "Arjun Malhotra"
        else (
            ActionOwnership.WAITING_ON_OTHER
            if owner is not None
            else ActionOwnership.UNCLEAR
        )
    )

    return create_action(
        action_id=action_id,
        title=title,
        owner=owner,
        recipient=recipient,
        ownership=ownership,
        action_type=action_type,
        source_type="test",
        source_id=action_id,
        excerpt=title,
        deadline_text=deadline_text,
    )


def test_similar_actions_are_merged():

    first = build_action(
        action_id="action_1",
        title="Send updated vendor list",
        owner="Arjun Malhotra",
        recipient="Raghav Sethi",
    )

    second = build_action(
        action_id="action_2",
        title="Send the updated vendor list to Raghav",
        owner="Arjun Malhotra",
        recipient="Raghav Sethi",
    )

    result = resolve_actions(
        [first, second]
    )

    assert len(result.canonical_actions) == 1

    assert (
        len(
            result.canonical_actions[0]
            .source_evidence
        )
        == 2
    )


def test_different_actions_remain_separate():

    first = build_action(
        action_id="action_1",
        title="Send updated vendor list",
        owner="Arjun Malhotra",
        recipient="Raghav Sethi",
    )

    second = build_action(
        action_id="action_2",
        title="Review Q3 campaign deck",
        owner="Arjun Malhotra",
        recipient="Neha Kapoor",
    )

    result = resolve_actions(
        [first, second]
    )

    assert len(result.canonical_actions) == 2


def test_ownership_conflict_is_detected():

    first = build_action(
        action_id="action_1",
        title="Prepare expense variance report",
        owner="Divya Rao",
    )

    second = build_action(
        action_id="action_2",
        title="Prepare the expense variance report",
        owner="Arjun Malhotra",
    )

    result = resolve_actions(
        [first, second]
    )

    assert len(result.canonical_actions) == 2

    ownership_conflicts = [
        conflict
        for conflict in result.conflicts
        if conflict.conflict_type
        == ConflictType.OWNERSHIP
    ]

    assert len(ownership_conflicts) == 1


def test_deadline_conflict_is_detected():

    first = build_action(
        action_id="action_1",
        title="Send updated vendor list",
        owner="Arjun Malhotra",
        deadline_text="Wednesday morning",
    )

    second = build_action(
        action_id="action_2",
        title="Send updated vendor list",
        owner="Arjun Malhotra",
        deadline_text="Thursday morning",
    )

    result = resolve_actions(
        [first, second]
    )

    deadline_conflicts = [
        conflict
        for conflict in result.conflicts
        if conflict.conflict_type
        == ConflictType.DEADLINE
    ]

    assert len(deadline_conflicts) == 1


def test_unclear_owner_can_merge_with_explicit_owner():

    first = build_action(
        action_id="action_1",
        title="Sign off Mumbai office renewal paperwork",
        owner=None,
    )

    second = build_action(
        action_id="action_2",
        title="Sign off the Mumbai office renewal paperwork",
        owner="Facilities",
    )

    result = resolve_actions(
        [first, second]
    )

    assert len(result.canonical_actions) == 1

    assert (
        result.canonical_actions[0].owner
        == "Facilities"
    )