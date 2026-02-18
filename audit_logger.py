"""Audit logging for customer data mutations."""
from datetime import datetime, timezone
from typing import Optional, Dict, Any


class AuditLogger:
    """Logger for tracking customer data mutations."""
    
    def __init__(self):
        self.logs = []
    
    def log_event(
        self,
        action: str,
        user: str,
        customer_id: Optional[int],
        before_state: Optional[Dict[str, Any]],
        after_state: Optional[Dict[str, Any]],
        metadata: Optional[Dict[str, Any]] = None
    ):
        """
        Log a customer data mutation event.
        
        Args:
            action: Type of action (CREATE, UPDATE, DELETE)
            user: User performing the action
            customer_id: ID of the customer being modified
            before_state: State before the change
            after_state: State after the change
            metadata: Additional metadata about the operation
        """
        log_entry = {
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'action': action,
            'user': user,
            'customer_id': customer_id,
            'before_state': before_state,
            'after_state': after_state,
            'metadata': metadata or {}
        }
        self.logs.append(log_entry)
        
        # In production, this would write to a persistent store
        print(f"[AUDIT] {log_entry['timestamp']} - {action} by {user} - Customer {customer_id}")
    
    def get_logs(self):
        """Get all audit logs."""
        return self.logs


# Global audit logger instance
audit_logger = AuditLogger()
