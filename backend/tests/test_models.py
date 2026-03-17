import app.models  # noqa: F401

from app.database import Base


def test_learning_system_core_tables_registered() -> None:
    expected_tables = {
        "users",
        "learning_profiles",
        "sessions",
        "exercises",
        "responses",
        "feedbacks",
        "vocabularies",
        "grammar_rules",
        "speaking_records",
        "learning_paths",
        "progress_logs",
    }

    assert expected_tables.issubset(set(Base.metadata.tables.keys()))
