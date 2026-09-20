from app.models.llm_output import ExtractedActions

from app.prompts.action_extraction import (
    ACTION_EXTRACTION_SYSTEM_PROMPT,
    ACTION_EXTRACTION_USER_PROMPT,
)

from app.services.llm_client import get_llm


def extract_actions_with_llm(
    source_type: str,
    source_id: str,
    source_content: str,
) -> ExtractedActions:
    """
    Extract structured actions from one source
    using LangChain + Groq.
    """

    llm = get_llm()

    structured_llm = llm.with_structured_output(
        ExtractedActions
    )

    messages = [
        (
            "system",
            ACTION_EXTRACTION_SYSTEM_PROMPT,
        ),
        (
            "human",
            ACTION_EXTRACTION_USER_PROMPT.format(
                source_type=source_type,
                source_id=source_id,
                source_content=source_content,
            ),
        ),
    ]

    result = structured_llm.invoke(messages)

    return result
    