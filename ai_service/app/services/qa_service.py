import json

from app.models.action import Action
from app.models.qa import QuestionAnswer
from app.prompts.qa import (
    QA_SYSTEM_PROMPT,
    QA_USER_PROMPT,
)
from app.services.llm_client import get_llm
from app.services.qa_retriever import retrieve_relevant_actions


def build_action_context(actions: list[Action]) -> str:
    context = []

    for action in actions:
        evidence = [
            {
                "source_type": item.source_type,
                "source_id": item.source_id,
                "excerpt": item.excerpt,
            }
            for item in action.source_evidence
        ]

        context.append(
            {
                "id": action.id,
                "title": action.title,
                "action_type": action.action_type.value,
                "owner": action.owner,
                "recipient": action.recipient,
                "ownership": action.ownership.value,
                "deadline": action.deadline_text,
                "status": action.status.value,
                "evidence": evidence,
                "notes": action.notes,
            }
        )

    return json.dumps(
        context,
        indent=2,
        ensure_ascii=False,
    )


def answer_question(
    question: str,
    actions: list[Action],
) -> QuestionAnswer:

    relevant_actions = retrieve_relevant_actions(
        question=question,
        actions=actions,
    )

    if not relevant_actions:
        return QuestionAnswer(
            question=question,
            answer=(
                "The supplied Assignment 1 data does not "
                "establish an answer to that question."
            ),
            action_ids=[],
            evidence=[],
            confidence=0.0,
        )

    context = build_action_context(
        relevant_actions
    )

    llm = get_llm()

    messages = [
        (
            "system",
            QA_SYSTEM_PROMPT,
        ),
        (
            "human",
            QA_USER_PROMPT.format(
                question=question,
                context=context,
            ),
        ),
    ]

    response = llm.invoke(messages)

    answer_text = response.content

    evidence = []

    for action in relevant_actions:
        for source in action.source_evidence:
            if source.excerpt:
                evidence.append(source.excerpt)

    confidence = min(
        1.0,
        0.6 + (0.1 * min(len(relevant_actions), 4)),
    )

    return QuestionAnswer(
        question=question,
        answer=answer_text,
        action_ids=[
            action.id
            for action in relevant_actions
        ],
        evidence=evidence,
        confidence=confidence,
    )