from fastapi import APIRouter, HTTPException

from app.services.codeprint import (
    codeforces_service,
    tier_service,
    topic_service,
    ai_signal_service,
    gemini_service,
)

from app.schemas.codeprint.dashboard import (
    UserDashboard,
    RadarResponse,
    AIInsightResponse,
)

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


@router.get("/user/{handle}", response_model=UserDashboard)
def get_user_info(handle: str):
    """
    Returns user info + tier for a given Codeforces handle.
    """
    user = codeforces_service.get_user_info(handle)
    if not user:
        raise HTTPException(status_code=404, detail="User not found on Codeforces")

    tier = tier_service.get_user_tier(user["rating"])

    return {
        "handle": user["handle"],
        "rating": user["rating"],
        "tier": tier,
        "rank": user["rank"],
        "maxRating": user["maxRating"],
        "maxRank": user["maxRank"],
    }


@router.get("/radar/{handle}", response_model=RadarResponse)
def get_radar_chart(handle: str):
    """
    Returns top 6 topic strengths for the user.
    """
    topics = topic_service.get_topic_strength(handle)
    if not topics:
        topics = topic_service.get_default_topics()

    topic_scores = {
        k: v["accuracy"] for k, v in topics["topics"].items()
    }

    top_topics = dict(
        sorted(topic_scores.items(), key=lambda x: x[1], reverse=True)[:6]
    )

    return {
        "handle": handle,
        "top_topics": top_topics,
    }


@router.get("/ai/{handle}", response_model=AIInsightResponse)
def get_ai_insight(handle: str):
    """
    Returns AI insights for the user.
    """
    signals = ai_signal_service.build_ai_signals(handle)
    if not signals:
        signals = ai_signal_service.get_default_signals(handle)

    message = gemini_service.generate_message(signals)

    return {
        "handle": handle,
        "ai_insight": message,
    }
