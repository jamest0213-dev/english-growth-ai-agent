from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_user_session_assessment_and_vocab_flow() -> None:
    user_res = client.post("/api/users", json={"learner_name": "Amy", "cefr_level": "A2"})
    assert user_res.status_code == 200
    user_payload = user_res.json()
    user_id = user_payload["id"]

    get_user_res = client.get(f"/api/users/{user_id}")
    assert get_user_res.status_code == 200
    assert get_user_res.json()["learner_name"] == "Amy"

    session_start_res = client.post("/api/sessions/start", json={"user_id": user_id, "topic": "Travel"})
    assert session_start_res.status_code == 200
    session_id = session_start_res.json()["session_id"]

    submit_res = client.post(f"/api/sessions/{session_id}/submit", json={"answer": "I go to airport yesterday."})
    assert submit_res.status_code == 200
    assert submit_res.json()["feedback"]
    submit_payload = submit_res.json()
    assert "pipeline" in submit_payload
    assert submit_payload["pipeline"]["feedback"]["grammar_correction"]
    assert submit_payload["pipeline"]["feedback"]["cefr_assessment"]
    assert submit_payload["pipeline"]["adaptive_plan"]["speech_rate"]

    feedback_res = client.get(f"/api/sessions/{session_id}/feedback")
    assert feedback_res.status_code == 200
    feedback_payload = feedback_res.json()
    assert feedback_payload["pipeline"]["scoring"]["score"] >= 0

    assessment_start = client.post("/api/assessment/start", json={"user_id": user_id})
    assert assessment_start.status_code == 200
    assessment_id = assessment_start.json()["assessment_id"]

    assessment_submit = client.post(
        "/api/assessment/submit",
        json={"assessment_id": assessment_id, "user_id": user_id, "answers": ["a", "b", "c", "d", "e", "f"]},
    )
    assert assessment_submit.status_code == 200
    assert assessment_submit.json()["cefr_level"] == "B1"

    result_res = client.get(f"/api/assessment/result?assessment_id={assessment_id}&user_id={user_id}")
    assert result_res.status_code == 200

    vocab_res = client.get("/api/vocabulary")
    assert vocab_res.status_code == 200
    assert len(vocab_res.json()["items"]) >= 1

    grammar_res = client.get("/api/grammar")
    assert grammar_res.status_code == 200
    assert len(grammar_res.json()["items"]) >= 1

    vocab_save_res = client.post(
        "/api/vocabulary/save", json={"user_id": user_id, "word": "resilient", "meaning": "有韌性的"}
    )
    assert vocab_save_res.status_code == 200

    speaking_res = client.post(
        "/api/speaking",
        json={
            "text": "I am practicing speaking every day.",
            "cefr_level": "A2",
            "enable_tts": True,
            "tts_provider": "azure",
        },
    )
    assert speaking_res.status_code == 200
    assert speaking_res.json()["transcript"]
    assert speaking_res.json()["pipeline"]["feedback"]["naturalness_suggestion"]
    assert speaking_res.json()["pronunciation_score"] >= 45
    assert speaking_res.json()["tts_audio_base64"]

    speaking_stt_res = client.post(
        "/api/speaking",
        json={
            "audio_base64": "U1RUIERFTU8=",
            "stt_provider": "whisper",
            "cefr_level": "A2",
        },
    )
    assert speaking_stt_res.status_code == 200
    assert speaking_stt_res.json()["transcript"].startswith("[mock-whisper]")

    learning_path_res = client.post("/api/learning-path/generate", json={"user_id": user_id})
    assert learning_path_res.status_code == 200
    path_payload = learning_path_res.json()
    assert len(path_payload["path"]) == 3
    assert {task["category"] for task in path_payload["path"]} == {"vocabulary", "grammar", "conversation"}

    daily_practice_res = client.get(f"/api/users/{user_id}/daily-practice")
    assert daily_practice_res.status_code == 200
    daily_payload = daily_practice_res.json()
    assert daily_payload["total_estimated_minutes"] > 0
    assert len(daily_payload["tasks"]) == 3

    progress_res = client.get(f"/api/users/{user_id}/progress")
    assert progress_res.status_code == 200
    progress_payload = progress_res.json()
    assert progress_payload["total_sessions"] == 1
    assert progress_payload["completed_sessions"] == 1
    assert progress_payload["saved_vocabulary_count"] == 1
