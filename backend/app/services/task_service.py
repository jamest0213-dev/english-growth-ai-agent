from app.services.progress_store import get_dashboard
from app.services.daily_service import get_daily


def generate_tasks():
    dashboard = get_dashboard()
    daily = get_daily()

    tasks = []

    # 任務1：單字
    tasks.append({
        "type": "vocab",
        "title": "學習今日5個單字",
        "detail": [v["word"] for v in daily["vocabularies"]],
        "status": "pending"
    })

    # 任務2：句子練習
    tasks.append({
        "type": "practice",
        "title": "用英文造句（至少1句）",
        "detail": "請使用今日主題練習一句英文",
        "status": "pending"
    })

    # 任務3：弱點加強
    weakness = dashboard.get("weakness", {})

    if weakness:
        main = max(weakness, key=weakness.get)
        tasks.append({
            "type": "weakness",
            "title": f"加強 {main}",
            "detail": f"請針對 {main} 多練習3句",
            "status": "pending"
        })

    return tasks