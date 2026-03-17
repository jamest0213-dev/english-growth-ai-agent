# English Growth AI Agent MVP - Stage 0 Scaffold

這一版已完成 **Stage 0 專案骨架 + 核心學習資料模型（Stage 1 部分）**，讓你可以快速在本機啟動前後端與資料庫，並具備核心資料表。

## 本階段包含
- Next.js + TypeScript + TailwindCSS 前端骨架
- FastAPI 後端骨架
- PostgreSQL（Docker）
- Alembic migration 設定與第一版 migration
- `GET /healthz` 健康檢查 API
- 核心學習資料模型（users / learning_profiles / sessions / exercises / responses / feedbacks / vocabularies / grammar_rules / speaking_records / learning_paths / progress_logs）
- 基本 lint / test 設定（Ruff + Pytest + Next lint）

## 本階段尚未包含
- 驗證登入（JWT）
- AI 整合
- CEFR 測評邏輯
- 每日任務與學習流程

## 目錄結構
```text
.
├── .env.example
├── docker-compose.yml
├── backend
│   ├── alembic
│   │   ├── env.py
│   │   ├── script.py.mako
│   │   └── versions
│   │       ├── 20261017_0001_create_user_progress.py
│   │       └── 20261017_0002_add_learning_system_core_tables.py
│   ├── app
│   │   ├── config.py
│   │   ├── database.py
│   │   ├── main.py
│   │   └── models.py
│   ├── tests
│   │   ├── test_healthz.py
│   │   └── test_models.py
│   ├── alembic.ini
│   ├── Dockerfile
│   ├── pyproject.toml
│   └── requirements.txt
├── frontend
│   ├── app
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
```

## 快速開始（建議）
1. 複製環境變數檔：
   ```bash
   cp .env.example .env
   ```
2. 啟動全部服務：
   ```bash
   docker compose up --build
   ```
3. 開啟：
   - Frontend: http://localhost:3000
   - Backend health: http://localhost:8000/healthz

## 僅測試 migration
```bash
docker compose up -d db
docker compose run --rm backend alembic upgrade head
```

## 本機（不使用 Docker）
### Backend
```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
alembic upgrade head
uvicorn app.main:app --reload
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

## 測試與檢查
### Backend
```bash
cd backend
pytest
ruff check .
```

### Frontend
```bash
cd frontend
npm install
npm run lint
```
