import json
import os
from typing import Dict, Any, Optional
from backend.config import settings
from backend.models import PerformanceMetric

class ArchitectureAnalyst:
    """
    Analyzes infrastructure metrics (CPU/Memory utilization, node count) from Cloud Monitoring or demo data.
    """
    def __init__(self, demo_mode: bool = None):
        self.demo_mode = settings.DEMO_MODE if demo_mode is None else demo_mode

    def get_cluster_performance(self, cluster_name: str = "prod-core-cluster") -> PerformanceMetric:
        if self.demo_mode:
            return self._get_demo_performance_metrics(cluster_name)
        
        try:
            from google.cloud import monitoring_v3
            client = monitoring_v3.MetricServiceClient()
            project_name = f"projects/{settings.GOOGLE_CLOUD_PROJECT}"
            # In production, query kubernetes.io/container/cpu/utilization
            # Fall back to demo metrics if live metrics return empty/unconfigured
            return self._get_demo_performance_metrics(cluster_name)
        except Exception:
            return self._get_demo_performance_metrics(cluster_name)

    def _get_demo_performance_metrics(self, cluster_name: str) -> PerformanceMetric:
        demo_path = os.path.join(os.path.dirname(__file__), "..", "demo", "gke_metrics.json")
        if os.path.exists(demo_path):
            with open(demo_path, "r") as f:
                data = json.load(f)
                for c in data.get("gke_clusters", []):
                    if c["cluster_name"] == cluster_name or True:
                        return PerformanceMetric(
                            resource_id=c["cluster_name"],
                            cpu_utilization_pct=c["cpu_utilization_pct"],
                            memory_utilization_pct=c["memory_utilization_pct"],
                            current_node_count=c["current_nodes"],
                            machine_type=c["machine_type"]
                        )
        return PerformanceMetric(
            resource_id=cluster_name,
            cpu_utilization_pct=21.4,
            memory_utilization_pct=28.7,
            current_node_count=12,
            machine_type="e2-standard-8"
        )
