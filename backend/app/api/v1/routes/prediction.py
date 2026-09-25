"""Crop disease prediction endpoint.

Flow: route (validation) -> PredictionService (business logic) ->
CropDiseasePredictor (ML). Until the ML Integration task connects a trained
model, the ML layer raises `ModelNotAvailableError`, which the global handler
turns into a clean HTTP 503 — never a fake prediction.
"""
from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, File, UploadFile, status

from app.api.deps import PredictionServiceDep, SettingsDep
from app.schemas.common import ErrorResponse
from app.schemas.prediction import PredictionResponse
from app.utils.images import read_validated_image

router = APIRouter(prefix="/predictions", tags=["prediction"])

ImageFile = Annotated[UploadFile, File(description="Crop/leaf image (JPEG, PNG or WebP).")]


@router.post(
    "",
    response_model=PredictionResponse,
    status_code=status.HTTP_200_OK,
    summary="Detect the disease in a crop image",
    responses={
        status.HTTP_413_REQUEST_ENTITY_TOO_LARGE: {
            "model": ErrorResponse,
            "description": "Image too large",
        },
        status.HTTP_415_UNSUPPORTED_MEDIA_TYPE: {
            "model": ErrorResponse,
            "description": "Unsupported image format",
        },
        status.HTTP_503_SERVICE_UNAVAILABLE: {
            "model": ErrorResponse,
            "description": "ML model not available yet",
        },
    },
)
async def create_prediction(
    file: ImageFile,
    settings: SettingsDep,
    service: PredictionServiceDep,
) -> PredictionResponse:
    """Upload a crop image and receive the predicted disease + confidence."""
    image_bytes = await read_validated_image(
        file, max_size_bytes=settings.max_upload_size_bytes
    )
    result = await service.predict_from_image(image_bytes)
    return PredictionResponse.from_result(result)