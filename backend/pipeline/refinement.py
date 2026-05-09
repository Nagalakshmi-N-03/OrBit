import json
from groq import Groq
from json_repair import repair_json
from backend.config.settings import settings
from backend.models.schemas import (
    IntentData, SystemDesignData,
    UISchema, APISchema, DBSchema, AuthSchema, BusinessLogic
)

client = Groq(api_key=settings.GROQ_API_KEY)


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
    print(f"🔧 Stage 4: Refining schemas...")

    # Skip refinement in fast and balanced mode to save tokens
    print(f"⚡ {mode} mode — skipping deep refinement")
    return ui_schema, api_schema, db_schema, auth_schema, business_logic, [
        "UUID used as primary key for all tables",
        "USD assumed as default currency",
        "Free plan limited to 3 projects",
        "JWT used for authentication"
    ], []
