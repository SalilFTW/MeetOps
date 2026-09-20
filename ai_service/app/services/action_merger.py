from app.models.action import Action


def merge_actions(
    primary: Action,
    duplicate: Action,
) -> Action:
    """
    Merge duplicate evidence into the primary action.

    The primary action remains the canonical action.
    Evidence from the duplicate is preserved.
    """

    existing_evidence_keys = {
        (
            evidence.source_type,
            evidence.source_id,
            evidence.reference_id,
            evidence.excerpt,
        )
        for evidence in primary.source_evidence
    }

    for evidence in duplicate.source_evidence:
        evidence_key = (
            evidence.source_type,
            evidence.source_id,
            evidence.reference_id,
            evidence.excerpt,
        )

        if evidence_key not in existing_evidence_keys:
            primary.source_evidence.append(
                evidence
            )

            existing_evidence_keys.add(
                evidence_key
            )

    existing_notes = set(primary.notes)

    for note in duplicate.notes:
        if note not in existing_notes:
            primary.notes.append(note)
            existing_notes.add(note)

    if (
        primary.confidence is None
        and duplicate.confidence is not None
    ):
        primary.confidence = duplicate.confidence

    elif (
        primary.confidence is not None
        and duplicate.confidence is not None
    ):
        primary.confidence = max(
            primary.confidence,
            duplicate.confidence,
        )

    if (
        primary.deadline_text is None
        and duplicate.deadline_text is not None
    ):
        primary.deadline_text = (
            duplicate.deadline_text
        )

    if (
        primary.deadline is None
        and duplicate.deadline is not None
    ):
        primary.deadline = duplicate.deadline

    if (
        primary.owner is None
        and duplicate.owner is not None
    ):
        primary.owner = duplicate.owner

    if (
        primary.recipient is None
        and duplicate.recipient is not None
    ):
        primary.recipient = duplicate.recipient

    return primary