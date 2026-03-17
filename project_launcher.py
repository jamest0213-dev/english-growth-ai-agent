"""Windows 一鍵啟動入口：啟動 FastAPI 後端服務。"""

from __future__ import annotations

import os
import socket
import subprocess
import sys
from pathlib import Path


def _find_available_port(start_port: int, max_attempts: int = 20) -> int:
    port = start_port
    for _ in range(max_attempts):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            if sock.connect_ex(("127.0.0.1", port)) != 0:
                return port
        port += 1
    raise RuntimeError("找不到可用的連接埠，請關閉占用中的程式後重試。")


def main() -> int:
    try:
        repo_root = Path(__file__).resolve().parent
        backend_dir = repo_root / "backend"

        if not backend_dir.exists():
            print("找不到 backend 資料夾，請確認專案檔案完整。")
            return 1

        env_port = os.environ.get("BACKEND_PORT", "8000")
        try:
            preferred_port = int(env_port)
        except ValueError:
            preferred_port = 8000

        port = _find_available_port(preferred_port)
        print(f"啟動 English Growth AI Agent 後端中（Port: {port}）...")
        print(f"Swagger 文件：http://127.0.0.1:{port}/docs")

        command = [
            sys.executable,
            "-m",
            "uvicorn",
            "app.main:app",
            "--host",
            "0.0.0.0",
            "--port",
            str(port),
        ]
        process = subprocess.run(command, cwd=backend_dir)
        return process.returncode
    except KeyboardInterrupt:
        print("\n已停止服務。")
        return 0
    except Exception as exc:  # noqa: BLE001
        print("發生錯誤。請複製以下訊息並發送給您的 AI 助手：")
        print(str(exc))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
