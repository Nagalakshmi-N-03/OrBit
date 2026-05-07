import json
import anthropic
from backend.config.settings import settings
from backend.models.schemas import (
    IntentData, SystemDesignData,
    UISchema, APISchema, DBSchema, AuthSchema, BusinessLogic
)

client = anthropic.Anthropic(api_key=settings.ANTHROPIC_API_KEY)

# ─────────────────────────────────────────
# UI SCHEMA PROMPT
# ─────────────────────────────────────────

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
                            "required": true/false
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

# ─────────────────────────────────────────
# API SCHEMA PROMPT
# ─────────────────────────────────────────

API_PROMPT = """
You are a backend architect. Generate a complete REST API schema.

Return ONLY valid JSON:
{{
    "base_url": "/api/v1",
    "endpoints": [
        {{
            "path": "/resource",
            "method": "GET/POST/PUT/DELETE/PATCH",
            "description": "what this endpoint does",
            "auth_required": true/false,
            "roles_allowed": ["roles"],
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

# ─────────────────────────────────────────
# DB SCHEMA PROMPT
# ─────────────────────────────────────────

DB_PROMPT = """
You are a database architect. Generate a complete database schema.

Return ONLY valid JSON:
{{
    "tables": [
        {{
            "name": "table_name",
            "columns": [
                {{
                    "name": "column_name",
                    "type": "UUID/VARCHAR/TEXT/INTEGER/BOOLEAN/TIMESTAMP/FLOAT",
                    "primary_key": true/false,
                    "nullable": true/false,
                    "unique": true/false,
                    "default": "value or null"
                }}
            ]
        }}
    ],
    "relationships": [
        {{
            "from_table": "table1",
            "to_table": "table2",
            "type": "one_to_many/many_to_many/one_to_one",
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

# ─────────────────────────────────────────
# AUTH SCHEMA PROMPT
# ─────────────────────────────────────────

AUTH_PROMPT = """
You are a security architect. Generate a complete auth and permissions schema.

Return ONLY valid JSON:
{{
    "roles": ["list of all roles"],
    "permissions": {{
        "role_name": ["list of permissions this role has"]
    }},
    "protected_routes": ["list of routes that need auth"],
    "premium_gates": ["list of features behind premium"]
}}

Rules:
- Return ONLY JSON, no markdown, no backticks
- Every role must have explicit permissions
- Super admin always has all permissions
- List every protected API route

Intent: {intent}
Design: {design}
"""

# ─────────────────────────────────────────
# BUSINESS LOGIC PROMPT
# ─────────────────────────────────────────

BUSINESS_PROMPT = """
You are a product architect. Generate complete business logic rules.

Return ONLY valid JSON:
{{
    "free_limits": {{
        "feature_name": "limit description"
    }},
    "premium_features": ["list of premium only features"],
    "validation_rules": ["list of data validation rules"],
    "notification_triggers": ["list of events that trigger notifications"]
}}

Rules:
- Return ONLY JSON, no markdown, no backticks
- Define clear free vs premium limits
- Cover all validation rules for forms
- List all notification events

Intent: {intent}
Design: {design}
"""

# ─────────────────────────────────────────
# GENERATOR FUNCTIONS
# ─────────────────────────────────────────

def _call_claude(prompt: str, mode: str, max_tokens: int = 2048) -> dict:
    temperature = {
        "fast": settings.TEMPERATURE_FAST,
        "balanced": settings.TEMPERATURE_BALANCED,
        "quality": settings.TEMPERATURE_QUALITY
    }.get(mode, settings.TEMPERATURE_BALANCED)

    response = client.messages.create(
        model=settings.PRIMARY_MODEL,
        max_tokens=max_tokens,
        temperature=temperature,
        messages=[{"role": "user", "content": prompt}]
    )

    raw = response.content[0].text.strip()
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

    # Generate UI Schema
    print("   → Generating UI Schema...")
    ui_data = _call_claude(
        UI_PROMPT.format(intent=intent_str, design=design_str),
        mode, 2048
    )
    ui_schema = UISchema(**ui_data)

    # Generate API Schema
    print("   → Generating API Schema...")
    api_data = _call_claude(
        API_PROMPT.format(intent=intent_str, design=design_str),
        mode, 2048
    )
    api_schema = APISchema(**api_data)

    # Generate DB Schema
    print("   → Generating DB Schema...")
    db_data = _call_claude(
        DB_PROMPT.format(intent=intent_str, design=design_str),
        mode, 2048
    )
    db_schema = DBSchema(**db_data)

    # Generate Auth Schema
    print("   → Generating Auth Schema...")
    auth_data = _call_claude(
        AUTH_PROMPT.format(intent=intent_str, design=design_str),
        mode, 1024
    )
    auth_schema = AuthSchema(**auth_data)

    # Generate Business Logic
    print("   → Generating Business Logic...")
    biz_data = _call_claude(
        BUSINESS_PROMPT.format(intent=intent_str, design=design_str),
        mode, 1024
    )
    business_logic = BusinessLogic(**biz_data)

    print(f"✅ Stage 3 Done — UI: {len(ui_schema.pages)} pages | API: {len(api_schema.endpoints)} endpoints | DB: {len(db_schema.tables)} tables")
    return ui_schema, api_schema, db_schema, auth_schema, business_logic