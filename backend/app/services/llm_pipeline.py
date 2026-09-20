from app.models.action import Action

from app.services.llm_action_extractor import (
    extract_actions_with_llm,
)

from app.services.llm_source_formatter import (
    format_source_for_llm,
)

from app.services.llm_to_action import (
    convert_extracted_action,
)


def process_source_with_llm(
    source_type: str,
    source_id: str,
    source_data: dict,
) -> list[Action]:
    """
    Process one actionable source through:

    source
      ↓
    formatter
      ↓
    LangChain
      ↓
    Groq
      ↓
    structured output
      ↓
    Action model
    """

    source_content = format_source_for_llm(
        source_type=source_type,
        source_id=source_id,
        source_data=source_data,
    )

    extracted = extract_actions_with_llm(
        source_type=source_type,
        source_id=source_id,
        source_content=source_content,
    )

    actions: list[Action] = []

    for index, extracted_action in enumerate(
        extracted.actions,
        start=1,
    ):
        action_id = (
            f"{source_id}_action_{index}"
        )

        action = convert_extracted_action(
            extracted=extracted_action,
            action_id=action_id,
            source_type=source_type,
            source_id=source_id,
        )

        actions.append(action)

    return actions