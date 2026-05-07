import time
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from backend.config.database import get_db
from backend.models.schemas import GenerateRequest, GenerateResponse, GenerationMode
from backend.models.db_models import GenerationLog
from backend.pipeline.intent_extraction import extract_intent
from backend.pipeline.system_design import design_system
from backend.pipeline.schema_generation import generate_schemas
from backend.pipeline.refinement import refine_schemas
from backend.validation.validator import validate_schemas
from backend.validation.repair import repair_schemas
from backend.runtime.simulator import simulate_execution

router = APIRouter(prefix="/api/generator", tags=["Generator"])


@router.post("/generate", response_model=GenerateResponse)
async def generate(request: GenerateRequest, db: Session = Depends(get_db)):
    """
    Main endpoint — runs full pipeline
    """
    start = time.time()
    retries = 0
    assumptions = []

    try:
        print(f"\n{'='*50}")
        print(f"🚀 Starting Pipeline")
        print(f"   Prompt : {request.prompt[:60]}...")
        print(f"   Mode   : {request.mode}")
        print(f"{'='*50}")

        # ── Stage 1: Intent Extraction
        intent = extract_intent(request.prompt, request.mode)

        # If clarification needed and vague
        if intent.clarification_needed and intent.confidence < 0.4:
            raise HTTPException(
                status_code=422,
                detail={
                    "error": "prompt_too_vague",
                    "message": "Your prompt needs more detail",
                    "question": intent.clarification_question
                }
            )

        # ── Stage 2: System Design
        design = design_system(intent, request.mode)

        # ── Stage 3: Schema Generation
        ui, api, db_schema, auth, biz = generate_schemas(
            intent, design, request.mode
        )

        # ── Stage 4: Refinement
        ui, api, db_schema, auth, biz, assumptions, changes = refine_schemas(
            intent, design, ui, api, db_schema, auth, biz, request.mode
        )

        # ── Validation
        report = validate_schemas(ui, api, db_schema, auth, biz)

        # ── Repair if needed
        if report.errors_found > 0:
            retries += 1
            ui, api, db_schema, auth, biz, report = repair_schemas(
                ui, api, db_schema, auth, biz, report
            )

        # ── Runtime Simulation
        simulation = simulate_execution(ui, api, db_schema, auth, biz)

        latency = round(time.time() - start, 2)

        # ── Save to DB
        log = GenerationLog(
            prompt=request.prompt,
            mode=request.mode,
            success=simulation.success,
            confidence=intent.confidence,
            retries=retries,
            latency=latency,
            output={
                "app_name": intent.app_name,
                "simulation_score": simulation.score
            }
        )
        db.add(log)
        db.commit()

        print(f"\n✅ Pipeline Complete!")
        print(f"   Latency : {latency}s")
        print(f"   Retries : {retries}")
        print(f"   Score   : {simulation.score}%")

        return GenerateResponse(
            app_name=intent.app_name,
            confidence=intent.confidence,
            mode=request.mode,
            assumptions=assumptions,
            intent=intent,
            system_design=design,
            ui_schema=ui,
            api_schema=api,
            db_schema=db_schema,
            auth_schema=auth,
            business_logic=biz,
            validation_report=report,
            latency_seconds=latency,
            retries_used=retries
        )

    except HTTPException:
        raise

    except Exception as e:
        latency = round(time.time() - start, 2)

        # Log failure
        log = GenerationLog(
            prompt=request.prompt,
            mode=request.mode,
            success=False,
            confidence=0.0,
            retries=retries,
            latency=latency,
            failure_type=type(e).__name__
        )
        db.add(log)
        db.commit()

        raise HTTPException(
            status_code=500,
            detail={
                "error": type(e).__name__,
                "message": str(e)
            }
        )


@router.get("/history")
async def get_history(db: Session = Depends(get_db)):
    """
    Returns recent generation history
    """
    logs = db.query(GenerationLog).order_by(
        GenerationLog.created_at.desc()
    ).limit(20).all()

    return {
        "history": [
            {
                "id": log.id,
                "prompt": log.prompt[:80],
                "mode": log.mode,
                "success": log.success,
                "confidence": log.confidence,
                "latency": log.latency,
                "retries": log.retries,
                "created_at": str(log.created_at)
            }
            for log in logs
        ]
    }