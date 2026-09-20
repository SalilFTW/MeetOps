import re


STOP_WORDS = {
    "the",
    "a",
    "an",
    "to",
    "for",
    "of",
    "and",
    "with",
    "on",
    "in",
    "by",
    "from",
    "this",
    "that",
    "will",
    "need",
    "needs",
}


def normalize_text(text: str | None) -> str:
    """
    Normalize text for comparison.

    This does not change the original Action.
    It only creates a comparison representation.
    """

    if not text:
        return ""

    text = text.lower()

    text = re.sub(
        r"[^a-z0-9\s]",
        " ",
        text,
    )

    text = re.sub(
        r"\s+",
        " ",
        text,
    ).strip()

    return text


def tokenize(text: str | None) -> set[str]:
    """
    Convert normalized text into comparison tokens.
    """

    normalized = normalize_text(text)

    if not normalized:
        return set()

    return {
        token
        for token in normalized.split()
        if token not in STOP_WORDS
    }


def text_similarity(
    first: str | None,
    second: str | None,
) -> float:
    """
    Calculate token-based Jaccard similarity.

    Returns a value between 0 and 1.
    """

    first_tokens = tokenize(first)
    second_tokens = tokenize(second)

    if not first_tokens or not second_tokens:
        return 0.0

    intersection = first_tokens & second_tokens
    union = first_tokens | second_tokens

    if not union:
        return 0.0

    return len(intersection) / len(union)