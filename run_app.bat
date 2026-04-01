@echo off
cd /d %~dp0

echo ===============================
echo 啟動 English Growth AI Agent
echo ===============================

REM ===== Backend =====
echo 啟動 Backend...
start cmd /k "cd backend && python -m venv .venv && call .venv\Scripts\activate && pip install -r requirements.txt && python -m uvicorn app.main:app --host 0.0.0.0 --port 8000"

timeout /t 5 >nul

REM ===== Frontend =====
echo 啟動 Frontend...
start cmd /k "cd frontend && npm install && npm run dev"

timeout /t 5 >nul

REM ===== 開啟瀏覽器 =====
start http://localhost:3000

pause