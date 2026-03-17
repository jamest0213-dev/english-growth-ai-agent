# API 文件（Swagger）

本專案後端使用 FastAPI，啟動後可直接使用內建 Swagger 文件。

## Swagger 入口

- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`
- OpenAPI JSON: `http://127.0.0.1:8000/openapi.json`

## 啟動方式

1. 進入 `backend/`
2. 執行：
   - `pip install -r requirements.txt`
   - `uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload`

## 驗收重點 API

- Chat Streaming: `POST /api/chat`
- 回饋內容：`POST /api/sessions/{id}/submit`、`POST /api/speaking`
- CEFR：`POST /api/assessment/submit`、`GET /api/assessment/result`
- Session 持久化：`POST /api/sessions/start` + `POST /api/sessions/{id}/submit`

所有錯誤回應皆採用：

```json
{
  "ok": false,
  "error": {
    "code": "...",
    "message": "...",
    "details": {}
  }
}
```
