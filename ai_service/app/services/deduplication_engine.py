from app.models.action import Action

from app.models.deduplication import (
    ActionConflict,
    ConflictType,
    DeduplicationResult,
)

from app.services.action_merger import (
    merge_actions,
)

from app.services.action_similarity import (
    are_likely_duplicates,
    are_task_similar,
)

from app.services.conflict_detector import (
    detect_conflicts,
)


def deduplicate_actions(
    actions: list[Action],
) -> DeduplicationResult:
    """
    Deduplicate a collection of actions.

    Actions that appear to represent the same underlying
    task are grouped together.

    Conflicts are detected before merging so that
    contradictory evidence is never silently lost.
    """

    canonical_actions: list[Action] = []

    merged_action_ids: dict[
        str,
        list[str],
    ] = {}

    conflicts: list[ActionConflict] = []

    for action in actions:

        matched = False

        for canonical in canonical_actions:

            if not are_task_similar(
                canonical,
                action,
            ):
                continue

            # IMPORTANT:
            # Detect conflicts between related actions.
            action_conflicts = detect_conflicts(
                canonical,
                action,
            )

            conflicts.extend(
                action_conflicts
            )

            # Do not merge if there is an ownership conflict or they are not duplicate-mergeable
            has_ownership_conflict = any(
                c.conflict_type == ConflictType.OWNERSHIP
                for c in action_conflicts
            )

            if has_ownership_conflict or not are_likely_duplicates(
                canonical,
                action,
            ):
                continue

            merge_actions(
                canonical,
                action,
            )

            merged_action_ids.setdefault(
                canonical.id,
                [],
            ).append(action.id)

            matched = True

            break

        if not matched:
            canonical_actions.append(
                action
            )

    return DeduplicationResult(
        canonical_actions=canonical_actions,
        merged_action_ids=merged_action_ids,
        conflicts=conflicts,
    )