def classify_level(accuracy: float) -> str:
    """
    Classifies user level based on quiz accuracy
    """
    if accuracy < 0.4:
        return "Beginner"
    elif accuracy < 0.7:
        return "Intermediate"
    else:
        return "Advanced"


def ai_insight(topic_breakdown: dict) -> str:
    """
    Generates a human-readable AI feedback message
    """
    if not topic_breakdown:
        return "No performance data yet. Try answering more questions."

    weak_topics = [
        topic for topic, score in topic_breakdown.items()
        if score < 0.5
    ]

    strong_topics = [
        topic for topic, score in topic_breakdown.items()
        if score >= 0.8
    ]

    if weak_topics:
        return f"You should focus more on: {', '.join(weak_topics)}."

    if strong_topics:
        return f"Great job! You're strong in: {', '.join(strong_topics)}."

    return "Nice progress! Keep practicing to improve consistency."
