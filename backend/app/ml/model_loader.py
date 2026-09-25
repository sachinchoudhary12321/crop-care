"""Model artifact loading — the single place models are read from disk.

The framework-specific loading (PyTorch `torch.load`, Ultralytics YOLO
weights, ...) is implemented in the ML Integration task. Everything above
this layer already talks to it via `CropDiseasePredictor`.

TODO(ML Integration task):
  1. Put the trained artifact at `settings.disease_model_path`
     (default: ml_models/crop_disease_model.pt).
  2. Replace the stub body of `load()` with the real framework call.
  3. Uncomment the ML dependencies in requirements.txt.
"""
from __future__ import annotations

import logging
from pathlib import Path
from typing import Any

from app.core.config import Settings, get_settings
from app.core.exceptions import ModelNotAvailableError

logger = logging.getLogger(__name__)


class ModelLoader:
    """Loads model artifacts from disk.

    One loader instance per model type: later models (YOLO detection, pest
    classification, ...) get their own loader class or method here.
    """

    def __init__(self, settings: Settings | None = None) -> None:
        self._settings = settings or get_settings()

    @property
    def model_path(self) -> Path:
        """Absolute-ish path of the disease model artifact."""
        return self._settings.disease_model_path

    @property
    def is_available(self) -> bool:
        """True when the configured model file exists on disk."""
        return self.model_path.is_file()

    def load(self) -> Any:
        """Load the disease detection model from disk.

        Raises:
            ModelNotAvailableError: if the artifact is missing, or if loading
                has not been implemented yet (current state).
        """
        path = self.model_path

        if not path.is_file():
            raise ModelNotAvailableError(
                f"Disease model not found at '{path}'. Place the trained model "
                "file there, or adjust ML_MODEL_DIR / DISEASE_MODEL_FILENAME in .env."
            )

        # ------------------------------------------------------------------
        # TODO(ML Integration task): replace this block with real loading, e.g.
        #
        #   import torch
        #   model = torch.load(path, map_location=self._settings.ml_device)
        #   model.eval()
        #   return model
        # ------------------------------------------------------------------
        raise ModelNotAvailableError(
            f"Model artifact found at '{path}', but framework loading is not "
            "implemented yet (see ModelLoader.load, ML Integration task)."
        )