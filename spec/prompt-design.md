# Prompt 設計文件

本文件說明 English Growth AI Agent 在「對話批改」與「口說回饋」流程中，如何產生可驗收的結構化學習回饋。

## 1. 設計目標

- 固定輸出五大欄位：
  - 文法修正（grammar_correction）
  - 自然度建議（naturalness_suggestion）
  - 替代句型（alternative_sentence）
  - CEFR 評估（cefr_assessment）
  - 成長建議（growth_suggestion）
- 支援 streaming 與 non-streaming 一致體驗。
- 在無 API Key 或 provider 失敗時，自動 fallback mock 並提供警示。

## 2. Prompt Pipeline（實作對應）

程式流程：

1. 使用者輸入（文字或語音轉寫）
2. 先做本地規則分析（文法錯誤、意圖、CEFR 預估）
3. 呼叫 LLM（OpenAI / Gemini / Mock）
4. 合成結構化 feedback
5. 進行 score 與 adaptive plan
6. 回傳 API 並保存 session state

## 3. 對話/口說任務 Prompt 原則

- 任務語氣：英文學習教練，鼓勵但具體。
- 優先順序：
  1) 先修正文法
  2) 再給自然語感替代句
  3) 最後給可執行的下一步練習
- CEFR 建議策略：
  - 依句子平均詞長與錯誤率估計
  - 不直接跳級到 C2（MVP 先穩定 A1~C1）

## 4. 輸出結構（契約）

API `pipeline.feedback` 保證具備下列欄位：

```json
{
  "grammar_correction": "...",
  "naturalness_suggestion": "...",
  "alternative_sentence": "...",
  "cefr_assessment": "A1|A2|B1|B2|C1|C2",
  "growth_suggestion": "..."
}
```

## 5. 失敗情境策略

- API key 缺失：使用 mock，並回傳 warning。
- Provider 中斷：streaming 時保留已輸出 chunk，後續切換 mock 補完。
- 驗證失敗：統一錯誤格式 `{ok:false,error:{...}}`。

## 6. 驗收對應

- QA「回饋內容完整」對應：本文件第 1 節固定欄位。
- QA「CEFR 評估合理」對應：第 3 節 CEFR 策略 + `backend/tests/test_cefr_levels.py`。
- QA「Chat streaming 正常」對應：`/api/chat` SSE + `backend/tests/test_chat.py`。
