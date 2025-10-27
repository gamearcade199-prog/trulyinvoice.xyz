"""
Audit Logging
FIX #11: Comprehensive Audit Logging for Compliance

Tracks all user actions for security and regulatory compliance
"""

from datetime import datetime
from enum import Enum
from typing import Optional, Dict, Any
import json
from sqlalchemy import Column, Integer, String, DateTime, Text
from app.core.database import Base
import logging

logger = logging.getLogger(__name__)


class AuditAction(str, Enum):
    """Audit action types"""
    # Authentication
    LOGIN = "login"
    LOGOUT = "logout"
    LOGIN_FAILED = "login_failed"
    PASSWORD_CHANGED = "password_changed"
    PASSWORD_RESET = "password_reset"
    
    # Subscription
    SUBSCRIPTION_CREATED = "subscription_created"
    SUBSCRIPTION_UPGRADED = "subscription_upgraded"
    SUBSCRIPTION_DOWNGRADED = "subscription_downgraded"
    SUBSCRIPTION_CANCELLED = "subscription_cancelled"
    SUBSCRIPTION_RENEWED = "subscription_renewed"
    
    # Payment
    PAYMENT_INITIATED = "payment_initiated"
    PAYMENT_COMPLETED = "payment_completed"
    PAYMENT_FAILED = "payment_failed"
    PAYMENT_REFUNDED = "payment_refunded"
    
    # Invoice
    INVOICE_UPLOADED = "invoice_uploaded"
    INVOICE_PROCESSED = "invoice_processed"
    INVOICE_EXPORTED = "invoice_exported"
    INVOICE_DELETED = "invoice_deleted"
    INVOICE_SHARED = "invoice_shared"
    
    # Account
    ACCOUNT_UPDATED = "account_updated"
    ACCOUNT_DELETED = "account_deleted"
    PROFILE_UPDATED = "profile_updated"
    EMAIL_VERIFIED = "email_verified"
    
    # Administrative
    ADMIN_ACTION = "admin_action"
    RATE_LIMIT_HIT = "rate_limit_hit"
    SECURITY_ALERT = "security_alert"


class AuditLog(Base):
    """Database model for audit logs"""
    __tablename__ = "audit_logs"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(String(255), nullable=True, index=True)
    action = Column(String(100), nullable=False, index=True)
    resource_type = Column(String(100), nullable=True)  # "invoice", "subscription", etc.
    resource_id = Column(String(255), nullable=True, index=True)
    status = Column(String(50), nullable=False)  # "success", "failure", "blocked"
    
    # Request details
    ip_address = Column(String(45), nullable=True)
    user_agent = Column(String(500), nullable=True)
    request_method = Column(String(10), nullable=True)  # GET, POST, etc.
    request_path = Column(String(500), nullable=True)
    
    # Change details
    old_values = Column(Text, nullable=True)  # JSON
    new_values = Column(Text, nullable=True)  # JSON
    
    # Additional context
    description = Column(Text, nullable=True)
    error_message = Column(Text, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow, index=True)
    
    def __repr__(self):
        return f"<AuditLog(user_id={self.user_id}, action={self.action}, status={self.status})>"
    
    def to_dict(self) -> Dict:
        """Convert to dictionary"""
        return {
            "id": self.id,
            "user_id": self.user_id,
            "action": self.action,
            "resource_type": self.resource_type,
            "resource_id": self.resource_id,
            "status": self.status,
            "ip_address": self.ip_address,
            "description": self.description,
            "created_at": self.created_at.isoformat()
        }


