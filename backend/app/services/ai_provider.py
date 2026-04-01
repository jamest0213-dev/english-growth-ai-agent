import os
from typing import Dict

try:
    from openai import OpenAI
except ImportError:
    OpenAI = None


CACHE = {}

# 🔥 👉 直接寫死（先讓你能用）
API_KEY = os.getenv("OPENAI_API_KEY") or "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"


def get_ai_response(user_input: str) -> Dict:
    if user_input in CACHE:
        return {
            "ok": True,
            "mode": "cache",
            "data": CACHE[user_input]
        }

    # ❌ 沒 KEY → mock
    if not API_KEY or API_KEY == "請貼你的APIKEY" or OpenAI is None:
        result = mock_response(user_input)
        CACHE[user_input] = result["data"]
        return result

    try:
        client = OpenAI(api_key=API_KEY)

        prompt = f"""
你是一位專業英文老師，請回傳 JSON：

{{
  "reply": "自然英文回覆",
  "correction": "修正句 + 中文",
  "explanation": "教學說明",
  "cefr_level": "A1/A2/B1/B2",
  "errors": ["tense","grammar"],
  "advice": "建議"
}}

句子：
{user_input}
"""

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
        )

        content = response.choices[0].message.content

        import json, re

        match = re.search(r"\{.*\}", content, re.DOTALL)
        if not match:
            raise ValueError("No JSON")

        data = json.loads(match.group())

        CACHE[user_input] = data

        return {
            "ok": True,
            "mode": "ai",
            "data": data
        }

    except Exception as e:
        print("❌ AI ERROR:", str(e))
        result = mock_response(user_input)
        CACHE[user_input] = result["data"]
        return result


def mock_response(user_input: str) -> Dict:
    return {
        "ok": True,
        "mode": "mock",
        "data": {
            "reply": f"(mock) You said: {user_input}",
            "correction": "這是模擬修正",
            "explanation": "這是模擬教學",
            "cefr_level": "A2",
            "errors": ["grammar"],
            "advice": "多練習"
        }
    }