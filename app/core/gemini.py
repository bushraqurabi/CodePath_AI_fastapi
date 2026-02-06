from google.genai import Client   
from app.core.config import settings

client = Client(api_key=settings.gemini_api_key)
GEMINI_MODEL = settings.gemini_model

def get_gemini_response(prompt: str) -> str:
    """
    Send a prompt to Gemini model using chats API.
    """
    chat = client.chats.create(model=GEMINI_MODEL)
    response = chat.send_message(prompt)
    return response.text
