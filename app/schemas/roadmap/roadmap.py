from typing import List, Optional

from pydantic import BaseModel


class TopicInput(BaseModel):
    id: Optional[int] = None
    title: str


class SkillAssessmentInput(BaseModel):
    assessmentType: Optional[str] = None
    score: Optional[float] = 0
    skillLevelId: Optional[int] = None


class TopicPerformanceInput(BaseModel):
    topic: str
    attempts: Optional[int] = 0
    solved: Optional[int] = 0
    total: Optional[int] = None
    accuracy: Optional[float] = None


class CodeforcesStatsInput(BaseModel):
    rating: Optional[int] = 0
    tier: Optional[str] = None
    problemsSolved: Optional[int] = 0
    accuracy: Optional[float] = None
    topicBreakdown: Optional[List[TopicPerformanceInput]] = []


class DifficultyRange(BaseModel):
    min: int
    max: int


class PracticeProblemOut(BaseModel):
    name: str
    contestId: int
    index: str
    rating: int
    tags: List[str]
    link: str


class RoadmapModuleOut(BaseModel):
    order: int
    topicId: Optional[int] = None
    topicTitle: str
    learningObjective: str
    estimatedHours: int
    suggestedDifficultyRange: DifficultyRange
    practiceProblems: List[PracticeProblemOut] = []


class RoadmapGenerateRequest(BaseModel):
    userId: str
    topics: List[TopicInput] = []
    skillAssessments: List[SkillAssessmentInput] = []
    quizPerformance: List[TopicPerformanceInput] = []
    codeforcesStats: Optional[CodeforcesStatsInput] = None


class RoadmapGenerateResponse(BaseModel):
    modules: List[RoadmapModuleOut]
