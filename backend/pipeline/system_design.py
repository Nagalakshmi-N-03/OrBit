import json
from groq import Groq
from backend.config.settings import settings
from backend.models.schemas import IntentData, SystemDesignData

client = Groq(api_key=settings.GROQ_API_KEY)

SYSTEM_DESIGN_PROMPT = """
You are a senior software architect.
Design the full system architecture for this app.

Return ONLY a valid JSON object:
{{
    "pages": ["Login", "Register", "Dashboard", "list all pages"],
    "entities": {{
        "EntityName": {{
            "fields": ["id", "name", "created_at"],
            "relations": ["related entity names"]
        }}
    }},
    "user_flows": [
        "User registers and logs in",
        "User creates a project"
    ],
    "data_flows": [
        "User submits form -> API -> Database"
    ],
    "architecture_notes": [
        "JWT used for authentication"
    ]
}}

Rules:
- Return ONLY JSON, no explanation, no markdown, no backticks
- Include Login and Register pages always
- Keep pages list concise (max 10 pages)
- Keep entities concise (max 6 entities)

App Intent:
{intent}
"""

def design_system(intent: IntentData, mode: str = "balanced") -> SystemDesignData:
    temperature = {
        "fast": settings.TEMPERATURE_FAST,
        "balanced": settings.TEMPERATURE_BALANCED,
        "quality": settings.TEMPERATURE_QUALITY
    }.get(mode, settings.TEMPERATURE_BALANCED)

    print(f"🏗️  Stage 2: Designing system architecture...")

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        temperature=temperature,
        max_tokens=1200,
        messages=[
            {
                "role": "user",
                "content": SYSTEM_DESIGN_PROMPT.format(
                    intent=json.dumps(intent.model_dump(), indent=2)
                )
            }
        ]
    )

    raw = response.choices[0].message.content.strip()
    raw = raw.replace("```json", "").replace("```", "").strip()

    data = json.loads(raw)
    design = SystemDesignData(**data)
    print(f"✅ Stage 2 Done — Pages: {len(design.pages)} | Entities: {len(design.entities)}")
    return design
