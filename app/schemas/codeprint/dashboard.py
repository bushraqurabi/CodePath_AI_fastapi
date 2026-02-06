from pydantic import BaseModel
from typing import Dict


class UserDashboard(BaseModel):
    handle: str
    rating: int
    tier: str
    rank: str | None = None
    maxRating: int | None = None
    maxRank: str | None = None


class RadarResponse(BaseModel):
    handle: str
    top_topics: Dict[str, int]


class AIInsightResponse(BaseModel):
    handle: str
    ai_insight: str
