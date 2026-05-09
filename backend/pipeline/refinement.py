import json
from groq import Groq
from backend.config.settings import settings
from backend.models.schemas import (
    IntentData, SystemDesignData,
    UISchema, APISchema, DBSchema, AuthSchema, BusinessLogic
)

client = Groq(api_key=settings.GROQ_API_KEY)

REFINEMENT_PROMPT = """
You are a senior software architect doing a final review.
Check all schemas for inconsistencies and fix them.

Return ONLY valid JSON with the corrected schemas in this exact structure:
{{
    "ui_schema": {{ "pages": [], "layouts": {{}}, "components": {{}} }},
    "api_schema": {{ "base_url": "/api/v1", "endpoints": [] }},
    "db_schema": {{ "tables": [], "relationships": [] }},
    "auth_schema": {{ "roles": [], "permissions": {{}}, "protected_routes": [], "premium_gates": [] }},
    "business_logic": {{ "free_limits": {{}}, "premium_features": [], "validation_rules": [], "notification_triggers": [] }},
    "assumptions": ["list of assumptions made"],
    "changes_made": ["list of changes made during refinement"]
}}

Check for these issues:
1. Every UI form field has a matching API endpoint
2. Every API field exists as a DB column
3. Every protected route has an auth rule
4. Premium features are gated by premium role
5. All foreign keys reference existing tables
6. No missing required fields in any schema

Current Schemas:
UI: {ui_schema}
API: {api_schema}
DB: {db_schema}
Auth: {auth_schema}
Business Logic: {business_logic}
"""

def refine_schemas(
    intent: IntentData,
    design: SystemDesignData,
    ui_schema: UISchema,
    api_schema: APISchema,
    db_schema: DBSchema,
    auth_schema: AuthSchema,
    business_logic: BusinessLogic,
    mode: str = "balanced"
) -> tuple[UISchema, APISchema, DBSchema, AuthSchema, BusinessLogic, list, list]:
    """
    Stage 4 — Refine and fix inconsistencies across all schemas
    """
    temperature = {
        "fast": settings.TEMPERATURE_FAST,
        "balanced": settings.TEMPERATURE_BALANCED,
        "quality": settings.TEMPERATURE_QUALITY
    }.get(mode, settings.TEMPERATURE_BALANCED)

    print(f"🔧 Stage 4: Refining schemas...")

    if mode == "fast":
        print("⚡ Fast mode — skipping deep refinement")
        return ui_schema, api_schema, db_schema, auth_schema, business_logic, [], []

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            temperature=temperature,
            max_tokens=4096,
            messages=[
                {
                    "role": "user",
                    "content": REFINEMENT_PROMPT.format(
                        ui_schema=json.dumps(ui_schema.model_dump(), indent=2),
                        api_schema=json.dumps(api_schema.model_dump(), indent=2),
                        db_schema=json.dumps(db_schema.model_dump(), indent=2),
                        auth_schema=json.dumps(auth_schema.model_dump(), indent=2),
                        business_logic=json.dumps(business_logic.model_dump(), indent=2)
                    )
                }
            ]
        )

        raw = response.choices[0].message.content.strip()
        raw = raw.replace("```json", "").replace("```", "").strip()
        data = json.loads(raw)

        refined_ui = UISchema(**data["ui_schema"])
        refined_api = APISchema(**data["api_schema"])
        refined_db = DBSchema(**data["db_schema"])
        refined_auth = AuthSchema(**data["auth_schema"])
        refined_biz = BusinessLogic(**data["business_logic"])
        assumptions = data.get("assumptions", [])
        changes = data.get("changes_made", [])

        print(f"✅ Stage 4 Done — Changes made: {len(changes)}")
        return refined_ui, refined_api, refined_db, refined_auth, refined_biz, assumptions, changes

    except Exception as e:
        print(f"⚠️ Refinement failed ({e}), returning original schemas")
        return ui_schema, api_schema, db_schema, auth_schema, business_logic, [], []