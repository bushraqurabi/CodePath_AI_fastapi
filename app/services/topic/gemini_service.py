import os
from dotenv import load_dotenv
from google.genai import Client

load_dotenv()

GEMINI_API_KEY = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise RuntimeError("GOOGLE_API_KEY or GEMINI_API_KEY not found")

client = Client(api_key=GEMINI_API_KEY)
MODEL_NAME = "gemini-2.5-flash"  

async def get_ai_insights(topic_name: str, performance: dict) -> dict:
    """
    Returns AI insights for a topic.
    The 'model' field is removed from output.
    """
    prompt = f"""
You are a competitive programming coach.

Topic: {topic_name}

User performance (JSON):
{performance}

Tasks:
1. Identify weak subskills
2. Suggest learning focus areas
3. Give one concise improvement recommendation
"""
    try:
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt,
        )
        return {
            "insights": response.text
        }

    except Exception as e:
        return {
            "error": "Gemini API failed",
            "details": str(e),
        }
