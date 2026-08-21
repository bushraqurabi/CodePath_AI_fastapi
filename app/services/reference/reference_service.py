"""Reference library curation.

Groups the user's saved solution snippets into study sections, orders the
sections by the user's weakest topics first, and writes a short personalised
intro for each section (Gemini, validated with Pydantic, deterministic
fallback on any LLM failure).
"""

import json
import re
from typing import Dict, List

from pydantic import BaseModel

from app.core.gemini import get_gemini_response
from app.schemas.reference.reference import (
    ReferenceCurateRequest,
    ReferenceCurateResponse,
    ReferenceSectionOut,
)
from app.services.common.topic_analysis import (
    compute_weakness_scores,
    order_topics_by_weakness,
)


class _GeminiSection(BaseModel):
    topicTitle: str
    intro: str
    snippetIds: List[str] = []


class _GeminiCurated(BaseModel):
    sections: List[_GeminiSection] = []


_UNCATEGORIZED = "Uncategorized"


def _group_snippets(request: ReferenceCurateRequest) -> List[Dict]:
    groups: Dict[str, Dict] = {}
    for snippet in request.snippets:
        title = (snippet.topicTitle or _UNCATEGORIZED).strip() or _UNCATEGORIZED
        group = groups.setdefault(
            title, {"topicId": snippet.topicId, "topicTitle": title, "snippetIds": []}
        )
        if group.get("topicId") is None and snippet.topicId is not None:
            group["topicId"] = snippet.topicId
        group["snippetIds"].append(snippet.id)
    return list(groups.values())


def _templated_intros(groups: List[Dict]) -> List[ReferenceSectionOut]:
    sections: List[ReferenceSectionOut] = []
    for idx, group in enumerate(groups):
        topic = group["topicTitle"]
        count = len(group["snippetIds"])
        sections.append(
            ReferenceSectionOut(
                topicId=group.get("topicId"),
                topicTitle=topic,
                intro=(
                    f"This section gathers the {count} solution(s) you saved for "
                    f"{topic}. Review them before contests to refresh the key ideas, "
                    "then re-solve a few without notes."
                ),
                snippetIds=group["snippetIds"],
            )
        )
    return sections


def _extract_json(text: str) -> dict:
    if not text:
        raise ValueError("empty Gemini response")
    cleaned = re.sub(r"```(?:json)?", "", text).strip()
    match = re.search(r"\{.*\}", cleaned, re.DOTALL)
    if not match:
        raise ValueError("no JSON object found")
    return json.loads(match.group(0))


def curate_reference(request: ReferenceCurateRequest) -> ReferenceCurateResponse:
    if not request.snippets:
        return ReferenceCurateResponse(sections=[])

    groups = _group_snippets(request)

    # Order groups weakest-first using whatever performance data we have.
    weakness_input = [{"title": g["topicTitle"]} for g in groups]
    weakness = compute_weakness_scores(
        weakness_input,
        quiz_performance=request.quizPerformance
        and [p.model_dump() for p in request.quizPerformance],
        codeforces_stats=request.codeforcesStats
        and request.codeforcesStats.model_dump(),
    )
    ordered_groups = order_topics_by_weakness(weakness_input, weakness, limit=None)

    ordered_groups = [
        next(g for g in groups if g["topicTitle"] == og["title"]) for og in ordered_groups
    ]

    try:
        sections = _gemini_intros(ordered_groups)
    except Exception:
        sections = _templated_intros(ordered_groups)

    return ReferenceCurateResponse(sections=sections)


def _gemini_intros(groups: List[Dict]) -> List[ReferenceSectionOut]:
    payload = [
        {"topicTitle": g["topicTitle"], "snippetIds": g["snippetIds"]} for g in groups
    ]
    prompt = f"""You are a competitive programming coach curating a personal reference library.

TASK: For each topic section below write a warm, practical 2-3 sentence intro that tells the user what this section is useful for right before a contest. Tie the intro to the number of snippets (e.g. "review these N solutions") and to the specific topic.

SECTIONS:
{json.dumps(payload, indent=2)}

Return STRICT JSON only, no markdown fences:
{{"sections":[{{"topicTitle": string (exact match from input), "intro": string, "snippetIds": [string]}}]}}"""

    raw = get_gemini_response(prompt)
    data = _GeminiCurated.model_validate(_extract_json(raw))

    by_title = {g["topicTitle"]: g for g in groups}
    sections: List[ReferenceSectionOut] = []
    for s in data.sections:
        group = by_title.get(s.topicTitle)
        if group is None:
            continue
        sections.append(
            ReferenceSectionOut(
                topicId=group.get("topicId"),
                topicTitle=group["topicTitle"],
                intro=s.intro,
                snippetIds=group["snippetIds"],
            )
        )

    # Any groups Gemini silently dropped keep a templated intro.
    covered = {s.topicTitle for s in sections}
    for group in groups:
        if group["topicTitle"] not in covered:
            sections.append(
                _templated_intros([group])[0]
            )

    return sections