class AuditLogger:
    """Log audit events to database"""
    
    @staticmethod
    def log_action(
        db,
        user_id: Optional[str],
        action: AuditAction,
        status: str = "success",
        resource_type: Optional[str] = None,
        resource_id: Optional[str] = None,
        description: Optional[str] = None,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None,
        request_method: Optional[str] = None,
        request_path: Optional[str] = None,
        old_values: Optional[Dict] = None,
        new_values: Optional[Dict] = None,
        error_message: Optional[str] = None
    ) -> AuditLog:
        """
        Log an action to audit log
        
        Args:
            db: Database session
            user_id: User performing action
            action: Action type
            status: success, failure, blocked
            resource_type: Type of resource affected
            resource_id: ID of resource
            description: Human-readable description
            ip_address: Client IP
            user_agent: Client user agent
            request_method: HTTP method
            request_path: Request path
            old_values: Previous state (for updates)
            new_values: New state (for updates)
            error_message: Error details if failed
        
        Returns:
            AuditLog record
        """
        try:
            audit_log = AuditLog(
                user_id=user_id,
                action=action.value,
                status=status,
                resource_type=resource_type,
                resource_id=resource_id,
                ip_address=ip_address,
                user_agent=user_agent,
                request_method=request_method,
                request_path=request_path,
                description=description,
                error_message=error_message,
                old_values=json.dumps(old_values) if old_values else None,
                new_values=json.dumps(new_values) if new_values else None,
                created_at=datetime.utcnow()
            )
            
            db.add(audit_log)
            db.flush()
            
            log_level = "WARNING" if status != "success" else "INFO"
            logger.log(
                getattr(logging, log_level),
                f"📋 AUDIT: {action.value} - User: {user_id}, "
                f"Resource: {resource_type}/{resource_id}, Status: {status}"
            )
            
            return audit_log
        
        except Exception as e:
            logger.error(f"❌ Failed to log audit: {str(e)}")
            # Don't raise - audit failure shouldn't break application
            return None
    
    @staticmethod
    def get_user_audit_log(db, user_id: str, limit: int = 100) -> list:
        """Get audit log for a user"""
        try:
            logs = db.query(AuditLog)\
                .filter_by(user_id=user_id)\
                .order_by(AuditLog.created_at.desc())\
                .limit(limit)\
                .all()
            return logs
        except Exception as e:
            logger.error(f"❌ Failed to get audit log: {str(e)}")
            return []
    
    @staticmethod
    def get_action_audit_log(db, action: AuditAction, limit: int = 100) -> list:
        """Get audit log for specific action"""
        try:
            logs = db.query(AuditLog)\
                .filter_by(action=action.value)\
                .order_by(AuditLog.created_at.desc())\
                .limit(limit)\
                .all()
            return logs
        except Exception as e:
            logger.error(f"❌ Failed to get audit log: {str(e)}")
            return []
    
    @staticmethod
    def get_failed_actions(db, limit: int = 100) -> list:
        """Get all failed actions (security incidents)"""
        try:
            logs = db.query(AuditLog)\
                .filter_by(status="failure")\
                .order_by(AuditLog.created_at.desc())\
                .limit(limit)\
                .all()
            return logs
        except Exception as e:
            logger.error(f"❌ Failed to get failed actions: {str(e)}")
            return []
    
    @staticmethod
    def get_suspicious_activity(db, limit: int = 50) -> list:
        """Get suspicious activity (brute force, rate limit hits, etc.)"""
        try:
            logs = db.query(AuditLog)\
                .filter(
                    (AuditLog.status == "failure") |
                    (AuditLog.action == "rate_limit_hit") |
                    (AuditLog.action == "security_alert")
                )\
                .order_by(AuditLog.created_at.desc())\
                .limit(limit)\
                .all()
            return logs
        except Exception as e:
            logger.error(f"❌ Failed to get suspicious activity: {str(e)}")
            return []
    
    @staticmethod
    def generate_compliance_report(db, days: int = 30) -> Dict:
        """Generate compliance report"""
        from datetime import timedelta
        from sqlalchemy import func
        
        try:
            start_date = datetime.utcnow() - timedelta(days=days)
            
            # Total actions
            total_actions = db.query(func.count(AuditLog.id))\
                .filter(AuditLog.created_at >= start_date)\
                .scalar()
            
            # Actions by status
            by_status = db.query(
                AuditLog.status,
                func.count(AuditLog.id).label("count")
            ).filter(
                AuditLog.created_at >= start_date
            ).group_by(AuditLog.status).all()
            
            # Actions by type
            by_action = db.query(
                AuditLog.action,
                func.count(AuditLog.id).label("count")
            ).filter(
                AuditLog.created_at >= start_date
            ).group_by(AuditLog.action).all()
            
            # Failed actions
            failed_actions = db.query(func.count(AuditLog.id))\
                .filter(
                    (AuditLog.created_at >= start_date) &
                    (AuditLog.status == "failure")
                )\
                .scalar()
            
            return {
                "period_days": days,
                "start_date": start_date.isoformat(),
                "total_actions": total_actions,
                "by_status": {status: count for status, count in by_status},
                "by_action": {action: count for action, count in by_action},
                "failed_actions": failed_actions,
                "success_rate": ((total_actions - failed_actions) / total_actions * 100) if total_actions > 0 else 0
            }
        
        except Exception as e:
            logger.error(f"❌ Failed to generate report: {str(e)}")
            return {"error": str(e)}


# FastAPI dependency to extract request info
def get_request_info(request) -> Dict:
    """Extract audit info from FastAPI request"""
    return {
        "ip_address": request.client.host if request.client else None,
        "user_agent": request.headers.get("user-agent", ""),
        "request_method": request.method,
        "request_path": request.url.path
    }


# Usage examples

def audit_login_attempt(db, user_id: str, success: bool, request_info: Dict):
    """Audit login attempt"""
    action = AuditAction.LOGIN if success else AuditAction.LOGIN_FAILED
    status = "success" if success else "failure"
    
    AuditLogger.log_action(
        db=db,
        user_id=user_id if success else None,
        action=action,
        status=status,
        description=f"Login attempt: {'successful' if success else 'failed'}",
        **request_info
    )


def audit_invoice_upload(db, user_id: str, invoice_id: str, file_name: str, request_info: Dict):
    """Audit invoice upload"""
    AuditLogger.log_action(
        db=db,
        user_id=user_id,
        action=AuditAction.INVOICE_UPLOADED,
        status="success",
        resource_type="invoice",
        resource_id=invoice_id,
        description=f"Uploaded invoice: {file_name}",
        **request_info
    )


def audit_payment_completed(db, user_id: str, payment_id: str, amount: float, request_info: Dict):
    """Audit payment completion"""
    AuditLogger.log_action(
        db=db,
        user_id=user_id,
        action=AuditAction.PAYMENT_COMPLETED,
        status="success",
        resource_type="payment",
        resource_id=payment_id,
        description=f"Payment completed: ₹{amount}",
        new_values={"amount": amount, "payment_id": payment_id},
        **request_info
    )


def audit_subscription_change(db, user_id: str, old_tier: str, new_tier: str, request_info: Dict):
    """Audit subscription tier change"""
    action = AuditAction.SUBSCRIPTION_UPGRADED if new_tier > old_tier else AuditAction.SUBSCRIPTION_DOWNGRADED
    
    AuditLogger.log_action(
        db=db,
        user_id=user_id,
        action=action,
        status="success",
        resource_type="subscription",
        resource_id=user_id,
        description=f"Subscription changed: {old_tier} → {new_tier}",
        old_values={"tier": old_tier},
        new_values={"tier": new_tier},
        **request_info
    )


if __name__ == "__main__":
    print("✅ Audit Logging module loaded")
    print("\nAudit actions available:")
    for action in AuditAction:
        print(f"  - {action.value}")
