"""Windows 一鍵啟動入口：同時啟動 FastAPI 後端與 Next.js 前端。"""

from __future__ import annotations

import os
import shutil
import socket
import subprocess
import sys
import time
import urllib.error
import urllib.request
import webbrowser
from pathlib import Path


def _find_available_port(start_port: int, max_attempts: int = 20) -> int:
    port = start_port
    for _ in range(max_attempts):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            if sock.connect_ex(("127.0.0.1", port)) != 0:
                return port
        port += 1
    raise RuntimeError("找不到可用的連接埠，請關閉占用中的程式後重試。")


def _wait_for_backend_ready(port: int, timeout_seconds: int = 30) -> bool:
    deadline = time.time() + timeout_seconds
    healthz_url = f"http://127.0.0.1:{port}/healthz"
    while time.time() < deadline:
        try:
            with urllib.request.urlopen(healthz_url, timeout=2) as response:
                if response.status == 200:
                    return True
        except (urllib.error.URLError, TimeoutError):
            time.sleep(0.5)
    return False


def _frontend_command() -> list[str]:
    npm_name = "npm.cmd" if os.name == "nt" else "npm"
    return [npm_name, "run", "dev"]


def main() -> int:
    backend_process: subprocess.Popen | None = None
    frontend_process: subprocess.Popen | None = None

    try:
        repo_root = Path(__file__).resolve().parent
        backend_dir = repo_root / "backend"
        frontend_dir = repo_root / "frontend"

        if not backend_dir.exists():
            print("找不到 backend 資料夾，請確認專案檔案完整。")
            return 1

        env_port = os.environ.get("BACKEND_PORT", "8000")
        try:
            preferred_backend_port = int(env_port)
        except ValueError:
            preferred_backend_port = 8000

        backend_port = _find_available_port(preferred_backend_port)
        frontend_port = _find_available_port(3000)

        backend_env = os.environ.copy()
        backend_env["CORS_ALLOW_ORIGINS"] = ",".join(
            [
                f"http://localhost:{frontend_port}",
                f"http://127.0.0.1:{frontend_port}",
            ]
        )

        print(f"啟動後端中（Port: {backend_port}）...")
        backend_process = subprocess.Popen(
            [
                sys.executable,
                "-m",
                "uvicorn",
                "app.main:app",
                "--host",
                "0.0.0.0",
                "--port",
                str(backend_port),
            ],
            cwd=backend_dir,
            env=backend_env,
        )

        if not _wait_for_backend_ready(backend_port):
            print("[ERROR] 後端啟動逾時，請稍後重試。")
            return 1

        frontend_url = f"http://127.0.0.1:{frontend_port}"

        if not frontend_dir.exists():
            print("找不到 frontend 資料夾，將只開啟後端 Swagger 文件。")
            webbrowser.open(f"http://127.0.0.1:{backend_port}/docs")
            backend_process.wait()
            return backend_process.returncode

        if shutil.which("node") is None:
            print("[WARN] 尚未安裝 Node.js，無法啟動前端。")
            print(f"目前可先使用 Swagger 文件：http://127.0.0.1:{backend_port}/docs")
            webbrowser.open(f"http://127.0.0.1:{backend_port}/docs")
            backend_process.wait()
            return backend_process.returncode

        npm_name = "npm.cmd" if os.name == "nt" else "npm"
        if shutil.which(npm_name) is None:
            print("[WARN] 找不到 npm，無法啟動前端。")
            print(f"目前可先使用 Swagger 文件：http://127.0.0.1:{backend_port}/docs")
            webbrowser.open(f"http://127.0.0.1:{backend_port}/docs")
            backend_process.wait()
            return backend_process.returncode

        next_binary = frontend_dir / "node_modules" / ".bin" / ("next.cmd" if os.name == "nt" else "next")
        if not next_binary.exists():
            print("正在安裝/修復前端套件（約需 1~3 分鐘）...")
            install = subprocess.run([npm_name, "install"], cwd=frontend_dir)
            if install.returncode != 0:
                print("[ERROR] 前端套件安裝失敗，請檢查網路後重試。")
                return install.returncode

        frontend_env = os.environ.copy()
        frontend_env["NEXT_PUBLIC_API_BASE_URL"] = f"http://127.0.0.1:{backend_port}"

        print(f"啟動前端中（Port: {frontend_port}）...")
        frontend_process = subprocess.Popen(
            [*_frontend_command(), "--", "-p", str(frontend_port)],
            cwd=frontend_dir,
            env=frontend_env,
        )

        print(f"前端首頁：{frontend_url}")
        print(f"後端文件：http://127.0.0.1:{backend_port}/docs")
        webbrowser.open(frontend_url)

        while True:
            backend_code = backend_process.poll()
            frontend_code = frontend_process.poll()

            if backend_code is not None:
                print(f"[ERROR] 後端已停止，結束碼：{backend_code}")
                return backend_code

            if frontend_code is not None:
                print(f"[ERROR] 前端已停止，結束碼：{frontend_code}")
                return frontend_code

            time.sleep(1)

    except KeyboardInterrupt:
        print("\n已停止服務。")
        return 0
    except Exception as exc:  # noqa: BLE001
        print("發生錯誤。請複製以下訊息並發送給您的 AI 助手：")
        print(str(exc))
        return 1
    finally:
        if frontend_process and frontend_process.poll() is None:
            frontend_process.terminate()
        if backend_process and backend_process.poll() is None:
            backend_process.terminate()


if __name__ == "__main__":
    raise SystemExit(main())
