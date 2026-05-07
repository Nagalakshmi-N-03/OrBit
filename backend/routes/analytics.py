from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from backend.config.database import get_db
from backend.models.db_models import GenerationLog, EvaluationLog

router = APIRouter(prefix="/api/analytics", tags=["Analytics"])


@router.get("/metrics")
async def get_metrics(db: Session = Depends(get_db)):
    """
    Returns live metrics for evaluation dashboard
    """
    total = db.query(GenerationLog).count()

    if total == 0:
        return {
            "total_generations": 0,
            "success_rate": 0,
            "average_latency": 0,
            "average_retries": 0,
            "average_confidence": 0,
            "failure_types": {}
        }

    # Success rate
    successful = db.query(GenerationLog).filter(
        GenerationLog.success == True
    ).count()

    # Averages
    averages = db.query(
        func.avg(GenerationLog.latency),
        func.avg(GenerationLog.retries),
        func.avg(GenerationLog.confidence)
    ).first()

    # Failure types
    failures = db.query(
        GenerationLog.failure_type,
        func.count(GenerationLog.failure_type)
    ).filter(
        GenerationLog.failure_type != None
    ).group_by(GenerationLog.failure_type).all()

    failure_types = {f[0]: f[1] for f in failures if f[0]}

    # Mode distribution
    modes = db.query(
        GenerationLog.mode,
        func.count(GenerationLog.mode)
    ).group_by(GenerationLog.mode).all()

    mode_dist = {m[0]: m[1] for m in modes}

    return {
        "total_generations": total,
        "success_rate": round(successful / total * 100, 2),
        "average_latency": round(float(averages[0] or 0), 2),
        "average_retries": round(float(averages[1] or 0), 2),
        "average_confidence": round(float(averages[2] or 0), 2),
        "failure_types": failure_types,
        "mode_distribution": mode_dist
    }


@router.get("/recent")
async def get_recent(db: Session = Depends(get_db)):
    """
    Returns last 10 generations with details
    """
    logs = db.query(GenerationLog).order_by(
        GenerationLog.created_at.desc()
    ).limit(10).all()

    return {
        "recent": [
            {
                "id": log.id,
                "prompt": log.prompt[:100],
                "mode": log.mode,
                "success": log.success,
                "confidence": round(log.confidence or 0, 2),
                "latency": round(log.latency or 0, 2),
                "retries": log.retries,
                "created_at": str(log.created_at)
            }
            for log in logs
        ]
    }