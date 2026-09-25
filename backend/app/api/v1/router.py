"""Aggregates every v1 router.

`app.main` mounts this under `settings.api_v1_prefix` (`/api/v1`).
Adding a new v1 module = create a router in `routes/` and include it here.
A future v2 gets its own `app/api/v2/` package — nothing else changes.
"""
from __future__ import annotations

from fastapi import APIRouter

from app.api.v1.routes import chatbot, health, prediction, recommendation

api_v1_router = APIRouter()
api_v1_router.include_router(health.router)
api_v1_router.include_router(prediction.router)
api_v1_router.include_router(recommendation.router)
api_v1_router.include_router(chatbot.router)