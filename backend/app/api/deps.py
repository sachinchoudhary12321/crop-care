"""Dependency-injection wiring.

Routes depend on the objects declared here; FastAPI resolves them. Concrete
implementations can be replaced in tests via `app.dependency_overrides`.
"""
from __future__ import annotations

from typing import Annotated

from fastapi import Depends, Request

from app.core.config import Settings
from app.ml.predictor import CropDiseasePredictor
from app.services.chatbot_service import ChatbotService
from app.services.prediction_service import PredictionService
from app.services.recommendation_service import RecommendationService


def get_app_settings(request: Request) -> Settings:
    """Return the Settings instance the application was created with."""
    return request.app.state.settings


def get_predictor(request: Request) -> CropDiseasePredictor:
    """Return the process-wide predictor created at application startup."""
    return request.app.state.predictor


PredictorDep = Annotated[CropDiseasePredictor, Depends(get_predictor)]


def get_prediction_service(predictor: PredictorDep) -> PredictionService:
    return PredictionService(predictor=predictor)


def get_recommendation_service() -> RecommendationService:
    return RecommendationService()


def get_chatbot_service() -> ChatbotService:
    return ChatbotService()


SettingsDep = Annotated[Settings, Depends(get_app_settings)]
PredictionServiceDep = Annotated[PredictionService, Depends(get_prediction_service)]
RecommendationServiceDep = Annotated[RecommendationService, Depends(get_recommendation_service)]
ChatbotServiceDep = Annotated[ChatbotService, Depends(get_chatbot_service)]