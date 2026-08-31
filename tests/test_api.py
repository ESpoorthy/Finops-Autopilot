import pytest
from fastapi.testclient import TestClient
from backend.main import app
from tools.memory_agent import MemoryAgent

client = TestClient(app)

def test_dashboard_metrics_endpoint():
    MemoryAgent().clear_memory()
    res = client.get("/api/metrics")
    assert res.status_code == 200
    data = res.json()
    assert "monthly_cloud_spend" in data
    assert "savings_identified_monthly" in data
    assert "validation_pass_rate" in data

def test_list_runs_endpoint():
    MemoryAgent().clear_memory()
    res = client.get("/api/runs")
    assert res.status_code == 200
    assert isinstance(res.json(), list)

def test_trigger_orchestrator_api():
    MemoryAgent().clear_memory()
    res = client.post("/api/run-orchestrator", json={"cluster_name": "prod-core-cluster", "demo_mode": True})
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "COMPLETED"
    assert data["projected_monthly_savings"] == 432.00
    assert data["projected_annual_savings"] == 5184.00

def test_pubsub_webhook_endpoint():
    res = client.post("/pubsub/trigger", json={"subscription": "projects/demo/subscriptions/sub"})
    assert res.status_code == 200
    assert res.json()["status"] == "ACK"
