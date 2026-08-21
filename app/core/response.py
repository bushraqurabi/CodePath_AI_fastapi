from typing import Any

from pydantic import BaseModel


class StandardResponse(BaseModel):
    """Standard envelope for every API response."""

    success: bool = True
    message: str = "Success"
    data: Any = None


def ok(data: Any = None, message: str = "Success") -> StandardResponse:
    return StandardResponse(success=True, message=message, data=data)
