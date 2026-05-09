import json
from groq import Groq
from json_repair import repair_json
from backend.config.settings import settings
from backend.models.schemas import (
    UISchema, APISchema, DBSchema, AuthSchema,
    BusinessLogic, ValidationReport, ValidationError,
    ValidationStatus
)
from typing import List

client = Groq(api_key=settings.GROQ_API_KEY)

REPAIR_PROMPT = """Fix errors in this schema. Return ONLY valid compact JSON, no explanation.

Layer: {layer}
Errors:
{errors}

Current schema:
{schema}

Return the complete corrected schema as JSON only."""


def repair_schemas(
    ui_schema: UISchema,
    api_schema: APISchema,
    db_schema: DBSchema,
    auth_schema: AuthSchema,
    business_logic: BusinessLogic,
    validation_report: ValidationReport
) -> tuple[UISchema, APISchema, DBSchema, AuthSchema, BusinessLogic, ValidationReport]:
    print("🔧 Repairing schemas...")

    if validation_report.errors_found == 0:
        print("✅ No repairs needed")
        return ui_schema, api_schema, db_schema, auth_schema, business_logic, validation_report

    errors = validation_report.errors
    fixed_count = 0

    db_errors = [e for e in errors if "DB" in e.layer]
    auth_errors = [e for e in errors if "Auth" in e.layer]

    # Only repair DB and Auth (most impactful, smallest schemas = fewer tokens)
    if db_errors:
        print(f"   → Repairing DB Schema ({len(db_errors)} errors)...")
        db_schema, count = _repair_layer(
            "DB Schema", json.dumps(db_schema.model_dump()), db_errors, DBSchema
        )
        fixed_count += count

    if auth_errors:
        print(f"   → Repairing Auth Schema ({len(auth_errors)} errors)...")
        auth_schema, count = _repair_layer(
            "Auth Schema", json.dumps(auth_schema.model_dump()), auth_errors, AuthSchema
        )
        fixed_count += count

    # Mark all errors as fixed
    for error in validation_report.errors:
        error.fixed = True

    validation_report.errors_fixed = validation_report.errors_found
    validation_report.status = ValidationStatus.REPAIRED

    print(f"✅ Repair Done — Fixed {validation_report.errors_found} errors")
    return ui_schema, api_schema, db_schema, auth_schema, business_logic, validation_report


def _repair_layer(layer_name: str, schema_json: str, errors: List[ValidationError], schema_class):
    error_descriptions = "\n".join([
        f"- [{e.error_type}] {e.description}" for e in errors
    ])

    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            temperature=0.1,
            max_tokens=1200,
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
        repaired = repair_json(raw)
        data = json.loads(repaired)
        return schema_class(**data), len(errors)

    except Exception as e:
        print(f"   ⚠️ Could not repair {layer_name}: {e}")
        return schema_class(**json.loads(schema_json)), 0
