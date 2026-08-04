from fastapi import APIRouter
from schemas.answer_schema import AnswerEvaluationRequest, AnswerEvaluationResponse
from services.answer_service import evaluate_answer


router = APIRouter()


@router.post("/answers/evaluate", response_model=AnswerEvaluationResponse)
def evaluate_user_answer(payload: AnswerEvaluationRequest):
    return evaluate_answer(payload.answer, payload.level)