import os
from typing import List, Optional, Dict, Any
from backend.config import settings
from backend.models import ExecutionRecord, RunStatus

# Global in-memory storage fallback for local/demo runs
_IN_MEMORY_RUNS: Dict[str, ExecutionRecord] = {}

class MemoryAgent:
    """
    Manages persistent state of optimization executions in Firestore (or in-memory fallback).
    Ensures idempotency by checking if a resource has already been optimized.
    """
    def __init__(self, demo_mode: bool = None):
        self.demo_mode = settings.DEMO_MODE if demo_mode is None else demo_mode

    def clear_memory(self):
        _IN_MEMORY_RUNS.clear()

    def is_already_optimized(self, resource_id: str, target_node_count: int) -> bool:
        """
        Idempotency check: returns True if an active PR or completed optimization exists for this resource and config.
        """
        runs = self.list_execution_records()
        for r in runs:
            if r.resource == resource_id:
                # If a run is PR_CREATED, VALIDATED, or COMPLETED with same or smaller node count
                if r.status in (RunStatus.PR_CREATED, RunStatus.VALIDATING, RunStatus.VALIDATED, RunStatus.COMPLETED):
                    if r.new_configuration.get("node_count") == target_node_count:
                        return True
        return False

    def save_execution_record(self, record: ExecutionRecord) -> bool:
        # Always update local memory cache
        _IN_MEMORY_RUNS[record.execution_id] = record

        if self.demo_mode:
            return True

        try:
            from google.cloud import firestore
            db = firestore.Client(project=settings.GOOGLE_CLOUD_PROJECT, database=settings.FIRESTORE_DATABASE)
            doc_ref = db.collection("finops_runs").document(record.execution_id)
            doc_ref.set(record.model_dump())
            return True
        except Exception:
            # Fall back cleanly to in-memory store
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
        records = list(_IN_MEMORY_RUNS.values())

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

        # Sort in-memory records descending by created_at
        records.sort(key=lambda r: r.created_at, reverse=True)
        return records[:limit]
