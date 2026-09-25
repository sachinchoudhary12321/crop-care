"""Schemas for the prediction API."""
from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field

from app.domain.prediction import PredictionRecord, PredictionStatus


class PredictionCreatedResponse(BaseModel):
    """Returned by POST /api/v1/predictions (201)."""

    prediction_id: UUID = Field(..., description="Unique id of the prediction request.")
    status: PredictionStatus = Field(..., description="Current lifecycle status.")
    filename: str = Field(
        ...,
        description="Server-generated storage filename. Safe to display; never a filesystem path.",
    )


class PredictionImageInfo(BaseModel):
    """Metadata about the stored image (no paths, no original filename)."""

    filename: str
    content_type: str
    size_bytes: int


class PredictionResponse(BaseModel):
    """Returned by GET /api/v1/predictions/{prediction_id}.

    `crop`, `disease` and `confidence` remain `null` until the status becomes
    `completed` (i.e. after the real ML model is connected). Nothing is
    invented in the meantime.
    """

    prediction_id: UUID
    status: PredictionStatus
    image: PredictionImageInfo
    crop: str | None = None
    disease: str | None = None
    confidence: float | None = Field(default=None, ge=0.0, le=1.0)
    error_code: str | None = Field(
        default=None, description="Set only when status == 'failed'."
    )
    created_at: datetime
    updated_at: datetime

    @classmethod
    def from_record(cls, record: PredictionRecord) -> "PredictionResponse":
        """Map an internal domain record onto the public API shape."""
        return cls(
            prediction_id=record.prediction_id,
            status=record.status,
            image=PredictionImageInfo(
                filename=record.stored_filename,
                content_type=record.content_type,
                size_bytes=record.size_bytes,
            ),
            crop=record.crop,
            disease=record.disease,
            confidence=record.confidence,
            error_code=record.error_code,
            created_at=record.created_at,
            updated_at=record.updated_at,
        )
