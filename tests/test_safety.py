import pytest
from agent.safety import SafetyAgent
from backend.models import OptimizationProposal

def test_safety_agent_allows_valid_proposal():
    agent = SafetyAgent(max_monthly_change=1000.0, min_confidence=0.80)
    proposal = OptimizationProposal(
        proposal_id="opt-123",
        resource_id="prod-core-cluster",
        resource_name="GKE Node Pool",
        resource_type="Google Kubernetes Engine",
        finding="Overprovisioned GKE nodes",
        evidence=["CPU utilization 21.4%"],
        current_config={"node_count": 12},
        recommended_config={"node_count": 5},
        projected_monthly_savings=432.00,
        projected_annual_savings=5184.00,
        confidence_score=0.94,
        risk_level="LOW"
    )
    result = agent.evaluate_proposal(proposal)
    assert result.is_allowed is True
    assert result.policy_name == "AUTONOMY_WITHIN_BOUNDARIES"

def test_safety_agent_blocks_protected_resource():
    agent = SafetyAgent()
    proposal = OptimizationProposal(
        proposal_id="opt-iam",
        resource_id="prod-iam-policy-binding",
        resource_name="IAM Admin Roles",
        resource_type="iam_policy",
        finding="Excessive IAM permissions",
        evidence=["Unused role"],
        current_config={"roles": ["owner"]},
        recommended_config={"roles": ["viewer"]},
        projected_monthly_savings=100.0,
        projected_annual_savings=1200.0,
        confidence_score=0.99,
        risk_level="HIGH"
    )
    result = agent.evaluate_proposal(proposal)
    assert result.is_allowed is False
    assert result.policy_name == "PROTECTED_RESOURCE_POLICY"

def test_safety_agent_blocks_low_confidence():
    agent = SafetyAgent(min_confidence=0.85)
    proposal = OptimizationProposal(
        proposal_id="opt-low-conf",
        resource_id="prod-cluster",
        resource_name="GKE Pool",
        resource_type="Google Kubernetes Engine",
        finding="Unclear metric pattern",
        evidence=["Spiky CPU"],
        current_config={"node_count": 10},
        recommended_config={"node_count": 5},
        projected_monthly_savings=200.0,
        projected_annual_savings=2400.0,
        confidence_score=0.65,
        risk_level="MEDIUM"
    )
    result = agent.evaluate_proposal(proposal)
    assert result.is_allowed is False
    assert result.policy_name == "MINIMUM_CONFIDENCE_POLICY"
