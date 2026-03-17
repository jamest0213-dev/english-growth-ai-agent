from __future__ import annotations

import base64
from dataclasses import dataclass


@dataclass
class SpeechSynthesisResult:
    provider: str
    audio_base64: str


class SpeechService:
    def speech_to_text(self, text: str | None, audio_base64: str | None, provider: str) -> str:
        if text:
            return text

        if not audio_base64:
            raise ValueError("請提供 text 或 audio_base64")

        try:
            decoded = base64.b64decode(audio_base64.encode("utf-8"), validate=True)
        except Exception as exc:  # noqa: BLE001
            raise ValueError("audio_base64 格式錯誤") from exc

        # MVP：沒有實際串接 STT 時，以固定可追蹤轉寫內容回傳
        # 後續可在此依 provider 串接 Whisper / Google STT SDK
        length_hint = len(decoded)
        return f"[mock-{provider}] 已接收語音資料（{length_hint} bytes），請繼續完成口說練習。"

    def text_to_speech(self, text: str, provider: str) -> SpeechSynthesisResult:
        # MVP：回傳可播放的 placeholder bytes（模擬音訊）
        placeholder_audio = f"TTS:{provider}:{text[:120]}".encode("utf-8")
        encoded = base64.b64encode(placeholder_audio).decode("utf-8")
        return SpeechSynthesisResult(provider=provider, audio_base64=encoded)

    def estimate_pronunciation_score(self, transcript: str, feedback_text: str) -> int:
        # 簡易版（LLM 前）：以長度 + 回饋內容品質提示做啟發式評分
        transcript_bonus = min(len(transcript) // 10, 20)
        feedback_bonus = 10 if "建議" in feedback_text or "suggestion" in feedback_text.lower() else 5
        return max(45, min(95, 60 + transcript_bonus + feedback_bonus))
