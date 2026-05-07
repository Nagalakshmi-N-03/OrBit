import json
import time
from pathlib import Path
from backend.pipeline.intent_extraction import extract_intent
from backend.pipeline.system_design import design_system
from backend.pipeline.schema_generation import generate_schemas
from backend.pipeline.refinement import refine_schemas
from backend.validation.validator import validate_schemas
from backend.validation.repair import repair_schemas
from backend.runtime.simulator import simulate_execution
from backend.models.schemas import EvaluationResult, EvaluationSummary

PROMPTS_FILE = Path(__file__).parent / "prompts.json"
RESULTS_FILE = Path(__file__).parent / "results.json"


def run_evaluation(mode: str = "balanced") -> EvaluationSummary:
    """
    Runs all 20 test prompts and tracks metrics
    """
    print("\n📊 Starting Evaluation Framework...")
    print("=" * 50)

    # Load prompts
    with open(PROMPTS_FILE) as f:
        data = json.load(f)

    all_prompts = data["real_prompts"] + data["edge_cases"]
    results = []

    for item in all_prompts:
        print(f"\n[{item['id']}/20] Testing: {item['prompt'][:60]}...")
        result = _run_single(item["prompt"], item["type"], mode)
        results.append(result)
        print(f"   → {'✅ Success' if result.success else '❌ Failed'} | Latency: {result.latency:.2f}s | Confidence: {result.confidence:.2f}")

    # Calculate summary
    total = len(results)
    successful = [r for r in results if r.success]
    success_rate = round(len(successful) / total * 100, 2)
    avg_latency = round(sum(r.latency for r in results) / total, 2)
    avg_retries = round(sum(r.retries for r in results) / total, 2)

    # Count failure types
    failure_types: dict = {}
    for r in results:
        if not r.success and r.failure_type:
            failure_types[r.failure_type] = failure_types.get(r.failure_type, 0) + 1

    summary = EvaluationSummary(
        total_prompts=total,
        success_rate=success_rate,
        average_latency=avg_latency,
        average_retries=avg_retries,
        failure_types=failure_types,
        results=results
    )

    # Save results
    with open(RESULTS_FILE, "w") as f:
        json.dump(summary.model_dump(), f, indent=2)

    print("\n" + "=" * 50)
    print(f"📊 Evaluation Complete!")
    print(f"   Success Rate : {success_rate}%")
    print(f"   Avg Latency  : {avg_latency}s")
    print(f"   Avg Retries  : {avg_retries}")
    print(f"   Failure Types: {failure_types}")
    print("=" * 50)

    return summary


def _run_single(
    prompt: str,
    prompt_type: str,
    mode: str
) -> EvaluationResult:
    """
    Runs the full pipeline for a single prompt
    """
    start = time.time()
    retries = 0
    confidence = 0.0

    try:
        # Stage 1
        intent = extract_intent(prompt, mode)
        confidence = intent.confidence

        # Stage 2
        design = design_system(intent, mode)

        # Stage 3
        ui, api, db, auth, biz = generate_schemas(intent, design, mode)

        # Stage 4
        ui, api, db, auth, biz, assumptions, changes = refine_schemas(
            intent, design, ui, api, db, auth, biz, mode
        )

        # Validate
        report = validate_schemas(ui, api, db, auth, biz)

        # Repair if needed
        if report.errors_found > 0:
            retries += 1
            ui, api, db, auth, biz, report = repair_schemas(
                ui, api, db, auth, biz, report
            )

        # Simulate
        sim = simulate_execution(ui, api, db, auth, biz)

        latency = round(time.time() - start, 2)

        return EvaluationResult(
            prompt=prompt,
            success=sim.success,
            retries=retries,
            latency=latency,
            failure_type=None if sim.success else "simulation_failed",
            confidence=confidence
        )

    except Exception as e:
        latency = round(time.time() - start, 2)
        return EvaluationResult(
            prompt=prompt,
            success=False,
            retries=retries,
            latency=latency,
            failure_type=type(e).__name__,
            confidence=confidence
        )