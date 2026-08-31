from enum import Enum
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from datetime import datetime, timezone

class RunStatus(str, Enum):
    PENDING = "PENDING"
    ANALYZING = "ANALYZING"
    OPTIMIZATION_FOUND = "OPTIMIZATION_FOUND"
    SAFETY_VALIDATED = "SAFETY_VALIDATED"
    SAFETY_BLOCKED = "SAFETY_BLOCKED"
    PR_CREATED = "PR_CREATED"
    VALIDATING = "VALIDATING"
    VALIDATED = "VALIDATED"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"

class CostMetric(BaseModel):
    resource_id: str
    resource_name: str
    resource_type: str
    monthly_cost: float
    currency: str = "USD"
    historical_trend: str = "stable"
    is_simulated: bool = False

class PerformanceMetric(BaseModel):
    resource_id: str
    cpu_utilization_pct: float
    memory_utilization_pct: float
    current_node_count: int
    machine_type: str
    is_simulated: bool = False

class OptimizationProposal(BaseModel):
    proposal_id: str
    resource_id: str
    resource_name: str
    resource_type: str
    finding: str
    evidence: List[str]
    current_config: Dict[str, Any]
    recommended_config: Dict[str, Any]
    projected_monthly_savings: float
    projected_annual_savings: float
    confidence_score: float = Field(..., ge=0.0, le=1.0)
    risk_level: str = "LOW"
    tf_file_path: str = "infrastructure/terraform/gke.tf"
    is_demo: bool = True
    gemini_reasoning: Optional[str] = None

class SafetyPolicyResult(BaseModel):
    is_allowed: bool
    policy_name: str
    reason: str
    blocked_categories: List[str] = []

class GitHubPRResult(BaseModel):
    pr_number: Optional[int] = None
    pr_url: Optional[str] = None
    branch_name: Optional[str] = None
    status: str = "SUCCESS" # e.g., SUCCESS or "SIMULATED (DEMO MODE)"
    title: str = ""
    body: str = ""
    is_simulated: bool = False

class ValidationResult(BaseModel):
    status: str # PASS or FAIL
    terraform_fmt: bool = True
    terraform_validate: bool = True
    terraform_plan: bool = True
    policy_check: bool = True
    integration_test: bool = True
    details: List[str] = []
    is_simulated: bool = False

class ExecutionRecord(BaseModel):
    execution_id: str
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    updated_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    status: RunStatus = RunStatus.PENDING
    resource: str = ""
    finding: Optional[str] = None
    evidence: List[str] = []
    old_configuration: Dict[str, Any] = {}
    new_configuration: Dict[str, Any] = {}
    projected_monthly_savings: float = 0.0
    projected_annual_savings: float = 0.0
    confidence: float = 0.0
    risk: str = "LOW"
    safety_result: Optional[SafetyPolicyResult] = None
    github_pr: Optional[GitHubPRResult] = None
    cloud_build_id: Optional[str] = None
    validation_result: Optional[ValidationResult] = None
    gemini_reasoning: Optional[str] = None
    logs: List[str] = []
    error_message: Optional[str] = None
    is_demo_mode: bool = True
