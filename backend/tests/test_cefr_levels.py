from app.learning_engine import LearningEngine


engine = LearningEngine()


def test_cefr_estimation_a1_to_c1_examples() -> None:
    cases = [
        ("I am Tom.", "A1"),
        ("I enjoy music every weekend.", "A2"),
        ("I always practice English after class.", "B1"),
        ("Students discuss global issues during regular classes.", "B2"),
        ("Interdisciplinary collaboration accelerates organizational transformation sustainably.", "C1"),
    ]

    for text, expected in cases:
        assert engine._estimate_cefr(text) == expected
