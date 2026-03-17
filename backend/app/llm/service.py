from __future__ import annotations

import logging
from collections.abc import AsyncIterator

from app.config import get_settings
from app.llm.adapters import MOCK_WARNING, GeminiAdapter, MockAdapter, OpenAIAdapter
from app.llm.base import LLMResult

logger = logging.getLogger(__name__)


class LLMService:
    def __init__(self) -> None:
        self.settings = get_settings()

    def _resolve_adapter(self, provider: str | None):
        selected_provider = (provider or self.settings.default_provider).lower()

        if selected_provider == "openai":
            if not self.settings.openai_api_key:
                logger.warning("OpenAI API Key 缺失，切換為 mock provider")
                return MockAdapter()
            return OpenAIAdapter(self.settings.openai_api_key)

        if selected_provider == "gemini":
            if not self.settings.gemini_api_key:
                logger.warning("Gemini API Key 缺失，切換為 mock provider")
                return MockAdapter()
            return GeminiAdapter(self.settings.gemini_api_key)

        logger.warning("未知 provider，切換為 mock provider")
        return MockAdapter()

    async def complete(self, message: str, provider: str | None = None) -> LLMResult:
        adapter = self._resolve_adapter(provider)
        try:
            result = await adapter.complete(message)
            if result.is_mock and not result.warning:
                result.warning = MOCK_WARNING
            return result
        except Exception as exc:  # noqa: BLE001
            logger.exception("LLM complete 發生錯誤，切換 fallback mock: %s", exc)
            fallback = await MockAdapter().complete(message)
            fallback.warning = MOCK_WARNING
            return fallback

    async def stream(self, message: str, provider: str | None = None) -> tuple[AsyncIterator[str], bool, str]:
        adapter = self._resolve_adapter(provider)
        is_mock = isinstance(adapter, MockAdapter)
        warning = MOCK_WARNING if is_mock else ""

        async def iterator() -> AsyncIterator[str]:
            try:
                async for chunk in adapter.stream(message):
                    yield chunk
            except Exception as exc:  # noqa: BLE001
                logger.exception("LLM stream 發生錯誤，使用 fallback mock: %s", exc)
                yield "\n[系統] 正式模型暫時不可用，已切換 mock 回應。"
                async for chunk in MockAdapter().stream(message):
                    yield chunk

        return iterator(), is_mock, warning
