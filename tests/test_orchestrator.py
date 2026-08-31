import pytest
from agent.orchestrator import FinOpsOrchestrator
from backend.models import RunStatus
from tools.memory_agent import MemoryAgent

def test_orchestrator_end_to_end_demo_run():
    MemoryAgent().clear_memory()
    orchestrator = FinOpsOrchestrator(demo_mode=True)
    record = orchestrator.run_autonomous_workflow("prod-core-cluster")

    assert record is not None
    assert record.status == RunStatus.COMPLETED
    assert record.projected_monthly_savings == 432.00
    assert record.projected_annual_savings == 5184.00
    assert record.old_configuration["node_count"] == 12
    assert record.new_configuration["node_count"] == 5
    assert record.github_pr is not None
    assert record.validation_result is not None
    assert record.validation_result.status == "PASS"

def test_orchestrator_idempotency_guard():
    MemoryAgent().clear_memory()
    orchestrator = FinOpsOrchestrator(demo_mode=True)
    # First run creates PR & completes optimization
    record1 = orchestrator.run_autonomous_workflow("prod-core-cluster")
    assert record1.status == RunStatus.COMPLETED
    assert record1.github_pr is not None

    # Immediate second run triggers idempotency guard
    record2 = orchestrator.run_autonomous_workflow("prod-core-cluster")
    assert record2.status == RunStatus.COMPLETED
    assert record2.github_pr is None # Skipped PR creation due to duplicate guard
