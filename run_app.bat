@echo off
chcp 65001 > nul
setlocal enabledelayedexpansion

cd /d "%~dp0"

set "PYTHON_BOOTSTRAP="
where py >nul 2>nul
if not errorlevel 1 (
  set "PYTHON_BOOTSTRAP=py -3"
) else (
  where python >nul 2>nul
  if not errorlevel 1 (
    set "PYTHON_BOOTSTRAP=python"
  )
)

if "%PYTHON_BOOTSTRAP%"=="" (
  echo [ERROR] 找不到 Python。請先安裝 Python 3.11 以上版本，並勾選「Add python.exe to PATH」。
  pause
  exit /b 1
)

if not exist ".venv" (
  echo [INFO] 正在建立虛擬環境...
  %PYTHON_BOOTSTRAP% -m venv .venv
  if errorlevel 1 (
    echo [ERROR] 無法建立 Python 虛擬環境，請先安裝 Python 3.11 以上版本。
    pause
    exit /b 1
  )
)

call ".venv\Scripts\activate.bat"
if errorlevel 1 (
  echo [ERROR] 啟用虛擬環境失敗。
  pause
  exit /b 1
)

echo [INFO] 正在安裝/更新必要套件...
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
if errorlevel 1 (
  echo [ERROR] 套件安裝失敗，請檢查網路後重試。
  pause
  exit /b 1
)

if not exist ".env" (
  if exist ".env.example" (
    copy /Y ".env.example" ".env" > nul
    echo [INFO] 已自動建立 .env 設定檔。
  )
)

echo [INFO] 啟動應用程式中...
python project_launcher.py

endlocal
