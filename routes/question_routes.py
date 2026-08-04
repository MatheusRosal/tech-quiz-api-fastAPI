from fastapi import APIRouter
from schemas.question_schema import QuestionGenerationRequest,QuestionGenerationResponse
from services.question_service import generate_question


router = APIRouter()


@router.post("/questions/generate", response_model=QuestionGenerationResponse)
def generation_response(payload: QuestionGenerationRequest):
    return generate_question(payload.topic, payload.level)