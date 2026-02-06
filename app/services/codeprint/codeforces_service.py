import requests

CF_USER_API = "https://codeforces.com/api/user.info"


def get_user_info(handle: str):
    r = requests.get(CF_USER_API, params={"handles": handle})
    if r.status_code != 200:
        return None

    data = r.json()
    if data["status"] != "OK":
        return None

    u = data["result"][0]
    return {
        "handle": u["handle"],
        "rating": u.get("rating", 0),
        "rank": u.get("rank", "unrated"),
        "maxRating": u.get("maxRating", 0),
        "maxRank": u.get("maxRank", "unrated"),
    }
