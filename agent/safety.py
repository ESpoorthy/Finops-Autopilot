from typing import List, Dict, Any
from backend.config import settings
from backend.models import OptimizationProposal, SafetyPolicyResult

class SafetyAgent:
    """
    Evaluates whether an infrastructure optimization proposal satisfies safety guardrails.
    Enforces autonomy within policy boundaries.
    """
    PROTECTED_CATEGORIES = [
        "iam",
        "kms",
        "encryption",
        "firewall",
        "vpc_network",
        "prod_database",
        "security_policy"
    ]

    def __init__(self,
                 max_monthly_change: float = None,
                 min_confidence: float = None):
        self.max_monthly_change = max_monthly_change or settings.MAX_MONTHLY_CHANGE
        self.min_confidence = min_confidence or settings.MIN_CONFIDENCE

    def evaluate_proposal(self, proposal: OptimizationProposal) -> SafetyPolicyResult:
        # Check 1: Protected Categories & Resources
        resource_lower = f"{proposal.resource_id} {proposal.resource_type} {proposal.tf_file_path}".lower()
        blocked_cats = [cat for cat in self.PROTECTED_CATEGORIES if cat in resource_lower]
        if blocked_cats:
            return SafetyPolicyResult(
                is_allowed=False,
                policy_name="PROTECTED_RESOURCE_POLICY",
                reason=f"Resource matches protected security/infrastructure categories: {', '.join(blocked_cats)}. Direct automated modification is forbidden.",
                blocked_categories=blocked_cats
            )

        # Check 2: Minimum Confidence Score
        if proposal.confidence_score < self.min_confidence:
            return SafetyPolicyResult(
                is_allowed=False,
                policy_name="MINIMUM_CONFIDENCE_POLICY",
                reason=f"Proposal confidence score ({proposal.confidence_score * 100:.1f}%) is below safety threshold ({self.min_confidence * 100:.1f}%)."
            )

        # Check 3: Max Monthly Financial Impact Change Limit
        if proposal.projected_monthly_savings > self.max_monthly_change:
            return SafetyPolicyResult(
                is_allowed=False,
                policy_name="MAX_MONTHLY_CHANGE_POLICY",
                reason=f"Projected monthly change (${proposal.projected_monthly_savings:.2f}) exceeds safety cap (${self.max_monthly_change:.2f}). Requires manual architectural review."
            )

        # Check 4: Staging Validation & Human Merge Mandatory
        return SafetyPolicyResult(
            is_allowed=True,
            policy_name="AUTONOMY_WITHIN_BOUNDARIES",
            reason=f"Proposal PASSED all safety guardrails. Changes are permitted via GitHub PR + Cloud Build validation + mandatory human merge."
        )
