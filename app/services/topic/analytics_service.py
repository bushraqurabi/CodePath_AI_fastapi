def compute_accuracy(accepted: int, total: int) -> float:
    if total == 0:
        return 0.0
    return round((accepted / total) * 100, 2)

def classify_level(accuracy: float) -> str:
    if accuracy >= 80:
        return "Advanced"
    elif accuracy >= 50:
        return "Intermediate"
    else:
        return "Beginner"

def compute_subskill_performance(submissions: list, subskill_tags: dict) -> dict:
    result = {}
    for subskill, tags in subskill_tags.items():
        filtered = [s for s in submissions if any(tag in s.get("problem", {}).get("tags", []) for tag in tags)]
        accepted = sum(1 for s in filtered if s.get("verdict") == "OK")
        total = len(filtered)
        accuracy = compute_accuracy(accepted, total)
        result[subskill] = {
            "accepted": accepted,
            "total": total,
            "accuracy": accuracy
        }
    return result
