# English Growth AI Agent

這是一個英語學習 AI 助手 MVP，提供：
- Chat 即時串流（SSE）
- 文法/自然度/替代句型/CEFR/成長建議
- CEFR 能力評估
- Speaking（STT/TTS mock）
- Session 狀態持久化（寫入 `data/app_state.json`）

## 給一般使用者的最短操作

1. 安裝 Python 3.11+
2. 打開專案後進入 `backend` 資料夾
3. 安裝套件：`pip install -r requirements.txt`
4. 啟動服務：`uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload`
5. 開啟 API 文件：`http://127.0.0.1:8000/docs`

> 若沒有設定 API Key，系統會自動使用 mock 模式，仍可完整演示流程。

---

## QA 驗收狀態（對應 spec 第 7 節）

- [x] Chat streaming 正常（`/api/chat` + 測試）
- [x] 回饋內容完整（文法/自然度/建議）
- [x] CEFR 評估合理（A1~C1 測試案例）
- [x] 語音可正常輸入/輸出（STT/TTS mock）
- [x] session 可持久化（`data/app_state.json`）

## 文件與交付狀態（對應 spec 第 8 節）

- [x] README（完整教學）
- [x] API 文件（Swagger）
- [x] Prompt 設計文件
- [x] 測試案例（CEFR A1~C1）

---

## API 文件位置

- Swagger UI：`/docs`
- ReDoc：`/redoc`
- OpenAPI：`/openapi.json`
- 補充說明：`spec/api-swagger.md`

## Prompt 設計文件

- `spec/prompt-design.md`

## 測試

在 `backend/` 執行：

- `pytest`

涵蓋：
- Chat streaming
- 核心學習 API
- CEFR A1~C1 案例
- Session 持久化

## 設定檔

- `.env.example`：環境變數範例
- `backend/app/config.py`：讀取 `OPENAI_API_KEY`、`GEMINI_API_KEY`、`DATABASE_URL`

## 最新目錄結構

```text
english-growth-ai-agent/
├─ backend/
│  ├─ app/
│  │  ├─ main.py
│  │  ├─ learning_engine.py
│  │  ├─ speech_service.py
│  │  └─ state_store.py
│  ├─ tests/
│  │  ├─ test_chat.py
│  │  ├─ test_learning_api.py
│  │  └─ test_cefr_levels.py
│  └─ requirements.txt
├─ frontend/
├─ spec/
│  ├─ english-growth-ai-agent-spec.md
│  ├─ api-swagger.md
│  └─ prompt-design.md
├─ data/
│  └─ app_state.json (執行後自動生成)
├─ todo.md
└─ README.md
```
