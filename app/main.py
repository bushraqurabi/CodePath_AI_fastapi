from fastapi import FastAPI

from app.api.quiz_router import router as quiz_router
from app.api.codeprint_router import router as codeprint_router
from app.api.topic_router import router as topic_router
from app.api.chatbot_router import router as chatbot_router


app = FastAPI(title="CodePath AI API")

app.include_router(quiz_router)
app.include_router(codeprint_router)
app.include_router(topic_router)
app.include_router(chatbot_router)
