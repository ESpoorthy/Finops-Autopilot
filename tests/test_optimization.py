import pytest
from tools.optimization_agent import OptimizationAgent
from tools.terraform_generator import TerraformGenerator

def test_optimization_agent_golden_scenario():
    opt_agent = OptimizationAgent(demo_mode=True)
    proposal = opt_agent.analyze_and_optimize("prod-core-cluster")
    
    assert proposal is not None
    assert proposal.current_config["node_count"] == 12
    assert proposal.recommended_config["node_count"] == 5
    assert proposal.projected_monthly_savings == 432.00
    assert proposal.projected_annual_savings == 5184.00
    assert proposal.confidence_score == 0.94

def test_terraform_generator_node_count_patch():
    file_path = "infrastructure/terraform/gke.tf"
    success, old_c, new_c = TerraformGenerator.update_node_count(file_path, 12, 5)
    assert success is True
    assert "node_count = 5" in new_c
