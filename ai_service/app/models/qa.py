from pydantic import BaseModel, Field


class QuestionRequest(BaseModel):
    question: str = Field(
        min_length=1,
        description="Natural-language question from the executive.",
    )


class QuestionAnswer(BaseModel):
    question: str
    answer: str
    action_ids: list[str] = Field(default_factory=list)
    evidence: list[str] = Field(default_factory=list)
    confidence: float = Field(ge=0.0, le=1.0)