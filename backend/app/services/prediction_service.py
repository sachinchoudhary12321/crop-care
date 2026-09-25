"""Business logic for crop disease prediction."""
from __future__ import annotations

import logging

from starlette.concurrency import run_in_threadpool

from app.ml.predictor import CropDiseasePredictor
from app.schemas.prediction import PredictionResult

logger = logging.getLogger(__name__)


class PredictionService:
    """Coordinates a single prediction request.

    Today it runs the ML layer off the event loop. During the Database
    Integration task this is where the prediction gets persisted and the
    stored record returned.
    """

    def __init__(self, predictor: CropDiseasePredictor) -> None:
        self._predictor = predictor

    async def predict_from_image(self, image_bytes: bytes) -> PredictionResult:
        """Run disease detection on raw image bytes.

        `CropDiseasePredictor.predict` is CPU-bound and synchronous, so it is
        executed in a worker thread — the async event loop keeps serving other
        requests while the model is inferring.
        """
        result = await run_in_threadpool(self._predictor.predict, image_bytes)

        # TODO(Database Integration task): persist the prediction (image
        # reference, label, confidence, timestamps) and return the stored
        # record so the API can expose a `prediction_id`.

        logger.info(
            "Prediction completed: label=%s confidence=%.4f",
            result.label,
            result.confidence,
        )
        return result