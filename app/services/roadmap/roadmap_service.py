"""Personalised roadmap generation.

The pipeline is:

1. Deterministic weakness scoring + prerequisite-aware ordering (weakest-first
   while respecting the CodePath tree roadmap) using *only* the performance
   data supplied by the backend.
2. A single strict-JSON Gemini call that picks the topics to include and adds
   the learning objectives.  The output is validated with Pydantic.
3. A fully deterministic fallback that mirrors the same schema, so the route
   never fails on LLM instability.
"""

import json
import re
from typing import Dict, List

from app.core.gemini import get_gemini_response
from app.schemas.roadmap.roadmap import (
    RoadmapGenerateRequest,
    RoadmapGenerateResponse,
    RoadmapModuleOut,
)
from app.services.common.topic_analysis import (
    compute_weakness_scores,
    order_topics_by_weakness,
    resolve_difficulty_range,
)
from app.services.roadmap.codeforces_problem_service import get_problems_for_topic

from pydantic import BaseModel

MAX_ROADMAP_TOPICS = 12


class _GeminiDifficulty(BaseModel):
    min: int
    max: int


class _GeminiTopic(BaseModel):
    topic: str
    include: bool = True
    order: int = 0
    learningObjective: str = ""
    estimatedHours: int = 6
    suggestedDifficultyRange: _GeminiDifficulty = _GeminiDifficulty(min=1000, max=1400)


class _GeminiRoadmap(BaseModel):
    topics: List[_GeminiTopic] = []


# Deterministic estimates used for the fallback and as hints to Gemini.
ESTIMATED_HOURS: Dict[str, int] = {
    "Arrays": 4,
    "Frequency": 4,
    "Prefix Sum": 4,
    "Two Pointers": 5,
    "Sliding Window": 5,
    "Sorting": 5,
    "Binary Search": 6,
    "STL": 4,
    "Set / Multiset": 4,
    "Map / Unordered Map": 4,
    "Hashing": 5,
    "Math Basics": 6,
    "Number Theory": 8,
    "Math & Geometry": 6,
    "Greedy Algorithms": 6,
    "Recursion": 5,
    "Backtracking": 6,
    "Trees": 6,
    "DFS / BFS": 6,
    "Segment Tree": 10,
    "Dynamic Programming": 10,
    "DP": 10,
    "Bitmask DP": 12,
    "Graph": 8,
    "Graphs": 8,
    "Shortest Paths": 8,
    "Game Theory": 8,
    "Advanced Geometry": 8,
    "Optimization Techniques": 8,
}

DEFAULT_HOURS = 6

# Empty-object defaults so Pydantic field defaults don't get evaluated eagerly.
def _default_range() -> dict:
    return {"min": 1000, "max": 1400}


def _hours_for(title: str) -> int:
    return ESTIMATED_HOURS.get(title, DEFAULT_HOURS)


def _topic_title_for(module: _GeminiTopic) -> str:
    return module.topic.strip()


def _build_deterministic_modules(
    request: RoadmapGenerateRequest,
) -> List[RoadmapModuleOut]:
    topics = [t.model_dump() for t in request.topics]
    weakness = compute_weakness_scores(
        topics,
        quiz_performance=request.quizPerformance
        and [p.model_dump() for p in request.quizPerformance],
        codeforces_stats=request.codeforcesStats
        and request.codeforcesStats.model_dump(),
    )
    tier = (request.codeforcesStats.tier if request.codeforcesStats else None) or "Beginner"

    ordered = order_topics_by_weakness(topics, weakness, limit=MAX_ROADMAP_TOPICS)

    modules: List[RoadmapModuleOut] = []
    for idx, topic in enumerate(ordered):
        title = topic["title"]
        modules.append(
            RoadmapModuleOut(
                order=idx,
                topicId=topic.get("id"),
                topicTitle=title,
                learningObjective=(
                    f"Master the fundamentals of {title} and apply them to "
                    "competitive programming problems."
                ),
                estimatedHours=_hours_for(title),
                suggestedDifficultyRange=resolve_difficulty_range(
                    title, tier
                ),
            )
        )
    return modules


def _extract_json(text: str) -> dict:
    """Strip markdown fences and return the first JSON object in `text`."""
    if not text:
        raise ValueError("empty Gemini response")
    cleaned = re.sub(r"```(?:json)?", "", text).strip()
    match = re.search(r"\{.*\}", cleaned, re.DOTALL)
    if not match:
        raise ValueError("no JSON object found")
    return json.loads(match.group(0))


