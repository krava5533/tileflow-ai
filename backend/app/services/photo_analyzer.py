"""
Photo AI Analyzer — принимает URL фото объекта и возвращает структурированный
Project Report: тип помещения, сложность, состояние поверхности, необходимость
waterproofing, примерная площадь и материалы.

VISION_SYSTEM_PROMPT ниже — это то, что реально отправляется в vision-модель
в проде. Сейчас analyze_photo() возвращает разумные дефолты, чтобы можно было
тестировать весь flow (upload → analysis → estimate) без живого API-ключа.
"""

from typing import Dict

VISION_SYSTEM_PROMPT = """You are a tile installation estimator analyzing a photo
of a room submitted by a potential customer. Look at the image and return ONLY
a JSON object with these fields:

{
  "room_type": "bathroom | kitchen | floor | shower | backsplash | outdoor_patio | other",
  "complexity": "low | medium | high",
  "surface_condition": "good | fair | poor",
  "waterproofing_needed": true | false,
  "estimated_sqft": <number>,
  "estimated_material_units": <number, tiles or boxes needed at standard coverage>
}

Base "complexity" on: number of corners/edges, fixtures to work around, uneven
surfaces, and existing tile that needs removal. Be conservative with sqft
estimates — flag it as approximate."""


def analyze_photo(image_url: str) -> Dict:
    """
    Replace this body with a real call, e.g.:

        import anthropic, json
        client = anthropic.Anthropic()
        response = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=300,
            system=VISION_SYSTEM_PROMPT,
            messages=[{
                "role": "user",
                "content": [
                    {"type": "image", "source": {"type": "url", "url": image_url}},
                    {"type": "text", "text": "Analyze this photo."}
                ]
            }]
        )
        return json.loads(response.content[0].text)
    """
    return {
        "room_type": "bathroom",
        "complexity": "medium",
        "surface_condition": "fair",
        "waterproofing_needed": True,
        "estimated_sqft": 45.0,
        "estimated_material_units": 50.0,
        "raw_ai_response": {"note": "stubbed response — connect vision API"},
    }
