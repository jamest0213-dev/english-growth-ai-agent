import os
import json
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def analyze_english(message: str) -> dict:

    if not os.getenv("OPENAI_API_KEY"):
        return {
            "corrected_sentence": message,
            "explanation": "OPENAI_API_KEY not set",
            "cefr_level": "A1",
            "learning_tip": "Set your API key."
        }

    prompt = f"""
You are an English teacher.

Return ONLY valid JSON.

Sentence:
"{message}"

Format:
{{
  "corrected_sentence": "...",
  "explanation": "...",
  "cefr_level": "A1/A2/B1/B2/C1/C2",
  "learning_tip": "..."
}}
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.3
        )

        raw_text = response.choices[0].message.content

        start = raw_text.find("{")
        end = raw_text.rfind("}") + 1

        return json.loads(raw_text[start:end])

    except Exception as e:
        return {
            "corrected_sentence": message,
            "explanation": f"OpenAI error: {str(e)}",
            "cefr_level": "A1",
            "learning_tip": "Check billing."
        }