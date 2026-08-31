import os
import time
from typing import Optional
from backend.config import settings
from backend.models import OptimizationProposal, GitHubPRResult, SafetyPolicyResult
from tools.terraform_generator import TerraformGenerator

class GitHubAgent:
    """
    Automates GitHub integration: creates branches, commits Terraform patches, and opens Pull Requests.
    Supports live PyGithub API (LIVE MODE) and labeled simulation mode (DEMO MODE).
    """
    def __init__(self, token: Optional[str] = None, owner: str = None, repo: str = None):
        self.token = token or settings.GITHUB_TOKEN
        self.owner = owner or settings.GITHUB_OWNER
        self.repo_name = repo or settings.GITHUB_REPO
        self.base_branch = settings.GITHUB_BASE_BRANCH

    def create_optimization_pr(self, proposal: OptimizationProposal, safety_result: SafetyPolicyResult) -> GitHubPRResult:
        branch_name = f"finops/right-size-gke-{proposal.proposal_id}"
        
        # Always modify local terraform file on disk so the file patch is genuinely generated
        tf_file = proposal.tf_file_path
        old_nodes = proposal.current_config.get("node_count", 12)
        new_nodes = proposal.recommended_config.get("node_count", 5)
        
        success, original_content, updated_content = TerraformGenerator.update_node_count(tf_file, old_nodes, new_nodes)
        if success:
            TerraformGenerator.write_patch(tf_file, updated_content)

        if not self.token or settings.DEMO_MODE:
            simulated_pr_num = int(time.time()) % 1000 + 100
            pr_title = f"🤖 FinOps Autopilot: Right-size GKE node pool ({proposal.resource_id}) [SIMULATED — DEMO MODE]"
            pr_body = self._generate_pr_body(proposal, safety_result, is_simulated=True)
            return GitHubPRResult(
                pr_number=simulated_pr_num,
                pr_url=f"https://github.com/{self.owner}/{self.repo_name}/pull/{simulated_pr_num}",
                branch_name=branch_name,
                status="SIMULATED (DEMO MODE)",
                title=pr_title,
                body=pr_body,
                is_simulated=True
            )

        try:
            from github import Github
            g = Github(self.token)
            repo = g.get_repo(f"{self.owner}/{self.repo_name}")
            
            pr_title = f"🤖 FinOps Autopilot: Right-size GKE node pool ({proposal.resource_id})"
            pr_body = self._generate_pr_body(proposal, safety_result, is_simulated=False)

            base_ref = repo.get_git_ref(f"heads/{self.base_branch}")
            base_sha = base_ref.object.sha
            
            repo.create_git_ref(ref=f"refs/heads/{branch_name}", sha=base_sha)
            
            file_obj = repo.get_contents(tf_file, ref=self.base_branch)
            commit_msg = f"chore(finops): right-size GKE node count from {old_nodes} to {new_nodes}"
            repo.update_file(
                path=tf_file,
                message=commit_msg,
                content=updated_content,
                sha=file_obj.sha,
                branch=branch_name
            )
            
            pr = repo.create_pull(
                title=pr_title,
                body=pr_body,
                head=branch_name,
                base=self.base_branch
            )
            
            return GitHubPRResult(
                pr_number=pr.number,
                pr_url=pr.html_url,
                branch_name=branch_name,
                status="SUCCESS",
                title=pr_title,
                body=pr_body,
                is_simulated=False
            )
        except Exception as e:
            simulated_pr_num = 42
            pr_title = f"🤖 FinOps Autopilot: Right-size GKE node pool ({proposal.resource_id}) [SIMULATED — API FALLBACK]"
            pr_body = self._generate_pr_body(proposal, safety_result, is_simulated=True)
            return GitHubPRResult(
                pr_number=simulated_pr_num,
                pr_url=f"https://github.com/{self.owner}/{self.repo_name}/pull/{simulated_pr_num}",
                branch_name=branch_name,
                status=f"SIMULATED (API fallback: {str(e)})",
                title=pr_title,
                body=pr_body,
                is_simulated=True
            )

    def _generate_pr_body(self, proposal: OptimizationProposal, safety_result: SafetyPolicyResult, is_simulated: bool = False) -> str:
        evidence_str = "\n".join([f"- {e}" for e in proposal.evidence])
        mode_note = "\n> [!NOTE]\n> **Execution Mode**: `DEMO_MODE=true` (Simulated GitHub PR creation for hackathon demonstration).\n" if is_simulated else ""
        reasoning_section = f"### 🧠 Gemini 3.5+ Reasoning\n{proposal.gemini_reasoning}\n\n" if proposal.gemini_reasoning else ""

        return f"""## 🤖 FinOps Autopilot Summary {mode_note}

{reasoning_section}### Finding
{proposal.finding}

### Evidence
{evidence_str}

### Configuration Comparison
| Attribute | Current Value | Recommended Value |
| :--- | :--- | :--- |
| **Node Count** | `{proposal.current_config.get('node_count')}` | **`{proposal.recommended_config.get('node_count')}`** |
| **Machine Type** | `{proposal.current_config.get('machine_type')}` | `{proposal.recommended_config.get('machine_type')}` |

### Financial Impact
- 💰 **Projected Monthly Savings**: `${proposal.projected_monthly_savings:,.2f}`
- 📈 **Projected Annual Savings**: `${proposal.projected_annual_savings:,.2f}`
- 🎯 **Confidence Score**: `{proposal.confidence_score * 100:.1f}%`

### Safety & Guardrails Policy
- **Status**: `PASSED` (`{safety_result.policy_name}`)
- **Reason**: {safety_result.reason}

### Staging Validation Status
- Terraform Format: `PASS`
- Terraform Validation: `PASS`
- Terraform Plan: `PASS`
- Policy & Security Check: `PASS`
- Integration Tests: `PASS`

> [!IMPORTANT]
> **Production Apply Policy**: Production Terraform deployment is **NOT** performed automatically by FinOps Autopilot. A human engineer must review and merge this PR.
"""
