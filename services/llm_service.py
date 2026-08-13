from openai import OpenAI
from openai import APIConnectionError, RateLimitError, APIError, AuthenticationError
from core.config import settings
from fastapi import HTTPException
from schemas.answer_schema import AnswerEvaluationResponse



client = OpenAI(api_key=settings.OPENAI_API_KEY)

def prompt_reader(caminho: str) -> str:
    try:
        with open(caminho, 'r', encoding='utf-8') as arquivo:
            prompt = arquivo.read()
        return prompt
    
    except FileNotFoundError:
        print(f"Erro: Arquivo {caminho} não encontrado")
    except UnicodeDecodeError:
        print(f"Não foi possivel decodificar o arquivo {caminho}")
    except Exception as e:
        print(f"Ocorreu um erro inesperado {e}")


def generate_question_with_llm(topic: str, level: str) -> str:
    if settings.ENVIRONMENT == "test":
        question = f"Pergunta generica sobre {topic} em um nivel {level}"
        return question
    
    prompt = prompt_reader("prompts/question_generation_system.md")


    try:
        response = client.responses.create(
            model=settings.OPENAI_MODEL,
            instructions=prompt,
            input=f"""
            Topic: {topic}
            level: {level}    
            """,
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




    #-----------------------------RESPOSTA REAL(LLM)-----------------------------

    
    prompt = prompt_reader("prompts/answer_evaluation_system.md")
    
    try:
        response = client.responses.parse(
            model=settings.OPENAI_MODEL,
            instructions=prompt,
            input=f""" 
            Question: {question} 
            Answer: {answer} 
            Level: {level}
            """,
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


