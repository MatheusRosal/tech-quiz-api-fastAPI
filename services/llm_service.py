from openai import OpenAI
from core.config import settings



client = OpenAI(api_key=settings.OPENAI_API_KEY)

def prompt_reader(caminho: str, topic: str, level: str) -> str:
    prompt_base = f"Você é um especialista em T.I e deve retornar uma pergunta que contemple o tema: {topic} e que seja compativel com o level:{level}. retorne apenas a pergunta e nada mais"
    try:
        with open(caminho, 'r', encoding='utf-8') as arquivo:
            prompt = arquivo.read()
        return prompt
    
    except FileNotFoundError:
        print(f"Erro: Arquivo {caminho} não encontrado")
        return prompt_base
    except UnicodeDecodeError:
        print(f"Não foi possivel decodificar o arquivo {caminho}")
        return prompt_base
    except Exception as e:
        print(f"Ocorreu um erro inesperado {e}")
        return prompt_base


def generate_question_with_llm(topic: str, level: str) -> str:
    if settings.ENVIRONMENT == "test":
        question = f"Pergunta generica sobre {topic} em um nivel {level}"
        return question
    
    prompt = prompt_reader("prompts/question_generation_system.md", topic, level)

    response = client.responses.create(
        model=settings.OPENAI_MODEL,
        instructions=prompt,
        input=f"""
        Topic:{topic}
        level:{level}    
        """,
    )
    
    return response.output_text


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