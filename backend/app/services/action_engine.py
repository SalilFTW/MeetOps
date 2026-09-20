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


def extract_actions(
    use_llm: bool = False,
) -> list[Action]:
    """
    Extract actions.

    use_llm=False:
        deterministic Assignment 1 baseline.

    use_llm=True:
        LangChain + Groq extraction.
    """

    if not use_llm:
        return extract_assignment1_actions()

    results = process_assignment1_sources_with_llm()

    actions: list[Action] = []

    for source_actions in results.values():
        actions.extend(source_actions)

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