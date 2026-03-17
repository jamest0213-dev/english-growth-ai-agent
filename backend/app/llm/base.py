from __future__ import annotations

from dataclasses import dataclass
from typing import AsyncIterator, Protocol


@dataclass(slots=True)
class LLMResult:
    content: str
    provider: str
    is_mock: bool
    warning: str | None = None


class LLMAdapter(Protocol):
    provider_name: str

    async def complete(self, message: str) -> LLMResult:
        ...

    async def stream(self, message: str) -> AsyncIterator[str]:
        ...
