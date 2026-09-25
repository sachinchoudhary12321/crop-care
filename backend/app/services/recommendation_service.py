"""Treatment recommendation business logic (Recommendation Integration task).

Interface only for now: the route is registered and the service raises
`FeatureNotImplementedError` (HTTP 501), so the API contract stays honest
until the engine is built.
"""
from __future__ import annotations

from app.core.exceptions import FeatureNotImplementedError
from app.schemas.recommendation import TreatmentItem


class RecommendationService:
    """Turns a detected disease into actionable treatment steps.

    TODO(Recommendation Integration task):
      * load a crop/disease knowledge base (rule-based or model-based)
      * combine prediction history and weather data for risk analysis
      * persist generated recommendations via the database layer
    """

    async def recommend_for_disease(self, disease_label: str) -> list[TreatmentItem]:
        raise FeatureNotImplementedError(
            "Treatment recommendations are implemented in the Recommendation Integration task."
        )