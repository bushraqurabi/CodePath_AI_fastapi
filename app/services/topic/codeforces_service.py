import httpx

CODEFORCES_API = "https://codeforces.com/api/user.status"

async def get_user_submissions(handle: str) -> list:
    async with httpx.AsyncClient() as client:
        response = await client.get(CODEFORCES_API, params={"handle": handle})
        data = response.json()
        if data["status"] != "OK":
            return []
        return data["result"]

def filter_problems_by_topic(submissions: list, topic_tags: list) -> list:
    filtered = []
    for s in submissions:
        tags = s.get("problem", {}).get("tags", [])
        if any(tag.lower() in [t.lower() for t in topic_tags] for tag in tags):
            filtered.append(s)
    return filtered
