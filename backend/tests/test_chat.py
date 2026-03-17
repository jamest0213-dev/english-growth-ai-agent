from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_chat_stream_contains_warning_and_done_event() -> None:
    with client.stream("POST", "/api/chat", json={"message": "Hi"}) as response:
        assert response.status_code == 200
        raw = "".join([chunk.decode("utf-8") for chunk in response.iter_raw()])

    assert '"type": "warning"' in raw
    assert '"type": "done"' in raw


def test_chat_complete_fallback_to_mock_without_api_key() -> None:
    response = client.post("/api/chat/complete", json={"message": "Hello"})

    assert response.status_code == 200
    payload = response.json()
    assert payload["ok"] is True
    assert payload["is_mock"] is True
    assert "Mock" in payload["content"]
    assert payload["warning"]


def test_chat_validation_error_format() -> None:
    response = client.post("/api/chat", json={"message": ""})

    assert response.status_code == 422
    payload = response.json()
    assert payload["ok"] is False
    assert payload["error"]["code"] == "VALIDATION_ERROR"
