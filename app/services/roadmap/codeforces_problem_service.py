"""Shared Codeforces problem-fetching service used by roadmap and contest.

Bulk-fetches the full Codeforces problem set once and caches it in memory
for 1 hour. Provides helpers to filter by topic tags + rating range.
"""

import random
import time
from typing import Dict, List

import httpx

CF_PROBLEMS_API = "https://codeforces.com/api/problemset.problems"

_cache: Dict = {"problems": [], "timestamp": 0.0}
CACHE_TTL = 3600  # seconds

# Roadmap topic → Codeforces problem tags
TOPIC_TO_CF_TAGS: Dict[str, List[str]] = {
    "Basic Programming": ["implementation", "math"],
    "Arrays": ["implementation", "data structures"],
    "Frequency": ["implementation"],
    "Prefix Sum": ["data structures", "math"],
    "Two Pointers": ["two pointers"],
    "Sliding Window": ["two pointers"],
    "Sorting": ["sorting"],
    "Binary Search": ["binary search"],
    "STL": ["data structures"],
    "Set / Multiset": ["data structures"],
    "Map / Unordered Map": ["data structures"],
    "Hashing": ["hash map"],
    "Math Basics": ["math"],
    "Number Theory": ["number theory", "math"],
    "Math & Geometry": ["geometry", "math"],
    "Greedy Algorithms": ["greedy"],
    "Recursion": ["recursion", "dfs and similar"],
    "Backtracking": ["backtracking"],
    "Trees": ["trees", "dfs and similar"],
    "DFS / BFS": ["dfs and similar", "graphs"],
    "Segment Tree": ["data structures", "segment tree"],
    "Dynamic Programming": ["dp"],
    "DP": ["dp"],
    "Bitmask DP": ["bitmask", "dp"],
    "Graph": ["graphs"],
    "Graphs": ["graphs"],
    "Shortest Paths": ["graphs", "shortest paths"],
    "Advanced Topics": ["math"],
    "Game Theory": ["games"],
    "Advanced Geometry": ["geometry"],
    "Optimization Techniques": ["math", "brute force"],
}


def _make_link(problem: dict) -> str:
    cid = problem.get("contestId", 0)
    idx = problem.get("index", "A")
    return f"https://codeforces.com/problemset/problem/{cid}/{idx}"


async def _fetch_all_problems() -> List[dict]:
    now = time.time()
    if _cache["problems"] and (now - _cache["timestamp"]) < CACHE_TTL:
        return _cache["problems"]

    async with httpx.AsyncClient(timeout=30) as client:
        resp = await client.get(CF_PROBLEMS_API)
        data = resp.json()
        if data.get("status") != "OK":
            return _cache["problems"] or []
        problems = data["result"]["problems"]
        _cache["problems"] = problems
        _cache["timestamp"] = now
        return problems


def _problem_to_out(p: dict) -> dict:
    return {
        "name": p.get("name", ""),
        "contestId": p.get("contestId", 0),
        "index": p.get("index", ""),
        "rating": p.get("rating", 0),
        "tags": p.get("tags", []),
        "link": _make_link(p),
    }


async def get_problems_for_topic(
    topic_title: str,
    min_rating: int,
    max_rating: int,
    limit: int = 5,
) -> List[dict]:
    all_problems = await _fetch_all_problems()
    tags = [t.lower() for t in TOPIC_TO_CF_TAGS.get(topic_title, [])]
    if not tags:
        return []

    candidates = []
    for p in all_problems:
        rating = p.get("rating", 0)
        if rating < min_rating or rating > max_rating:
            continue
        p_tags = [t.lower() for t in p.get("tags", [])]
        if any(t in p_tags for t in tags):
            candidates.append(_problem_to_out(p))

    candidates.sort(key=lambda x: x["rating"])
    return candidates[:limit]


TIER_BASE_RATING: Dict[str, int] = {
    "Beginner": 900,
    "Intermediate": 1300,
    "Advanced": 1700,
    "Expert": 2100,
}


async def get_problems_for_contest(
    tier: str,
    weak_topics: List[str],
    at_level_count: int = 6,
    above_count: int = 3,
    hard_count: int = 3,
) -> List[dict]:
    base = TIER_BASE_RATING.get(tier, 1300)
    all_problems = await _fetch_all_problems()

    tag_filter: set = set()
    for topic in weak_topics:
        for t in TOPIC_TO_CF_TAGS.get(topic, []):
            tag_filter.add(t.lower())

    def matches_tags(p: dict) -> bool:
        if not tag_filter:
            return True
        p_tags = [t.lower() for t in p.get("tags", [])]
        return any(t in p_tags for t in tag_filter)

    buckets = [
        ("at_level", base, base + 200, at_level_count),
        ("above_level", base + 200, base + 400, above_count),
        ("hard", base + 400, base + 800, hard_count),
    ]

    results: List[dict] = []
    for tier_name, lo, hi, count in buckets:
        pool = [
            p for p in all_problems
            if lo <= p.get("rating", 0) <= hi and matches_tags(p)
        ]
        if tier_name == "hard":
            hard_tags = {"dp", "graphs", "data structures", "math", "greedy"}
            icpc = [
                p for p in pool
                if hard_tags & {t.lower() for t in p.get("tags", [])}
            ]
            if len(icpc) >= count:
                pool = icpc

        random.shuffle(pool)
        for p in pool[:count]:
            out = _problem_to_out(p)
            out["difficultyTier"] = tier_name
            results.append(out)

    return results
