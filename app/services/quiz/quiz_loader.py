import json
from pathlib import Path
from app.schemas.quiz.question import Question

QUESTIONS_DIR = Path(__file__).resolve().parents[2] / "questions"


def load_questions():
    questions = []

    for file in QUESTIONS_DIR.glob("*.json"):
        with open(file, "r", encoding="utf-8") as f:
            data = json.load(f)
            for q in data:
                questions.append(Question(**q))

    return questions
