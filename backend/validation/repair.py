import json
from groq import Groq
from backend.config.settings import settings
from backend.models.schemas import (
    UISchema, APISchema, DBSchema, AuthSchema,
    BusinessLogic, ValidationReport, ValidationError,
    ValidationStatus
)
from typing import List

client = Groq(api_key=settings.GROQ_API_KEY)

REPAIR_PROMPT = """
You are a system repair engine.
The following schema has errors that need to be fixed.

Layer with errors: {layer}
Errors found:
{errors}

Current schema:
{schema}

Fix ONLY the errors listed above.
Return the complete corrected schema as valid JSON only.
No explanation, no markdown, no backticks.
"""

def repair_schemas(
    ui_schema: UISchema,
    api_schema: APISchema,
    db_schema: DBSchema,
    auth_schema: AuthSchema,
    business_logic: BusinessLogic,
    validation_report: ValidationReport
) -> tuple[UISchema, APISchema, DBSchema, AuthSchema, BusinessLogic, ValidationReport]:
    """
    Repairs only the broken parts — not full regeneration
    """
    print("🔧 Repairing schemas...")

    if validation_report.errors_found == 0:
        print("✅ No repairs needed")
        return ui_schema, api_schema, db_schema, auth_schema, business_logic, validation_report

    errors = validation_report.errors
    fixed_count = 0

    ui_errors = [e for e in errors if "UI" in e.layer]
    api_errors = [e for e in errors if "API" in e.layer]
    db_errors = [e for e in errors if "DB" in e.layer]
    auth_errors = [e for e in errors if "Auth" in e.layer]
    biz_errors = [e for e in errors if "Business" in e.layer]

    if ui_errors:
        print(f"   → Repairing UI Schema ({len(ui_errors)} errors)...")
        ui_schema, count = _repair_layer(
            "UI Schema", json.dumps(ui_schema.model_dump(), indent=2), ui_errors, UISchema
        )
        fixed_count += count

    if api_errors:
        print(f"   → Repairing API Schema ({len(api_errors)} errors)...")
        api_schema, count = _repair_layer(
            "API Schema", json.dumps(api_schema.model_dump(), indent=2), api_errors, APISchema
        )
        fixed_count += count

    if db_errors:
        print(f"   → Repairing DB Schema ({len(db_errors)} errors)...")
        db_schema, count = _repair_layer(
            "DB Schema", json.dumps(db_schema.model_dump(), indent=2), db_errors, DBSchema
        )
        fixed_count += count

    if auth_errors:
        print(f"   → Repairing Auth Schema ({len(auth_errors)} errors)...")
        auth_schema, count = _repair_layer(
            "Auth Schema", json.dumps(auth_schema.model_dump(), indent=2), auth_errors, AuthSchema
        )
        fixed_count += count

    if biz_errors:
        print(f"   → Repairing Business Logic ({len(biz_errors)} errors)...")
        business_logic, count = _repair_layer(
            "Business Logic", json.dumps(business_logic.model_dump(), indent=2), biz_errors, BusinessLogic
        )
        fixed_count += count

    for error in validation_report.errors:
        error.fixed = True

    validation_report.errors_fixed = fixed_count
    validation_report.status = (
        ValidationStatus.CLEAN
        if fixed_count == validation_report.errors_found
        else ValidationStatus.REPAIRED
    )

    print(f"✅ Repair Done — Fixed {fixed_count}/{validation_report.errors_found} errors")
    return ui_schema, api_schema, db_schema, auth_schema, business_logic, validation_report


def _repair_layer(layer_name: str, schema_json: str, errors: List[ValidationError], schema_class):
    error_descriptions = "\n".join([
        f"- [{e.error_type}] {e.description}" for e in errors
    ])

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            temperature=0.1,
            max_tokens=2048,
            messages=[
                {
                    "role": "user",
                    "content": REPAIR_PROMPT.format(
                        layer=layer_name,
                        errors=error_descriptions,
                        schema=schema_json
                    )
                }
            ]
        )

        raw = response.choices[0].message.content.strip()
        raw = raw.replace("```json", "").replace("```", "").strip()
        data = json.loads(raw)
        repaired = schema_class(**data)
        return repaired, len(errors)

    except Exception as e:
        print(f"   ⚠️ Could not repair {layer_name}: {e}")
        return schema_class(**json.loads(schema_json)), 0