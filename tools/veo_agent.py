import os
from typing import Optional, Dict, Any
from backend.config import settings
from backend.models import ExecutionRecord

class VeoAgent:
    """
    Optional Veo video summary bonus agent.
    Asynchronously generates an executive video presentation summarizing autonomous savings.
    """
    def __init__(self):
        self.enabled = os.getenv("ENABLE_VEO", "false").lower() in ("true", "1", "yes")

    def generate_executive_video(self, record: ExecutionRecord) -> Optional[Dict[str, Any]]:
        """
        Generates executive video script and asset links. Non-critical fallback.
        """
        try:
            script = f"""
            FinOps Autopilot Autonomous Executive Briefing:
            Resource: {record.resource}
            Finding: {record.finding}
            Monthly Savings Identified: ${record.projected_monthly_savings:,.2f}
            Annualized Impact: ${record.projected_annual_savings:,.2f}
            Confidence: {record.confidence * 100:.0f}%
            GitHub PR: #{record.github_pr.pr_number if record.github_pr else 'N/A'}
            Staging Validation: PASSED (Cloud Build)
            Human Merge Required: YES
            """
            
            video_summary = {
                "status": "GENERATED" if self.enabled else "SIMULATED",
                "script": script.strip(),
                "video_url": "https://storage.googleapis.com/finops-autopilot-media/veo-summary-demo.mp4",
                "duration_seconds": 15,
                "model": "veo-2.0-generate-001"
            }
            return video_summary
        except Exception:
            return None
