from fastapi import FastAPI
from routes import health_routes, answer_routes, question_routes


app = FastAPI()

app.include_router(health_routes.router)
app.include_router(answer_routes.router)
app.include_router(question_routes.router)