def _gemini_modules(request: RoadmapGenerateRequest) -> List[RoadmapModuleOut]:
    topics = [t.model_dump() for t in request.topics]
    weakness = compute_weakness_scores(
        topics,
        quiz_performance=request.quizPerformance
        and [p.model_dump() for p in request.quizPerformance],
        codeforces_stats=request.codeforcesStats
        and request.codeforcesStats.model_dump(),
    )
    tier = (request.codeforcesStats.tier if request.codeforcesStats else None) or "Beginner"

    ordered = order_topics_by_weakness(topics, weakness, limit=None)

    topic_payload = []
    for topic in ordered:
        title = topic["title"]
        w = weakness.get(title, {}).get("weakness", 50.0)
        topic_payload.append(
            {
                "topicId": topic.get("id"),
                "topic": title,
                "weaknessScore": round(w, 2),
                "estimatedHours": _hours_for(title),
                "suggestedDifficultyRange": resolve_difficulty_range(title, tier),
            }
        )

    prompt = f"""You are an expert competitive programming coach.

TASK: Design a personal study roadmap for a CodePath user. Select between 6 and {MAX_ROADMAP_TOPICS} topics from the list below and order them so the user learns prerequisites before harder material. The user's weaker topics should appear as early as is consistent with that order.

USER CONTEXT
- Skill tier: {tier}
- Topics with weakness scores (0 = strongest, 100 = weakest):

{json.dumps(topic_payload, indent=2)}

RULES
- Return STRICT JSON only, no prose, no markdown fences.
- Include the exact topic title strings from the input.
- "include": true only for topics the user should study now. Prefer the weakest topics (highest weaknessScore) that are not blocked by missing prerequisites.
- "order" must be a unique 0-based integer matching the final study order (prerequisites first).
- Keep "learningObjective" to one clear, concrete sentence.
- "estimatedHours" should be the total study hours for the topic.
- "suggestedDifficultyRange" should be Codeforces rating brackets appropriate for a {tier} tier learner, roughly aligned with the suggestedDifficultyRange hints.

JSON schema:
{{"topics":[{{"topic": string, "include": bool, "order": int, "learningObjective": string, "estimatedHours": int, "suggestedDifficultyRange": {{"min": int, "max": int}}}}]}}"""

    raw = get_gemini_response(prompt)
    payload = _extract_json(raw)
    gemini = _GeminiRoadmap.model_validate(payload)

    id_by_title: Dict[str, int] = {}
    for topic in topics:
        id_by_title[topic["title"]] = topic.get("id")

    picked = sorted(
        (t for t in gemini.topics if t.include),
        key=lambda t: (t.order, prereq_rank_of(t.topic)),
    )
    if not picked:
        raise ValueError("Gemini selected no topics")

    modules: List[RoadmapModuleOut] = []
    for idx, t in enumerate(picked):
        modules.append(
            RoadmapModuleOut(
                order=idx,
                topicId=id_by_title.get(t.topic, next(
                    (topic.get("id") for topic in topics
                     if topic["title"].lower() == t.topic.lower()), None)),
                topicTitle=t.topic,
                learningObjective=t.learningObjective,
                estimatedHours=t.estimatedHours,
                suggestedDifficultyRange=t.suggestedDifficultyRange,
            )
        )
    return modules


def prereq_rank_of(title: str) -> int:
    from app.services.common.topic_analysis import prereq_rank

    return prereq_rank(title)


async def _attach_practice_problems(
    modules: List[RoadmapModuleOut],
    tier: str,
) -> List[RoadmapModuleOut]:
    for module in modules:
        dr = module.suggestedDifficultyRange
        try:
            problems = await get_problems_for_topic(
                module.topicTitle, dr.min, dr.max, limit=5,
            )
            module.practiceProblems = problems
        except Exception:
            module.practiceProblems = []
    return modules


async def generate_roadmap(request: RoadmapGenerateRequest) -> RoadmapGenerateResponse:
    if not request.topics:
        return RoadmapGenerateResponse(modules=[])

    tier = (request.codeforcesStats.tier if request.codeforcesStats else None) or "Beginner"

    try:
        modules = _gemini_modules(request)
    except Exception:
        modules = _build_deterministic_modules(request)

    modules = await _attach_practice_problems(modules, tier)

    return RoadmapGenerateResponse(modules=modules)
