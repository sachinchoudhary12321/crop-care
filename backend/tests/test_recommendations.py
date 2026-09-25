"""Tests for the recommendation endpoint (contract only for now)."""
from __future__ import annotations

from fastapi.testclient import TestClient

RECOMMENDATIONS_URL = "/api/v1/recommendations"

_VALID_PAYLOAD = {
    "crop": "tomato",
    "disease": "late blight",
    "confidence": 0.92,
    "context": {"location": "Pune", "growth_stage": "flowering"},
}


def test_valid_recommendation_request_returns_501(client: TestClient) -> None:
    response = client.post(RECOMMENDATIONS_URL, json=_VALID_PAYLOAD)

    assert response.status_code == 501
    error = response.json()["error"]
    assert error["code"] == "NOT_IMPLEMENTED"
    assert "message" in error


def test_malformed_recommendation_request_returns_422(client: TestClient) -> None:
    response = client.post(RECOMMENDATIONS_URL, json={"crop": "tomato"})  # `disease` missing

    assert response.status_code == 422
    body = response.json()
    assert body["error"]["code"] == "VALIDATION_ERROR"
    assert body["error"]["details"]  # field-level details included


def test_invalid_confidence_returns_422(client: TestClient) -> None:
    payload = {**_VALID_PAYLOAD, "confidence": 1.5}  # outside [0, 1]

    response = client.post(RECOMMENDATIONS_URL, json=payload)

    assert response.status_code == 422
    assert response.json()["error"]["code"] == "VALIDATION_ERROR"
