from services.llm_service import evaluate_answer_with_llm


def evaluate_answer(question: str, answer: str, level: str):
    return evaluate_answer_with_llm(question, answer, level)