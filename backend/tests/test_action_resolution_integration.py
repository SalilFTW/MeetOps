from app.models.action import (
    ActionOwnership,
    ActionType,
)

from app.services.action_extractor import (
    create_action,
)

from app.services.action_resolution import (
    resolve_actions,
)


def test_vendor_list_from_multiple_sources_becomes_one_action():

    meeting_action = create_action(
        action_id="meeting_vendor",
        title="Send updated vendor list",
        owner="Arjun Malhotra",
        recipient="Raghav Sethi",
        ownership=ActionOwnership.MY_ACTION,
        action_type=ActionType.COMMITMENT,
        source_type="meeting_transcript",
        source_id="leadership_sync",
        excerpt=(
            "I told Raghav I’d send him the updated vendor list."
        ),
    )

    email_action = create_action(
        action_id="email_vendor",
        title="Send the updated vendor list to Raghav",
        owner="Arjun Malhotra",
        recipient="Raghav Sethi",
        ownership=ActionOwnership.MY_ACTION,
        action_type=ActionType.TASK,
        source_type="email",
        source_id="vendor_thread",
        excerpt=(
            "I'll send the updated vendor list tomorrow morning."
        ),
    )

    voice_action = create_action(
        action_id="voice_vendor",
        title="Get Raghav the vendor list",
        owner="Arjun Malhotra",
        recipient="Raghav Sethi",
        ownership=ActionOwnership.MY_ACTION,
        action_type=ActionType.FOLLOW_UP,
        source_type="voice_note",
        source_id="voice_001",
        excerpt=(
            "Need to get Raghav vendor list."
        ),
    )

    result = resolve_actions(
        [
            meeting_action,
            email_action,
            voice_action,
        ]
    )

    assert len(result.canonical_actions) == 1

    canonical = result.canonical_actions[0]

    assert (
        canonical.owner
        == "Arjun Malhotra"
    )

    assert (
        canonical.recipient
        == "Raghav Sethi"
    )

    assert (
        len(canonical.source_evidence)
        == 3
    )

    assert (
        "meeting_transcript",
        "leadership_sync",
        None,
        "I told Raghav I’d send him the updated vendor list.",
    ) in {
        (
            evidence.source_type,
            evidence.source_id,
            evidence.reference_id,
            evidence.excerpt,
        )
        for evidence in canonical.source_evidence
    }