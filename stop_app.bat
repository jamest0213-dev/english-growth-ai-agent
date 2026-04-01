@echo off

echo ===============================
echo Stopping English Growth AI Agent
echo ===============================

for /f "tokens=5" %%a in ('netstat -ano ^| findstr :3000') do taskkill /PID %%a /F >nul 2>nul
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :8000') do taskkill /PID %%a /F >nul 2>nul

echo Done.

pause