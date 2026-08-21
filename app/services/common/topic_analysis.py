"""Shared deterministic topic analysis used by the roadmap, contest and
reference services.

The canonical topic structure mirrors "Roadmap - CodePath.json" (the CodePath
tree roadmap).  The ordering below is the tree flattened depth-first so that a
parent always precedes its children, which lets downstream code respect
prerequisite structure (e.g. Arrays before Sorting before Binary Search, DP
after Recursion, etc.) while ranking weaknesses.
"""

from typing import Dict, List, Optional

# Depth-first pre-order flattening of the CodePath tree roadmap.
# Topics not present here get a default rank at the end.
CANONICAL_TOPIC_ORDER: List[str] = [
    "Basic Programming",
    "Arrays",
    "Frequency",
    "Prefix Sum",
    "Two Pointers",
    "Sliding Window",
    "Sorting",
    "Binary Search",
    "STL",
    "Set / Multiset",
    "Map / Unordered Map",
    "Hashing",
    "Math Basics",
    "Number Theory",
    "Math & Geometry",
    "Greedy Algorithms",
    "Recursion",
    "Backtracking",
    "Trees",
    "DFS / BFS",
    "Segment Tree",
    "Dynamic Programming",
    "DP",
    "Bitmask DP",
    "Graph",
    "Graphs",
    "Shortest Paths",
    "Advanced Topics",
    "Game Theory",
    "Advanced Geometry",
    "Optimization Techniques",
]

# Alias names -> canonical entry so different labels resolve to one rank.
TOPIC_ALIASES: Dict[str, str] = {
    "greedy": "Greedy Algorithms",
    "greedy algorithms": "Greedy Algorithms",
    "recursion & backtracking": "Recursion",
    "dfs / bfs": "DFS / BFS",
    "segment tree": "Segment Tree",
    "dynamic programming": "Dynamic Programming",
    "dp": "Dynamic Programming",
    "bitmask dp": "Bitmask DP",
    "graph": "Graph",
    "graphs": "Graphs",
    "graph theory": "Graphs",
    "math basics": "Math Basics",
    "number theory": "Number Theory",
    "math & geometry": "Math & Geometry",
    "game theory": "Game Theory",
    "advanced geometry": "Advanced Geometry",
    "arrays": "Arrays",
    "prefix sum": "Prefix Sum",
    "two pointers": "Two Pointers",
    "sliding window": "Sliding Window",
    "sorting": "Sorting",
    "binary search": "Binary Search",
    "stl": "STL",
    "set": "Set / Multiset",
    "hashing": "Hashing",
    "backtracking": "Backtracking",
    "trees": "Trees",
}

_TOPIC_RANK: Dict[str, int] = {
    title: idx for idx, title in enumerate(CANONICAL_TOPIC_ORDER)
}

# Default rank assigned to topics outside the canonical tree.
DEFAULT_TOPIC_RANK = len(CANONICAL_TOPIC_ORDER)


def normalize_topic_title(title: str) -> str:
    """Return the canonical title for a topic (case-insensitive) or the raw title."""
    key = (title or "").strip().lower()
    canonical = TOPIC_ALIASES.get(key, key)
    return canonical


def prereq_rank(title: str) -> int:
    canonical = normalize_topic_title(title)
    return _TOPIC_RANK.get(canonical, DEFAULT_TOPIC_RANK)


# Difficulty tiers used only to pick sensible *starting* targets for topics
# that have no performance data at all.
TIER_BASE_RATING: Dict[str, int] = {
    "Beginner": 900,
    "Intermediate": 1300,
    "Advanced": 1700,
    "Expert": 2100,
    "Master": 2400,
}

# Advanced topics that deserve a slightly higher difficulty bump.
ADVANCED_TOPIC_NAMES = {
    "Dynamic Programming",
    "DP",
    "Bitmask DP",
    "Segment Tree",
    "Graph",
    "Graphs",
    "Shortest Paths",
    "Number Theory",
    "Game Theory",
    "Advanced Geometry",
    "Optimization Techniques",
}


