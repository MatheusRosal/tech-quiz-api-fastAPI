


def generate_question_with_llm(topic: str, level: str) -> str:
    question = f"Pergunta generica sobre {topic} em um nivel {level}"

    return question


def evaluate_answer_with_llm(question: str, answer: str, level: str):
    score = 0
    feedback = ""
    #TODO: Adicionar serviço de llm real para avaliar resposta
    #Por enquanto regra de negocio extensa para simular diferentes respostas
    if level == "beginner":
        if len(answer) < 40:
            score = 5
            feedback = "Sua resposta está muito curta. Tente explicar melhor."
        elif len(answer) < 120:
            score = 7
            feedback = "Boa resposta, mas ainda pode trazer mais detalhes"
        else:
            score = 9
            feedback = "Ótima resposta. Você trouxe uma explicação mais completa."

    elif level == "intermediate":
        if len(answer) < 60:
            score = 5
            feedback = "Sua resposta está muito curta. Tente explicar melhor."
        elif len(answer) < 160:
            score = 7
            feedback = "Boa resposta, mas ainda pode trazer mais detalhes"
        else:
            score = 9
            feedback = "Ótima resposta. Você trouxe uma explicação mais completa."

    else:
        if len(answer) < 100:
            score = 5
            feedback = "Sua resposta está muito curta. Tente explicar melhor."
        elif len(answer) < 220:
            score = 7
            feedback = "Boa resposta, mas ainda pode trazer mais detalhes"
        else:
            score = 9
            feedback = "Ótima resposta. Você trouxe uma explicação mais completa."

    return {
        "score": score,
        "feedback": feedback
    }