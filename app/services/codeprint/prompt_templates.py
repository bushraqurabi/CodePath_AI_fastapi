def build_dashboard_prompt(signal: dict) -> str:
    """
    Build AI prompt for Gemini/LLM
    """
    weak_topics = ", ".join(signal.get("weak_topics", [])) or "general topics"
    trend = signal.get("trend", "stable")
    return (
        f"Generate actionable advice for a competitive programmer. "
        f"The user is currently {trend} in progress. "
        f"They need to focus on improving: {weak_topics}. "
        f"Provide 3-4 specific steps or exercises, concise, encouraging tone."
    )