def tier_base_rating(tier: Optional[str]) -> int:
    if not tier:
        return 1300
    for key, value in TIER_BASE_RATING.items():
        if key.lower() == tier.strip().lower():
            return value
    # Guess the rating from an arbitrary numeric string like "1500"
    try:
        return int(str(tier).strip())
    except ValueError:
        return 1300


def resolve_difficulty_range(topic: str, tier: Optional[str]) -> Dict[str, int]:
    """Deterministic difficulty suggestion for a topic based on the tier."""
    base = tier_base_rating(tier)
    bump = 200 if normalize_topic_title(topic) in ADVANCED_TOPIC_NAMES else 0
    low = base + bump
    return {"min": low, "max": low + 400}


def compute_weakness_scores(
    topics: List[Dict],
    quiz_performance: Optional[List[Dict]] = None,
    codeforces_stats: Optional[Dict] = None,
    default_weakness: Optional[float] = None,
) -> Dict[str, Dict]:
    """Compute a deterministic 0-100 weakness score per topic title.

    Topics with real performance data are scored from their accuracy (lower
    accuracy => weaker) combined with a small penalty for very few attempts.
    Topics with no data fall back to `default_weakness` (or 50).
    """
    quiz_by_topic: Dict[str, Dict] = {}
    for item in quiz_performance or []:
        title = normalize_topic_title(str(item.get("topic", "")))
        accuracy = _to_float(item.get("accuracy"))
        attempts = _to_int(item.get("attempts"))
        if accuracy is None:
            solved = _to_int(item.get("solved"))
            total = _to_int(item.get("total"))
            accuracy = round((solved / total) * 100, 2) if total else None
        quiz_by_topic[title] = {"accuracy": accuracy, "attempts": attempts}

    cf_by_topic: Dict[str, Dict] = {}
    stats = codeforces_stats or {}
    for item in (stats.get("topicBreakdown") or []):
        title = normalize_topic_title(str(item.get("topic", "")))
        accuracy = _to_float(item.get("accuracy"))
        attempts = _to_int(item.get("attempts"))
        if accuracy is None:
            solved = _to_int(item.get("solved"))
            total = _to_int(item.get("total"))
            accuracy = round((solved / total) * 100, 2) if total else None
        cf_by_topic[title] = {"accuracy": accuracy, "attempts": attempts}

    scores: Dict[str, Dict] = {}
    for topic in topics or []:
        title = normalize_topic_title(str(topic.get("title", "")))
        if not title:
            continue

        source_scores: List[float] = []
        for source in (quiz_by_topic.get(title), cf_by_topic.get(title)):
            if source and source["accuracy"] is not None:
                base_weakness = 100.0 - source["accuracy"]
                attempts = source["attempts"] or 0
                # Very few attempts => slightly less certain, nudge weaker.
                certainty_penalty = max(0.0, 10.0 - min(attempts, 10.0))
                source_scores.append(base_weakness + certainty_penalty)

        if source_scores:
            weakness = sum(source_scores) / len(source_scores)
        else:
            weakness = default_weakness if default_weakness is not None else 50.0

        weakness = max(0.0, min(100.0, weakness))
        scores[title] = {
            "originalTitle": str(topic.get("title", title)),
            "weakness": round(weakness, 2),
        }

    return scores


def order_topics_by_weakness(
    topics: List[Dict],
    weakness_scores: Optional[Dict[str, Dict]] = None,
    limit: Optional[int] = None,
) -> List[Dict]:
    """Order topics weakest-first while respecting prerequisite structure.

    Primary sort key is the prerequisite rank (parents before children), then
    weakness descending so that the weakest topic of each stage leads the path.
    """
    if weakness_scores is None:
        weakness_scores = compute_weakness_scores(topics)

    ordered = sorted(
        topics or [],
        key=lambda t: (prereq_rank(str(t.get("title", ""))),
                       -weakness_scores.get(
                           normalize_topic_title(str(t.get("title", ""))), {}
                       ).get("weakness", 50.0)),
    )

    if limit and limit > 0:
        ordered = ordered[:limit]

    return ordered


def _to_float(value) -> Optional[float]:
    if value is None:
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _to_int(value) -> int:
    if value is None:
        return 0
    try:
        return int(value)
    except (TypeError, ValueError):
        return 0
