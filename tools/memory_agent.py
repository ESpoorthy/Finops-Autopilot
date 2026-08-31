import json
import os
from typing import List, Optional, Dict
from backend.config import settings
from backend.models import ExecutionRecord, RunStatus

# Global in-memory storage cache
_IN_MEMORY_RUNS: Dict[str, ExecutionRecord] = {}

class MemoryAgent:
    """
    Manages persistent state of optimization executions in Firestore (LIVE MODE) or local JSON file (DEMO MODE).
    Ensures idempotency by checking if a resource has already been optimized.
    """
    def __init__(self, demo_mode: bool = None):
        self.demo_mode = settings.DEMO_MODE if demo_mode is None else demo_mode
        self.file_path = os.path.join(os.path.dirname(__file__), "..", "demo", "execution_history.json")
        self._load_from_file()

    def clear_memory(self):
        _IN_MEMORY_RUNS.clear()
        if os.path.exists(self.file_path):
            try:
                os.remove(self.file_path)
            except Exception:
                pass

    def is_already_optimized(self, resource_id: str, target_node_count: int) -> bool:
        """
        Idempotency check: returns True if an active PR or completed optimization exists for this resource and config.
        """
        runs = self.list_execution_records()
        for r in runs:
            if r.resource == resource_id:
                if r.status in (RunStatus.PR_CREATED, RunStatus.VALIDATING, RunStatus.VALIDATED, RunStatus.COMPLETED):
                    if r.new_configuration.get("node_count") == target_node_count:
                        return True
        return False

    def save_execution_record(self, record: ExecutionRecord) -> bool:
        _IN_MEMORY_RUNS[record.execution_id] = record
        self._save_to_file()

        if self.demo_mode:
            return True

        try:
            from google.cloud import firestore
            db = firestore.Client(project=settings.GOOGLE_CLOUD_PROJECT, database=settings.FIRESTORE_DATABASE)
            doc_ref = db.collection("finops_runs").document(record.execution_id)
            doc_ref.set(record.model_dump())
            return True
        except Exception:
            return True

    def get_execution_record(self, execution_id: str) -> Optional[ExecutionRecord]:
        if execution_id in _IN_MEMORY_RUNS:
            return _IN_MEMORY_RUNS[execution_id]

        if not self.demo_mode:
            try:
                from google.cloud import firestore
                db = firestore.Client(project=settings.GOOGLE_CLOUD_PROJECT, database=settings.FIRESTORE_DATABASE)
                doc_ref = db.collection("finops_runs").document(execution_id)
                doc = doc_ref.get()
                if doc.exists:
                    return ExecutionRecord(**doc.to_dict())
            except Exception:
                pass
        return None

    def list_execution_records(self, limit: int = 20) -> List[ExecutionRecord]:
        if not self.demo_mode:
            try:
                from google.cloud import firestore
                db = firestore.Client(project=settings.GOOGLE_CLOUD_PROJECT, database=settings.FIRESTORE_DATABASE)
                docs = db.collection("finops_runs").order_by("created_at", direction=firestore.Query.DESCENDING).limit(limit).stream()
                fs_records = [ExecutionRecord(**doc.to_dict()) for doc in docs]
                if fs_records:
                    return fs_records
            except Exception:
                pass

        records = list(_IN_MEMORY_RUNS.values())
        records.sort(key=lambda r: r.created_at, reverse=True)
        return records[:limit]

    def _save_to_file(self):
        try:
            os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
            data = [r.model_dump() for r in _IN_MEMORY_RUNS.values()]
            with open(self.file_path, "w") as f:
                json.dump(data, f, indent=2)
        except Exception:
            pass

    def _load_from_file(self):
        if os.path.exists(self.file_path):
            try:
                with open(self.file_path, "r") as f:
                    data = json.load(f)
                    for item in data:
                        rec = ExecutionRecord(**item)
                        _IN_MEMORY_RUNS[rec.execution_id] = rec
            except Exception:
                pass
