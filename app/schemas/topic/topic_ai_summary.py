from pydantic import BaseModel
from typing import Dict, Any

class TopicAISummaryResponse(BaseModel):
    topic: str
    performance: Dict[str, Any] 
    ai_insights: Dict[str, Any]  
