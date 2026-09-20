from app.models.action import (
    ActionOwnership,
    ActionType,
)

from app.services.action_extractor import (
    create_action,
)

from app.services.action_similarity import (
    are_likely_duplicates,
)


def make_action(
    action_id: str,
    title: str,
    owner: str | None,
    recipient: str | None = None,
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
        recipient=recipient,
        ownership=ownership,
        action_type=ActionType.TASK,
        source_type="test",
        source_id=action_id,
        excerpt=title,
    )


def test_similar_titles_match():

    first = make_action(
        "a1",
        "Send updated vendor list",
        "Arjun Malhotra",
        "Raghav Sethi",
    )

    second = make_action(
        "a2",
        "Send the updated vendor list to Raghav",
        "Arjun Malhotra",
        "Raghav Sethi",
    )

    assert are_likely_duplicates(
        first,
        second,
    )


def test_unrelated_titles_do_not_match():

    first = make_action(
        "a1",
        "Send updated vendor list",
        "Arjun Malhotra",
    )

    second = make_action(
        "a2",
        "Review campaign deck",
        "Arjun Malhotra",
    )

    assert not are_likely_duplicates(
        first,
        second,
    )


def test_different_explicit_owners_do_not_match():

    first = make_action(
        "a1",
        "Prepare expense variance report",
        "Divya Rao",
    )

    second = make_action(
        "a2",
        "Prepare expense variance report",
        "Arjun Malhotra",
    )

    assert not are_likely_duplicates(
        first,
        second,
    )