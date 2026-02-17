import json
import os
from datetime import datetime, timezone
from typing import Dict, Any, Optional


class AuditLogger:
    """
    KYC Audit Logger for tracking all customer data mutations.
    Logs are written to a JSON file for compliance and auditing purposes.
    """
    
    def __init__(self, log_file: str = "audit_logs.json"):
        self.log_file = log_file
        self._ensure_log_file_exists()
    
    def _ensure_log_file_exists(self):
        """Create log file if it doesn't exist."""
        if not os.path.exists(self.log_file):
            with open(self.log_file, 'w') as f:
                json.dump([], f)
    
    def log_mutation(
        self,
        action: str,
        entity_type: str,
        entity_id: Optional[str],
        user: str,
        data_before: Optional[Dict[str, Any]] = None,
        data_after: Optional[Dict[str, Any]] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Log a customer data mutation for KYC audit purposes.
        
        Args:
            action: The type of mutation (CREATE, UPDATE, DELETE)
            entity_type: Type of entity being mutated (e.g., 'customer')
            entity_id: Unique identifier of the entity
            user: User who performed the action
            data_before: State of data before mutation (for UPDATE/DELETE)
            data_after: State of data after mutation (for CREATE/UPDATE)
            metadata: Additional context or metadata
        
        Returns:
            The created audit log entry
        """
        log_entry = {
            "timestamp": datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z'),
            "action": action,
            "entity_type": entity_type,
            "entity_id": entity_id,
            "user": user,
            "data_before": data_before,
            "data_after": data_after,
            "metadata": metadata or {}
        }
        
        # Read existing logs
        with open(self.log_file, 'r') as f:
            logs = json.load(f)
        
        # Append new log
        logs.append(log_entry)
        
        # Write back to file
        with open(self.log_file, 'w') as f:
            json.dump(logs, f, indent=2)
        
        return log_entry
    
    def get_logs(
        self,
        entity_type: Optional[str] = None,
        entity_id: Optional[str] = None,
        action: Optional[str] = None,
        user: Optional[str] = None
    ) -> list:
        """
        Retrieve audit logs with optional filtering.
        
        Args:
            entity_type: Filter by entity type
            entity_id: Filter by entity ID
            action: Filter by action type
            user: Filter by user
        
        Returns:
            List of matching audit log entries
        """
        with open(self.log_file, 'r') as f:
            logs = json.load(f)
        
        filtered_logs = logs
        
        if entity_type:
            filtered_logs = [log for log in filtered_logs if log.get('entity_type') == entity_type]
        
        if entity_id:
            filtered_logs = [log for log in filtered_logs if log.get('entity_id') == entity_id]
        
        if action:
            filtered_logs = [log for log in filtered_logs if log.get('action') == action]
        
        if user:
            filtered_logs = [log for log in filtered_logs if log.get('user') == user]
        
        return filtered_logs
