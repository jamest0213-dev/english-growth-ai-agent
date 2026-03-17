# English Growth AI Agent MVP - Stage 1 API + Stage 0 Foundation

目前已完成：
- ✅ Stage 0（基礎架構）
- ✅ Stage 1（核心 API MVP）

系統已具備完整後端 API、資料模型、LLM 串流與基礎前後端架構，可進行實際開發與測試。

---

## 本階段完成項目

### 🔹 基礎架構（Stage 0）
- 前端：Next.js + TypeScript + TailwindCSS 骨架
- 後端：FastAPI 架構
- LLM Adapter：OpenAI / Gemini / Mock
- Streaming：`/api/chat/stream`（SSE）
- fallback：`/api/chat`（非串流）
- 無 API Key 自動 fallback Mock
- 全域錯誤處理（Exception Handler + try-except）
- logs 分級：
  - `logs/info.log`
  - `logs/warning.log`
  - `logs/error.log`
- 敏感資料遮罩（token / api key）
- SQLite（dev） / PostgreSQL（prod）
- Alembic migration
- `GET /healthz` 健康檢查

---

### 🔹 核心學習資料模型（Stage 1 基礎）
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

---

### 🔹 後端 API（Stage 1 MVP）
- 使用者與學習
  - `POST /api/users`
  - `GET /api/users/{id}`
  - `GET /api/users/{id}/progress`

- 學習任務
  - `POST /api/sessions/start`
  - `POST /api/sessions/{id}/submit`
  - `GET /api/sessions/{id}/feedback`

- CEFR 評估
  - `POST /api/assessment/start`
  - `POST /api/assessment/submit`
  - `GET /api/assessment/result`

- 單字與文法
  - `GET /api/vocabulary`
  - `GET /api/grammar`
  - `POST /api/vocabulary/save`

- AI 對話
  - `POST /api/chat`（SSE streaming）
  - `POST /api/chat/stream`（舊路徑相容）
  - `POST /api/chat/complete`（非串流 fallback）

- Speaking
  - `POST /api/speaking`（文字模擬語音評估）

---

### 🔹 錯誤格式統一
```json
{
  "ok": false,
  "error": {
    "code": "...",
    "message": "...",
    "details": {}
  }
}