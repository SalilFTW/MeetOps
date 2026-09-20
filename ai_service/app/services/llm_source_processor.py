from app.services.source_loader import (
    load_and_validate_sources,
)

from app.services.llm_pipeline import (
    process_source_with_llm,
)


ACTION_SOURCE_NAMES = [
    "meeting",
    "emails",
    "voice_notes",
]


def process_assignment1_sources_with_llm():
    """
    Process only action-bearing Assignment 1 sources
    through the LLM.

    People and calendar data are retained as context
    and are not blindly treated as action sources.
    """

    sources = load_and_validate_sources()

    results = {}

    for source_name in ACTION_SOURCE_NAMES:
        source = sources[source_name]

        results[source_name] = process_source_with_llm(
            source_type=source["source_type"],
            source_id=source["source_id"],
            source_data=source,
        )

    return results