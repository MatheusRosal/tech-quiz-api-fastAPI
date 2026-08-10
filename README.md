# Tech Quiz API

API desenvolvida com FastAPI para geração de perguntas de tecnologia e avaliação de respostas.  
O projeto foi criado como laboratório de estudo para backend, testes automatizados, Docker, Docker Compose e práticas iniciais de DevOps.

Atualmente, a integração com LLM está mockada. Futuramente, o serviço será conectado a uma LLM real para gerar perguntas e avaliar respostas de forma mais inteligente.

## Tecnologias

- Python 3.13
- FastAPI
- Pydantic
- Uvicorn
- Pytest
- Docker
- Docker Compose
- GitHub Actions

## Estrutura do projeto

```text
tech-quiz-api/
├── .github/
│   └── workflows/
│       └── ci.yml
├── core/
│   └── config.py
├── routes/
│   ├── answer_routes.py
│   ├── health_routes.py
│   └── question_routes.py
├── schemas/
│   ├── answer_schema.py
│   └── question_schema.py
├── services/
│   ├── answer_service.py
│   ├── llm_service.py
│   └── question_service.py
├── tests/
│   ├── test_answer_routes.py
│   ├── test_health_routes.py
│   └── test_question_routes.py
├── Dockerfile
├── docker-compose.yml
├── docker-compose.override.yml
├── Makefile
├── requirements.txt
└── main.py
```

## Variáveis de ambiente

Crie um arquivo `.env` na raiz do projeto com:

```env
APP_NAME=Tech Quiz API
APP_VERSION=0.1.0
ENVIRONMENT=development
```

O arquivo `.env` não deve ser versionado nem copiado para a imagem Docker.

## Como rodar localmente

Crie e ative o ambiente virtual:

```bash
python -m venv .venv
source .venv/bin/activate
```

Instale as dependências:

```bash
pip install -r requirements.txt
```

Rode a aplicação:

```bash
uvicorn main:app --reload
```

Acesse:

```text
http://localhost:8000
http://localhost:8000/health
http://localhost:8000/docs
```

## Como rodar com Docker

Build da imagem:

```bash
docker build -t tech-quiz-api .
```

Rodar o container:

```bash
docker run --name tech-quiz-api-container -p 8000:8000 --env-file .env tech-quiz-api
```

Acesse:

```text
http://localhost:8000/docs
```

Para parar e remover:

```bash
docker stop tech-quiz-api-container
docker rm tech-quiz-api-container
```

## Como rodar com Docker Compose

### Ambiente de desenvolvimento

O projeto usa `docker-compose.override.yml` para desenvolvimento, com volume e reload automático.

```bash
docker compose up --build
```

Para derrubar:

```bash
docker compose down
```

### Modo base

Para rodar apenas com o `docker-compose.yml`, sem override:

```bash
docker compose -f docker-compose.yml up --build -d
```

Para derrubar:

```bash
docker compose -f docker-compose.yml down
```

## Comandos com Makefile

O projeto possui um `Makefile` para simplificar comandos comuns.

```bash
make test
```

Roda os testes automatizados.

```bash
make dev
```

Sobe o ambiente de desenvolvimento com Docker Compose, volume e reload.

```bash
make down
```

Derruba o ambiente de desenvolvimento.

```bash
make docker-build
```

Builda a imagem Docker.

```bash
make prod-up
```

Sobe o ambiente base, sem override.

```bash
make prod-down
```

Derruba o ambiente base.

```bash
make ci-local
```

Simula localmente o fluxo principal do CI.

## Endpoints

### Health check

```http
GET /health
```

Resposta esperada:

```json
{
  "status": "ok"
}
```

### Gerar pergunta

```http
POST /questions/generate
```

Body:

```json
{
  "topic": "Docker",
  "level": "beginner"
}
```

Resposta esperada:

```json
{
  "question": "Pergunta genérica sobre Docker em um nível beginner",
  "topic": "Docker",
  "level": "beginner"
}
```

Valores aceitos para `level`:

```text
beginner
intermediate
advanced
```

### Avaliar resposta

```http
POST /answers/evaluate
```

Body:

```json
{
  "question": "Explique o que é Docker.",
  "answer": "Docker é uma tecnologia usada para empacotar aplicações em containers.",
  "level": "beginner"
}
```

Resposta esperada:

```json
{
  "score": 7,
  "feedback": "Boa resposta, mas ainda pode trazer mais detalhes"
}
```

## Testes

Rodar testes localmente:

```bash
pytest -v
```

Ou usando Makefile:

```bash
make test
```

## CI/CD

O projeto possui uma pipeline de CI com GitHub Actions.

A pipeline roda em:

- push para `main`
- pull request para `main`

Fluxo atual da pipeline:

```text
checkout do código
↓
setup do Python
↓
instalação das dependências
↓
criação de .env para testes
↓
execução dos testes com pytest
↓
build da imagem Docker
↓
execução do container com Docker Compose
↓
teste da rota /health
↓
exibição dos logs do container
↓
remoção do container
```

## Docker Healthcheck

O `docker-compose.yml` possui um healthcheck usando a rota:

```text
/health
```

O container é considerado saudável quando a API responde corretamente.

## Próximos passos

- Integrar com uma LLM real
- Melhorar prompts de geração e avaliação
- Adicionar banco de dados PostgreSQL
- Persistir histórico de perguntas e avaliações
- Criar migrations
- Melhorar cobertura de testes
- Preparar deploy em ambiente cloud
