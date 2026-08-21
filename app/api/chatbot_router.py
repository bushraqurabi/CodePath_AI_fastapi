from fastapi import APIRouter, HTTPException, Query
from app.core.response import StandardResponse, ok
from app.schemas.chatbot.chat_schemas import ChatRequest, ChatResponse
from app.services.chatbot.chat_service import get_ai_reply
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api", tags=["Chatbot"])

@router.post("/chat", response_model=StandardResponse)
async def chat_endpoint(
    request: ChatRequest,
    add_examples: bool = Query(True, description="Include examples in AI response")
):
    """
    Endpoint to send a question to Gemini AI.
    """
    try:
        logger.info(f"User question: {request.question}")
        reply = get_ai_reply(request.question, add_examples=add_examples)
        logger.info(f"AI reply: {reply}")
        return ok(ChatResponse(reply=reply))
    except Exception as e:
        logger.exception("Chatbot error")
        raise HTTPException(status_code=500, detail=str(e))
