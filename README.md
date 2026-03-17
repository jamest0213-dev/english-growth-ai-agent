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
  - `POST /api/speaking`（支援 STT/TTS provider 參數與發音評分）

- Learning Path
  - `POST /api/learning-path/generate`（依 CEFR 產生單字/文法/情境對話路徑）
  - `GET /api/users/{id}/daily-practice`（每日任務）

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
```

---

## 前端 Stage 6 完成狀態（React + TypeScript）

已完成並可在單一頁籤式介面中操作：
- Dashboard：今日學習進度、CEFR 等級、成長曲線
- 對話學習頁：SSE 串流、AI 角色切換、修正句/評分/建議
- 單字學習頁：翻轉單字卡、發音、例句
- 寫作訓練頁：輸入作文、AI 批改（Grammar + Style）
- 口說訓練頁：錄音狀態切換、即時回饋、發音建議分數
- 進度分析頁：CEFR 成長、錯誤類型統計、學習時間
- Toast：支援一鍵複製訊息

## 最新目錄結構

```text
english-growth-ai-agent/
├─ backend/
│  ├─ app/
│  └─ tests/
├─ frontend/
│  ├─ app/
│  │  ├─ globals.css
│  │  ├─ layout.tsx
│  │  └─ page.tsx
│  ├─ package.json
│  └─ tsconfig.json
├─ spec/
│  └─ english-growth-ai-agent-spec.md
├─ README.md
└─ todo.md
```
