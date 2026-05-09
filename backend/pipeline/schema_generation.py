import json
from groq import Groq
from json_repair import repair_json
from backend.config.settings import settings
from backend.models.schemas import (
    IntentData, SystemDesignData,
    UISchema, APISchema, DBSchema, AuthSchema, BusinessLogic
)

client = Groq(api_key=settings.GROQ_API_KEY)

UI_PROMPT = """Generate a UI schema. Return ONLY compact JSON, no explanation.

Format:
{{"pages":[{{"name":"Login","route":"/login","access":["public"],"components":["LoginForm","Logo"],"forms":[{{"name":"LoginForm","fields":[{{"name":"email","type":"email","required":true}},{{"name":"password","type":"password","required":true}}]}}]}},{{"name":"Dashboard","route":"/dashboard","access":["admin","user"],"components":["Sidebar","Header","StatsCard"],"forms":[]}}],"layouts":{{"authenticated":"sidebar + navbar","public":"centered"}},"components":{{"shared":["Navbar","Sidebar","Button","Modal"]}}}}

App type: {app_type}
Features: {features}
Roles: {roles}
Pages: {pages}

Include Login and Register pages. Keep it concise."""

API_PROMPT = """Generate an API schema. Return ONLY compact JSON, no explanation.

Format:
{{"base_url":"/api/v1","endpoints":[{{"path":"/auth/login","method":"POST","description":"User login","auth_required":false,"roles_allowed":["public"],"request_body":{{"email":"string","password":"string"}},"response":{{"token":"string"}}}},{{"path":"/auth/register","method":"POST","description":"Register","auth_required":false,"roles_allowed":["public"],"request_body":{{"name":"string","email":"string","password":"string"}},"response":{{"user":"object"}}}}]}}

App type: {app_type}
Features: {features}
Entities: {entities}
Roles: {roles}

Include auth endpoints + CRUD for each entity. Keep concise."""

DB_PROMPT = """Generate a database schema. Return ONLY compact JSON, no explanation.

Format:
{{"tables":[{{"name":"users","columns":[{{"name":"id","type":"UUID","primary_key":true,"nullable":false,"unique":true,"default":null}},{{"name":"name","type":"VARCHAR","primary_key":false,"nullable":false,"unique":false,"default":null}},{{"name":"email","type":"VARCHAR","primary_key":false,"nullable":false,"unique":true,"default":null}},{{"name":"created_at","type":"TIMESTAMP","primary_key":false,"nullable":false,"unique":false,"default":"now()"}}]}}],"relationships":[{{"from_table":"tasks","to_table":"users","type":"many_to_one","foreign_key":"user_id"}}]}}

App type: {app_type}
Entities: {entities}

Every table needs id (UUID) and created_at. Include users table."""

AUTH_PROMPT = """Generate an auth schema. Return ONLY compact JSON, no explanation.

Format:
{{"roles":["admin","user"],"permissions":{{"admin":["create","read","update","delete"],"user":["read","update_own"]}},"protected_routes":["/api/v1/dashboard"],"premium_gates":["advanced_analytics","exports"]}}

Roles: {roles}
Has payments: {has_payments}
Features: {features}"""

BUSINESS_PROMPT = """Generate business logic rules. Return ONLY compact JSON, no explanation.

Format:
{{"free_limits":{{"projects":"max 3","members":"max 5"}},"premium_features":["unlimited_projects","advanced_analytics","exports"],"validation_rules":["email must be unique","password min 8 chars"],"notification_triggers":["task assigned","deadline approaching","comment added"]}}

App type: {app_type}
Has payments: {has_payments}
Features: {features}"""


def _call_groq(prompt: str, mode: str, max_tokens: int = 1200) -> dict:
    temperature = {
        "fast": settings.TEMPERATURE_FAST,
        "balanced": settings.TEMPERATURE_BALANCED,
        "quality": settings.TEMPERATURE_QUALITY
    }.get(mode, settings.TEMPERATURE_BALANCED)

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        temperature=temperature,
        max_tokens=max_tokens,
        messages=[{"role": "user", "content": prompt}]
    )

    raw = response.choices[0].message.content.strip()
    raw = raw.replace("```json", "").replace("```", "").strip()
    repaired = repair_json(raw)
    return json.loads(repaired)


def generate_schemas(
    intent: IntentData,
    design: SystemDesignData,
    mode: str = "balanced"
) -> tuple[UISchema, APISchema, DBSchema, AuthSchema, BusinessLogic]:
    print(f"⚙️  Stage 3: Generating schemas...")

    features_str = ", ".join(intent.features)
    roles_str = ", ".join(intent.roles)
    entities_str = ", ".join(intent.entities)
    pages_str = ", ".join(design.pages)

    print("   → Generating UI Schema...")
    ui_data = _call_groq(UI_PROMPT.format(
        app_type=intent.app_type,
        features=features_str,
        roles=roles_str,
        pages=pages_str
    ), mode, 1200)
    ui_schema = UISchema(**ui_data)

    print("   → Generating API Schema...")
    api_data = _call_groq(API_PROMPT.format(
        app_type=intent.app_type,
        features=features_str,
        entities=entities_str,
        roles=roles_str
    ), mode, 1200)
    api_schema = APISchema(**api_data)

    print("   → Generating DB Schema...")
    db_data = _call_groq(DB_PROMPT.format(
        app_type=intent.app_type,
        entities=entities_str
    ), mode, 1200)
    db_schema = DBSchema(**db_data)

    print("   → Generating Auth Schema...")
    auth_data = _call_groq(AUTH_PROMPT.format(
        roles=roles_str,
        has_payments=intent.has_payments,
        features=features_str
    ), mode, 600)
    auth_schema = AuthSchema(**auth_data)

    print("   → Generating Business Logic...")
    biz_data = _call_groq(BUSINESS_PROMPT.format(
        app_type=intent.app_type,
        has_payments=intent.has_payments,
        features=features_str
    ), mode, 600)
    business_logic = BusinessLogic(**biz_data)

    print(f"✅ Stage 3 Done — UI: {len(ui_schema.pages)} pages | API: {len(api_schema.endpoints)} endpoints | DB: {len(db_schema.tables)} tables")
    return ui_schema, api_schema, db_schema, auth_schema, business_logic
