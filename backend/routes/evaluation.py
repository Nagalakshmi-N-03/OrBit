from fastapi import APIRouter, BackgroundTasks
from backend.evaluation.evaluator import run_evaluation
import json
from pathlib import Path

router = APIRouter(prefix="/api/evaluation", tags=["Evaluation"])

RESULTS_FILE = Path(__file__).parent.parent / "evaluation" / "results.json"


@router.post("/run")
async def run_eval(background_tasks: BackgroundTasks, mode: str = "balanced"):
    """
    Runs full evaluation in background
    """
    background_tasks.add_task(run_evaluation, mode)
    return {
        "message": "Evaluation started in background",
        "mode": mode
    }


@router.get("/results")
async def get_results():
    """
    Returns latest evaluation results
    """
    if not RESULTS_FILE.exists():
        return {"message": "No evaluation results yet. Run /run first"}

    with open(RESULTS_FILE) as f:
        data = json.load(f)

    return data