from __future__ import annotations

import json
import logging
import traceback

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, StreamingResponse

from app.llm.service import LLMService
from app.logging_config import configure_logging
from app.schemas import ChatRequest, ChatResponse

configure_logging()
logger = logging.getLogger(__name__)

app = FastAPI(title="English Growth AI Agent API", version="0.2.0")
llm_service = LLMService()


@app.exception_handler(Exception)
async def global_exception_handler(_: Request, exc: Exception) -> JSONResponse:
    logger.exception("未預期錯誤：%s", exc)
    return JSONResponse(
        status_code=500,
        content={
            "ok": False,
            "error": {
                "code": "INTERNAL_SERVER_ERROR",
                "message": "發生錯誤。請複製以下訊息並發送給您的 AI 助手：",
                "details": {"traceback": traceback.format_exc()},
            },
        },
    )


@app.get("/healthz")
def healthz() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest) -> ChatResponse:
    result = await llm_service.complete(message=request.message, provider=request.provider)
    return ChatResponse(
        provider=result.provider,
        is_mock=result.is_mock,
        warning=result.warning,
        content=result.content,
    )


@app.post("/api/chat/stream")
async def chat_stream(request: ChatRequest) -> StreamingResponse:
    stream_iterator, is_mock, warning = await llm_service.stream(
        message=request.message,
        provider=request.provider,
    )

    async def sse_events():
        if warning:
            yield f"data: {json.dumps({'type': 'warning', 'message': warning}, ensure_ascii=False)}\n\n"
        async for chunk in stream_iterator:
            yield f"data: {json.dumps({'type': 'chunk', 'content': chunk, 'is_mock': is_mock}, ensure_ascii=False)}\n\n"
        yield "data: {\"type\": \"done\"}\n\n"

    return StreamingResponse(sse_events(), media_type="text/event-stream")


if __name__ == "__main__":
    try:
        import uvicorn

        uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
    except Exception as exc:  # noqa: BLE001
        logger.exception("主程式啟動失敗：%s", exc)
