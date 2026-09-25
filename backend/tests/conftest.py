"""Shared pytest fixtures."""
from __future__ import annotations

from collections.abc import Iterator

import pytest
from fastapi.testclient import TestClient

from app.core.config import Settings
from app.main import create_app


@pytest.fixture()
def client() -> Iterator[TestClient]:
    """A TestClient bound to a freshly created app instance.

    Using `with TestClient(...)` triggers startup/shutdown (lifespan) events,
    exactly like a real server run.
    """
    app = create_app(Settings())
    with TestClient(app) as test_client:
        yield test_client