# English Growth AI Agent 開發待辦（依 `spec/english-growth-ai-agent-spec.md` 整理）

## 0) 基礎準備（架構與環境）
- [x] 完成前後端分離架構（Next.js Frontend + FastAPI Backend）
  - [x] 建立 frontend 專案骨架（Next.js + TypeScript + Tailwind）
  - [x] 建立 backend 專案骨架（FastAPI）
- [x] 完成資料層基礎設計（開發 PostgreSQL 流程，保留 SQLite→PostgreSQL 遷移策略）
  - [x] 建立 SQLAlchemy + Alembic 設定
  - [x] 建立第一版 migration
  - [x] 建立 PostgreSQL docker-compose 設定
- [x] 完成 LLM Provider Adapter（OpenAI / Gemini）
  - [x] 建立統一 Provider 介面
  - [x] 實作 OpenAI Adapter
  - [x] 實作 Gemini Adapter
  - [x] 補齊 Provider 切換設定（含無 API Key mock）
- [x] 完成 Streaming 與 fallback 機制
  - [x] 實作 SSE 串流基礎元件（後端）
  - [x] 實作前端串流消費器（chat/speaking）
  - [x] 實作非 streaming fallback
  - [x] 無 API Key 自動切換 mock，並在回應中顯示提醒
- [x] 完成全域錯誤處理與 Logging
  - [x] 主程式入口全域 try-except
  - [x] logs/ 分級輸出（INFO/WARNING/ERROR）
  - [x] 設定敏感資訊遮罩（token/對話內容）

## 1) 核心資料模型（學習系統）
- [x] users（使用者）
- [x] learning_profiles（CEFR 等級、目標）
- [x] sessions（學習歷程）
- [x] exercises（題目）
- [x] responses（使用者回答）
- [x] feedbacks（AI 回饋）
- [x] vocabularies（單字庫）
- [x] grammar_rules（文法）
- [x] speaking_records（語音紀錄）
- [x] learning_paths（學習路徑）
- [x] progress_logs（能力成長紀錄）

## 2) 後端 API（FastAPI `/api`）
### 2.1 使用者與學習
- [x] POST `/users`
- [x] GET `/users/{id}`
- [x] GET `/users/{id}/progress`

### 2.2 學習任務
- [x] POST `/sessions/start`
- [x] POST `/sessions/{id}/submit`
- [x] GET `/sessions/{id}/feedback`

### 2.3 CEFR 評估
- [x] POST `/assessment/start`
- [x] POST `/assessment/submit`
- [x] GET `/assessment/result`

### 2.4 單字與文法
- [x] GET `/vocabulary`
- [x] GET `/grammar`
- [x] POST `/vocabulary/save`

### 2.5 AI 對話（核心）
- [x] POST `/chat`（SSE streaming）
- [x] POST `/speaking`（語音→文字→回饋）

### 2.6 API 一致性
- [x] 統一錯誤格式
  - [x] 全 API 回傳 `{ok:false,error:{code,message,details}}`
  - [x] 建立例外到錯誤碼映射

## 3) LLM 學習引擎（核心）
- [x] 建立四大能力模組（Listening / Speaking / Reading / Writing）
- [x] 自適應學習（Adaptive Learning）
  - [x] 依 CEFR 等級調整題目
  - [x] 依錯誤率動態調整難度
  - [x] 依學習歷史調整單字複雜度與語速
- [x] AI 回饋引擎
  - [x] 文法修正
  - [x] 自然度建議
  - [x] 替代句型
  - [x] CEFR 等級判定
  - [x] 成長建議
- [x] Prompt Pipeline
  - [x] User Input 分析（Grammar / Intent / CEFR）
  - [x] LLM 回應
  - [x] Scoring
  - [x] 結構化 feedback
  - [x] session 儲存

## 4) 語音系統（Speaking）
- [x] Speech-to-Text（Whisper / Google STT，MVP 先提供 provider 介面與 mock 轉寫）
- [x] Text-to-Speech（ElevenLabs / Azure，MVP 先提供 provider 介面與 mock 音訊）
- [x] 發音評分（先用簡易啟發式與 LLM 回饋整合）

## 5) 學習路徑系統（Learning Path）
- [x] 初始能力測試 → CEFR 分級
- [x] 自動生成學習路徑
  - [x] 單字
  - [x] 文法
  - [x] 情境對話
- [x] 每日任務（Daily Practice）

## 6) 前端（React + TypeScript）
- [x] 套用 UI Design Token
  - [x] 主色 #1E3A8A
  - [x] 輔色 #C9A96E
  - [x] 背景 #F8FAFC
  - [x] Toast（支援可複製內容）
- [x] Dashboard（今日學習進度/CEFR/成長曲線）
- [x] Chat UI（即時串流 + 角色切換 + 修正句/評分/建議）
- [x] 單字學習頁（翻轉卡/發音/例句）
- [x] 寫作訓練頁（輸入作文 + AI 批改）
- [x] 口說訓練頁（錄音 + 即時回饋 + 發音建議）
- [x] 進度分析頁（CEFR 成長/錯誤類型/學習時間）

## 7) QA 驗收
- [x] Chat streaming 正常
- [x] 回饋內容完整（文法/自然度/建議）
- [x] CEFR 評估合理（rule-based MVP）
- [x] 語音可正常輸入/輸出（文字模擬 STT）
- [x] session 可持久化

## 8) 文件與交付
- [x] README（初版啟動教學與目錄結構）
- [x] README（最終版完整教學）
- [x] API 文件（Swagger）
- [x] Prompt 設計文件
- [x] 測試案例（CEFR A1~C1）

## 9) 目前已完成的基礎項目（延續既有成果）
- [x] `/healthz` endpoint
- [x] backend 基本測試（pytest）
- [x] 基本 lint 設定（ruff / next lint）
- [x] `.env.example`

## 10) 本次交付打包項目（Windows 一鍵啟動）
- [x] 新增根目錄 `requirements.txt`
- [x] 新增根目錄 `run_app.bat`
- [x] 新增根目錄 `project_launcher.py`
- [x] 將 `.env.example` 複製為 `.env`
- [x] 產出可下載 ZIP 交付檔

## 11) Release 1 上線前缺口清單（2026-03 盤點）
- [ ] 將主要 API 的資料來源由記憶體 store 收斂到 SQLAlchemy + PostgreSQL/SQLite
- [ ] Dashboard/Analysis 前端改為串接真實 API，移除固定假資料
- [ ] Writing 改為 Streaming（移除 `/api/chat/complete` 依賴）
- [ ] Speaking 補真實錄音上傳與音訊預覽（非僅切換狀態）
- [ ] Vocabulary 補齊 CRUD（新增/編輯/刪除/搜尋）
- [x] run_app 一鍵啟動改為可同時開啟前後端並導向前端首頁
- [ ] 新增 release checklist（migration/備份/回滾/監控）
