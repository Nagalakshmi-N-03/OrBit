import json
from groq import Groq
from backend.config.settings import settings
from backend.models.schemas import (
    IntentData, SystemDesignData,
    UISchema, APISchema, DBSchema, AuthSchema, BusinessLogic
)

client = Groq(api_key=settings.GROQ_API_KEY)

UI_PROMPT = """
You are a UI architect. Generate a complete UI schema.

Return ONLY valid JSON:
{{
    "pages": [
        {{
            "name": "PageName",
            "route": "/route",
            "access": ["roles that can access"],
            "components": ["list of components on this page"],
            "forms": [
                {{
                    "name": "FormName",
                    "fields": [
                        {{
                            "name": "fieldName",
                            "type": "text/email/password/select/date",
                            "required": true
                        }}
                    ]
                }}
            ]
        }}
    ],
    "layouts": {{
        "authenticated": "sidebar + navbar",
        "public": "centered"
    }},
    "components": {{
        "shared": ["list of shared components"]
    }}
}}

Rules:
- Return ONLY JSON, no markdown, no backticks
- Every page must have at least 2 components
- Include Login and Register pages always

Intent: {intent}
Design: {design}
"""

API_PROMPT = """
You are a backend architect. Generate a complete REST API schema.

Return ONLY valid JSON:
{{
    "base_url": "/api/v1",
    "endpoints": [
        {{
            "path": "/resource",
            "method": "GET",
            "description": "what this endpoint does",
            "auth_required": true,
            "roles_allowed": ["admin"],
            "request_body": {{
                "field": "type"
            }},
            "response": {{
                "field": "type"
            }}
        }}
    ]
}}

Rules:
- Return ONLY JSON, no markdown, no backticks
- Include CRUD endpoints for every entity
- Always include auth endpoints (login, register, logout)
- Mark which endpoints need authentication

Intent: {intent}
Design: {design}
"""

DB_PROMPT = """
You are a database architect. Generate a complete database schema.

Return ONLY valid JSON:
{{
    "tables": [
        {{
            "name": "table_name",
            "columns": [
                {{
                    "name": "id",
                    "type": "UUID",
                    "primary_key": true,
                    "nullable": false,
                    "unique": true,
                    "default": null
                }}
            ]
        }}
    ],
    "relationships": [
        {{
            "from_table": "table1",
            "to_table": "table2",
            "type": "one_to_many",
            "foreign_key": "column_name"
        }}
    ]
}}

Rules:
- Return ONLY JSON, no markdown, no backticks
- Every table must have an id column (UUID)
- Every table must have created_at timestamp
- Include users table always

Intent: {intent}
Design: {design}
"""

AUTH_PROMPT = """
You are a security architect. Generate a complete auth and permissions schema.

Return ONLY valid JSON:
{{
    "roles": ["admin", "user"],
    "permissions": {{
        "admin": ["create", "read", "update", "delete"],
        "user": ["read", "update"]
    }},
    "protected_routes": ["/api/v1/dashboard", "/api/v1/admin"],
    "premium_gates": ["advanced_analytics", "exports"]
}}

Rules:
- Return ONLY JSON, no markdown, no backticks
- Every role must have explicit permissions
- Super admin always has all permissions
- List every protected API route

Intent: {intent}
Design: {design}
"""

BUSINESS_PROMPT = """
You are a product architect. Generate complete business logic rules.

Return ONLY valid JSON:
{{
    "free_limits": {{
        "projects": "max 3 projects",
        "members": "max 5 members per project"
    }},
    "premium_features": ["unlimited_projects", "advanced_analytics", "exports"],
    "validation_rules": ["email must be unique", "password min 8 chars"],
    "notification_triggers": ["task assigned", "deadline approaching", "comment added"]
}}

Rules:
- Return ONLY JSON, no markdown, no backticks
- Define clear free vs premium limits
- Cover all validation rules for forms
- List all notification events

Intent: {intent}
Design: {design}
"""


def _call_groq(prompt: str, mode: str, max_tokens: int = 2048) -> dict:
    temperature = {
        "fast": settings.TEMPERATURE_FAST,
        "balanced": settings.TEMPERATURE_BALANCED,
        "quality": settings.TEMPERATURE_QUALITY
    }.get(mode, settings.TEMPERATURE_BALANCED)

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        temperature=temperature,
        max_tokens=max_tokens,
        messages=[{"role": "user", "content": prompt}]
    )

    raw = response.choices[0].message.content.strip()
    raw = raw.replace("```json", "").replace("```", "").strip()
    return json.loads(raw)


def generate_schemas(
    intent: IntentData,
    design: SystemDesignData,
    mode: str = "balanced"
) -> tuple[UISchema, APISchema, DBSchema, AuthSchema, BusinessLogic]:
    """
    Stage 3 — Generate all 4 schemas + business logic
    """
    print(f"⚙️  Stage 3: Generating schemas...")

    intent_str = json.dumps(intent.model_dump(), indent=2)
    design_str = json.dumps(design.model_dump(), indent=2)

    print("   → Generating UI Schema...")
    ui_data = _call_groq(UI_PROMPT.format(intent=intent_str, design=design_str), mode, 2048)
    ui_schema = UISchema(**ui_data)

    print("   → Generating API Schema...")
    api_data = _call_groq(API_PROMPT.format(intent=intent_str, design=design_str), mode, 2048)
    api_schema = APISchema(**api_data)

    print("   → Generating DB Schema...")
    db_data = _call_groq(DB_PROMPT.format(intent=intent_str, design=design_str), mode, 2048)
    db_schema = DBSchema(**db_data)

    print("   → Generating Auth Schema...")
    auth_data = _call_groq(AUTH_PROMPT.format(intent=intent_str, design=design_str), mode, 1024)
    auth_schema = AuthSchema(**auth_data)

    print("   → Generating Business Logic...")
    biz_data = _call_groq(BUSINESS_PROMPT.format(intent=intent_str, design=design_str), mode, 1024)
    business_logic = BusinessLogic(**biz_data)

    print(f"✅ Stage 3 Done — UI: {len(ui_schema.pages)} pages | API: {len(api_schema.endpoints)} endpoints | DB: {len(db_schema.tables)} tables")
    return ui_schema, api_schema, db_schema, auth_schema, business_logic