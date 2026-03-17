from __future__ import annotations

import json
import logging
import traceback
from datetime import datetime, timezone
from pathlib import Path

from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, StreamingResponse

from app.config import get_settings
from app.learning_engine import LearningEngine
from app.llm.service import LLMService
from app.logging_config import configure_logging
from app.schemas import (
    AssessmentResultResponse,
    AssessmentStartRequest,
    AssessmentStartResponse,
    AssessmentSubmitRequest,
    AssessmentSubmitResponse,
    ChatRequest,
    DailyPracticeResponse,
    ErrorResponse,
    GrammarItem,
    GrammarResponse,
    LearningPathGenerateRequest,
    LearningPathGenerateResponse,
    LearningPathTask,
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
from app.speech_service import SpeechService
from app.state_store import AppState, StateStore

configure_logging()
logger = logging.getLogger(__name__)
settings = get_settings()

app = FastAPI(title="English Growth AI Agent API", version="0.3.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_allow_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

llm_service = LLMService()
learning_engine = LearningEngine()
speech_service = SpeechService()

state_store = StateStore(Path(__file__).resolve().parents[2] / "data" / "app_state.json")
state = state_store.load()

users_store: dict[int, dict] = state.users_store
sessions_store: dict[int, dict] = state.sessions_store
assessments_store: dict[int, dict] = state.assessments_store
vocabulary_store: dict[int, list[dict]] = state.vocabulary_store
learning_path_store: dict[int, list[dict]] = state.learning_path_store

user_id_seq = state.user_id_seq
session_id_seq = state.session_id_seq
assessment_id_seq = state.assessment_id_seq


def persist_state() -> None:
    state_store.save(
        AppState(
            users_store=users_store,
            sessions_store=sessions_store,
            assessments_store=assessments_store,
            vocabulary_store=vocabulary_store,
            learning_path_store=learning_path_store,
            user_id_seq=user_id_seq,
            session_id_seq=session_id_seq,
            assessment_id_seq=assessment_id_seq,
        )
    )

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
    learning_path_store.setdefault(user_id, [])
    persist_state()
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
    persist_state()
    return SessionStartResponse(**session)


@app.post("/api/sessions/{session_id}/submit", response_model=SessionSubmitResponse)
async def submit_session(session_id: int, request: SessionSubmitRequest) -> SessionSubmitResponse:
    session = sessions_store.get(session_id)
    if not session:
        raise HTTPException(status_code=404, detail={"session_id": session_id, "message": "找不到學習任務"})

    user = users_store.get(session["user_id"])
    if not user:
        raise HTTPException(status_code=404, detail={"user_id": session["user_id"], "message": "找不到使用者"})

    llm_result = await llm_service.complete(
        message=f"請針對以下英文回答給學習建議：{request.answer}", provider=request.provider
    )

    user_history = [
        {"score": s.get("score", 60)}
        for s in sessions_store.values()
        if s["user_id"] == session["user_id"] and s["status"] == "submitted"
    ]
    pipeline = learning_engine.run_pipeline(
        user_input=request.answer,
        llm_output=llm_result.content,
        user_cefr=user["cefr_level"],
        history=user_history,
    )

    session["answer"] = request.answer
    session["feedback"] = pipeline.feedback["growth_suggestion"]
    session["pipeline"] = {
        "analysis": pipeline.analysis,
        "adaptive_plan": pipeline.adaptive_plan,
        "scoring": pipeline.scoring,
        "feedback": pipeline.feedback,
    }
    session["score"] = pipeline.scoring["score"]
    session["status"] = "submitted"
    persist_state()

    return SessionSubmitResponse(
        session_id=session_id,
        answer=request.answer,
        feedback=session["feedback"],
        pipeline=session["pipeline"],
    )


@app.get("/api/sessions/{session_id}/feedback", response_model=SessionFeedbackResponse)
def get_session_feedback(session_id: int) -> SessionFeedbackResponse:
    session = sessions_store.get(session_id)
    if not session:
        raise HTTPException(status_code=404, detail={"session_id": session_id, "message": "找不到學習任務"})

    if not session["feedback"]:
        raise HTTPException(status_code=400, detail={"session_id": session_id, "message": "尚未提交答案"})

    return SessionFeedbackResponse(
        session_id=session_id,
        feedback=session["feedback"],
        pipeline=session["pipeline"],
    )


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
    persist_state()

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
    persist_state()
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
    try:
        transcript = speech_service.speech_to_text(
            text=request.text,
            audio_base64=request.audio_base64,
            provider=request.stt_provider,
        )
    except ValueError as exc:
        raise HTTPException(status_code=422, detail={"message": str(exc)}) from exc

    result = await llm_service.complete(
        message=f"請對以下口說內容提供文法與流暢度建議：{transcript}", provider=request.provider
    )
    pipeline = learning_engine.run_pipeline(
        user_input=transcript,
        llm_output=result.content,
        user_cefr=request.cefr_level.upper(),
        history=[],
    )

    pronunciation_score = speech_service.estimate_pronunciation_score(transcript, pipeline.feedback["growth_suggestion"])
    tts_audio_base64 = None
    tts_provider = None
    if request.enable_tts:
        tts_result = speech_service.text_to_speech(pipeline.feedback["growth_suggestion"], request.tts_provider)
        tts_audio_base64 = tts_result.audio_base64
        tts_provider = tts_result.provider

    return SpeakingResponse(
        transcript=transcript,
        feedback=pipeline.feedback["growth_suggestion"],
        pipeline={
            "analysis": pipeline.analysis,
            "adaptive_plan": pipeline.adaptive_plan,
            "scoring": pipeline.scoring,
            "feedback": pipeline.feedback,
        },
        provider=result.provider,
        is_mock=result.is_mock,
        warning=result.warning,
        stt_provider=request.stt_provider,
        tts_provider=tts_provider,
        tts_audio_base64=tts_audio_base64,
        pronunciation_score=pronunciation_score,
    )


def _build_learning_path(cefr_level: str) -> list[LearningPathTask]:
    level = cefr_level.upper()
    vocab_target = "基礎生活單字" if level in {"A1", "A2"} else "進階情境單字"
    grammar_target = "現在式與過去式" if level in {"A1", "A2"} else "條件句與關係子句"
    conversation_target = "旅遊與日常購物" if level in {"A1", "A2"} else "職場會議與簡報"

    return [
        LearningPathTask(
            id=f"vocab-{level.lower()}",
            category="vocabulary",
            title=f"{level} 單字訓練",
            objective=vocab_target,
            recommended_minutes=20,
        ),
        LearningPathTask(
            id=f"grammar-{level.lower()}",
            category="grammar",
            title=f"{level} 文法訓練",
            objective=grammar_target,
            recommended_minutes=20,
        ),
        LearningPathTask(
            id=f"dialog-{level.lower()}",
            category="conversation",
            title=f"{level} 情境對話",
            objective=conversation_target,
            recommended_minutes=25,
        ),
    ]


@app.post("/api/learning-path/generate", response_model=LearningPathGenerateResponse)
def generate_learning_path(request: LearningPathGenerateRequest) -> LearningPathGenerateResponse:
    user = users_store.get(request.user_id)
    if not user:
        raise HTTPException(status_code=404, detail={"user_id": request.user_id, "message": "找不到使用者"})

    path = _build_learning_path(user["cefr_level"])
    learning_path_store[request.user_id] = [task.model_dump() for task in path]
    persist_state()
    return LearningPathGenerateResponse(user_id=request.user_id, cefr_level=user["cefr_level"], path=path)


@app.get("/api/users/{user_id}/daily-practice", response_model=DailyPracticeResponse)
def get_daily_practice(user_id: int) -> DailyPracticeResponse:
    user = users_store.get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail={"user_id": user_id, "message": "找不到使用者"})

    path = learning_path_store.get(user_id)
    if not path:
        generated = _build_learning_path(user["cefr_level"])
        path = [task.model_dump() for task in generated]
        learning_path_store[user_id] = path
        persist_state()

    tasks = [LearningPathTask(**task) for task in path]
    return DailyPracticeResponse(
        user_id=user_id,
        date=datetime.now(timezone.utc).date().isoformat(),
        total_estimated_minutes=sum(item.recommended_minutes for item in tasks),
        tasks=tasks,
    )


if __name__ == "__main__":
    try:
        import uvicorn

        uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
    except Exception as exc:  # noqa: BLE001
        logger.exception("主程式啟動失敗：%s", exc)
