from __future__ import annotations

import logging
import re
from logging.handlers import RotatingFileHandler
from pathlib import Path

LOG_DIR = Path(__file__).resolve().parents[2] / "logs"


class SensitiveDataFilter(logging.Filter):
    """Redact token/key-like values if they appear in logs."""

    _pattern = re.compile(r"(?i)(api[_-]?key|token|authorization)\s*[=:]\s*[^\s,;]+")

    def filter(self, record: logging.LogRecord) -> bool:
        message = record.getMessage()
        redacted = self._pattern.sub(r"\1=[REDACTED]", message)
        record.msg = redacted
        record.args = ()
        return True


def configure_logging() -> None:
    LOG_DIR.mkdir(parents=True, exist_ok=True)

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    logger.handlers.clear()

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    info_handler = RotatingFileHandler(LOG_DIR / "info.log", maxBytes=1_000_000, backupCount=3)
    info_handler.setLevel(logging.INFO)
    info_handler.addFilter(lambda r: r.levelno == logging.INFO)
    info_handler.addFilter(SensitiveDataFilter())
    info_handler.setFormatter(formatter)

    warning_handler = RotatingFileHandler(
        LOG_DIR / "warning.log", maxBytes=1_000_000, backupCount=3
    )
    warning_handler.setLevel(logging.WARNING)
    warning_handler.addFilter(lambda r: r.levelno == logging.WARNING)
    warning_handler.addFilter(SensitiveDataFilter())
    warning_handler.setFormatter(formatter)

    error_handler = RotatingFileHandler(LOG_DIR / "error.log", maxBytes=1_000_000, backupCount=3)
    error_handler.setLevel(logging.ERROR)
    error_handler.addFilter(lambda r: r.levelno >= logging.ERROR)
    error_handler.addFilter(SensitiveDataFilter())
    error_handler.setFormatter(formatter)

    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)
    stream_handler.addFilter(SensitiveDataFilter())
    stream_handler.setFormatter(formatter)

    logger.addHandler(info_handler)
    logger.addHandler(warning_handler)
    logger.addHandler(error_handler)
    logger.addHandler(stream_handler)
