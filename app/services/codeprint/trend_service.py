from datetime import datetime, timedelta
import random

def get_monthly_trends(handle: str):
    """Return last 6 months trends."""
    trends = []
    today = datetime.today()
    for i in range(6):
        month = (today - timedelta(days=i*30)).strftime("%Y-%m")
        trends.append({
            "month": month,
            "problems_solved": random.randint(0, 15),
            "accuracy": round(random.uniform(40, 100), 2),
            "trend": random.choice(["improving", "declining", "stable"])
        })
    trends.reverse()
    return {"handle": handle, "timeline": trends}

def get_daily_activity(handle: str):
    """Return last 30 days dummy activity"""
    daily = []
    today = datetime.today()
    for i in range(30):
        day = (today - timedelta(days=i)).strftime("%Y-%m-%d")
        daily.append({
            "date": day,
            "problems_solved": random.randint(0, 3)
        })
    daily.reverse()
    return daily
