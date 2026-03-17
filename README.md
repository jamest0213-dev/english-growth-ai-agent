# English Growth AI Agent MVP - Stage 0

目前已完成 **Stage 0（基礎準備）**：前後端分離、LLM Adapter、SSE Streaming + fallback、以及全域錯誤與 logging。

## 本階段完成項目
- 前端：Next.js + TypeScript + TailwindCSS 骨架
- 後端：FastAPI 架構
- LLM 統一 Adapter：OpenAI / Gemini / Mock
- Streaming：`/api/chat/stream`（SSE）
- fallback：`/api/chat`（非串流）
- 無 API Key 時自動使用 Mock，且每次回應附上提醒訊息
- 全域錯誤處理（`Exception Handler` + 主程式入口 `try-except`）
- logs 分級輸出：`logs/info.log`、`logs/warning.log`、`logs/error.log`
- 敏感資料遮罩（token / api key）
- 開發環境預設 SQLite，正式環境可切 PostgreSQL

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
│   │   │   ├── adapters.py
│   │   │   ├── base.py
│   │   │   └── service.py
│   │   ├── config.py
│   │   ├── database.py
│   │   ├── logging_config.py
│   │   ├── main.py
│   │   ├── models.py
│   │   └── schemas.py
│   ├── tests/
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

## API 範例
- 非串流 fallback：`POST /api/chat`
- 串流 SSE：`POST /api/chat/stream`

## 測試
```bash
cd backend
pytest
```
