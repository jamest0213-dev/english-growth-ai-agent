from fastapi import FastAPI, Body
from fastapi.middleware.cors import CORSMiddleware
import random
from datetime import datetime

app = FastAPI()

# ===== CORS =====
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ===== Health Check =====
@app.get("/healthz")
def healthz():
    return {"status": "ok"}


# ===== 記憶體 =====
HISTORY = []


# ===== 儲存紀錄（關鍵）=====
def save_history(user_text="", score=None, cefr=None):
    print("🔥 save_history 被呼叫")  # Debug用

    HISTORY.append({
        "user_text": user_text,
        "score": score,
        "cefr": cefr,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M")
    })

    print("🔥 HISTORY 長度:", len(HISTORY))


# ===== Chat =====
@app.post("/api/chat")
async def chat(data: dict = Body(...)):
    user_text = data.get("message", "")

    if not user_text:
        return {
            "ok": False,
            "error": {
                "code": "INVALID_INPUT",
                "message": "請輸入句子",
                "details": ""
            }
        }

    corrected = user_text.capitalize()
    cefr = random.choice(["A1", "A2", "B1"])

    # ✅ 這行是關鍵（一定要有）
    save_history(user_text=user_text, score=None, cefr=cefr)

    return {
        "ok": True,
        "data": {
            "corrected": corrected,
            "cefr": cefr,
            "suggestion": "可以再自然一點"
        }
    }


# ===== Speaking =====
@app.post("/api/speaking/score")
async def speaking_score(data: dict = Body(...)):
    user_text = data.get("user_text", "")
    reference = data.get("reference", "")

    if not user_text or not reference:
        return {
            "ok": False,
            "error": {
                "code": "INVALID_INPUT",
                "message": "缺少語音內容或標準句",
                "details": ""
            }
        }

    score = random.randint(70, 95)
    cefr = random.choice(["A1", "A2", "B1"])

    # ✅ 這行也是關鍵
    save_history(user_text=user_text, score=score, cefr=cefr)

    return {
        "ok": True,
        "data": {
            "score": score,
            "cefr": cefr,
            "feedback": "發音不錯"
        }
    }


# ===== History =====
@app.get("/api/history")
def get_history():
    return {
        "ok": True,
        "data": HISTORY[::-1][:10]
    }


# ===== Recommendation API（任務核心） =====
@app.get("/api/recommendation")
def recommendation():
    return {
        "ok": True,
        "data": {
            "weakness": "基礎句型",
            "suggestion": "建議練習主詞 + 動詞句型",
            "next_action": "請完成 3 句英文描述今天的行程"
        }
    }