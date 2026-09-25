"""Crop disease inference — the stable ML interface.

The rest of the backend only depends on `CropDiseasePredictor.predict()` and
`warm_up()`. When the real model is integrated, only `_run_inference()` (and
`ModelLoader.load()`) change — no route, service or schema needs to move.
"""
from __future__ import annotations

import logging
from typing import Any

from app.core.exceptions import ModelNotAvailableError
from app.ml.model_loader import ModelLoader
from app.schemas.prediction import PredictionResult

logger = logging.getLogger(__name__)


class CropDiseasePredictor:
    """Runs crop disease detection on a single image."""

    def __init__(self, model_loader: ModelLoader | None = None) -> None:
        self._loader = model_loader or ModelLoader()
        self._model: Any | None = None

    @property
    def is_ready(self) -> bool:
        """True once a model has actually been loaded into memory."""
        return self._model is not None

    def warm_up(self) -> None:
        """Load the model ahead of the first request (best effort).

        Called during application startup. When no trained artifact is
        available yet (current state), a warning is logged and the service
        keeps running — prediction requests answer HTTP 503 instead.
        """
        try:
            self._ensure_loaded()
            logger.info("Crop disease model loaded and ready.")
        except ModelNotAvailableError as exc:
            logger.warning("Crop disease model is not available yet: %s", exc)

    def predict(self, image_bytes: bytes) -> PredictionResult:
        """Predict the disease for one image.

        Synchronous and CPU-bound by design: `PredictionService` calls it in
        a worker thread so the event loop is never blocked.
        """
        self._ensure_loaded()
        return self._run_inference(image_bytes)

    def _ensure_loaded(self) -> None:
        if self._model is None:
            self._model = self._loader.load()

    def _run_inference(self, image_bytes: bytes) -> PredictionResult:
        """Actual inference — implemented in the ML Integration task.

        Steps to implement (only this method should change):
          1. Decode + validate the image (OpenCV / Pillow).
          2. Pre-process (resize, normalise, convert to tensor).
          3. Run the model (torch / ultralytics YOLO) on the configured device.
          4. Map the output index to a label from the model's class list.
          5. Return PredictionResult(label=..., confidence=..., model_version=...).
        """
        raise ModelNotAvailableError(
            "Disease prediction is not connected to a trained model yet. "
            "Implement ModelLoader.load() and CropDiseasePredictor._run_inference()."
        )