from typing import Optional

from pydantic import BaseModel, Field


class ExtractedAction(BaseModel):
    title: str = Field(
        description="Short description of the action or commitment."
    )

    action_type: str = Field(
        description="One of: commitment, task, follow_up."
    )

    owner: Optional[str] = Field(
        default=None,
        description="Person explicitly responsible for the action."
    )

    recipient: Optional[str] = Field(
        default=None,
        description="Person who receives the result or is involved."
    )

    deadline_text: Optional[str] = Field(
        default=None,
        description="Original natural-language deadline from the source."
    )

    ownership_reason: str = Field(
        description=(
            "Brief explanation of why the identified person owns the "
            "action, or why ownership is unclear."
        )
    )

    evidence_excerpt: str = Field(
        description="Short exact excerpt supporting the extracted action."
    )

    confidence: float = Field(
        ge=0.0,
        le=1.0,
        description="Confidence between 0 and 1."
    )


class ExtractedActions(BaseModel):
    actions: list[ExtractedAction] = Field(
        default_factory=list
    )