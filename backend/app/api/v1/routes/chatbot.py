"""AI chatbot endpoints.

Not active yet: registered for contract visibility, returns HTTP 501 until
the Chatbot Integration task implements `ChatbotService` (LangChain +
LangGraph + Llama 3 via Ollama).
"""
from __future__ import annotations

from fastapi import APIRouter, status

from app.api.deps import ChatbotServiceDep
from app.schemas.chatbot import ChatRequest, ChatResponse
from app.schemas.common import ErrorResponse

router = APIRouter(prefix="/chatbot", tags=["chatbot"])


@router.post(
    "/messages",
    response_model=ChatResponse,
    summary="Ask the crop-care assistant (not implemented yet)",
    responses={
        status.HTTP_501_NOT_IMPLEMENTED: {
            "model": ErrorResponse,
            "description": "Not implemented yet",
        }
    },
)
async def send_message(payload: ChatRequest, service: ChatbotServiceDep) -> ChatResponse:
    return await service.answer(payload.message, session_id=payload.session_id)