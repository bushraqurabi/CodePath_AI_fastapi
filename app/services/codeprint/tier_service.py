def get_user_tier(rating: int) -> str:
    if rating < 1200:
        return "Beginner"
    elif rating < 1600:
        return "Intermediate"
    elif rating < 2000:
        return "Advanced"
    else:
        return "Expert"
