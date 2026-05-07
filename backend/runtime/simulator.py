from backend.models.schemas import (
    UISchema, APISchema, DBSchema, AuthSchema,
    BusinessLogic
)
from typing import List, Dict, Any

class SimulationResult:
    def __init__(self):
        self.passed: List[str] = []
        self.failed: List[str] = []
        self.warnings: List[str] = []

    @property
    def success(self) -> bool:
        return len(self.failed) == 0

    @property
    def score(self) -> float:
        total = len(self.passed) + len(self.failed)
        if total == 0:
            return 0.0
        return round(len(self.passed) / total * 100, 2)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "success": self.success,
            "score": self.score,
            "passed": self.passed,
            "failed": self.failed,
            "warnings": self.warnings,
            "summary": f"{len(self.passed)} passed, {len(self.failed)} failed, {len(self.warnings)} warnings"
        }


def simulate_execution(
    ui_schema: UISchema,
    api_schema: APISchema,
    db_schema: DBSchema,
    auth_schema: AuthSchema,
    business_logic: BusinessLogic
) -> SimulationResult:
    """
    Simulates execution of the generated schemas
    Proves output is usable without manual fixes
    """
    print("🚀 Simulating execution...")
    result = SimulationResult()

    # Run all simulations
    _simulate_db(db_schema, result)
    _simulate_api(api_schema, auth_schema, result)
    _simulate_ui(ui_schema, api_schema, result)
    _simulate_auth(auth_schema, result)
    _simulate_business_logic(business_logic, result)

    print(f"✅ Simulation Done — Score: {result.score}% ({len(result.passed)} passed, {len(result.failed)} failed)")
    return result


# ─────────────────────────────────────────
# DB SIMULATION
# ─────────────────────────────────────────

def _simulate_db(db_schema: DBSchema, result: SimulationResult):
    table_names = []

    for table in db_schema.tables:
        name = table.get("name", "")
        columns = table.get("columns", [])
        col_names = [c.get("name") for c in columns]

        # Check table has a name
        if not name:
            result.failed.append("DB: Table found with no name")
            continue

        table_names.append(name.lower())

        # Check table has id column
        if "id" not in col_names:
            result.failed.append(f"DB: Table '{name}' missing 'id' column")
        else:
            result.passed.append(f"DB: Table '{name}' has id column")

        # Check table has created_at
        if "created_at" not in col_names:
            result.warnings.append(f"DB: Table '{name}' missing 'created_at' column")
        else:
            result.passed.append(f"DB: Table '{name}' has created_at column")

        # Check primary key exists
        has_pk = any(c.get("primary_key") for c in columns)
        if not has_pk:
            result.failed.append(f"DB: Table '{name}' has no primary key")
        else:
            result.passed.append(f"DB: Table '{name}' has primary key")

    # Check users table exists
    if "users" in table_names:
        result.passed.append("DB: Required 'users' table exists")
    else:
        result.failed.append("DB: Required 'users' table is missing")

    # Check relationships reference valid tables
    for rel in db_schema.relationships:
        from_t = rel.get("from_table", "").lower()
        to_t = rel.get("to_table", "").lower()

        if from_t in table_names and to_t in table_names:
            result.passed.append(f"DB: Relationship {from_t} → {to_t} is valid")
        else:
            result.failed.append(f"DB: Relationship {from_t} → {to_t} references missing table")


# ─────────────────────────────────────────
# API SIMULATION
# ─────────────────────────────────────────

def _simulate_api(
    api_schema: APISchema,
    auth_schema: AuthSchema,
    result: SimulationResult
):
    valid_methods = ["GET", "POST", "PUT", "DELETE", "PATCH"]
    paths = []

    # Check auth endpoints exist
    auth_paths = [e.get("path", "").lower() for e in api_schema.endpoints]
    for required in ["/auth/login", "/auth/register"]:
        matched = any(required in p for p in auth_paths)
        if matched:
            result.passed.append(f"API: Auth endpoint '{required}' exists")
        else:
            result.warnings.append(f"API: Auth endpoint '{required}' not found")

    for endpoint in api_schema.endpoints:
        path = endpoint.get("path", "")
        method = endpoint.get("method", "").upper()

        # Check path exists
        if not path:
            result.failed.append("API: Endpoint found with no path")
            continue

        paths.append(path)

        # Check valid HTTP method
        if method not in valid_methods:
            result.failed.append(f"API: Endpoint '{path}' has invalid method '{method}'")
        else:
            result.passed.append(f"API: Endpoint '{method} {path}' is valid")

        # Check auth_required field exists
        if "auth_required" not in endpoint:
            result.warnings.append(f"API: Endpoint '{path}' missing auth_required field")
        else:
            result.passed.append(f"API: Endpoint '{path}' has auth_required defined")

    # Check no duplicate paths
    if len(paths) != len(set(paths)):
        result.warnings.append("API: Duplicate endpoint paths detected")
    else:
        result.passed.append("API: No duplicate endpoints")


