"""Application error types and global FastAPI exception handlers.

Every deliberate failure in the backend raises an `AppError` subclass from
any layer (service, ML, database). `register_exception_handlers` maps them to
a uniform JSON envelope:

    {"error": {"code": "...", "message": "...", "details": ...}}

so clients (the React/Next.js frontend) only ever need one error parser.
"""
from __future__ import annotations

import logging
from typing import Any

from fastapi import FastAPI, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

logger = logging.getLogger(__name__)


class AppError(Exception):
    """Base class for errors the application raises deliberately."""

    status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR
    error_code: str = "internal_error"
    default_message: str = "An unexpected error occurred."

    def __init__(self, message: str | None = None) -> None:
        self.message = message or self.default_message
        super().__init__(self.message)


class InvalidImageError(AppError):
    """The uploaded file is not a supported image."""

    status_code = status.HTTP_415_UNSUPPORTED_MEDIA_TYPE
    error_code = "invalid_image"
    default_message = "The uploaded file is not a supported image."


class ImageTooLargeError(AppError):
    """The uploaded image exceeds the configured size limit."""

    status_code = status.HTTP_413_REQUEST_ENTITY_TOO_LARGE
    error_code = "image_too_large"
    default_message = "The uploaded image is too large."


class ModelNotAvailableError(AppError):
    """The ML model is missing or not integrated yet."""

    status_code = status.HTTP_503_SERVICE_UNAVAILABLE
    error_code = "model_not_available"
    default_message = "The ML model is not available."


class DatabaseNotConfiguredError(AppError):
    """The database layer was used before being configured."""

    status_code = status.HTTP_503_SERVICE_UNAVAILABLE
    error_code = "database_not_configured"
    default_message = "The database is not configured."


class FeatureNotImplementedError(AppError):
    """A planned feature (recommendation, chatbot, ...) is not built yet."""

    status_code = status.HTTP_501_NOT_IMPLEMENTED
    error_code = "not_implemented"
    default_message = "This feature is not implemented yet."


def _error_payload(code: str, message: str, details: Any = None) -> dict[str, Any]:
    """Build the uniform error envelope."""
    payload: dict[str, Any] = {"error": {"code": code, "message": message}}
    if details is not None:
        payload["error"]["details"] = details
    return payload


def register_exception_handlers(app: FastAPI) -> None:
    """Attach global exception handlers to the application."""

    @app.exception_handler(AppError)
    async def handle_app_error(request: Request, exc: AppError) -> JSONResponse:
        logger.warning(
            "%s %s -> %s (%s)",
            request.method,
            request.url.path,
            exc.status_code,
            exc.error_code,
        )
        return JSONResponse(
            status_code=exc.status_code,
            content=_error_payload(exc.error_code, exc.message),
        )

    @app.exception_handler(RequestValidationError)
    async def handle_validation_error(
        request: Request, exc: RequestValidationError
    ) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content=_error_payload(
                "validation_error",
                "Request validation failed.",
                jsonable_encoder(exc.errors()),
            ),
        )

    @app.exception_handler(StarletteHTTPException)
    async def handle_http_exception(
        request: Request, exc: StarletteHTTPException
    ) -> JSONResponse:
        message = exc.detail if isinstance(exc.detail, str) else "Request failed."
        return JSONResponse(
            status_code=exc.status_code,
            content=_error_payload("http_error", message),
        )

    @app.exception_handler(Exception)
    async def handle_unexpected_error(request: Request, exc: Exception) -> JSONResponse:
        logger.exception("Unhandled exception on %s %s", request.method, request.url.path)
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=_error_payload("internal_error", "Internal server error."),
        )