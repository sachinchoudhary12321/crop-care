"""Schemas for the AI chatbot API (Chatbot task)."""
from __future__ import annotations

from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    """A message sent to the assistant."""

    message: str = Field(
        ...,
        min_length=1,
        max_length=2000,
        examples=["What should I do about brown spots on my tomato leaves?"],
    )
    session_id: str | None = Field(
        default=None, description="Existing conversation id; omit to start a new conversation."
    )


class ChatResponse(BaseModel):
    """The assistant's reply."""

    session_id: str = Field(..., description="Conversation id (echoed for multi-turn chats)")
    reply: str = Field(..., examples=["Late blight is likely. Remove infected leaves and ..."])