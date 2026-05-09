import json
from groq import Groq
from backend.config.settings import settings
from backend.models.schemas import IntentData

client = Groq(api_key=settings.GROQ_API_KEY)

INTENT_PROMPT = """
You are an expert software architect AI.
Your job is to extract structured intent from a user's app description.

Analyze the prompt and return ONLY a valid JSON object with this exact structure:
{{
    "app_type": "string (e.g. CRM, Project Management, E-Commerce)",
    "app_name": "string (suggest a good name)",
    "features": ["list", "of", "features"],
    "roles": ["list", "of", "user", "roles"],
    "entities": ["list", "of", "data", "entities"],
    "has_payments": true,
    "has_analytics": true,
    "has_notifications": true,
    "confidence": 0.85,
    "clarification_needed": false,
    "clarification_question": null
}}

Rules:
- Return ONLY JSON, no explanation, no markdown, no backticks
- If prompt is too vague (under 5 words with no features), set clarification_needed to true
- confidence should reflect how well you understood the prompt (0.0 to 1.0)
- Always include at least 2 roles minimum
- Always include at least 3 entities minimum

User Prompt: {prompt}
"""

def extract_intent(prompt: str, mode: str = "balanced") -> IntentData:
    """
    Stage 1 — Extract intent from user prompt
    """
    temperature = {
        "fast": settings.TEMPERATURE_FAST,
        "balanced": settings.TEMPERATURE_BALANCED,
        "quality": settings.TEMPERATURE_QUALITY
    }.get(mode, settings.TEMPERATURE_BALANCED)

    print(f"🔍 Stage 1: Extracting intent from prompt...")

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        temperature=temperature,
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": INTENT_PROMPT.format(prompt=prompt)
            }
        ]
    )

    raw = response.choices[0].message.content.strip()
    raw = raw.replace("```json", "").replace("```", "").strip()

    data = json.loads(raw)
    intent = IntentData(**data)
    print(f"✅ Stage 1 Done — App: {intent.app_name} | Confidence: {intent.confidence}")
    return intent