import os
from fastapi import FastAPI, BackgroundTasks, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse
from pydantic import BaseModel
from typing import Optional, Dict, Any, List

from backend.config import settings
from backend.models import ExecutionRecord, RunStatus
from agent.orchestrator import FinOpsOrchestrator
from tools.memory_agent import MemoryAgent

app = FastAPI(
    title="FinOps Autopilot API",
    description="Autonomous Cloud Cost & Architecture Optimization Platform powered by Google ADK & Gemini",
    version="1.0.0"
)

memory_agent = MemoryAgent()
orchestrator = FinOpsOrchestrator()

# Mount static files for dashboard UI
static_dir = os.path.join(os.path.dirname(__file__), "static")
if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")

class RunRequest(BaseModel):
    cluster_name: str = "prod-core-cluster"
    demo_mode: Optional[bool] = None

class PubSubMessage(BaseModel):
    message: Optional[Dict[str, Any]] = None
    subscription: Optional[str] = None

@app.get("/", response_class=HTMLResponse)
def get_dashboard():
    index_file = os.path.join(static_dir, "index.html")
    if os.path.exists(index_file):
        return FileResponse(index_file)
    return "<h1>FinOps Autopilot Dashboard</h1><p>API is running. Access endpoints at /api/runs or /api/metrics.</p>"

@app.post("/api/run-orchestrator", response_model=ExecutionRecord)
def trigger_orchestrator(req: RunRequest):
    """
    Triggers an autonomous FinOps Autopilot workflow run.
    """
    demo_mode = req.demo_mode if req.demo_mode is not None else settings.DEMO_MODE
    orc = FinOpsOrchestrator(demo_mode=demo_mode)
    record = orc.run_autonomous_workflow(cluster_name=req.cluster_name)
    return record

@app.post("/pubsub/trigger")
def pubsub_trigger(pubsub_msg: PubSubMessage, background_tasks: BackgroundTasks):
    """
    Webhook endpoint for Cloud Scheduler -> Pub/Sub push topic.
    """
    background_tasks.add_task(orchestrator.run_autonomous_workflow, "prod-core-cluster")
    return {"status": "ACK", "message": "Autonomous FinOps run scheduled"}

@app.get("/api/runs", response_model=List[ExecutionRecord])
def list_runs(limit: int = 20):
    """
    Lists recent autonomous optimization execution records.
    """
    return memory_agent.list_execution_records(limit=limit)

@app.get("/api/runs/{execution_id}", response_model=ExecutionRecord)
def get_run(execution_id: str):
    rec = memory_agent.get_execution_record(execution_id)
    if not rec:
        raise HTTPException(status_code=404, detail="Execution record not found")
    return rec

@app.get("/api/metrics")
def get_dashboard_metrics():
    """
    Computes overall FinOps Autopilot metrics for dashboard display.
    """
    runs = memory_agent.list_execution_records()
    total_spend = 2354.88
    total_savings_mo = sum(r.projected_monthly_savings for r in runs if r.status in (RunStatus.COMPLETED, RunStatus.VALIDATED, RunStatus.PR_CREATED))
    total_savings_yr = sum(r.projected_annual_savings for r in runs if r.status in (RunStatus.COMPLETED, RunStatus.VALIDATED, RunStatus.PR_CREATED))
    prs_created = sum(1 for r in runs if r.github_pr is not None)
    validations_passed = sum(1 for r in runs if r.validation_result and r.validation_result.status == "PASS")
    total_validations = sum(1 for r in runs if r.validation_result is not None)
    pass_rate = (validations_passed / total_validations * 100) if total_validations > 0 else 100.0

    return {
        "monthly_cloud_spend": total_spend,
        "potential_savings": total_savings_mo,
        "savings_identified_monthly": total_savings_mo,
        "savings_identified_annual": total_savings_yr,
        "optimizations_found": len(runs),
        "prs_created": prs_created,
        "validation_pass_rate": round(pass_rate, 1),
        "environment": settings.ENVIRONMENT,
        "demo_mode": settings.DEMO_MODE
    }
