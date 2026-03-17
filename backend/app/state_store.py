from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path


@dataclass
class AppState:
    users_store: dict[int, dict]
    sessions_store: dict[int, dict]
    assessments_store: dict[int, dict]
    vocabulary_store: dict[int, list[dict]]
    learning_path_store: dict[int, list[dict]]
    user_id_seq: int
    session_id_seq: int
    assessment_id_seq: int


class StateStore:
    def __init__(self, file_path: Path) -> None:
        self.file_path = file_path
        self.file_path.parent.mkdir(parents=True, exist_ok=True)

    def load(self) -> AppState:
        if not self.file_path.exists():
            return self._default_state()

        raw = json.loads(self.file_path.read_text(encoding="utf-8"))
        users_store = {
            int(key): {
                **value,
                "created_at": self._parse_datetime(value.get("created_at")),
            }
            for key, value in raw.get("users_store", {}).items()
        }

        return AppState(
            users_store=users_store,
            sessions_store={int(key): value for key, value in raw.get("sessions_store", {}).items()},
            assessments_store={int(key): value for key, value in raw.get("assessments_store", {}).items()},
            vocabulary_store={int(key): value for key, value in raw.get("vocabulary_store", {}).items()},
            learning_path_store={int(key): value for key, value in raw.get("learning_path_store", {}).items()},
            user_id_seq=int(raw.get("user_id_seq", 1)),
            session_id_seq=int(raw.get("session_id_seq", 1)),
            assessment_id_seq=int(raw.get("assessment_id_seq", 1)),
        )

    def save(self, state: AppState) -> None:
        payload = {
            "users_store": {
                str(key): {
                    **value,
                    "created_at": self._serialize_datetime(value.get("created_at")),
                }
                for key, value in state.users_store.items()
            },
            "sessions_store": {str(key): value for key, value in state.sessions_store.items()},
            "assessments_store": {str(key): value for key, value in state.assessments_store.items()},
            "vocabulary_store": {str(key): value for key, value in state.vocabulary_store.items()},
            "learning_path_store": {str(key): value for key, value in state.learning_path_store.items()},
            "user_id_seq": state.user_id_seq,
            "session_id_seq": state.session_id_seq,
            "assessment_id_seq": state.assessment_id_seq,
        }
        self.file_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    def _default_state(self) -> AppState:
        return AppState(
            users_store={},
            sessions_store={},
            assessments_store={},
            vocabulary_store={},
            learning_path_store={},
            user_id_seq=1,
            session_id_seq=1,
            assessment_id_seq=1,
        )

    def _parse_datetime(self, value: str | None) -> datetime | None:
        if not value:
            return None
        return datetime.fromisoformat(value)

    def _serialize_datetime(self, value: datetime | None) -> str | None:
        if not value:
            return None
        return value.isoformat()
