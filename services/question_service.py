from services.llm_service import generate_question_with_llm


def generate_question(topic: str, level: str):
    question = generate_question_with_llm(topic, level)
    return {
        "question": question,
        "topic": topic,
        "level": level
    }
    
