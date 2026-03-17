# ✅ English Growth AI Agent — 開發規範（Vibe Coding版）

## TODO

### 0. 基礎準備（架構與環境）

- [x] 架構設計：
  - Frontend（Next.js / React）＋ Backend（FastAPI）前後端分離
  - LLM Provider（OpenAI / Gemini）統一 Adapter 層
  - SQLite（開發）→ PostgreSQL（正式）

- [x] Streaming 機制：
  - 採用 SSE（語音/對話/回饋即時輸出）
  - fallback：非 streaming response
  - 無 API Key → 啟用 mock（⚠️ 每次需提醒使用者為 mock）

- [x] 錯誤與 Logging：
  - 全域 try-except（主程式入口）
  - logs/ 分級：INFO / WARNING / ERROR
  - 禁止紀錄敏感資料（token / 使用者對話）

### 1. 核心資料模型（學習系統）

- [ ] users（使用者）
- [ ] learning_profiles（CEFR 等級、目標）
- [ ] sessions（學習歷程）
- [ ] exercises（題目）
- [ ] responses（使用者回答）
- [ ] feedbacks（AI回饋）
- [ ] vocabularies（單字庫）
- [ ] grammar_rules（文法）
- [ ] speaking_records（語音紀錄）
- [ ] learning_paths（學習路徑）
- [ ] progress_logs（能力成長紀錄）

### 2. 後端 API（FastAPI `/api`）

#### 使用者與學習

- [ ] POST /users
- [ ] GET /users/{id}
- [ ] GET /users/{id}/progress

#### 學習任務

- [ ] POST /sessions/start
- [ ] POST /sessions/{id}/submit
- [ ] GET /sessions/{id}/feedback

#### CEFR 評估

- [ ] POST /assessment/start
- [ ] POST /assessment/submit
- [ ] GET /assessment/result

#### 單字與文法

- [ ] GET /vocabulary
- [ ] GET /grammar
- [ ] POST /vocabulary/save

#### AI 對話（核心）

- [ ] POST /chat (SSE streaming)
- [ ] POST /speaking (語音→文字→回饋)

#### 錯誤格式統一

```json
{"ok": false, "error": {"code": "...", "message": "...", "details": {}}}
```

### 3. LLM 學習引擎（核心靈魂）

#### 能力拆解（四大核心）

- Listening（聽力）
- Speaking（口說）
- Reading（閱讀）
- Writing（寫作）

#### [ ] 自適應學習（Adaptive Learning）

- 根據：
  - CEFR 等級（A1~C2）
  - 錯誤率
  - 學習歷史
- 動態調整：
  - 題目難度
  - 單字複雜度
  - 語速

#### [ ] AI 回饋引擎

輸出必須包含：
- 文法修正
- 自然度建議
- 替代句型
- CEFR 等級判定
- 成長建議

#### [ ] Prompt Pipeline

流程：

```text
User Input
→ 分析（Grammar / Intent / CEFR）
→ LLM 回應
→ 評分（Scoring）
→ 結構化 feedback
→ 儲存 session
```

### 4. 語音系統（Speaking）

- [ ] Speech-to-Text（Whisper / Google STT）
- [ ] Text-to-Speech（ElevenLabs / Azure）
- [ ] 發音評分（簡易版先用 LLM）

### 5. 學習路徑系統（Learning Path）

- [ ] 初始能力測試 → CEFR 分級
- [ ] 自動生成學習路徑：
  - 單字
  - 文法
  - 情境對話
- [ ] 每日任務（Daily Practice）

### 6. 前端（React + TypeScript）

#### UI 原則（延續你系統風格）

- 主色：#1E3A8A（深藍）
- 輔色：#C9A96E（金色）
- 背景：#F8FAFC
- 支援 Toast（可複製）

#### [ ] 主頁（Dashboard）

- 今日學習進度
- CEFR 等級
- 成長曲線

#### [ ] 對話學習頁（Chat UI）

- 即時 streaming
- AI 角色（老師 / 面試官 / 旅遊情境）
- 顯示：
  - 修正句
  - 評分
  - 建議

#### [ ] 單字學習頁

- 單字卡（翻轉）
- 發音
- 例句

#### [ ] 寫作訓練頁

- 輸入作文
- AI 批改（Grammar + Style）

#### [ ] 口說訓練頁

- 錄音
- 即時回饋
- 發音建議

#### [ ] 進度分析頁

- CEFR 成長
- 錯誤類型統計
- 學習時間

### 7. QA 驗收

- [ ] Chat streaming 正常
- [ ] 回饋內容完整（文法/自然度/建議）
- [ ] CEFR 評估合理
- [ ] 語音可正常輸入/輸出
- [ ] session 可持久化

### 8. 文件與交付

- [ ] README（完整教學）
- [ ] API 文件（Swagger）
- [ ] Prompt 設計文件
- [ ] 測試案例（CEFR A1~C1）
