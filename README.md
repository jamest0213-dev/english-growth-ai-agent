# English Growth AI Agent

English Growth AI Agent 是一個以 **CEFR 分級、聽說讀寫、AI 回饋、學習歷程** 為核心的英文學習專案。  
目前以 **Windows 本地啟動穩定** 為第一優先，先完成 Stage 0 / Stage 0.5 驗收，再逐步擴充功能。

---

## 1) Windows 本地啟動（Stage 0）

> 建議環境：Windows 10/11、Python 3.11+、Node.js 20+

### 步驟 A：設定環境變數

1. 複製 `frontend/.env.example` 為 `frontend/.env.local`
2. 複製 `backend/.env.example` 為 `backend/.env`

前端至少要有：

```env
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
```

若尚未準備 API Key，可先留空，系統會自動進入 **Mock 模式**。

---

### 步驟 B：啟動 Backend（FastAPI）

在 PowerShell：

```powershell
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

健康檢查：

- 瀏覽器開啟 `http://localhost:8000/healthz`
- 預期回應：`{"status":"ok"}`

---

### 步驟 C：啟動 Frontend（Next.js）

另開一個 PowerShell：

```powershell
cd frontend
npm install
npm run dev
```

瀏覽器開啟：

- `http://localhost:3000`

---

## 2) 前後端連線驗收（Stage 0）

- 前端讀取 `NEXT_PUBLIC_API_BASE_URL`
- 前端可呼叫後端 API
- 若後端未啟動，前端仍可開啟，不會白屏
- API 失敗時會顯示友善繁中訊息（例如：系統暫時無法連線）

---

## 3) 最小鏈路（Stage 0.5）

### Backend 最小 API

- `GET /healthz`
- `POST /api/chat`（SSE Streaming）
- `POST /api/chat/complete`（非串流備援）

### Frontend 最小功能

- 可輸入訊息
- 可送出到 `/api/chat`
- 可顯示 AI 回應
- 無 API Key 時進入 Mock 模式，畫面會明確顯示「目前為模擬模式（Mock）」

---

## 4) 一鍵啟動（Mode B / 交付模式）

根目錄提供：

- `run_app.bat`

可雙擊啟動（會協助檢查並啟動前後端）。

---

## 5) 常見錯誤排查

### Q1：前端顯示「系統暫時無法連線」

- 請先確認後端終端機是否正在執行 `uvicorn`
- 確認 `frontend/.env.local` 的 `NEXT_PUBLIC_API_BASE_URL` 是否正確
- 確認 Windows 防火牆未阻擋 `8000`

### Q2：`/healthz` 無法開啟

- 確認埠號是否被占用
- 可改用：

```powershell
uvicorn app.main:app --reload --host 0.0.0.0 --port 8001
```

若改成 8001，請同步更新 `frontend/.env.local`：

```env
NEXT_PUBLIC_API_BASE_URL=http://localhost:8001
```

### Q3：沒有 API Key 能用嗎？

可以。系統會自動切換到 Mock 模式，供流程測試與 UI 驗收。

---

## 6) 測試（Backend）

```powershell
cd backend
pytest
```

---

## 7) 專案結構（節錄）

```text
english-growth-ai-agent/
├─ backend/
│  ├─ app/
│  ├─ tests/
│  └─ .env.example
├─ frontend/
│  ├─ app/
│  └─ .env.example
├─ run_app.bat
└─ README.md
```
