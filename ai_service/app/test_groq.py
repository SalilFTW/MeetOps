import sys

if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from app.services.llm_action_extractor import (
    extract_actions_with_llm,
)

from app.services.llm_source_formatter import (
    format_source_for_llm,
)

from app.services.source_loader import (
    load_and_validate_sources,
)


def main():
    print("=" * 60)
    print("MEETOPS - GROQ INTEGRATION TEST")
    print("=" * 60)

    print("\n1. Loading Assignment 1 sources...")

    sources = load_and_validate_sources()

    meeting = sources["meeting"]

    print("Source loaded successfully.")
    print(f"Source type: {meeting['source_type']}")
    print(f"Source ID: {meeting['source_id']}")

    print("\n2. Formatting source for LangChain...")

    source_content = format_source_for_llm(
        source_type=meeting["source_type"],
        source_id=meeting["source_id"],
        source_data=meeting,
    )

    print("Source formatted successfully.")

    print("\n3. Sending source to Groq through LangChain...")
    print("Please wait...")

    result = extract_actions_with_llm(
        source_type=meeting["source_type"],
        source_id=meeting["source_id"],
        source_content=source_content,
    )

    print("\n4. Groq returned structured output.")
    print("-" * 60)

    if not result.actions:
        print("No actions were extracted.")
    else:
        for index, action in enumerate(
            result.actions,
            start=1,
        ):
            print(f"\nAction {index}")
            print(f"Title: {action.title}")
            print(f"Type: {action.action_type}")
            print(f"Owner: {action.owner}")
            print(f"Recipient: {action.recipient}")
            print(
                f"Deadline: {action.deadline_text}"
            )
            print(
                f"Confidence: {action.confidence}"
            )
            print(
                f"Reason: {action.ownership_reason}"
            )
            print(
                f"Evidence: {action.evidence_excerpt}"
            )

    print("\n" + "=" * 60)
    print("GROQ INTEGRATION TEST COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    main()