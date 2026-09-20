from app.models.action import Action


def normalize_query(text: str) -> str:
    return " ".join(text.lower().strip().split())


def retrieve_relevant_actions(
    question: str,
    actions: list[Action],
) -> list[Action]:
    query = normalize_query(question)

    if not query:
        return []

    results: list[tuple[int, Action]] = []

    for action in actions:
        score = 0

        title = normalize_query(action.title)

        owner = normalize_query(action.owner or "")
        recipient = normalize_query(action.recipient or "")

        evidence_text = " ".join(
            normalize_query(evidence.excerpt)
            for evidence in action.source_evidence
        )

        searchable_text = " ".join(
            [
                title,
                owner,
                recipient,
                evidence_text,
                action.deadline_text or "",
            ]
        )

        words = set(query.split())

        for word in words:
            if len(word) < 3:
                continue

            if word in searchable_text:
                score += 1

        if "promise" in query or "promised" in query:
            if action.action_type.value == "commitment":
                score += 3

        if "waiting" in query:
            if action.ownership.value == "waiting_on_other":
                score += 5

        if "unclear" in query:
            if action.ownership.value == "unclear":
                score += 5

        if "overdue" in query:
            if action.status.value == "overdue":
                score += 5

        if "today" in query:
            if action.deadline_text:
                score += 1

        if score > 0:
            results.append((score, action))

    results.sort(
        key=lambda item: item[0],
        reverse=True,
    )

    return [
        action
        for _, action in results
    ]