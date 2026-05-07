from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from enum import Enum

# ─────────────────────────────────────────
# ENUMS
# ─────────────────────────────────────────

class GenerationMode(str, Enum):
    FAST = "fast"
    BALANCED = "balanced"
    QUALITY = "quality"

class ValidationStatus(str, Enum):
    CLEAN = "clean"
    REPAIRED = "repaired"
    FAILED = "failed"

# ─────────────────────────────────────────
# REQUEST MODELS
# ─────────────────────────────────────────

class GenerateRequest(BaseModel):
    prompt: str = Field(..., min_length=5, max_length=2000)
    mode: GenerationMode = GenerationMode.BALANCED

# ─────────────────────────────────────────
# PIPELINE STAGE MODELS
# ─────────────────────────────────────────

class IntentData(BaseModel):
    app_type: str
    app_name: str
    features: List[str]
    roles: List[str]
    entities: List[str]
    has_payments: bool
    has_analytics: bool
    has_notifications: bool
    confidence: float
    clarification_needed: bool
    clarification_question: Optional[str] = None

class SystemDesignData(BaseModel):
    pages: List[str]
    entities: Dict[str, Any]
    user_flows: List[str]
    data_flows: List[str]
    architecture_notes: List[str]

# ─────────────────────────────────────────
# SCHEMA OUTPUT MODELS
# ─────────────────────────────────────────

class UISchema(BaseModel):
    pages: List[Dict[str, Any]]
    layouts: Dict[str, Any]
    components: Dict[str, Any]

class APISchema(BaseModel):
    base_url: str
    endpoints: List[Dict[str, Any]]

class DBSchema(BaseModel):
    tables: List[Dict[str, Any]]
    relationships: List[Dict[str, Any]]

class AuthSchema(BaseModel):
    roles: List[str]
    permissions: Dict[str, List[str]]
    protected_routes: List[str]
    premium_gates: List[str]

class BusinessLogic(BaseModel):
    free_limits: Dict[str, Any]
    premium_features: List[str]
    validation_rules: List[str]
    notification_triggers: List[str]

# ─────────────────────────────────────────
# VALIDATION MODELS
# ─────────────────────────────────────────

class ValidationError(BaseModel):
    layer: str
    error_type: str
    description: str
    fixed: bool
    fix_applied: Optional[str] = None

class ValidationReport(BaseModel):
    status: ValidationStatus
    errors_found: int
    errors_fixed: int
    errors: List[ValidationError]

# ─────────────────────────────────────────
# FINAL OUTPUT MODEL
# ─────────────────────────────────────────

class GenerateResponse(BaseModel):
    app_name: str
    confidence: float
    mode: GenerationMode
    assumptions: List[str]
    intent: IntentData
    system_design: SystemDesignData
    ui_schema: UISchema
    api_schema: APISchema
    db_schema: DBSchema
    auth_schema: AuthSchema
    business_logic: BusinessLogic
    validation_report: ValidationReport
    latency_seconds: float
    retries_used: int

# ─────────────────────────────────────────
# EVALUATION MODELS
# ─────────────────────────────────────────

class EvaluationResult(BaseModel):
    prompt: str
    success: bool
    retries: int
    latency: float
    failure_type: Optional[str] = None
    confidence: float

class EvaluationSummary(BaseModel):
    total_prompts: int
    success_rate: float
    average_latency: float
    average_retries: float
    failure_types: Dict[str, int]
    results: List[EvaluationResult]