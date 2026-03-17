# English Growth AI Agent MVP - Stage 1 API 完整化

目前已補齊 spec 第 2 章的 FastAPI `/api` 主要端點（MVP 版本，採用記憶體儲存），包含使用者、學習任務、CEFR 評估、單字文法、SSE 對話與 speaking 回饋。

## 本階段完成項目
- 後端 API：
  - 使用者與學習：`POST /api/users`、`GET /api/users/{id}`、`GET /api/users/{id}/progress`
  - 學習任務：`POST /api/sessions/start`、`POST /api/sessions/{id}/submit`、`GET /api/sessions/{id}/feedback`
  - CEFR 評估：`POST /api/assessment/start`、`POST /api/assessment/submit`、`GET /api/assessment/result`
  - 單字與文法：`GET /api/vocabulary`、`GET /api/grammar`、`POST /api/vocabulary/save`
  - AI 對話：`POST /api/chat`（SSE streaming）
  - Speaking：`POST /api/speaking`（文字模擬語音轉文字→回饋）
- 相容保留：`POST /api/chat/stream`（舊路徑）與 `POST /api/chat/complete`（非串流 fallback）
- 錯誤格式統一：
  ```json
  {"ok": false, "error": {"code": "...", "message": "...", "details": {}}}
  ```
- 測試擴充：新增 API flow 測試與錯誤格式測試

## 目錄結構
```text
.
├── .env.example
├── docker-compose.yml
├── logs/
├── spec/
├── backend
│   ├── alembic/
│   ├── app
│   │   ├── llm/
│   │   ├── config.py
│   │   ├── database.py
│   │   ├── logging_config.py
│   │   ├── main.py
│   │   ├── models.py
│   │   └── schemas.py
│   ├── tests/
│   │   ├── test_chat.py
│   │   ├── test_healthz.py
│   │   └── test_learning_api.py
│   ├── requirements.txt
│   └── pyproject.toml
├── frontend/
└── todo.md
```

## 啟動方式
1. 複製環境變數
   ```bash
   cp .env.example .env
   ```
2. 啟動服務
   ```bash
   docker compose up --build
   ```
3. 開啟網址
   - Frontend: http://localhost:3000
   - Backend health: http://localhost:8000/healthz
   - Swagger: http://localhost:8000/docs

## 測試
```bash
cd backend
pytest
```
