import json
import os
from typing import List
from backend.config import settings
from backend.models import CostMetric

class CostAnalyst:
    """
    Analyzes cloud cost and billing exports from BigQuery (LIVE MODE) or seeded demo data (DEMO MODE).
    """
    def __init__(self, demo_mode: bool = None):
        self.demo_mode = settings.DEMO_MODE if demo_mode is None else demo_mode

    def get_top_spending_resources(self, limit: int = 5) -> List[CostMetric]:
        if self.demo_mode:
            return self._get_demo_cost_metrics()
        
        try:
            from google.cloud import bigquery
            client = bigquery.Client(project=settings.GOOGLE_CLOUD_PROJECT)
            query = f"""
                SELECT
                    service.description AS resource_type,
                    sku.description AS resource_name,
                    SUM(cost) AS total_cost
                FROM `{settings.GOOGLE_CLOUD_PROJECT}.billing_export.gcp_billing_export_v1`
                WHERE _PARTITIONDATE >= DATE_SUB(CURRENT_DATE(), INTERVAL 30 DAY)
                GROUP BY 1, 2
                ORDER BY total_cost DESC
                LIMIT {limit}
            """
            query_job = client.query(query)
            results = query_job.result()
            metrics = []
            for row in results:
                metrics.append(CostMetric(
                    resource_id=f"bq-{row.resource_name}",
                    resource_name=row.resource_name,
                    resource_type=row.resource_type,
                    monthly_cost=float(row.total_cost),
                    currency="USD",
                    historical_trend="stable",
                    is_simulated=False
                ))
            return metrics if metrics else self._get_demo_cost_metrics()
        except Exception:
            # Fallback cleanly if GCP BigQuery permissions/dataset are unavailable
            return self._get_demo_cost_metrics()

    def _get_demo_cost_metrics(self) -> List[CostMetric]:
        demo_path = os.path.join(os.path.dirname(__file__), "..", "demo", "gke_metrics.json")
        if os.path.exists(demo_path):
            with open(demo_path, "r") as f:
                data = json.load(f)
                clusters = data.get("gke_clusters", [])
                if clusters:
                    c = clusters[0]
                    return [
                        CostMetric(
                            resource_id=c["cluster_name"],
                            resource_name=f"GKE Node Pool ({c['node_pool_name']}) [DEMO MODE]",
                            resource_type="Google Kubernetes Engine",
                            monthly_cost=c["total_monthly_cost"],
                            currency="USD",
                            historical_trend="high_waste",
                            is_simulated=True
                        )
                    ]
        return [
            CostMetric(
                resource_id="prod-core-cluster",
                resource_name="GKE Node Pool (default-pool) [DEMO MODE]",
                resource_type="Google Kubernetes Engine",
                monthly_cost=2354.88,
                currency="USD",
                historical_trend="high_waste",
                is_simulated=True
            )
        ]
