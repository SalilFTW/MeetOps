from app.models.action import Action
from app.models.deduplication import (
    ActionConflict,
    ConflictType,
)


def detect_ownership_conflict(
    first: Action,
    second: Action,
) -> ActionConflict | None:
    """
    Detect contradictory explicit owners.
    """

    if first.owner is None or second.owner is None:
        return None

    first_owner = first.owner.strip().lower()
    second_owner = second.owner.strip().lower()

    if first_owner == second_owner:
        return None

    return ActionConflict(
        action_ids=[
            first.id,
            second.id,
        ],
        conflict_type=ConflictType.OWNERSHIP,
        description=(
            f"Different explicit owners were extracted: "
            f"'{first.owner}' and '{second.owner}'."
        ),
        severity="high",
    )


def detect_deadline_conflict(
    first: Action,
    second: Action,
) -> ActionConflict | None:
    """
    Detect different explicit deadline text.

    We only flag a conflict when both actions have
    deadline information and the text differs.

    We do not try to interpret natural-language dates here.
    """

    if (
        first.deadline_text is None
        or second.deadline_text is None
    ):
        return None

    first_deadline = (
        first.deadline_text.strip().lower()
    )

    second_deadline = (
        second.deadline_text.strip().lower()
    )

    if first_deadline == second_deadline:
        return None

    return ActionConflict(
        action_ids=[
            first.id,
            second.id,
        ],
        conflict_type=ConflictType.DEADLINE,
        description=(
            f"Different deadline statements were found: "
            f"'{first.deadline_text}' and "
            f"'{second.deadline_text}'."
        ),
        severity="medium",
    )


def detect_action_type_conflict(
    first: Action,
    second: Action,
) -> ActionConflict | None:
    """
    Detect different action classifications.

    This is informational rather than automatically
    treating the actions as separate.
    """

    if first.action_type == second.action_type:
        return None

    return ActionConflict(
        action_ids=[
            first.id,
            second.id,
        ],
        conflict_type=ConflictType.ACTION_TYPE,
        description=(
            f"The same-looking action was classified "
            f"as '{first.action_type.value}' and "
            f"'{second.action_type.value}'."
        ),
        severity="low",
    )


def detect_conflicts(
    first: Action,
    second: Action,
) -> list[ActionConflict]:
    """
    Detect all supported conflicts between two actions.
    """

    conflicts: list[ActionConflict] = []

    ownership_conflict = detect_ownership_conflict(
        first,
        second,
    )

    if ownership_conflict:
        conflicts.append(
            ownership_conflict
        )

    deadline_conflict = detect_deadline_conflict(
        first,
        second,
    )

    if deadline_conflict:
        conflicts.append(
            deadline_conflict
        )

    type_conflict = detect_action_type_conflict(
        first,
        second,
    )

    if type_conflict:
        conflicts.append(
            type_conflict
        )

    return conflicts