from pydantic import BaseModel

class TopicResponse(BaseModel):
    topic: str
    accuracy: float
    level: str
    accepted: int
    wrong: int
