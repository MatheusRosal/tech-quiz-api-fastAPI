from fastapi import FastAPI
from routes import health_routes, answer_routes, question_routes
from core.config import settings


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
)


app.include_router(health_routes.router)
app.include_router(answer_routes.router)
app.include_router(question_routes.router)






