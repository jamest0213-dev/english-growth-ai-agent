from __future__ import annotations

import json
import logging
import traceback
from datetime import datetime, timezone

from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse, StreamingResponse

from app.llm.service import LLMService
from app.logging_config import configure_logging
from app.schemas import (
    AssessmentResultResponse,
    AssessmentStartRequest,
    AssessmentStartResponse,
    AssessmentSubmitRequest,
    AssessmentSubmitResponse,
    ChatRequest,
    ErrorResponse,
    GrammarItem,
    GrammarResponse,
    SessionFeedbackResponse,
    SessionStartRequest,
    SessionStartResponse,
    SessionSubmitRequest,
    SessionSubmitResponse,
    SpeakingRequest,
    SpeakingResponse,
    UserCreateRequest,
    UserProgressResponse,
    UserResponse,
    VocabularyItem,
    VocabularyResponse,
    VocabularySaveRequest,
    VocabularySaveResponse,
)

configure_logging()
logger = logging.getLogger(__name__)

app = FastAPI(title="English Growth AI Agent API", version="0.3.0")
llm_service = LLMService()

users_store: dict[int, dict] = {}
sessions_store: dict[int, dict] = {}
assessments_store: dict[int, dict] = {}
vocabulary_store: dict[int, list[dict]] = {}

user_id_seq = 1
session_id_seq = 1
assessment_id_seq = 1

DEFAULT_VOCABULARY = [
    VocabularyItem(id=1, word="achievement", meaning="成就"),
    VocabularyItem(id=2, word="consistent", meaning="持續穩定的"),
]

DEFAULT_GRAMMAR = [
    GrammarItem(id=1, rule="現在完成式", example="I have studied English for three years."),
    GrammarItem(id=2, rule="條件句（第一類）", example="If I have time, I will read this article."),
]


def error_response(status_code: int, code: str, message: str, details: dict | None = None) -> JSONResponse:
    payload = ErrorResponse(error={"code": code, "message": message, "details": details})
    return JSONResponse(status_code=status_code, content=payload.model_dump())


@app.exception_handler(HTTPException)
async def http_exception_handler(_: Request, exc: HTTPException) -> JSONResponse:
    details = exc.detail if isinstance(exc.detail, dict) else {"reason": exc.detail}
    return error_response(status_code=exc.status_code, code="HTTP_ERROR", message="請求失敗", details=details)


@app.exception_handler(RequestValidationError)
async def request_validation_handler(_: Request, exc: RequestValidationError) -> JSONResponse:
    return error_response(
        status_code=422,
        code="VALIDATION_ERROR",
        message="參數驗證失敗",
        details={"errors": exc.errors()},
    )


@app.exception_handler(Exception)
async def global_exception_handler(_: Request, exc: Exception) -> JSONResponse:
    logger.exception("未預期錯誤：%s", exc)
    return error_response(
        status_code=500,
        code="INTERNAL_SERVER_ERROR",
        message="發生錯誤。請複製以下訊息並發送給您的 AI 助手：",
        details={"traceback": traceback.format_exc()},
    )


@app.get("/healthz")
def healthz() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/api/users", response_model=UserResponse)
def create_user(request: UserCreateRequest) -> UserResponse:
    global user_id_seq
    user_id = user_id_seq
    user_id_seq += 1

    user = {
        "id": user_id,
        "learner_name": request.learner_name,
        "cefr_level": request.cefr_level.upper(),
        "created_at": datetime.now(timezone.utc),
    }
    users_store[user_id] = user
    vocabulary_store.setdefault(user_id, [])
    return UserResponse(**user)


@app.get("/api/users/{user_id}", response_model=UserResponse)
def get_user(user_id: int) -> UserResponse:
    user = users_store.get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail={"user_id": user_id, "message": "找不到使用者"})
    return UserResponse(**user)


@app.get("/api/users/{user_id}/progress", response_model=UserProgressResponse)
def get_user_progress(user_id: int) -> UserProgressResponse:
    if user_id not in users_store:
        raise HTTPException(status_code=404, detail={"user_id": user_id, "message": "找不到使用者"})

    user_sessions = [s for s in sessions_store.values() if s["user_id"] == user_id]
    completed = [s for s in user_sessions if s["status"] == "submitted"]
    saved_words = vocabulary_store.get(user_id, [])

    return UserProgressResponse(
        user_id=user_id,
        total_sessions=len(user_sessions),
        completed_sessions=len(completed),
        saved_vocabulary_count=len(saved_words),
    )


@app.post("/api/sessions/start", response_model=SessionStartResponse)
def start_session(request: SessionStartRequest) -> SessionStartResponse:
    global session_id_seq
    if request.user_id not in users_store:
        raise HTTPException(status_code=404, detail={"user_id": request.user_id, "message": "找不到使用者"})

    session_id = session_id_seq
    session_id_seq += 1
    session = {
        "session_id": session_id,
        "user_id": request.user_id,
        "topic": request.topic,
        "status": "started",
        "answer": "",
        "feedback": "",
    }
    sessions_store[session_id] = session
    return SessionStartResponse(**session)


