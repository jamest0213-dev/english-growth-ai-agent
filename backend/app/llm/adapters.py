from __future__ import annotations

import json
from collections.abc import AsyncIterator

import httpx

from app.llm.base import LLMAdapter, LLMResult

MOCK_WARNING = "目前使用 Mock 回應（未偵測到 API Key），內容僅供測試。"


class MockAdapter(LLMAdapter):
    provider_name = "mock"

    async def complete(self, message: str) -> LLMResult:
        content = f"[Mock] 已收到你的訊息：{message}\n建議：請設定 API Key 以啟用正式模型。"
        return LLMResult(content=content, provider=self.provider_name, is_mock=True, warning=MOCK_WARNING)

    async def stream(self, message: str) -> AsyncIterator[str]:
        base = [
            "[Mock] 已收到你的訊息。",
            "\n",
            "建議：請設定 API Key 以啟用正式模型。",
        ]
        for chunk in base:
            yield chunk


class OpenAIAdapter(LLMAdapter):
    provider_name = "openai"

    def __init__(self, api_key: str):
        self.api_key = api_key

    async def complete(self, message: str) -> LLMResult:
        url = "https://api.openai.com/v1/chat/completions"
        payload = {
            "model": "gpt-4o-mini",
            "messages": [{"role": "user", "content": message}],
            "temperature": 0.5,
        }
        headers = {"Authorization": f"Bearer {self.api_key}"}

        async with httpx.AsyncClient(timeout=60) as client:
            response = await client.post(url, json=payload, headers=headers)
            response.raise_for_status()
            data = response.json()

        content = data["choices"][0]["message"]["content"]
        return LLMResult(content=content, provider=self.provider_name, is_mock=False)

    async def stream(self, message: str) -> AsyncIterator[str]:
        url = "https://api.openai.com/v1/chat/completions"
        payload = {
            "model": "gpt-4o-mini",
            "messages": [{"role": "user", "content": message}],
            "temperature": 0.5,
            "stream": True,
        }
        headers = {"Authorization": f"Bearer {self.api_key}"}

        async with httpx.AsyncClient(timeout=60) as client:
            async with client.stream("POST", url, json=payload, headers=headers) as response:
                response.raise_for_status()
                async for line in response.aiter_lines():
                    if not line.startswith("data:"):
                        continue
                    data_part = line.replace("data:", "", 1).strip()
                    if data_part == "[DONE]":
                        break
                    try:
                        data = json.loads(data_part)
                        delta = data["choices"][0]["delta"]
                    except (json.JSONDecodeError, KeyError, IndexError):
                        continue
                    content = delta.get("content")
                    if content:
                        yield content


class GeminiAdapter(LLMAdapter):
    provider_name = "gemini"

    def __init__(self, api_key: str):
        self.api_key = api_key

    async def complete(self, message: str) -> LLMResult:
        url = (
            "https://generativelanguage.googleapis.com/v1beta/models/"
            f"gemini-1.5-flash:generateContent?key={self.api_key}"
        )
        payload = {"contents": [{"parts": [{"text": message}]}]}

        async with httpx.AsyncClient(timeout=60) as client:
            response = await client.post(url, json=payload)
            response.raise_for_status()
            data = response.json()

        content = data["candidates"][0]["content"]["parts"][0]["text"]
        return LLMResult(content=content, provider=self.provider_name, is_mock=False)

    async def stream(self, message: str) -> AsyncIterator[str]:
        result = await self.complete(message)
        yield result.content
