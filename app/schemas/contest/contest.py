from typing import Dict, List, Optional

from pydantic import BaseModel


class ContestTopicInput(BaseModel):
    id: Optional[int] = None
    title: str


class ContestTopicPerformanceInput(BaseModel):
    topic: str
    attempts: Optional[int] = 0
    solved: Optional[int] = 0
    total: Optional[int] = None
    accuracy: Optional[float] = None


class ContestCodeforcesStatsInput(BaseModel):
    rating: Optional[int] = 0
    tier: Optional[str] = None
    topicBreakdown: Optional[List[ContestTopicPerformanceInput]] = []


class ContestProblemCriteriaOut(BaseModel):
    topicId: Optional[int] = None
    topicTitle: str
    suggestedDifficulty: int
    count: int


class ContestProblemOut(BaseModel):
    name: str
    contestId: int
    index: str
    rating: int
    tags: List[str]
    link: str
    difficultyTier: str


class ContestSelectionRequest(BaseModel):
    userId: str
    targetSkillTier: str = "Beginner"
    topics: List[ContestTopicInput] = []
    quizPerformance: List[ContestTopicPerformanceInput] = []
    codeforcesStats: Optional[ContestCodeforcesStatsInput] = None
    totalProblems: int = 12


class ContestSelectionResponse(BaseModel):
    criteria: List[ContestProblemCriteriaOut]
    totalProblems: int
    problems: List[ContestProblemOut] = []
    contestTiming: Optional[Dict[str, str]] = None
