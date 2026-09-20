import json
from typing import Any


def format_source_for_llm(
    source_type: str,
    source_id: str,
    source_data: dict[str, Any],
) -> str:
    """
    Convert structured source data into readable JSON
    for the LLM.

    This function only prepares data.
    It does not perform reasoning.
    """

    return json.dumps(
        {
            "source_type": source_type,
            "source_id": source_id,
            "content": source_data,
        },
        indent=2,
        ensure_ascii=False,
    )
    