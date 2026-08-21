from fastapi import APIRouter, HTTPException

from app.core.response import StandardResponse, ok
from app.schemas.roadmap.roadmap import (
    RoadmapGenerateRequest,
    RoadmapGenerateResponse,
)
from app.services.roadmap.roadmap_service import generate_roadmap

import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/roadmap", tags=["Roadmap"])


@router.post("/generate", response_model=StandardResponse)
async def generate_roadmap_endpoint(request: RoadmapGenerateRequest):
    """
    Build a personalised, weakness-ranked study roadmap for the user.
    """
    try:
        return ok(await generate_roadmap(request))
    except Exception as e:
        logger.exception("Roadmap generation failed")
        raise HTTPException(status_code=500, detail=str(e))
