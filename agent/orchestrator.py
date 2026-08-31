import uuid
from typing import Dict, Any, Optional
from google.adk import Agent
from backend.config import settings
from backend.models import ExecutionRecord, RunStatus, SafetyPolicyResult, GitHubPRResult
from tools.cost_analyst import CostAnalyst
from tools.architecture_analyst import ArchitectureAnalyst
from tools.optimization_agent import OptimizationAgent
from agent.safety import SafetyAgent
from tools.github_agent import GitHubAgent
from tools.validation_agent import ValidationAgent
from tools.memory_agent import MemoryAgent
from agent.prompts import FINOPS_ORCHESTRATOR_SYSTEM_PROMPT

class FinOpsOrchestrator:
    """
    Google ADK FinOps Orchestrator.
    Coordinates the autonomous end-to-end cloud cost optimization workflow.
    """
    def __init__(self, demo_mode: bool = None):
        self.demo_mode = settings.DEMO_MODE if demo_mode is None else demo_mode
        self.adk_agent = Agent(
            name="FinOpsOrchestratorAgent",
            model=settings.GEMINI_MODEL,
            instruction=FINOPS_ORCHESTRATOR_SYSTEM_PROMPT
        )
        self.opt_agent = OptimizationAgent(demo_mode=self.demo_mode)
        self.safety_agent = SafetyAgent()
        self.github_agent = GitHubAgent()
        self.validation_agent = ValidationAgent()
        self.memory_agent = MemoryAgent(demo_mode=self.demo_mode)

    def run_autonomous_workflow(self, cluster_name: str = "prod-core-cluster") -> ExecutionRecord:
        execution_id = f"exec-{uuid.uuid4().hex[:8]}"
        logs = []

        def log(msg: str):
            logs.append(msg)

        log(f"[1/8 PENDING] Initialized execution run {execution_id} for resource {cluster_name}.")
        
        record = ExecutionRecord(
            execution_id=execution_id,
            status=RunStatus.PENDING,
            resource=cluster_name,
            logs=logs
        )
        self.memory_agent.save_execution_record(record)

        # Step 2: ANALYZING
        record.status = RunStatus.ANALYZING
        log("[2/8 ANALYZING] Querying BigQuery billing export and Cloud Monitoring metrics...")
        self.memory_agent.save_execution_record(record)

        proposal = self.opt_agent.analyze_and_optimize(cluster_name)
        if not proposal:
            record.status = RunStatus.COMPLETED
            log("[2/8 ANALYZING] No actionable waste detected. Cluster is right-sized.")
            self.memory_agent.save_execution_record(record)
            return record

        log(f"[3/8 OPTIMIZATION_FOUND] Detected over-provisioned GKE pool. Finding: {proposal.finding}")
        log(f"Projected Monthly Savings: ${proposal.projected_monthly_savings:,.2f} | Confidence: {proposal.confidence_score*100:.1f}%")
        
        record.status = RunStatus.OPTIMIZATION_FOUND
        record.finding = proposal.finding
        record.evidence = proposal.evidence
        record.old_configuration = proposal.current_config
        record.new_configuration = proposal.recommended_config
        record.projected_monthly_savings = proposal.projected_monthly_savings
        record.projected_annual_savings = proposal.projected_annual_savings
        record.confidence = proposal.confidence_score
        record.risk = proposal.risk_level
        self.memory_agent.save_execution_record(record)

        # Idempotency check: check if already proposed/applied
        target_nodes = proposal.recommended_config.get("node_count", 5)
        if self.memory_agent.is_already_optimized(cluster_name, target_nodes):
            log(f"[IDEMPOTENCY] Active PR or optimization already exists for {cluster_name} with target nodes={target_nodes}. Skipping duplicate action.")
            record.status = RunStatus.COMPLETED
            self.memory_agent.save_execution_record(record)
            return record

        # Step 4: SAFETY_CHECK
        log("[4/8 SAFETY_CHECK] Evaluating proposal against safety guardrail policies...")
        safety_res = self.safety_agent.evaluate_proposal(proposal)
        record.safety_result = safety_res

        if not safety_res.is_allowed:
            record.status = RunStatus.SAFETY_BLOCKED
            log(f"[4/8 SAFETY_BLOCKED] Proposal blocked by policy '{safety_res.policy_name}': {safety_res.reason}")
            self.memory_agent.save_execution_record(record)
            return record

        log(f"[4/8 SAFETY_CHECK] Passed policy guardrails ({safety_res.policy_name}).")

        # Step 5: PR_CREATED
        log("[5/8 PR_CREATED] Applying Terraform patch and opening GitHub Pull Request...")
        pr_res = self.github_agent.create_optimization_pr(proposal, safety_res)
        record.github_pr = pr_res
        record.status = RunStatus.PR_CREATED
        log(f"[5/8 PR_CREATED] GitHub PR #{pr_res.pr_number} created: {pr_res.pr_url}")
        self.memory_agent.save_execution_record(record)

        # Step 6: VALIDATING
        log("[6/8 VALIDATING] Triggering Cloud Build staging validation pipeline...")
        record.status = RunStatus.VALIDATING
        val_res, build_id = self.validation_agent.run_staging_validation(proposal.tf_file_path)
        record.validation_result = val_res
        record.cloud_build_id = build_id

        if val_res.status == "PASS":
            record.status = RunStatus.VALIDATED
            log(f"[6/8 VALIDATED] Cloud Build {build_id} PASSED (fmt, validate, plan, policy checks).")
        else:
            record.status = RunStatus.FAILED
            record.error_message = "Staging validation failed"
            log(f"[6/8 FAILED] Cloud Build {build_id} FAILED validation.")
            self.memory_agent.save_execution_record(record)
            return record

        # Step 7 & 8: RECORD & COMPLETED
        record.status = RunStatus.COMPLETED
        log(f"[7/8 RECORD] Persisted execution record {execution_id} into Firestore memory.")
        log(f"[8/8 COMPLETED] FinOps Autopilot successfully completed golden right-sizing run.")
        self.memory_agent.save_execution_record(record)

        return record
