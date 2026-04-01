def generate_recommendation(weakness: dict):
    if not weakness:
        return {
            "focus": "基礎句型",
            "advice": "建議從簡單英文句子開始練習"
        }

    # 找最大弱點
    main_weakness = max(weakness, key=weakness.get)

    if main_weakness == "tense":
        return {
            "focus": "時態（過去式）",
            "advice": "請加強動詞過去式，例如 go → went, eat → ate"
        }

    if main_weakness == "grammar":
        return {
            "focus": "文法結構",
            "advice": "請注意句型結構，例如主詞 + 動詞 + 受詞"
        }

    if main_weakness == "vocabulary":
        return {
            "focus": "單字量",
            "advice": "建議每天記5個常用單字並造句"
        }

    return {
        "focus": "基礎英文",
        "advice": "持續練習簡單句子"
    }