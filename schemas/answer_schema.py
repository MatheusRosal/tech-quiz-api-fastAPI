from typing import Literal

from pydantic import BaseModel


class AnswerEvaluationRequest(BaseModel):
    question: str
    answer: str
    level: Literal["beginner", "intermediate", "advanced"]


class AnswerEvaluationResponse(BaseModel):
    score: int
    feedback: str