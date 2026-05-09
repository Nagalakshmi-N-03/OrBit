from sqlalchemy import Column, String, Float, Integer, Boolean, DateTime, Text, JSON
from sqlalchemy.sql import func
from backend.config.database import Base
import uuid

def generate_uuid():
    return str(uuid.uuid4())

# ─────────────────────────────────────────
# GENERATION LOGS
# ─────────────────────────────────────────

class GenerationLog(Base):
    __tablename__ = "generation_logs"

    id = Column(String, primary_key=True, default=generate_uuid)
    prompt = Column(Text, nullable=False)
    mode = Column(String, nullable=False)
    success = Column(Boolean, default=False)
    confidence = Column(Float, default=0.0)
    retries = Column(Integer, default=0)
    latency = Column(Float, default=0.0)
    failure_type = Column(String, nullable=True)
    output = Column(JSON, nullable=True)
    created_at = Column(DateTime, server_default=func.now())

# ─────────────────────────────────────────
# EVALUATION RESULTS
# ─────────────────────────────────────────

class EvaluationLog(Base):
    __tablename__ = "evaluation_logs"

    id = Column(String, primary_key=True, default=generate_uuid)
    prompt = Column(Text, nullable=False)
    prompt_type = Column(String, nullable=False)  # real / edge_case
    success = Column(Boolean, default=False)
    retries = Column(Integer, default=0)
    latency = Column(Float, default=0.0)
    confidence = Column(Float, default=0.0)
    failure_type = Column(String, nullable=True)
    created_at = Column(DateTime, server_default=func.now())
