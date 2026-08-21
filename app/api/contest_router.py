from fastapi import APIRouter, HTTPException

from app.core.response import StandardResponse, ok
from app.schemas.contest.contest import (
    ContestSelectionRequest,
    ContestSelectionResponse,
)
from app.services.contest.contest_service import select_contest_problems

import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/contest", tags=["Contest"])


@router.post("/select-problems", response_model=StandardResponse)
async def select_contest_problems_endpoint(request: ContestSelectionRequest):
    """
    Build a virtual contest: 12 real Codeforces problems (6 at level,
    3 above, 3 hard) with start/end times.
    """
    try:
        return ok(await select_contest_problems(request))
    except Exception as e:
        logger.exception("Contest problem selection failed")
        raise HTTPException(status_code=500, detail=str(e))
