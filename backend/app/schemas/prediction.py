"""Schemas for the crop disease prediction API."""
from __future__ import annotations

from pydantic import BaseModel, Field


class PredictionResult(BaseModel):
    """Raw output of the ML layer for one image.

    Produced by `app.ml.predictor.CropDiseasePredictor` and passed up to the
    API layer. Class labels come from the trained model's class list.
    """

    label: str = Field(
        ..., description="Predicted disease/class label", examples=["Tomato___Late_blight"]
    )
    confidence: float = Field(
        ..., ge=0.0, le=1.0, description="Model confidence (0-1)", examples=[0.97]
    )
    model_version: str = Field(
        ...,
        description="Identifier of the model that produced the prediction",
        examples=["crop-disease-v1"],
    )


class PredictionResponse(BaseModel):
    """Public API response for POST /api/v1/predictions."""

    label: str = Field(..., examples=["Tomato___Late_blight"])
    confidence: float = Field(..., ge=0.0, le=1.0, examples=[0.97])
    model_version: str = Field(..., examples=["crop-disease-v1"])

    @classmethod
    def from_result(cls, result: PredictionResult) -> "PredictionResponse":
        """Map the internal ML result onto the public response contract."""
        return cls(
            label=result.label,
            confidence=result.confidence,
            model_version=result.model_version,
        )