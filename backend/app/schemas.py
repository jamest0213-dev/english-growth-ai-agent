from __future__ import annotations

from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=5000)
    provider: str | None = Field(default=None, description="openai | gemini")


class ChatResponse(BaseModel):
    ok: bool = True
    provider: str
    is_mock: bool
    warning: str | None = None
    content: str
