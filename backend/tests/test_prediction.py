"""Tests for POST /api/v1/predictions.

The model is not integrated yet, so the endpoint must fail *cleanly*
(no fake predictions). Update/remove the first test once the real model
is connected in the ML Integration task.
"""
from __future__ import annotations

from fastapi.testclient import TestClient


def test_prediction_without_model_returns_503(client: TestClient) -> None:
    files = {"file": ("leaf.jpg", b"not-a-real-image-yet", "image/jpeg")}

    response = client.post("/api/v1/predictions", files=files)

    assert response.status_code == 503
    assert response.json()["error"]["code"] == "model_not_available"


def test_prediction_rejects_non_image_upload(client: TestClient) -> None:
    files = {"file": ("notes.txt", b"hello", "text/plain")}

    response = client.post("/api/v1/predictions", files=files)

    assert response.status_code == 415
    assert response.json()["error"]["code"] == "invalid_image"