from app.services.codeprint.feature_service import extract_user_features
from app.services.codeprint.topic_service import get_topic_strength
from app.services.codeprint.trend_service import get_monthly_trends


def build_ai_signals(handle: str) -> dict:
    features = extract_user_features(handle)
    topics = get_topic_strength(handle)
    trends = get_monthly_trends(handle)

    weak_topics = [
        t for t, v in topics["topics"].items()
        if v["status"] == "weak"
    ]

    return {
        "handle": handle,
        "weak_topics": weak_topics,
        "trend": trends["timeline"][-1]["trend"],
        "features": features
    }


def get_default_signals(handle: str) -> dict:
    return {
        "handle": handle,
        "weak_topics": ["Dynamic Programming", "Graphs"],
        "trend": "stable"
    }
