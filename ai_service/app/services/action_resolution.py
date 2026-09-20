from app.models.action import Action

from app.models.deduplication import (
    DeduplicationResult,
)

from app.services.deduplication_engine import (
    deduplicate_actions,
)


def resolve_actions(
    actions: list[Action],
) -> DeduplicationResult:
    """
    Resolve raw extracted actions into canonical actions.

    Current resolution stages:

    1. Deduplicate similar actions.
    2. Merge evidence.
    3. Detect conflicts.
    """

    return deduplicate_actions(
        actions
    )