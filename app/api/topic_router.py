from fastapi import APIRouter, HTTPException
from app.schemas.topic.topic_response import TopicResponse
from app.schemas.topic.topic_ai_summary import TopicAISummaryResponse
from app.services.topic.codeforces_service import get_user_submissions, filter_problems_by_topic
from app.services.topic.analytics_service import compute_accuracy, classify_level, compute_subskill_performance
from app.services.topic.gemini_service import get_ai_insights

router = APIRouter(
    prefix="/topic",
    tags=["Topic Intelligence"]
)

# ================== Topics → Tags ==================
TOPIC_TAGS = {
    "Arrays": ["arrays", "implementation"],
    "Prefix Sum": ["prefix sums"],
    "Two Pointers": ["two pointers", "sliding window"],
    "Sorting": ["sorting", "binary search"],
    "Binary Search": ["binary search"],
    "STL": ["data structures", "set", "map", "hashing"],
    "Math Basics": ["math", "number theory", "geometry"],
    "Greedy Algorithms": ["greedy"],
    "Recursion & Backtracking": ["backtracking", "recursion"],
    "Trees": ["trees", "dfs", "bfs"],
    "Segment Tree": ["segment tree", "fenwick tree"],
    "Dynamic Programming": ["dynamic programming", "dp", "bitmask"],
    "Graphs": ["graph", "dfs", "bfs", "shortest paths", "dijkstra", "bellman-ford", "minimum spanning tree"],
    "Game Theory": ["games", "nim", "sprague-grundy"],
    "Advanced Geometry": ["geometry", "computational geometry"]
}

# ================== Subskills for AI ==================
TOPIC_SUBSKILLS = {
    "Dynamic Programming": {
        "1D DP": ["dynamic programming"],
        "2D DP": ["dynamic programming"],
        "DP on Trees": ["trees", "dynamic programming"],
        "Bitmask DP": ["bitmask"]
    },
    "Graphs": {
        "Traversal (BFS/DFS)": ["bfs", "dfs"],
        "Shortest Paths": ["dijkstra", "bellman-ford"],
        "MST": ["minimum spanning tree"],
        "Graph DP": ["dynamic programming", "graph"]
    },
    "Trees": {
        "DFS / BFS": ["dfs", "bfs"],
        "Segment Tree": ["segment tree", "fenwick tree"]
    },
    "Greedy Algorithms": {
        "Basic Greedy": ["greedy"],
        "Sorting Greedy": ["sorting"]
    },
    "Game Theory": {
        "Impartial Games": ["nim", "sprague-grundy"],
        "Game DP": ["games", "dynamic programming"]
    }
}

# ================== Helper for case-insensitive matching ==================
def match_topic(input_name: str, topic_dict: dict):
    """Return the key from topic_dict that matches input_name case-insensitively."""
    input_name_clean = input_name.strip().lower()
    for key in topic_dict:
        if key.lower() == input_name_clean:
            return key
    return None

# ================== Topic Overview ==================
@router.get("/{topic_name}", response_model=TopicResponse)
async def get_topic_overview(topic_name: str, user_handle: str):
    matched_topic = match_topic(topic_name, TOPIC_TAGS)
    if not matched_topic:
        raise HTTPException(status_code=404, detail="Unknown topic")

    tags = TOPIC_TAGS[matched_topic]
    submissions = await get_user_submissions(user_handle)
    topic_subs = filter_problems_by_topic(submissions, tags)

    accepted = sum(1 for s in topic_subs if s.get("verdict") == "OK")
    wrong = sum(1 for s in topic_subs if s.get("verdict") not in ("OK", None))
    total = accepted + wrong

    accuracy = compute_accuracy(accepted, total)
    level = classify_level(accuracy)

    return TopicResponse(
        topic=matched_topic,
        accuracy=accuracy,
        level=level,
        accepted=accepted,
        wrong=wrong
    )

# ================== Topic AI Summary ==================
@router.get("/{topic_name}/ai-summary", response_model=TopicAISummaryResponse)
async def topic_ai_summary(topic_name: str, user_handle: str):
    matched_topic = match_topic(topic_name, TOPIC_SUBSKILLS)
    if not matched_topic:
        raise HTTPException(status_code=404, detail="AI analysis not available for this topic")

    subskills = TOPIC_SUBSKILLS[matched_topic]
    submissions = await get_user_submissions(user_handle)
    performance = compute_subskill_performance(submissions=submissions, subskill_tags=subskills)
    ai_insights = await get_ai_insights(matched_topic, performance)

    return TopicAISummaryResponse(
        topic=matched_topic,
        performance=performance,
        ai_insights=ai_insights
    )
