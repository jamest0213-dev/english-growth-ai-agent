from __future__ import annotations

from dataclasses import dataclass

CEFR_ORDER = ["A1", "A2", "B1", "B2", "C1", "C2"]


@dataclass
class PipelineResult:
    analysis: dict
    adaptive_plan: dict
    scoring: dict
    feedback: dict


class LearningEngine:
    def run_pipeline(
        self,
        user_input: str,
        llm_output: str,
        user_cefr: str,
        history: list[dict],
    ) -> PipelineResult:
        analysis = self._analyze_input(user_input)
        adaptive_plan = self._adaptive_learning(user_cefr, analysis["error_rate"], history)
        scoring = self._score_response(analysis["error_rate"], user_input)
        feedback = self._build_feedback(user_input, llm_output, analysis)
        return PipelineResult(analysis=analysis, adaptive_plan=adaptive_plan, scoring=scoring, feedback=feedback)

    def _analyze_input(self, text: str) -> dict:
        grammar_issues: list[str] = []
        lower_text = text.lower()

        if "yesterday" in lower_text and " go " in f" {lower_text} ":
            grammar_issues.append("過去時間搭配現在式動詞，建議改為過去式。")
        if "i am agree" in lower_text:
            grammar_issues.append("agree 為動詞，建議改為 'I agree'。")
        if text and text.strip() and text.strip()[0].islower():
            grammar_issues.append("句首建議大寫。")

        intent = self._classify_intent(lower_text)
        estimated_cefr = self._estimate_cefr(text)
        sentence_count = max(text.count(".") + text.count("!") + text.count("?") + 1, 1)
        error_rate = round(len(grammar_issues) / sentence_count, 2)

        return {
            "grammar_issues": grammar_issues,
            "intent": intent,
            "estimated_cefr": estimated_cefr,
            "error_rate": error_rate,
        }

    def _classify_intent(self, text: str) -> str:
        if any(keyword in text for keyword in ["why", "how", "explain", "what"]):
            return "question"
        if any(keyword in text for keyword in ["please", "help", "can you"]):
            return "request"
        return "statement"

    def _estimate_cefr(self, text: str) -> str:
        words = [token.strip(".,!?") for token in text.split() if token.strip(".,!?")]
        if not words:
            return "A1"

        avg_length = sum(len(word) for word in words) / len(words)
        if avg_length >= 7:
            return "C1"
        if avg_length >= 6:
            return "B2"
        if avg_length >= 5:
            return "B1"
        if avg_length >= 4:
            return "A2"
        return "A1"

    def _adaptive_learning(self, user_cefr: str, error_rate: float, history: list[dict]) -> dict:
        base_level = CEFR_ORDER.index(user_cefr) if user_cefr in CEFR_ORDER else 0
        recent_scores = [item.get("score", 60) for item in history[-5:] if isinstance(item.get("score"), int)]
        avg_score = sum(recent_scores) / len(recent_scores) if recent_scores else 60

        level_shift = 0
        if error_rate > 0.4 or avg_score < 55:
            level_shift = -1
        elif error_rate < 0.15 and avg_score >= 80:
            level_shift = 1

        new_level_index = min(max(base_level + level_shift, 0), len(CEFR_ORDER) - 1)
        difficulty = max(1, min(new_level_index + 1, 6))

        if new_level_index <= 1:
            vocabulary_complexity = "basic"
            speech_rate = "slow"
        elif new_level_index <= 3:
            vocabulary_complexity = "intermediate"
            speech_rate = "normal"
        else:
            vocabulary_complexity = "advanced"
            speech_rate = "fast"

        return {
            "exercise_difficulty": difficulty,
            "vocabulary_complexity": vocabulary_complexity,
            "speech_rate": speech_rate,
        }

    def _score_response(self, error_rate: float, text: str) -> dict:
        length_bonus = 5 if len(text.split()) >= 12 else 0
        base_score = max(0, min(100, int((1 - error_rate) * 100) + length_bonus))
        confidence = round(min(0.98, 0.6 + (len(text.split()) / 50)), 2)
        return {"score": base_score, "confidence": confidence}

    def _build_feedback(self, original_text: str, llm_output: str, analysis: dict) -> dict:
        corrected = original_text
        if "yesterday" in original_text.lower() and " go " in f" {original_text.lower()} ":
            corrected = original_text.replace("go", "went")

        if analysis["grammar_issues"]:
            naturalness = "建議加入連接詞（例如 because, however）讓句子更自然流暢。"
        else:
            naturalness = "語句整體自然，下一步可以增加更精準的動詞與副詞。"

        alternative = f"You could also say: {corrected}"
        growth = (
            "每日 10 分鐘針對本次錯誤類型練習，並在下一次回答中使用 1~2 個新單字。"
            if analysis["grammar_issues"]
            else "維持目前表現，嘗試改寫句型來提升表達層次。"
        )

        return {
            "grammar_correction": corrected,
            "naturalness_suggestion": naturalness,
            "alternative_sentence": alternative,
            "cefr_assessment": analysis["estimated_cefr"],
            "growth_suggestion": f"{growth}（AI補充：{llm_output[:120]}）",
        }
