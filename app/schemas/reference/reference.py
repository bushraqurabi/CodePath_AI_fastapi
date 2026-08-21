from typing import List, Optional

from pydantic import BaseModel


class ReferenceSnippetInput(BaseModel):
    id: str
    title: str
    topicId: Optional[int] = None
    topicTitle: Optional[str] = None
    language: Optional[str] = None
    notesPreview: Optional[str] = None


class ReferencePerformanceInput(BaseModel):
    topic: str
    attempts: Optional[int] = 0
    solved: Optional[int] = 0
    total: Optional[int] = None
    accuracy: Optional[float] = None


class ReferenceCodeforcesStatsInput(BaseModel):
    rating: Optional[int] = 0
    tier: Optional[str] = None
    topicBreakdown: Optional[List[ReferencePerformanceInput]] = []


class ReferenceSectionOut(BaseModel):
    topicId: Optional[int] = None
    topicTitle: str
    intro: str
    snippetIds: List[str]


class ReferenceCurateRequest(BaseModel):
    userId: str
    snippets: List[ReferenceSnippetInput] = []
    quizPerformance: List[ReferencePerformanceInput] = []
    codeforcesStats: Optional[ReferenceCodeforcesStatsInput] = None


class ReferenceCurateResponse(BaseModel):
    sections: List[ReferenceSectionOut]
