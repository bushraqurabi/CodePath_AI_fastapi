from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api.quiz_router import router as quiz_router
from app.api.codeprint_router import router as codeprint_router
from app.api.topic_router import router as topic_router
from app.api.chatbot_router import router as chatbot_router
from app.api.roadmap_router import router as roadmap_router
from app.api.contest_router import router as contest_router
from app.api.reference_router import router as reference_router


app = FastAPI(title="CodePath AI API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"success": False, "message": exc.detail, "data": None},
    )


@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"success": False, "message": "Internal Server Error", "data": None},
    )


app.include_router(quiz_router)
app.include_router(codeprint_router)
app.include_router(topic_router)
app.include_router(chatbot_router)
app.include_router(roadmap_router)
app.include_router(contest_router)
app.include_router(reference_router)
