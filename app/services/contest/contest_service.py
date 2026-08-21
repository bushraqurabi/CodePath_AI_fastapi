"""Contest problem selection.

Picks the topics a contest should target based on the user's weakest areas,
fetches 12 real Codeforces problems (6 at level, 3 above, 3 hard), and
returns them as a virtual contest with start/end times.
"""

from datetime import datetime, timedelta
from typing import List

from app.schemas.contest.contest import (
    ContestProblemCriteriaOut,
    ContestSelectionRequest,
    ContestSelectionResponse,
)
from app.services.common.topic_analysis import (
    compute_weakness_scores,
    order_topics_by_weakness,
    tier_base_rating,
)
from app.services.roadmap.codeforces_problem_service import get_problems_for_contest

DEFAULT_TOTAL_PROBLEMS = 12
MAX_FOCUS_TOPICS = 6
DIFFICULTY_STEP = 100
CONTEST_DURATION_MINUTES = 300


async def select_contest_problems(
    request: ContestSelectionRequest,
) -> ContestSelectionResponse:
    total = request.totalProblems if request.totalProblems > 0 else DEFAULT_TOTAL_PROBLEMS

    if not request.topics:
        return ContestSelectionResponse(criteria=[], totalProblems=total)

    topics = [t.model_dump() for t in request.topics]
    weakness = compute_weakness_scores(
        topics,
        quiz_performance=request.quizPerformance
        and [p.model_dump() for p in request.quizPerformance],
        codeforces_stats=request.codeforcesStats
        and request.codeforcesStats.model_dump(),
    )

    ordered = order_topics_by_weakness(topics, weakness)
    focus = ordered[: min(MAX_FOCUS_TOPICS, len(ordered))]

    weights: List[float] = []
    for topic in focus:
        title = topic["title"]
        weights.append(weakness.get(title, {}).get("weakness", 50.0))

    weight_sum = sum(weights) or 1.0

    base = tier_base_rating(request.targetSkillTier) - 200

    criteria: List[ContestProblemCriteriaOut] = []
    allocated = 0
    for idx, topic in enumerate(focus):
        if idx == len(focus) - 1:
            count = total - allocated
        else:
            count = max(1, round(total * (weights[idx] / weight_sum)))
        allocated += count
        if count <= 0:
            continue
        suggested = max(400, base + idx * DIFFICULTY_STEP)
        criteria.append(
            ContestProblemCriteriaOut(
                topicId=topic.get("id"),
                topicTitle=topic["title"],
                suggestedDifficulty=suggested,
                count=count,
            )
        )

    tier = request.targetSkillTier or "Beginner"
    weak_topics = [t["title"] for t in focus]

    problems = await get_problems_for_contest(
        tier=tier,
        weak_topics=weak_topics,
        at_level_count=6,
        above_count=3,
        hard_count=3,
    )

    now = datetime.utcnow()
    end = now + timedelta(minutes=CONTEST_DURATION_MINUTES)

    return ContestSelectionResponse(
        criteria=criteria,
        totalProblems=total,
        problems=problems,
        contestTiming={
            "startTime": now.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "endTime": end.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "durationMinutes": str(CONTEST_DURATION_MINUTES),
        },
    )
