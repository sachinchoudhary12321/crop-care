"""Schemas for the treatment recommendation API (Recommendation task).

The contract is intentionally minimal for now; it will grow (risk levels,
dosage, safety notes, sources) when the recommendation engine is built.
"""
from __future__ import annotations

from pydantic import BaseModel, Field


class TreatmentItem(BaseModel):
    """A single recommended treatment step."""

    title: str = Field(..., examples=["Apply copper-based fungicide"])
    description: str = Field(..., examples=["Spray every 7-10 days until symptoms stop spreading."])


class RecommendationRequest(BaseModel):
    """Request body for POST /api/v1/recommendations."""

    disease_label: str = Field(..., min_length=1, examples=["Tomato___Late_blight"])


class RecommendationResponse(BaseModel):
    """Recommended treatments for a detected disease."""

    disease_label: str = Field(..., examples=["Tomato___Late_blight"])
    treatments: list[TreatmentItem]