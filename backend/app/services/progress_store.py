from datetime import date

SESSIONS = []
LAST_DATE = None
STREAK = 0


def save_session(user_input: str, ai_result: dict):
    global LAST_DATE, STREAK

    today = date.today()

    # ✅ streak 計算
    if LAST_DATE is None:
        STREAK = 1
    else:
        diff = (today - LAST_DATE).days

        if diff == 1:
            STREAK += 1
        elif diff > 1:
            STREAK = 1

    LAST_DATE = today

    session = {
        "input": user_input,
        "cefr": ai_result.get("cefr_level"),
        "errors": ai_result.get("errors", [])
    }

    SESSIONS.append(session)


def get_dashboard():
    total = len(SESSIONS)

    if total == 0:
        return {
            "total_sessions": 0,
            "avg_cefr": "A1",
            "last_cefr": "A1",
            "history": [],
            "weakness": {},
            "streak": 0
        }

    last = SESSIONS[-1]["cefr"]

    cefr_order = ["A1", "A2", "B1", "B2", "C1", "C2"]
    levels = [s["cefr"] for s in SESSIONS if s["cefr"] in cefr_order]

    if levels:
        avg_index = int(sum([cefr_order.index(l) for l in levels]) / len(levels))
        avg_cefr = cefr_order[avg_index]
    else:
        avg_cefr = "A1"

    # ✅ 錯誤統計
    error_count = {}
    for s in SESSIONS:
        for e in s.get("errors", []):
            error_count[e] = error_count.get(e, 0) + 1

    return {
        "total_sessions": total,
        "avg_cefr": avg_cefr,
        "last_cefr": last,
        "history": levels,
        "weakness": error_count,
        "streak": STREAK  # 🔥 新增
    }