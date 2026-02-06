from app.services.chatbot.prompt_service import optimize_prompt, build_chat_prompt
from app.core.gemini import get_gemini_response

def get_ai_reply(user_question: str, add_examples: bool = True) -> str:
    """
    Full pipeline: optimize -> build prompt -> call Gemini
    """
    optimized = optimize_prompt(user_question)
    final_prompt = build_chat_prompt(optimized, add_examples=add_examples)
    return get_gemini_response(final_prompt)
