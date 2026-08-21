from openai import OpenAI
from openai import APIConnectionError, RateLimitError, APIError, AuthenticationError
from core.config import settings
from fastapi import HTTPException
from schemas.answer_schema import AnswerEvaluationResponse


QUESTION_GENERATION_PROMPT_PATH = "prompts/question_generation_system.md"
ANSWER_EVALUATION_PROMPT_PATH = "prompts/answer_evaluation_system.md"


client = OpenAI(api_key=settings.OPENAI_API_KEY)


def read_prompt_file(path: str) -> str:
    try:
        with open(path, 'r', encoding='utf-8') as file:
            prompt = file.read()
        return prompt
    
    except FileNotFoundError:
        print(f"Erro: Arquivo {path} não encontrado")
        raise  HTTPException(
            status_code=500,
            detail="Arquivo de prompt não encontrado"
        )

    except UnicodeDecodeError:
        print(f"Não foi possivel decodificar o arquivo {path}")
        raise HTTPException(
            status_code=500,
            detail="Não foi posivel ler o arquivo de prompt"
        )
        
    except Exception as e:
        print(f"Ocorreu um erro inesperado {e}")
        raise HTTPException(
            status_code=500,
            detail="Erro interno ao carregar prompt"
        )



def generate_question_with_llm(topic: str, level: str) -> str:

    #-----------------------------RESPOSTA MOCKADA-----------------------------


    if settings.ENVIRONMENT == "test":
        return generate_question_with_llm_MOCK(topic, level)


    #-----------------------------RESPOSTA REAL(LLM)-----------------------------


    prompt = read_prompt_file(QUESTION_GENERATION_PROMPT_PATH)

    input_question = build_question_generation_input(topic, level)

    try:
        response = client.responses.create(
            model=settings.OPENAI_MODEL,
            instructions=prompt,
            input=input_question,
        )

        question = response.output_text.strip()


        if not question:
            raise HTTPException(
                status_code = 502,
                detail="A IA retornou uma resposta vazia. Tente novamente mais tarde."
            )
        
        return question

    except AuthenticationError as e:
        print(f"OpenAI authentication error: {e}")
        raise HTTPException(
            status_code=401,
            detail="Erro de autenticação com o serviço de IA."
        )
    except APIConnectionError as e:
        print(f"Failed to connect to OpenAI API: {e}")
        raise HTTPException(
            status_code=503,
            detail="Não foi possível conectar ao serviço de IA. Tente novamente mais tarde."
        )
    except RateLimitError as e:
        print(f"OpenAI API request exceeded rate limit: {e}")
        raise HTTPException(
            status_code=429,
            detail="Limite ou cota de serviço de IA excedido. Tente novamente mais tarde."
        )
    except APIError as e:
        print(f"An error has occurred in OpenAI API: {e}")
        raise HTTPException(
            status_code=502,
            detail="O serviço de IA retornou um erro. Tente novamente mais tarde."
        )


   


def evaluate_answer_with_llm(question: str, answer: str, level: str):

    #-----------------------------RESPOSTA MOCKADA-----------------------------


    if settings.ENVIRONMENT == "test":
        
        return evaluate_answer_with_llm_MOCK(answer, level)


    #-----------------------------RESPOSTA REAL(LLM)-----------------------------

    
    prompt = read_prompt_file(ANSWER_EVALUATION_PROMPT_PATH)

    input_answer = build_answer_evaluation_input(question, answer, level)
    
    try:
        response = client.responses.parse(
            model=settings.OPENAI_MODEL,
            instructions=prompt,
            input=input_answer,
            text_format=AnswerEvaluationResponse
        )
        
        evaluation = response.output_parsed
    
        if not evaluation:
            raise HTTPException(
                status_code = 502,
                detail="A IA retornou uma resposta vazia. Tente novamente mais tarde."
            )

        return evaluation
    
    except AuthenticationError as e:
        print(f"OpenAI authentication error: {e}")
        raise HTTPException(
            status_code=401,
            detail="Erro de autenticação com o serviço de IA."
        )
    except APIConnectionError as e:
        print(f"Failed to connect to OpenAI API: {e}")
        raise HTTPException(
            status_code=503,
            detail="Não foi possível conectar ao serviço de IA. Tente novamente mais tarde."
        )
    except RateLimitError as e:
        print(f"OpenAI API request exceeded rate limit: {e}")
        raise HTTPException(
            status_code=429,
            detail="Limite ou cota de serviço de IA excedido. Tente novamente mais tarde."
        )
    except APIError as e:
        print(f"An error has occurred in OpenAI API: {e}")
        raise HTTPException(
            status_code=502,
            detail="O serviço de IA retornou um erro. Tente novamente mais tarde."
        )



def evaluate_answer_with_llm_MOCK(answer: str, level: str) -> dict:

    #-----------------------------RESPOSTA MOCKADA-----------------------------
        
    score = 0
    feedback = ""
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



def generate_question_with_llm_MOCK(topic: str, level: str) -> str:

    #-----------------------------RESPOSTA MOCKADA-----------------------------

    question = f"Pergunta generica sobre {topic} em um nivel {level}"
    return question



def build_question_generation_input(topic: str, level: str) -> str:

    return f"""
            Topic: {topic}
            level: {level}    
            """



def build_answer_evaluation_input(question: str, answer: str, level: str) -> str:

    return f""" 
            Question: {question} 
            Answer: {answer} 
            Level: {level}
            """