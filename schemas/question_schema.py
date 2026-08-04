from pydantic import BaseModel
from typing import Literal

class QuestionGenerationRequest(BaseModel):
    topic: str
    level: Literal["beginner", "intermediate", "advanced"]


class QuestionGenerationResponse(BaseModel):
    question: str
    topic: str
    level: Literal["beginner", "intermediate", "advanced"]


