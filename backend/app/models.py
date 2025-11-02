"""
Database Models
SQLAlchemy ORM models for TrulyInvoice
"""
from sqlalchemy import Column, String, Integer, DateTime, Boolean, Text, Float
from sqlalchemy.sql import func
from datetime import datetime
from app.core.database import Base


class Subscription(Base):
    """
    User subscription model
    Tracks subscription tier, status, usage, and billing
    """
    __tablename__ = "subscriptions"
    
    # Primary Key
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    
    # User Information
    user_id = Column(String(255), unique=True, nullable=False, index=True)
    
    # Subscription Details
    tier = Column(String(50), nullable=False, default="free")  # free, basic, pro, ultra, max
    status = Column(String(50), nullable=False, default="active")  # active, cancelled, expired
    
    # Usage Tracking
    scans_used_this_period = Column(Integer, nullable=False, default=0)
    
    # Billing Cycle
    billing_cycle = Column(String(20), nullable=True, default="monthly")  # monthly, yearly
    current_period_start = Column(DateTime, nullable=False, default=datetime.utcnow)
    current_period_end = Column(DateTime, nullable=False)
    
    # Payment Information
    razorpay_order_id = Column(String(255), nullable=True)
    razorpay_payment_id = Column(String(255), nullable=True)
    razorpay_subscription_id = Column(String(255), nullable=True, unique=True, index=True)
    razorpay_plan_id = Column(String(255), nullable=True)
    
    # Auto-renewal
    auto_renew = Column(Boolean, nullable=False, default=True)
    
    # Billing Dates
    next_billing_date = Column(DateTime, nullable=True)
    last_payment_date = Column(DateTime, nullable=True)
    payment_retry_count = Column(Integer, nullable=False, default=0)
    last_payment_attempt = Column(DateTime, nullable=True)
    grace_period_ends_at = Column(DateTime, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow, server_default=func.now())
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow, server_default=func.now())
    
    # Cancellation
    cancelled_at = Column(DateTime, nullable=True)
    cancellation_reason = Column(Text, nullable=True)
    
    def __repr__(self):
        return f"<Subscription(user_id='{self.user_id}', tier='{self.tier}', status='{self.status}')>"


class Invoice(Base):
    """
    Invoice document model
    Stores uploaded invoices and their metadata
    """
    __tablename__ = "invoices"
    
    # Primary Key
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    
    # User Information
    user_id = Column(String(255), nullable=False, index=True)
    
    # File Information
    file_name = Column(String(500), nullable=False)
    file_path = Column(String(1000), nullable=True)
    file_size = Column(Integer, nullable=True)  # Size in bytes
    file_type = Column(String(50), nullable=True)  # pdf, png, jpg, etc.
    
    # Storage
    storage_url = Column(String(1000), nullable=True)  # Supabase storage URL
    
    # Processing Status
    status = Column(String(50), nullable=False, default="pending")  # pending, processing, completed, failed
    
    # Extracted Data (JSON stored as Text)
    extracted_data = Column(Text, nullable=True)  # JSON string of extracted invoice data
    
    # Confidence Scores
    confidence_score = Column(Float, nullable=True)
    
    # Timestamps
    uploaded_at = Column(DateTime, nullable=False, default=datetime.utcnow, server_default=func.now())
    processed_at = Column(DateTime, nullable=True)
    
    # Retention
    expires_at = Column(DateTime, nullable=True)  # Based on user's plan storage limit
    
    def __repr__(self):
        return f"<Invoice(id={self.id}, user_id='{self.user_id}', file_name='{self.file_name}')>"


class UsageLog(Base):
    """
    Usage tracking log
    Records each scan/operation for analytics and quota enforcement
    """
    __tablename__ = "usage_logs"
    
    # Primary Key
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    
    # User Information
    user_id = Column(String(255), nullable=False, index=True)
    
    # Operation Details
    operation_type = Column(String(50), nullable=False)  # scan, export, bulk_upload, etc.
    resource_id = Column(String(255), nullable=True)  # Invoice ID, Document ID, etc.
    
    # Metadata (renamed from 'metadata' to avoid SQLAlchemy reserved word)
    extra_data = Column(Text, nullable=True)  # JSON string for additional data
    
    # Timestamp
    timestamp = Column(DateTime, nullable=False, default=datetime.utcnow, server_default=func.now(), index=True)
    
    def __repr__(self):
        return f"<UsageLog(user_id='{self.user_id}', operation='{self.operation_type}', timestamp='{self.timestamp}')>"


class RateLimitLog(Base):
    """
    Rate limiting tracking
    Stores rate limit hits for monitoring and enforcement
    """
    __tablename__ = "rate_limit_logs"
    
    # Primary Key
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    
    # User/IP Information
    user_id = Column(String(255), nullable=True, index=True)
    ip_address = Column(String(45), nullable=True, index=True)  # IPv4/IPv6
    
    # Request Details
    endpoint = Column(String(500), nullable=False)
    method = Column(String(10), nullable=False)  # GET, POST, etc.
    
    # Rate Limit Info
    limit_exceeded = Column(Boolean, nullable=False, default=False)
    
    # Timestamp
    timestamp = Column(DateTime, nullable=False, default=datetime.utcnow, server_default=func.now(), index=True)
    
    def __repr__(self):
        return f"<RateLimitLog(user_id='{self.user_id}', endpoint='{self.endpoint}')>"


class PaymentLog(Base):
    """
    Payment transaction log
    Records all payment attempts and their outcomes
    """
    __tablename__ = "payment_logs"
    
    # Primary Key
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    
    # User Information
    user_id = Column(String(255), nullable=False, index=True)
    
    # Razorpay IDs
    razorpay_order_id = Column(String(255), nullable=False, unique=True, index=True)
    razorpay_payment_id = Column(String(255), nullable=True, index=True)
    
    # Payment Details
    amount = Column(Integer, nullable=False)  # Amount in paise
    currency = Column(String(10), nullable=False, default="INR")
    tier = Column(String(50), nullable=False)  # Plan tier purchased
    billing_cycle = Column(String(20), nullable=False)  # monthly, yearly
    
    # Status
    status = Column(String(50), nullable=False, default="created")  # created, pending, success, failed
    
    # Timestamps
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow, server_default=func.now())
    completed_at = Column(DateTime, nullable=True)
    
    # Error Details
    error_code = Column(String(100), nullable=True)
    error_description = Column(Text, nullable=True)
    
    def __repr__(self):
        return f"<PaymentLog(order_id='{self.razorpay_order_id}', status='{self.status}')>"
