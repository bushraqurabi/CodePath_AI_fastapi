from fastapi import APIRouter, HTTPException

from app.core.response import StandardResponse, ok
from app.schemas.reference.reference import (
    ReferenceCurateRequest,
    ReferenceCurateResponse,
)
from app.services.reference.reference_service import curate_reference

import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/reference", tags=["Reference"])


@router.post("/curate", response_model=StandardResponse)
async def curate_reference_endpoint(request: ReferenceCurateRequest):
    """
    Group the user's saved solution snippets into weakness-ordered sections
    with personalised intros.
    """
    try:
        return ok(curate_reference(request))
    except Exception as e:
        logger.exception("Reference curation failed")
        raise HTTPException(status_code=500, detail=str(e))
