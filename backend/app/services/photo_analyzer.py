"""
Photo AI Analyzer — принимает URL фото объекта и возвращает структурированный
Project Report: тип помещения, сложность, состояние поверхности, необходимость
waterproofing, примерная площадь и материалы.
"""

import json
import os
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
estimates -- flag it as approximate. Return ONLY the JSON object, no other text."""


def analyze_photo(image_url: str) -> Dict:
    if not os.getenv("ANTHROPIC_API_KEY"):
        return {
            "room_type": "other",
            "complexity": "medium",
            "surface_condition": "fair",
            "waterproofing_needed": False,
            "estimated_sqft": 50.0,
            "estimated_material_units": 55.0,
            "raw_ai_response": {"note": "ANTHROPIC_API_KEY not set -- using placeholder values"},
        }

    import anthropic

    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

    # image_url must be publicly reachable (S3 URL) for the "url" source type.
    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=300,
        system=VISION_SYSTEM_PROMPT,
        messages=[{
            "role": "user",
            "content": [
                {"type": "image", "source": {"type": "url", "url": image_url}},
                {"type": "text", "text": "Analyze this photo."},
            ],
        }],
    )
    text = response.content[0].text.strip()
    start = text.find("{")
    end = text.rfind("}")
    if start == -1 or end == -1 or end < start:
        return {
            "room_type": "other", "complexity": "medium", "surface_condition": "fair",
            "waterproofing_needed": False, "estimated_sqft": 50.0,
            "estimated_material_units": 55.0,
            "raw_ai_response": {"note": "model did not return JSON", "raw_text": text},
        }
    try:
        parsed = json.loads(text[start:end + 1])
    except json.JSONDecodeError:
        return {
            "room_type": "other", "complexity": "medium", "surface_condition": "fair",
            "waterproofing_needed": False, "estimated_sqft": 50.0,
            "estimated_material_units": 55.0,
            "raw_ai_response": {"note": "model returned malformed JSON", "raw_text": text},
        }
    parsed["raw_ai_response"] = parsed.copy()
    return parsed
