"""FastAPI application entry point.

Run locally with:
    uvicorn app.main:app --reload --port 8000

The application is built by `create_app()` (factory pattern) so tests can
build isolated instances with custom `Settings`.
"""
from __future__ import annotations

import logging
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.router import api_v1_router
from app.core.config import Settings, get_settings
from app.core.exceptions import register_exception_handlers
from app.core.logging import configure_logging
from app.core.middleware import RequestLoggingMiddleware
from app.database.connection import dispose_engine
from app.ml.model_loader import ModelLoader
from app.ml.predictor import CropDiseasePredictor

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """Application startup / shutdown logic (replaces deprecated on_event)."""
    settings: Settings = app.state.settings

    logger.info(
        "Starting %s v%s (environment=%s)",
        settings.app_name,
        settings.app_version,
        settings.environment,
    )

    # ML: load the model once per process. Best effort — when no trained
    # artifact is available yet (current state) a warning is logged and the
    # API keeps running; prediction requests answer with HTTP 503 instead.
    app.state.predictor.warm_up()

    # TODO(Database Integration task): verify database connectivity here.

    yield

    # Release shared resources. No-op until the DB engine is actually created.
    await dispose_engine()
    logger.info("%s stopped.", settings.app_name)


def create_app(settings: Settings | None = None) -> FastAPI:
    """Create and configure the FastAPI application."""
    settings = settings or get_settings()
    configure_logging(settings.log_level)

    app = FastAPI(
        title="Crop Care Crop API",
        description="AI-powered crop disease detection and recommendation backend.",
        version=settings.app_version,
        debug=settings.debug,
        lifespan=lifespan,
    )

    # Long-lived, process-wide objects live on app.state.
    app.state.settings = settings
    app.state.predictor = CropDiseasePredictor(model_loader=ModelLoader(settings))

    # Middleware — the LAST one added runs FIRST (outermost).
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origin_list,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.add_middleware(RequestLoggingMiddleware)

    register_exception_handlers(app)
    app.include_router(api_v1_router, prefix=settings.api_v1_prefix)

    return app


app = create_app()


if __name__ == "__main__":  # convenience for `python -m app.main`
    import uvicorn

    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)