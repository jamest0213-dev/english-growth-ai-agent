
# English Growth AI Agent MVP - Stage 0

目前已完成 **Stage 0（基礎準備）**，並納入 **Stage 1 部分核心學習資料模型**，可快速在本機啟動前後端與資料庫，並具備可延伸的基礎架構。

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
- Alembic migration 設定與初始 migration
- `GET /healthz` 健康檢查 API
- 核心學習資料模型：
  - `users`
  - `learning_profiles`
  - `sessions`
  - `exercises`
  - `responses`
  - `feedbacks`
  - `vocabularies`
  - `grammar_rules`
  - `speaking_records`
  - `learning_paths`
  - `progress_logs`

## 本階段尚未包含
- 驗證登入（JWT）
- AI 個人化教學策略深化
- CEFR 正式測評邏輯
- 每日任務與完整學習流程編排
- 正式版權限管理與後台營運功能

## 目錄結構
```text
.
├── .env.example
├── docker-compose.yml
├── logs/
├── spec/
├── backend/
│   ├── alembic/
│   │   ├── env.py
│   │   ├── script.py.mako
│   │   └── versions/
│   │       ├── 20261017_0001_create_user_progress.py
│   │       └── 20261017_0002_add_learning_system_core_tables.py
│   ├── app/
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
│   │   ├── test_healthz.py
│   │   └── test_models.py
│   ├── alembic.ini
│   ├── Dockerfile
│   ├── pyproject.toml
│   └── requirements.txt
├── frontend/
│   ├── app/
│   │   ├── globals.css
│   │   ├── layout.tsx
│   │   └── page.tsx
│   ├── .eslintrc.json
│   ├── Dockerfile
│   ├── next.config.js
│   ├── package.json
│   ├── postcss.config.js
│   ├── tailwind.config.ts
│   └── tsconfig.json
└── todo.md