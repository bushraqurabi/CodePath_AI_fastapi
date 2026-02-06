import logging

logger = logging.getLogger(__name__)

def generate_message(signal: dict) -> str:
    """
    Converts signals into human-friendly AI message.
    """
    weak = ", ".join(signal.get("weak_topics", [])) or "your weak areas"
    trend = signal.get("trend", "stable")

    return (
        f"You are currently {trend} in your progress. "
        f"Focus on improving {weak} to keep moving forward. "
        f"Consistency is key — keep practicing! "
        f"Try solving 20–30 problems in your weak topics to level up faster."
    )
