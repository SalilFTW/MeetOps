from app.models.action import Action

from app.services.text_normalizer import (
    text_similarity,
    tokenize,
)


ACTION_WORDS = {
    "send",
    "sent",
    "prepare",
    "prepared",
    "pull",
    "pulled",
    "review",
    "reviewed",
    "sign",
    "signed",
    "confirm",
    "confirmed",
    "reconfirm",
    "reconfirmed",
    "get",
    "got",
    "provide",
    "provided",
    "update",
    "updated",
    "complete",
    "completed",
    "submit",
    "submitted",
    "receive",
    "received",
}


def owner_matches(
    first: Action,
    second: Action,
) -> bool:
    """
    Compare explicit owners.

    If either action has no explicit owner (None), they can match.
    If both actions have explicit owners that differ, they do not match as duplicates.
    """

    if (
        first.owner is None
        or second.owner is None
    ):
        return True

    return (
        first.owner.strip().lower()
        == second.owner.strip().lower()
    )


def recipient_matches(
    first: Action,
    second: Action,
) -> bool:
    """
    Compare recipients.

    Missing recipient information does not prevent
    two actions from being considered duplicates.
    """

    if (
        first.recipient is None
        or second.recipient is None
    ):
        return True

    return (
        first.recipient.strip().lower()
        == second.recipient.strip().lower()
    )


def action_title_similarity(
    first: Action,
    second: Action,
) -> float:
    """
    Compare action titles using token similarity.
    """

    return text_similarity(
        first.title,
        second.title,
    )


def shared_action_words(
    first: Action,
    second: Action,
) -> set[str]:
    """
    Find meaningful action words shared by both titles.
    """

    first_tokens = tokenize(first.title)
    second_tokens = tokenize(second.title)

    return (
        first_tokens
        & second_tokens
        & ACTION_WORDS
    )


def are_task_similar(
    first: Action,
    second: Action,
    threshold: float = 0.40,
) -> bool:
    """
    Determine whether two actions represent the same underlying task,
    regardless of whether owners conflict.
    """

    if not recipient_matches(
        first,
        second,
    ):
        return False

    similarity = action_title_similarity(
        first,
        second,
    )

    if similarity >= threshold:
        return True

    first_tokens = tokenize(first.title)
    second_tokens = tokenize(second.title)
    common_tokens = first_tokens & second_tokens

    if len(common_tokens) >= 2:
        # Both contain action verbs (even if different e.g. send vs get)
        has_first_action = bool(first_tokens & ACTION_WORDS)
        has_second_action = bool(second_tokens & ACTION_WORDS)
        if has_first_action and has_second_action:
            return True

        if common_tokens & ACTION_WORDS:
            return True

        if first.recipient and second.recipient:
            return True

    return False


def are_likely_duplicates(
    first: Action,
    second: Action,
    threshold: float = 0.40,
) -> bool:
    """
    Determine whether two actions likely represent
    the same underlying action and can be safely merged.

    Actions with different explicit owners do not match as duplicates;
    they represent an ownership conflict.
    """

    if not owner_matches(
        first,
        second,
    ):
        return False

    return are_task_similar(
        first,
        second,
        threshold=threshold,
    )