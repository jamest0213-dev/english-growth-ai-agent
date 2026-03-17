# English Growth AI Agent 現況盤點與 Release 1 缺口分析

> 目的：根據 `spec/english-growth-ai-agent-spec.md` 與目前程式碼現況，整理「已完成能力、未完成項目、架構缺點、Release 1 上線前必要步驟」。

## 1) 目前已完成的功能（以可運作能力為主）

### 1.1 後端 API 與流程（MVP 可用）
- 已提供使用者、學習任務、CEFR 評估、單字/文法、聊天、口說、學習路徑、每日任務等 API。
- `/api/chat` 已用 SSE 串流回傳 chunk；同時有 `/api/chat/complete` 非串流模式可用。
- 錯誤處理採統一格式，並有全域例外攔截。
- 狀態會寫入 `data/app_state.json`，啟動後可延續上次資料（user/session/assessment/vocabulary/learning_path）。

### 1.2 LLM 與語音服務
- 已有 OpenAI / Gemini / Mock 統一 Adapter，並支援 fallback（API Key 缺失自動 mock）。
- 已有語音服務介面：STT（text 或 base64）與 TTS（mock/provider 介面），口說 API 可回傳發音分數。

### 1.3 前端介面（展示型 MVP）
- 已有 Dashboard、Chat、Vocabulary、Writing、Speaking、Analysis 六個頁籤介面。
- Chat 有串流接收流程；Toast 支援複製訊息。
- 視覺主色/輔色/背景色與 spec 設計方向一致。

### 1.4 測試與啟動
- 後端 `pytest` 測試已覆蓋主流程（chat/learning/speaking/assessment/持久化等）。
- 根目錄有 `run_app.bat` + `project_launcher.py`，可在 Windows 建立 `.venv`、安裝套件、啟動後端。

## 2) 對照規格後，仍未做到或僅做到「骨架」的部分

## 2.1 前端尚未達「可正式教學使用」
- Dashboard/Analysis 目前是固定假資料，尚未串接真實學習數據。
- Vocabulary/Writing/Speaking 仍偏示範流程，缺少完整 CRUD 與歷史資料管理。
- Speaking 頁面的「錄音」是狀態切換示意，非真正麥克風錄音與音訊上傳流程。

## 2.2 串流策略未完全一致
- 規格要求 LLM 輸出全面 streaming，但寫作頁目前呼叫 `/api/chat/complete` 走非串流。
- Gemini `stream()` 目前為一次性回傳 complete 結果，不是真正分塊串流。

## 2.3 資料層與 API 存在雙軌（技術債）
- 雖然已建立 SQLAlchemy models 與 Alembic migration，但主 API 目前仍以記憶體 dict + `app_state.json` 為主。
- 導致資料一致性、查詢能力、併發安全、後續報表分析能力受限。

## 2.4 Release 級產品尚缺的營運功能
- 缺少登入/權限（至少匿名 session 或最小身分識別策略）。
- 缺少可觀測性（API latency、error rate、trace ID）與告警。
- 缺少部署與版本升級流程文件（正式環境 DB migration runbook、回滾策略）。

## 3) 目前架構上的主要缺點（風險排序）

1. **資料存取分裂（最高風險）**  
   ORM 與 migration 已在，但 API 還沒切到資料庫，造成「看起來有資料模型，實際服務不吃 DB」的落差。Release 後一旦流量增加，記憶體 store 與檔案持久化會成為瓶頸。

2. **前端與後端契約未完全產品化**  
   前端多數區塊仍是展示資料；即使 API 已有功能，使用者端仍感知不到完整產品價值。

3. **串流一致性不足**  
   chat 是串流、writing 不是、Gemini pseudo-stream；對使用者體驗與錯誤恢復策略會產生不一致。

4. **啟動流程偏後端導向**  
   一鍵啟動目前主要服務 Swagger；若要給一般使用者，還缺「前端 UI 一起開」與「可直接進入學習頁」。

5. **缺少正式營運保護欄**  
   尚無最低限度的身份隔離、速率限制、監控告警、備份策略，對 Release 1 風險較高。

## 4) 若目標是 Release 1（可讓一般使用者使用），建議必做步驟

## 4.1 先定義 Release 1 範圍（避免過度擴張）
- 只保留 3 條主流程：
  1) 註冊/建立學習者 → CEFR 初始評估  
  2) 每日任務（chat + writing + speaking 至少兩種）  
  3) 進度回顧（本週分數、錯誤類型、建議）

## 4.2 後端資料層收斂（必要）
- 把 users/sessions/responses/feedbacks/progress_logs 的讀寫切換到 SQLAlchemy。
- 保留 `app_state.json` 僅作 dev fallback，不作正式資料來源。
- 補 migration smoke test 與 seed script。

## 4.3 前端產品化（必要）
- Dashboard/Analysis 改為讀實際 API。
- Writing 改成串流輸出（與 chat 體驗一致）。
- Speaking 補真正錄音與音訊預覽（至少可上傳 wav/webm + 回傳 transcript）。
- 補完整 CRUD：單字收藏可新增、編輯、刪除與搜尋。

## 4.4 可維運與交付（必要）
- 一鍵啟動改為「前後端同時啟動」或提供單一入口（例如本機打開前端 URL）。
- 增加 `.env.example` 的正式說明（OpenAI/Gemini key、DB URL、CORS）。
- 建立 release checklist：測試、migration、回滾、備份、監控。

## 4.5 上線門檻（DoD）
- 功能：3 條主流程 E2E 可跑通。
- 品質：關鍵 API 測試 + 前端 smoke test 全綠。
- 體驗：所有 AI 輸出皆串流、錯誤訊息皆中文可操作。
- 交付：Windows 使用者解壓後雙擊即可啟動前後端並打開瀏覽器。
