import pytest
from fastapi.testclient import TestClient
from backend.main import app
from tools.memory_agent import MemoryAgent

client = TestClient(app)

def test_health_endpoint():
    res = client.get("/health")
    assert res.status_code == 200
    assert res.json()["status"] == "HEALTHY"

def test_dashboard_metrics_and_runs_single_source_of_truth():
    MemoryAgent().clear_memory()
    
    # Trigger orchestrator run
    run_res = client.post("/api/run-orchestrator", json={"cluster_name": "prod-core-cluster", "demo_mode": True})
    assert run_res.status_code == 200
    run_data = run_res.json()
    assert run_data["status"] == "COMPLETED"

    # Verify metrics matches run data
    metrics_res = client.get("/api/metrics")
    assert metrics_res.status_code == 200
    m_data = metrics_res.json()
    assert m_data["potential_savings"] == run_data["projected_monthly_savings"]
    assert m_data["savings_identified_annual"] == run_data["projected_annual_savings"]
    assert m_data["optimizations_found"] >= 1

def test_pubsub_webhook_endpoint():
    res = client.post("/pubsub/trigger", json={"subscription": "projects/demo/subscriptions/sub"})
    assert res.status_code == 200
    assert res.json()["status"] == "ACK"