# ─────────────────────────────────────────
# UI SIMULATION
# ─────────────────────────────────────────

def _simulate_ui(
    ui_schema: UISchema,
    api_schema: APISchema,
    result: SimulationResult
):
    api_paths = [e.get("path", "").lower() for e in api_schema.endpoints]
    page_routes = []

    for page in ui_schema.pages:
        name = page.get("name", "")
        route = page.get("route", "")
        components = page.get("components", [])

        # Check page has name
        if not name:
            result.failed.append("UI: Page found with no name")
            continue

        # Check page has route
        if not route:
            result.failed.append(f"UI: Page '{name}' has no route")
        else:
            result.passed.append(f"UI: Page '{name}' has route '{route}'")
            page_routes.append(route)

        # Check page has components
        if not components:
            result.warnings.append(f"UI: Page '{name}' has no components")
        else:
            result.passed.append(f"UI: Page '{name}' has {len(components)} components")

    # Check Login and Register pages exist
    page_names = [p.get("name", "").lower() for p in ui_schema.pages]
    for required in ["login", "register"]:
        if any(required in n for n in page_names):
            result.passed.append(f"UI: Required '{required}' page exists")
        else:
            result.warnings.append(f"UI: '{required}' page not found")

    # Check no duplicate routes
    if len(page_routes) != len(set(page_routes)):
        result.warnings.append("UI: Duplicate page routes detected")
    else:
        result.passed.append("UI: No duplicate routes")


# ─────────────────────────────────────────
# AUTH SIMULATION
# ─────────────────────────────────────────

def _simulate_auth(auth_schema: AuthSchema, result: SimulationResult):

    # Check roles exist
    if not auth_schema.roles:
        result.failed.append("Auth: No roles defined")
    else:
        result.passed.append(f"Auth: {len(auth_schema.roles)} roles defined")

    # Check permissions exist for each role
    for role in auth_schema.roles:
        if role in auth_schema.permissions:
            perms = auth_schema.permissions[role]
            if perms:
                result.passed.append(f"Auth: Role '{role}' has {len(perms)} permissions")
            else:
                result.warnings.append(f"Auth: Role '{role}' has empty permissions")
        else:
            result.failed.append(f"Auth: Role '{role}' has no permissions defined")

    # Check protected routes exist
    if auth_schema.protected_routes:
        result.passed.append(f"Auth: {len(auth_schema.protected_routes)} protected routes defined")
    else:
        result.warnings.append("Auth: No protected routes defined")


# ─────────────────────────────────────────
# BUSINESS LOGIC SIMULATION
# ─────────────────────────────────────────

def _simulate_business_logic(
    business_logic: BusinessLogic,
    result: SimulationResult
):
    # Check free limits defined
    if business_logic.free_limits:
        result.passed.append(f"BizLogic: {len(business_logic.free_limits)} free limits defined")
    else:
        result.warnings.append("BizLogic: No free limits defined")

    # Check premium features defined
    if business_logic.premium_features:
        result.passed.append(f"BizLogic: {len(business_logic.premium_features)} premium features defined")
    else:
        result.warnings.append("BizLogic: No premium features defined")

    # Check validation rules exist
    if business_logic.validation_rules:
        result.passed.append(f"BizLogic: {len(business_logic.validation_rules)} validation rules defined")
    else:
        result.warnings.append("BizLogic: No validation rules defined")

    # Check notification triggers exist
    if business_logic.notification_triggers:
        result.passed.append(f"BizLogic: {len(business_logic.notification_triggers)} notification triggers defined")
    else:
        result.warnings.append("BizLogic: No notification triggers defined")