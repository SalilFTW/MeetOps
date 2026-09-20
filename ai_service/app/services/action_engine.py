from app.models.action import (
    Action,
    ActionOwnership,
)

from app.services.assignment1_extractor import (
    extract_assignment1_actions,
)

from app.services.llm_source_processor import (
    process_assignment1_sources_with_llm,
)

from app.services.action_resolution import (
    resolve_actions,
)


def extract_actions(
    use_llm: bool = False,
    resolve_duplicates: bool = False,
) -> list[Action]:
    """
    Extract actions.

    use_llm=False:
        deterministic Assignment 1 baseline.

    use_llm=True:
        LangChain + Groq extraction.

    resolve_duplicates=True:
        Run Phase 4 deduplication and return
        canonical actions.
    """

    if not use_llm:
        actions = extract_assignment1_actions()

    else:
        results = (
            process_assignment1_sources_with_llm()
        )

        actions = []

        for source_actions in results.values():
            actions.extend(
                source_actions
            )

    if resolve_duplicates:
        result = resolve_actions(
            actions
        )

        return result.canonical_actions

    return actions


def group_actions(
    actions: list[Action],
) -> dict[str, list[Action]]:
    """
    Group actions according to ownership.
    """

    return {
        "my_actions": [
            action
            for action in actions
            if action.ownership
            == ActionOwnership.MY_ACTION
        ],
        "waiting_on_others": [
            action
            for action in actions
            if action.ownership
            == ActionOwnership.WAITING_ON_OTHER
        ],
        "unclear": [
            action
            for action in actions
            if action.ownership
            == ActionOwnership.UNCLEAR
        ],
    }