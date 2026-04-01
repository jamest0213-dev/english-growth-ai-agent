import random
import datetime
import os

try:
    from openai import OpenAI
except ImportError:
    OpenAI = None


# =========================
# ✅ 快取（一天一次）
# =========================
DAILY_CACHE = {
    "date": None,
    "data": None
}


TOPICS = ["Travel", "Food", "Work", "Shopping", "Health"]


def generate_mock():
    return {
        "topic": random.choice(TOPICS),
        "vocabularies": [
            {"word": "reservation", "meaning": "預約"},
            {"word": "schedule", "meaning": "行程"},
            {"word": "delicious", "meaning": "美味的"},
            {"word": "appointment", "meaning": "預約"},
            {"word": "comfortable", "meaning": "舒適的"},
        ],
        "conversation": {
            "en": "I would like to make a reservation.",
            "zh": "我想要訂位。"
        },
        "summary": "今天請練習基本生活英文對話。"
    }


def generate_ai():
    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key or OpenAI is None:
        return generate_mock()

    try:
        client = OpenAI(api_key=api_key)

        prompt = """
請產生今日英文學習內容，回傳 JSON：

{
  "topic": "主題",
  "vocabularies": [
    {"word": "單字", "meaning": "中文"},
    ...
  ],
  "conversation": {
    "en": "英文句子",
    "zh": "中文翻譯"
  },
  "summary": "今日學習整理（中文）"
}

規則：
1. vocab 必須 5 個
2. conversation 要簡單
3. summary 要白話
"""

        res = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )

        import json
        return json.loads(res.choices[0].message.content)

    except Exception:
        return generate_mock()


def get_daily():
    today = str(datetime.date.today())

    # ✅ 如果今天已經生成 → 直接回傳
    if DAILY_CACHE["date"] == today:
        return DAILY_CACHE["data"]

    # ✅ 生成新內容（AI 或 mock）
    data = generate_ai()

    # ✅ 存入 cache
    DAILY_CACHE["date"] = today
    DAILY_CACHE["data"] = data

    return data