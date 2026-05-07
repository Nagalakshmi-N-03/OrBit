from backend.models.schemas import (
    UISchema, APISchema, DBSchema, AuthSchema,
    BusinessLogic, ValidationError, ValidationReport,
    ValidationStatus
)
from typing import List

def validate_schemas(
    ui_schema: UISchema,
    api_schema: APISchema,
    db_schema: DBSchema,
    auth_schema: AuthSchema,
    business_logic: BusinessLogic
) -> ValidationReport:
    """
    Validates all schemas against each other
    Checks cross-layer consistency
    """
    print("🔍 Validating schemas...")
    errors: List[ValidationError] = []

    # Run all checks
    errors += _check_ui_vs_api(ui_schema, api_schema)
    errors += _check_api_vs_db(api_schema, db_schema)
    errors += _check_auth_vs_api(auth_schema, api_schema)
    errors += _check_premium_gates(auth_schema, business_logic)
    errors += _check_db_relationships(db_schema)
    errors += _check_required_tables(db_schema)

    total = len(errors)
    print(f"   → Found {total} issues")

    return ValidationReport(
        status=ValidationStatus.CLEAN if total == 0 else ValidationStatus.REPAIRED,
        errors_found=total,
        errors_fixed=0,  # repair.py will update this
        errors=errors
    )


# ─────────────────────────────────────────
# CHECK 1 — UI fields must map to API
# ─────────────────────────────────────────

def _check_ui_vs_api(
    ui_schema: UISchema,
    api_schema: APISchema
) -> List[ValidationError]:
    errors = []
    api_paths = [e["path"] for e in api_schema.endpoints]

    for page in ui_schema.pages:
        for form in page.get("forms", []):
            for field in form.get("fields", []):
                field_name = field.get("name", "")
                # Check if a related API endpoint exists
                matched = any(
                    field_name.lower() in path.lower()
                    for path in api_paths
                )
                if not matched and field.get("required"):
                    errors.append(ValidationError(
                        layer="UI → API",
                        error_type="missing_endpoint",
                        description=f"Required field '{field_name}' on page '{page.get('name')}' has no matching API endpoint",
                        fixed=False
                    ))
    return errors


# ─────────────────────────────────────────
# CHECK 2 — API fields must exist in DB
# ─────────────────────────────────────────

def _check_api_vs_db(
    api_schema: APISchema,
    db_schema: DBSchema
) -> List[ValidationError]:
    errors = []

    # Collect all DB column names
    all_columns = []
    for table in db_schema.tables:
        for col in table.get("columns", []):
            all_columns.append(col.get("name", "").lower())

    for endpoint in api_schema.endpoints:
        body = endpoint.get("request_body", {})
        for field in body.keys():
            if field.lower() not in all_columns:
                errors.append(ValidationError(
                    layer="API → DB",
                    error_type="missing_column",
                    description=f"API field '{field}' in endpoint '{endpoint.get('path')}' has no matching DB column",
                    fixed=False
                ))
    return errors


# ─────────────────────────────────────────
# CHECK 3 — Protected routes must have auth rules
# ─────────────────────────────────────────

def _check_auth_vs_api(
    auth_schema: AuthSchema,
    api_schema: APISchema
) -> List[ValidationError]:
    errors = []
    protected = auth_schema.protected_routes

    for endpoint in api_schema.endpoints:
        if endpoint.get("auth_required"):
            path = endpoint.get("path", "")
            matched = any(
                path.lower() in r.lower() or r.lower() in path.lower()
                for r in protected
            )
            if not matched:
                errors.append(ValidationError(
                    layer="Auth → API",
                    error_type="missing_auth_rule",
                    description=f"Endpoint '{path}' requires auth but has no auth rule defined",
                    fixed=False
                ))
    return errors


# ─────────────────────────────────────────
# CHECK 4 — Premium features must be gated
# ─────────────────────────────────────────

def _check_premium_gates(
    auth_schema: AuthSchema,
    business_logic: BusinessLogic
) -> List[ValidationError]:
    errors = []

    for feature in business_logic.premium_features:
        gated = any(
            feature.lower() in gate.lower()
            for gate in auth_schema.premium_gates
        )
        if not gated:
            errors.append(ValidationError(
                layer="Business Logic → Auth",
                error_type="missing_premium_gate",
                description=f"Premium feature '{feature}' is not gated in auth rules",
                fixed=False
            ))
    return errors


# ─────────────────────────────────────────
# CHECK 5 — DB foreign keys must reference existing tables
# ─────────────────────────────────────────

def _check_db_relationships(
    db_schema: DBSchema
) -> List[ValidationError]:
    errors = []
    table_names = [t.get("name", "").lower() for t in db_schema.tables]

    for rel in db_schema.relationships:
        from_table = rel.get("from_table", "").lower()
        to_table = rel.get("to_table", "").lower()

        if from_table not in table_names:
            errors.append(ValidationError(
                layer="DB",
                error_type="missing_table",
                description=f"Relationship references non-existent table '{from_table}'",
                fixed=False
            ))

        if to_table not in table_names:
            errors.append(ValidationError(
                layer="DB",
                error_type="missing_table",
                description=f"Relationship references non-existent table '{to_table}'",
                fixed=False
            ))
    return errors


# ─────────────────────────────────────────
# CHECK 6 — Required tables must exist
# ─────────────────────────────────────────

def _check_required_tables(
    db_schema: DBSchema
) -> List[ValidationError]:
    errors = []
    table_names = [t.get("name", "").lower() for t in db_schema.tables]
    required = ["users"]

    for table in required:
        if table not in table_names:
            errors.append(ValidationError(
                layer="DB",
                error_type="missing_required_table",
                description=f"Required table '{table}' is missing from DB schema",
                fixed=False
            ))
    return errors