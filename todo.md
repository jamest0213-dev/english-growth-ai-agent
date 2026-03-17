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
  - [ ] 實作前端串流消費器（chat/speaking）
  - [x] 實作非 streaming fallback
  - [x] 無 API Key 自動切換 mock，並在回應中顯示提醒
- [x] 完成全域錯誤處理與 Logging
  - [x] 主程式入口全域 try-except
  - [x] logs/ 分級輸出（INFO/WARNING/ERROR）
  - [x] 設定敏感資訊遮罩（token/對話內容）

## 1) 核心資料模型（學習系統）
- [ ] users（使用者）
- [ ] learning_profiles（CEFR 等級、目標）
- [ ] sessions（學習歷程）
- [ ] exercises（題目）
- [ ] responses（使用者回答）
- [ ] feedbacks（AI 回饋）
- [ ] vocabularies（單字庫）
- [ ] grammar_rules（文法）
- [ ] speaking_records（語音紀錄）
- [ ] learning_paths（學習路徑）
- [ ] progress_logs（能力成長紀錄）

## 2) 後端 API（FastAPI `/api`）
### 2.1 使用者與學習
- [ ] POST `/users`
- [ ] GET `/users/{id}`
- [ ] GET `/users/{id}/progress`

### 2.2 學習任務
- [ ] POST `/sessions/start`
- [ ] POST `/sessions/{id}/submit`
- [ ] GET `/sessions/{id}/feedback`

### 2.3 CEFR 評估
- [ ] POST `/assessment/start`
- [ ] POST `/assessment/submit`
- [ ] GET `/assessment/result`

### 2.4 單字與文法
- [ ] GET `/vocabulary`
- [ ] GET `/grammar`
- [ ] POST `/vocabulary/save`

### 2.5 AI 對話（核心）
- [ ] POST `/chat`（SSE streaming）
- [ ] POST `/speaking`（語音→文字→回饋）

### 2.6 API 一致性
- [ ] 統一錯誤格式
  - [ ] 全 API 回傳 `{ok:false,error:{code,message,details}}`
  - [ ] 建立例外到錯誤碼映射

## 3) LLM 學習引擎（核心）
- [ ] 建立四大能力模組（Listening / Speaking / Reading / Writing）
- [ ] 自適應學習（Adaptive Learning）
  - [ ] 依 CEFR 等級調整題目
  - [ ] 依錯誤率動態調整難度
  - [ ] 依學習歷史調整單字複雜度與語速
- [ ] AI 回饋引擎
  - [ ] 文法修正
  - [ ] 自然度建議
  - [ ] 替代句型
  - [ ] CEFR 等級判定
  - [ ] 成長建議
- [ ] Prompt Pipeline
  - [ ] User Input 分析（Grammar / Intent / CEFR）
  - [ ] LLM 回應
  - [ ] Scoring
  - [ ] 結構化 feedback
  - [ ] session 儲存

## 4) 語音系統（Speaking）
- [ ] Speech-to-Text（Whisper / Google STT）
- [ ] Text-to-Speech（ElevenLabs / Azure）
- [ ] 發音評分（先用 LLM 版本）

## 5) 學習路徑系統（Learning Path）
- [ ] 初始能力測試 → CEFR 分級
- [ ] 自動生成學習路徑
  - [ ] 單字
  - [ ] 文法
  - [ ] 情境對話
- [ ] 每日任務（Daily Practice）

## 6) 前端（React + TypeScript）
- [ ] 套用 UI Design Token
  - [ ] 主色 #1E3A8A
  - [ ] 輔色 #C9A96E
  - [ ] 背景 #F8FAFC
  - [ ] Toast（支援可複製內容）
- [ ] Dashboard（今日學習進度/CEFR/成長曲線）
- [ ] Chat UI（即時串流 + 角色切換 + 修正句/評分/建議）
- [ ] 單字學習頁（翻轉卡/發音/例句）
- [ ] 寫作訓練頁（輸入作文 + AI 批改）
- [ ] 口說訓練頁（錄音 + 即時回饋 + 發音建議）
- [ ] 進度分析頁（CEFR 成長/錯誤類型/學習時間）

## 7) QA 驗收
- [ ] Chat streaming 正常
- [ ] 回饋內容完整（文法/自然度/建議）
- [ ] CEFR 評估合理
- [ ] 語音可正常輸入/輸出
- [ ] session 可持久化

## 8) 文件與交付
- [x] README（初版啟動教學與目錄結構）
- [ ] README（最終版完整教學）
- [ ] API 文件（Swagger）
- [ ] Prompt 設計文件
- [ ] 測試案例（CEFR A1~C1）

## 9) 目前已完成的基礎項目（延續既有成果）
- [x] `/healthz` endpoint
- [x] backend 基本測試（pytest）
- [x] 基本 lint 設定（ruff / next lint）
- [x] `.env.example`
