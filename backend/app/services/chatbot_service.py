"""Chatbot business logic (Chatbot Integration task)."""
from __future__ import annotations

from app.core.exceptions import FeatureNotImplementedError
from app.schemas.chatbot import ChatResponse


class ChatbotService:
    """Conversational assistant for farmers.

    TODO(Chatbot Integration task):
      * LangChain/LangGraph agent backed by Llama 3 via Ollama
        (settings.ollama_base_url, settings.ollama_model)
      * tools: disease lookup, treatment lookup, prediction history
      * conversation memory keyed by `session_id`
    """

    async def answer(self, message: str, session_id: str | None = None) -> ChatResponse:
        raise FeatureNotImplementedError(
            "The AI chatbot is implemented in the Chatbot Integration task."
        )