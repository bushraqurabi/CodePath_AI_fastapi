from fastapi import APIRouter, HTTPException
from random import sample

from app.core.response import StandardResponse, ok
from app.services.quiz.quiz_loader import load_questions
from app.services.quiz.quiz_tracker import record_answers, get_stats
from app.services.quiz.quiz_analyzer import classify_level, ai_insight
from app.schemas.quiz.submission import Submission

router = APIRouter(prefix="/quiz", tags=["Quiz"])

QUESTIONS = load_questions()
QUESTION_MAP = {q.id: q for q in QUESTIONS}


@router.get("/start", response_model=StandardResponse)
def start_quiz(limit: int = 5):
    if not QUESTIONS:
        raise HTTPException(status_code=500, detail="No questions available")

    selected = sample(QUESTIONS, k=min(limit, len(QUESTIONS)))

    return ok([
        {
            "id": q.id,
            "topic": q.topic,
            "difficulty": q.difficulty,
            "question": q.question,
            "options": q.options,
        }
        for q in selected
    ])


@router.post("/submit", response_model=StandardResponse)
def submit_quiz(submission: Submission):
    record_answers(submission.answers, QUESTION_MAP)

    stats = get_stats()
    stats["level"] = classify_level(stats["accuracy"])
    stats["ai_insight"] = ai_insight(stats["topic_breakdown"])

    return ok(stats)
