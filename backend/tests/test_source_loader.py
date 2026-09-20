from app.services.source_loader import load_and_validate_sources


def test_all_assignment1_sources_load():
    sources = load_and_validate_sources()

    assert "people" in sources
    assert "meeting" in sources
    assert "calendar" in sources
    assert "emails" in sources
    assert "voice_notes" in sources


def test_people_source():
    sources = load_and_validate_sources()

    assert sources["people"]["source_type"] == "people_directory"
    assert len(sources["people"]["people"]) == 6


def test_meeting_source():
    sources = load_and_validate_sources()

    assert sources["meeting"]["source_type"] == "meeting_transcript"
    assert sources["meeting"]["meeting"]["title"] == "Leadership Sync"


def test_email_source():
    sources = load_and_validate_sources()

    assert sources["emails"]["source_type"] == "email"
    assert len(sources["emails"]["threads"]) == 5


def test_voice_note_source():
    sources = load_and_validate_sources()

    assert sources["voice_notes"]["source_type"] == "voice_note_transcript"
    assert len(sources["voice_notes"]["notes"]) == 2