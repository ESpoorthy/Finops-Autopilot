import pytest
from tools.memory_agent import MemoryAgent
from backend.models import ExecutionRecord, RunStatus

def test_memory_agent_persistence_and_idempotency():
    memory = MemoryAgent(demo_mode=True)
    memory.clear_memory()

    rec = ExecutionRecord(
        execution_id="exec-test-1",
        resource="prod-core-cluster",
        status=RunStatus.COMPLETED,
        new_configuration={"node_count": 5},
        projected_monthly_savings=432.00,
        projected_annual_savings=5184.00
    )
    memory.save_execution_record(rec)

    # Check persistence retrieval
    fetched = memory.get_execution_record("exec-test-1")
    assert fetched is not None
    assert fetched.execution_id == "exec-test-1"

    # Check idempotency guard
    assert memory.is_already_optimized("prod-core-cluster", 5) is True
    assert memory.is_already_optimized("prod-core-cluster", 8) is False
