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

def get_topic_strength(handle: str):
    """
    Returns user topic performance.
    For now, randomly generate some values to demo.
    """
    import random

    topics = {}
    for topic in TOPIC_TAGS.keys():
        topics[topic] = {
            "accuracy": random.randint(0, 100),
            "status": "weak" if random.randint(0, 1) else "strong"
        }

    return {"handle": handle, "topics": topics}

def get_default_topics():
    """
    Returns default topics for users with no submissions.
    """
    return get_topic_strength("default_user")
