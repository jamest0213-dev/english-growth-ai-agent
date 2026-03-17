from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field


class ErrorDetail(BaseModel):
    code: str
    message: str
    details: dict | None = None


class ErrorResponse(BaseModel):
    ok: bool = False
    error: ErrorDetail


class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=5000)
    provider: str | None = Field(default=None, description="openai | gemini")


class ChatResponse(BaseModel):
    ok: bool = True
    provider: str
    is_mock: bool
    warning: str | None = None
    content: str


class AdaptivePlan(BaseModel):
    exercise_difficulty: int
    vocabulary_complexity: str
    speech_rate: str


class InputAnalysis(BaseModel):
    grammar_issues: list[str]
    intent: str
    estimated_cefr: str
    error_rate: float


class FeedbackPayload(BaseModel):
    grammar_correction: str
    naturalness_suggestion: str
    alternative_sentence: str
    cefr_assessment: str
    growth_suggestion: str


class ScoringPayload(BaseModel):
    score: int
    confidence: float


class SessionPipelinePayload(BaseModel):
    analysis: InputAnalysis
    adaptive_plan: AdaptivePlan
    scoring: ScoringPayload
    feedback: FeedbackPayload


class UserCreateRequest(BaseModel):
    learner_name: str = Field(min_length=1, max_length=100)
    cefr_level: str = Field(default="A1", min_length=2, max_length=2)


class UserResponse(BaseModel):
    ok: bool = True
    id: int
    learner_name: str
    cefr_level: str
    created_at: datetime


class UserProgressResponse(BaseModel):
    ok: bool = True
    user_id: int
    total_sessions: int
    completed_sessions: int
    saved_vocabulary_count: int


class SessionStartRequest(BaseModel):
    user_id: int
    topic: str = Field(min_length=1, max_length=200)


class SessionStartResponse(BaseModel):
    ok: bool = True
    session_id: int
    user_id: int
    topic: str
    status: str


class SessionSubmitRequest(BaseModel):
    answer: str = Field(min_length=1, max_length=5000)
    provider: str | None = Field(default=None, description="openai | gemini")


class SessionSubmitResponse(BaseModel):
    ok: bool = True
    session_id: int
    answer: str
    feedback: str
    pipeline: SessionPipelinePayload


class SessionFeedbackResponse(BaseModel):
    ok: bool = True
    session_id: int
    feedback: str
    pipeline: SessionPipelinePayload


class AssessmentStartRequest(BaseModel):
    user_id: int


class AssessmentStartResponse(BaseModel):
    ok: bool = True
    assessment_id: int
    user_id: int
    status: str


class AssessmentSubmitRequest(BaseModel):
    assessment_id: int
    user_id: int
    answers: list[str] = Field(min_length=1)


class AssessmentSubmitResponse(BaseModel):
    ok: bool = True
    assessment_id: int
    cefr_level: str
    score: int


class AssessmentResultResponse(BaseModel):
    ok: bool = True
    assessment_id: int
    user_id: int
    cefr_level: str
    score: int


class VocabularyItem(BaseModel):
    id: int
    word: str
    meaning: str


class VocabularyResponse(BaseModel):
    ok: bool = True
    items: list[VocabularyItem]


class GrammarItem(BaseModel):
    id: int
    rule: str
    example: str


class GrammarResponse(BaseModel):
    ok: bool = True
    items: list[GrammarItem]


class VocabularySaveRequest(BaseModel):
    user_id: int
    word: str = Field(min_length=1, max_length=100)
    meaning: str = Field(min_length=1, max_length=200)


class VocabularySaveResponse(BaseModel):
    ok: bool = True
    user_id: int
    saved_count: int


class SpeakingRequest(BaseModel):
    text: str = Field(min_length=1, max_length=5000, description="此版本以文字模擬語音轉文字")
    provider: str | None = Field(default=None, description="openai | gemini")
    cefr_level: str = Field(default="A1", min_length=2, max_length=2)


class SpeakingResponse(BaseModel):
    ok: bool = True
    transcript: str
    feedback: str
    pipeline: SessionPipelinePayload
    provider: str
    is_mock: bool
    warning: str | None = None
