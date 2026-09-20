import json
from pathlib import Path
from typing import Any


BASE_DIR = Path(__file__).resolve().parents[3]
SOURCE_DIR = BASE_DIR / "data" / "raw" / "assignment1"


def load_json_file(filename: str) -> dict[str, Any]:
    """
    Load one JSON source file from the Assignment 1 source directory.
    """
    file_path = SOURCE_DIR / filename

    if not file_path.exists():
        raise FileNotFoundError(f"Source file not found: {file_path}")

    with file_path.open("r", encoding="utf-8") as file:
        return json.load(file)


def load_all_sources() -> dict[str, dict[str, Any]]:
    """
    Load all Assignment 1 source files.
    """
    return {
        "people": load_json_file("people.json"),
        "meeting": load_json_file("meeting.json"),
        "calendar": load_json_file("calendar.json"),
        "emails": load_json_file("emails.json"),
        "voice_notes": load_json_file("voice_notes.json"),
    }


def validate_source(source_name: str, data: dict[str, Any]) -> None:
    """
    Perform basic structural validation for a source.
    """
    required_fields = {
        "people": ["source_type", "source_id", "people"],
        "meeting": ["source_type", "source_id", "meeting"],
        "calendar": ["source_type", "source_id", "calendars"],
        "emails": ["source_type", "source_id", "threads"],
        "voice_notes": ["source_type", "source_id", "notes"],
    }

    if source_name not in required_fields:
        raise ValueError(f"Unknown source: {source_name}")

    for field in required_fields[source_name]:
        if field not in data:
            raise ValueError(
                f"Source '{source_name}' is missing required field '{field}'"
            )


def load_and_validate_sources() -> dict[str, dict[str, Any]]:
    """
    Load all sources and validate their basic structure.
    """
    sources = load_all_sources()

    for source_name, source_data in sources.items():
        validate_source(source_name, source_data)

    return sources