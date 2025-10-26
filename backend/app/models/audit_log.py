"""
Audit Logging Models
Tracks all security-relevant events for compliance and forensics
"""

from sqlalchemy import Column, String, DateTime, JSON, Boolean, Integer, Float
from sqlalchemy.orm import declarative_base
from datetime import datetime
import uuid

Base = declarative_base()


class PaymentLog(Base):
    """
    Payment transaction audit log
    Tracks all payment attempts for compliance and fraud detection
    """
    __tablename__ = "payment_logs"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    
    # User and order information
    user_id = Column(String, nullable=False, index=True)
    order_id = Column(String, nullable=False, index=True)
    payment_id = Column(String)
    
    # Payment details
    amount = Column(Integer)  # In paise
    currency = Column(String, default="INR")
    status = Column(String, nullable=False, index=True)  # success, failed, pending, cancelled
    
    # Verification
    payment_verified = Column(Boolean, default=False)
    signature_valid = Column(Boolean, default=False)
    ownership_verified = Column(Boolean, default=False)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    processed_at = Column(DateTime)
    
    # Logging
    ip_address = Column(String)
    user_agent = Column(String)
    error = Column(String)
    metadata = Column(JSON)  # Additional data


class AuditLog(Base):
    """
    General audit log for all user actions
    Tracks file uploads, exports, data access
    """
    __tablename__ = "audit_logs"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    
    # User and action
    user_id = Column(String, nullable=False, index=True)
    action = Column(String, nullable=False, index=True)  # upload, export, access, delete, scan
    resource = Column(String, nullable=False)  # What was accessed
    resource_id = Column(String)
    
    # Action result
    status = Column(String, nullable=False)  # success, denied, error
    
    # Request context
    ip_address = Column(String)
    user_agent = Column(String)
    
    # Details
    details = Column(JSON)
    error = Column(String)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    duration_ms = Column(Integer)  # How long the action took


class LoginLog(Base):
    """
    Login attempt audit log
    Tracks all authentication attempts for security monitoring
    """
    __tablename__ = "login_logs"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    
    # User information
    email = Column(String, nullable=False, index=True)
    user_id = Column(String, index=True)
    
    # Attempt details
    success = Column(Boolean, nullable=False, index=True)
    method = Column(String, default="email_password")  # email_password, oauth, etc
    
    # Security context
    ip_address = Column(String)
    user_agent = Column(String)
    country = Column(String)  # Optional: geolocation
    
    # Error info if failed
    error_message = Column(String)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, index=True)


class SessionLog(Base):
    """
    Session lifecycle audit log
    Tracks session creation, timeout, and logout
    """
    __tablename__ = "session_logs"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    
    # Session information
    user_id = Column(String, nullable=False, index=True)
    session_id = Column(String, nullable=False, unique=True)
    
    # Session lifecycle
    event = Column(String, nullable=False)  # created, timeout, logout, forced_logout
    ip_address = Column(String)
    user_agent = Column(String)
    
    # Session timing
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    expires_at = Column(DateTime)
    ended_at = Column(DateTime)
    duration_seconds = Column(Integer)
    
    # Additional info
    reason = Column(String)  # Why session ended
    metadata = Column(JSON)


class SecurityEventLog(Base):
    """
    Security event audit log
    Tracks suspicious activities and security-related events
    """
    __tablename__ = "security_events"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    
    # Event details
    event_type = Column(String, nullable=False, index=True)  # rate_limit, fraud_attempt, unauthorized_access
    severity = Column(String, nullable=False)  # low, medium, high, critical
    user_id = Column(String, index=True)
    
    # What happened
    description = Column(String, nullable=False)
    affected_resource = Column(String)
    
    # Context
    ip_address = Column(String)
    user_agent = Column(String)
    
    # Response
    action_taken = Column(String)  # block, alert, log, disconnect
    resolved = Column(Boolean, default=False)
    resolved_at = Column(DateTime)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    
    # Additional data
    metadata = Column(JSON)


# Helper functions for logging

def create_payment_log(
    user_id: str,
    order_id: str,
    status: str,
    db,
    amount: int = None,
    payment_id: str = None,
    signature_valid: bool = False,
    ownership_verified: bool = False,
    ip_address: str = None,
    error: str = None
) -> PaymentLog:
    """Create a payment log entry"""
    log = PaymentLog(
        user_id=user_id,
        order_id=order_id,
        payment_id=payment_id,
        amount=amount,
        status=status,
        signature_valid=signature_valid,
        ownership_verified=ownership_verified,
        ip_address=ip_address,
        error=error,
        created_at=datetime.utcnow()
    )
    db.add(log)
    db.commit()
    return log


def create_audit_log(
    user_id: str,
    action: str,
    resource: str,
    status: str,
    db,
    resource_id: str = None,
    ip_address: str = None,
    details: dict = None,
    error: str = None,
    duration_ms: int = None
) -> AuditLog:
    """Create an audit log entry"""
    log = AuditLog(
        user_id=user_id,
        action=action,
        resource=resource,
        resource_id=resource_id,
        status=status,
        ip_address=ip_address,
        details=details,
        error=error,
        duration_ms=duration_ms,
        created_at=datetime.utcnow()
    )
    db.add(log)
    db.commit()
    return log


def create_login_log(
    email: str,
    success: bool,
    db,
    user_id: str = None,
    ip_address: str = None,
    error_message: str = None
) -> LoginLog:
    """Create a login log entry"""
    log = LoginLog(
        email=email,
        user_id=user_id,
        success=success,
        ip_address=ip_address,
        error_message=error_message,
        created_at=datetime.utcnow()
    )
    db.add(log)
    db.commit()
    return log


def create_security_event_log(
    event_type: str,
    severity: str,
    description: str,
    db,
    user_id: str = None,
    ip_address: str = None,
    action_taken: str = None,
    affected_resource: str = None
) -> SecurityEventLog:
    """Create a security event log entry"""
    log = SecurityEventLog(
        event_type=event_type,
        severity=severity,
        user_id=user_id,
        description=description,
        affected_resource=affected_resource,
        ip_address=ip_address,
        action_taken=action_taken,
        created_at=datetime.utcnow()
    )
    db.add(log)
    db.commit()
    return log
