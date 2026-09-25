"""Treatment recommendation endpoints.

Not active yet: the endpoint is registered so the frontend team can see the
contract in /docs, and it returns HTTP 501 until the Recommendation
Integration task implements `RecommendationService`.
"""
from __future__ import annotations

from fastapi import APIRouter, status

from app.api.deps import RecommendationServiceDep
from app.schemas.common import ErrorResponse
from app.schemas.recommendation import RecommendationRequest, RecommendationResponse

router = APIRouter(prefix="/recommendations", tags=["recommendation"])


@router.post(
    "",
    response_model=RecommendationResponse,
    status_code=status.HTTP_200_OK,
    summary="Get treatment recommendations for a disease (not implemented yet)",
    responses={
        status.HTTP_501_NOT_IMPLEMENTED: {
            "model": ErrorResponse,
            "description": "Not implemented yet",
        }
    },
)
async def create_recommendation(
    payload: RecommendationRequest,
    service: RecommendationServiceDep,
) -> RecommendationResponse:
    treatments = await service.recommend_for_disease(payload.disease_label)
    return RecommendationResponse(disease_label=payload.disease_label, treatments=treatments)