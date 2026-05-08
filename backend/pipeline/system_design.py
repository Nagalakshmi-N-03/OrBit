import json
from openai import OpenAI
from backend.config.settings import settings
from backend.models.schemas import IntentData, SystemDesignData

client = OpenAI(api_key=settings.OPENAI_API_KEY)

SYSTEM_DESIGN_PROMPT = """
You are a senior software architect.
Based on the extracted app intent below, design the full system architecture.

Return ONLY a valid JSON object with this exact structure:
{{
    "pages": ["list of all pages in the app"],
    "entities": {{
        "EntityName": {{
            "fields": ["field1", "field2"],
            "relations": ["related entity names"]
        }}
    }},
    "user_flows": [
        "describe each main user flow as a string"
    ],
    "data_flows": [
        "describe how data moves between parts"
    ],
    "architecture_notes": [
        "important design decisions made"
    ]
}}

Rules:
- Return ONLY JSON, no explanation, no markdown, no backticks
- Pages must cover all features mentioned
- Every role must have at least one unique page
- Entities must cover all data needs
- Include auth pages always (Login, Register)

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
        model="gpt-4o-mini",
        temperature=temperature,
        max_tokens=2048,
        messages=[{
            "role": "user",
            "content": SYSTEM_DESIGN_PROMPT.format(
                intent=json.dumps(intent.model_dump(), indent=2)
            )
        }]
    )

    raw = response.choices[0].message.content.strip()
    raw = raw.replace("```json", "").replace("```", "").strip()
    data = json.loads(raw)

    design = SystemDesignData(**data)
    print(f"✅ Stage 2 Done — Pages: {len(design.pages)} | Entities: {len(design.entities)}")
    return design