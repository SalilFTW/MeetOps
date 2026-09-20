from langchain_groq import ChatGroq

from app.config import GROQ_API_KEY, GROQ_MODEL


def get_llm() -> ChatGroq:
    """
    Create the configured Groq chat model.
    """

    if not GROQ_API_KEY:
        raise RuntimeError(
            "GROQ_API_KEY is not configured. "
            "Add it to the .env file before running LLM extraction."
        )

    return ChatGroq(
        model=GROQ_MODEL,
        api_key=GROQ_API_KEY,
        temperature=0,
        max_tokens=4096,
    )