@app.post("/api/sessions/{session_id}/submit", response_model=SessionSubmitResponse)
async def submit_session(session_id: int, request: SessionSubmitRequest) -> SessionSubmitResponse:
    session = sessions_store.get(session_id)
    if not session:
        raise HTTPException(status_code=404, detail={"session_id": session_id, "message": "找不到學習任務"})

    llm_result = await llm_service.complete(
        message=f"請針對以下英文回答給學習建議：{request.answer}", provider=request.provider
    )

    session["answer"] = request.answer
    session["feedback"] = llm_result.content
    session["status"] = "submitted"

    return SessionSubmitResponse(session_id=session_id, answer=request.answer, feedback=llm_result.content)


@app.get("/api/sessions/{session_id}/feedback", response_model=SessionFeedbackResponse)
def get_session_feedback(session_id: int) -> SessionFeedbackResponse:
    session = sessions_store.get(session_id)
    if not session:
        raise HTTPException(status_code=404, detail={"session_id": session_id, "message": "找不到學習任務"})

    if not session["feedback"]:
        raise HTTPException(status_code=400, detail={"session_id": session_id, "message": "尚未提交答案"})

    return SessionFeedbackResponse(session_id=session_id, feedback=session["feedback"])


@app.post("/api/assessment/start", response_model=AssessmentStartResponse)
def start_assessment(request: AssessmentStartRequest) -> AssessmentStartResponse:
    global assessment_id_seq
    if request.user_id not in users_store:
        raise HTTPException(status_code=404, detail={"user_id": request.user_id, "message": "找不到使用者"})

    assessment_id = assessment_id_seq
    assessment_id_seq += 1
    assessments_store[assessment_id] = {
        "assessment_id": assessment_id,
        "user_id": request.user_id,
        "status": "started",
        "score": 0,
        "cefr_level": "A1",
    }
    return AssessmentStartResponse(assessment_id=assessment_id, user_id=request.user_id, status="started")


@app.post("/api/assessment/submit", response_model=AssessmentSubmitResponse)
def submit_assessment(request: AssessmentSubmitRequest) -> AssessmentSubmitResponse:
    assessment = assessments_store.get(request.assessment_id)
    if not assessment or assessment["user_id"] != request.user_id:
        raise HTTPException(status_code=404, detail={"assessment_id": request.assessment_id, "message": "找不到測驗"})

    score = min(len(request.answers) * 10, 100)
    if score >= 80:
        cefr_level = "B2"
    elif score >= 60:
        cefr_level = "B1"
    elif score >= 40:
        cefr_level = "A2"
    else:
        cefr_level = "A1"

    assessment.update({"status": "submitted", "score": score, "cefr_level": cefr_level})
    user = users_store[request.user_id]
    user["cefr_level"] = cefr_level

    return AssessmentSubmitResponse(assessment_id=request.assessment_id, cefr_level=cefr_level, score=score)


@app.get("/api/assessment/result", response_model=AssessmentResultResponse)
def get_assessment_result(assessment_id: int, user_id: int) -> AssessmentResultResponse:
    assessment = assessments_store.get(assessment_id)
    if not assessment or assessment["user_id"] != user_id:
        raise HTTPException(status_code=404, detail={"assessment_id": assessment_id, "message": "找不到測驗結果"})

    return AssessmentResultResponse(
        assessment_id=assessment_id,
        user_id=user_id,
        cefr_level=assessment["cefr_level"],
        score=assessment["score"],
    )


@app.get("/api/vocabulary", response_model=VocabularyResponse)
def get_vocabulary() -> VocabularyResponse:
    return VocabularyResponse(items=DEFAULT_VOCABULARY)


@app.get("/api/grammar", response_model=GrammarResponse)
def get_grammar() -> GrammarResponse:
    return GrammarResponse(items=DEFAULT_GRAMMAR)


@app.post("/api/vocabulary/save", response_model=VocabularySaveResponse)
def save_vocabulary(request: VocabularySaveRequest) -> VocabularySaveResponse:
    if request.user_id not in users_store:
        raise HTTPException(status_code=404, detail={"user_id": request.user_id, "message": "找不到使用者"})

    user_vocab = vocabulary_store.setdefault(request.user_id, [])
    user_vocab.append({"word": request.word, "meaning": request.meaning})
    return VocabularySaveResponse(user_id=request.user_id, saved_count=len(user_vocab))


@app.post("/api/chat")
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


@app.post("/api/chat/complete")
async def chat_complete(request: ChatRequest):
    result = await llm_service.complete(message=request.message, provider=request.provider)
    return {
        "ok": True,
        "provider": result.provider,
        "is_mock": result.is_mock,
        "warning": result.warning,
        "content": result.content,
    }


@app.post("/api/chat/stream")
async def chat_stream_compat(request: ChatRequest) -> StreamingResponse:
    return await chat_stream(request)


@app.post("/api/speaking", response_model=SpeakingResponse)
async def speaking(request: SpeakingRequest) -> SpeakingResponse:
    result = await llm_service.complete(
        message=f"請對以下口說內容提供文法與流暢度建議：{request.text}", provider=request.provider
    )
    return SpeakingResponse(
        transcript=request.text,
        feedback=result.content,
        provider=result.provider,
        is_mock=result.is_mock,
        warning=result.warning,
    )


if __name__ == "__main__":
    try:
        import uvicorn

        uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
    except Exception as exc:  # noqa: BLE001
        logger.exception("主程式啟動失敗：%s", exc)
