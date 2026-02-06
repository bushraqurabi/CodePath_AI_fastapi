from pydantic import BaseModel, field_validator
from typing import List


class Question(BaseModel):
    id: int
    topic: str
    difficulty: str
    question: str
    options: List[str]
    correct_option: int

    @field_validator("correct_option")
    @classmethod
    def validate_correct_option(cls, v, info):
        options = info.data.get("options", [])
        if not (0 <= v < len(options)):
            raise ValueError("correct_option must be a valid option index")
        return v
