from pydantic import BaseModel
from typing import List


class Answer(BaseModel):
    question_id: int
    selected_option: int


class Submission(BaseModel):
    answers: List[Answer]
