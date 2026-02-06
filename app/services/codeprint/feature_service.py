import json
from pathlib import Path

MODEL_DIR = Path(__file__).resolve().parents[2] / "models"
DATA_DIR = Path(__file__).resolve().parents[2] / "data"

def extract_user_features(handle: str) -> dict:
    """
    Extract features for a given user handle from CSV/json.
    Returns dict of features for ML model and signal analysis.
    """
    users_file = DATA_DIR / "users_features.csv"
    try:
        import pandas as pd
        df = pd.read_csv(users_file)
        row = df[df["handle"] == handle].iloc[0]
        return {
            "avg_rating": row.get("avg_rating", 0),
            "accuracy": row.get("accuracy", 0),
            "dp_accuracy": row.get("dp_accuracy", 0),
            "graph_accuracy": row.get("graph_accuracy", 0),
            "recent_solved": row.get("recent_solved", 0)
        }
    except Exception:
        return {
            "avg_rating": 1200,
            "accuracy": 0.5,
            "dp_accuracy": 0.3,
            "graph_accuracy": 0.5,
            "recent_solved": 0
        }
