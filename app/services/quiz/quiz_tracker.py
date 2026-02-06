from typing import List, Dict
from app.schemas.quiz.submission import Answer

# In-memory stats (OK for MVP / demo)
_stats = {
    "total": 0,
    "correct": 0,
    "topic_breakdown": {}
}


def reset_stats():
    """Optional: call this when starting a new quiz session"""
    global _stats
    _stats = {
        "total": 0,
        "correct": 0,
        "topic_breakdown": {}
    }


def record_answers(answers: List[Answer], question_map: Dict):
    """
    Records submitted answers safely.
    - Ignores invalid question_id
    - Uses option index comparison
    - Never crashes
    """
    global _stats

    for answer in answers:
        question = question_map.get(answer.question_id)
        if not question:
            continue  # invalid question_id → skip safely

        _stats["total"] += 1

        is_correct = answer.selected_option == question.correct_option

        if is_correct:
            _stats["correct"] += 1

        topic = question.topic

        if topic not in _stats["topic_breakdown"]:
            _stats["topic_breakdown"][topic] = {
                "total": 0,
                "correct": 0
            }

        _stats["topic_breakdown"][topic]["total"] += 1
        if is_correct:
            _stats["topic_breakdown"][topic]["correct"] += 1


def get_stats():
    """
    Returns computed accuracy & topic performance
    """
    if _stats["total"] == 0:
        return {
            "accuracy": 0.0,
            "topic_breakdown": {}
        }

    accuracy = _stats["correct"] / _stats["total"]

    topic_accuracy = {}
    for topic, data in _stats["topic_breakdown"].items():
        topic_accuracy[topic] = (
            data["correct"] / data["total"]
            if data["total"] > 0 else 0.0
        )

    return {
        "accuracy": round(accuracy, 2),
        "topic_breakdown": topic_accuracy
    }
