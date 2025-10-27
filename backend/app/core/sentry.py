"""
Sentry Integration for Error Tracking
CRITICAL FIX #2: Production Error Monitoring

Install: pip install sentry-sdk
"""

import sentry_sdk
from sentry_sdk.integrations.fastapi import FastApiIntegration
from sentry_sdk.integrations.sqlalchemy import SqlAlchemyIntegration
import os
from dotenv import load_dotenv

load_dotenv()

SENTRY_DSN = os.getenv("SENTRY_DSN", "")
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")


def init_sentry():
    """
    Initialize Sentry for error tracking
    
    Environment variables needed:
        SENTRY_DSN: Your Sentry project DSN
        ENVIRONMENT: development/staging/production
    
    Usage:
        Call this in main.py before creating FastAPI app
        init_sentry()
    """
    
    if not SENTRY_DSN:
        print("⚠️  SENTRY_DSN not configured. Error tracking disabled.")
        return
    
    sentry_sdk.init(
        dsn=SENTRY_DSN,
        integrations=[
            FastApiIntegration(),
            SqlAlchemyIntegration(),
        ],
        environment=ENVIRONMENT,
        
        # Error sampling (capture all errors in production)
        traces_sample_rate=0.1 if ENVIRONMENT == "production" else 1.0,
        
        # Enable profiling
        profiles_sample_rate=0.1 if ENVIRONMENT == "production" else 1.0,
        
        # Attach additional context
        debug=ENVIRONMENT != "production",
        
        # Don't capture local requests
        before_send=lambda event, hint: event if not is_local_request(event) else None
    )
    
    print(f"✅ Sentry initialized for {ENVIRONMENT} environment")


def is_local_request(event):
    """Filter out local/internal requests"""
    request = event.get("request", {})
    url = request.get("url", "")
    return url.startswith("http://localhost") or url.startswith("http://127.0.0.1")


def capture_exception(exception, context=None):
    """
    Manually capture an exception with context
    
    Usage:
        from app.core.sentry import capture_exception
        
        try:
            risky_operation()
        except Exception as e:
            capture_exception(e, {"user_id": user_id, "operation": "payment"})
    """
    with sentry_sdk.push_scope() as scope:
        if context:
            for key, value in context.items():
                scope.set_context(key, {"value": value})
        sentry_sdk.capture_exception(exception)


def capture_message(message, level="info", context=None):
    """
    Manually capture a message
    
    Usage:
        from app.core.sentry import capture_message
        
        capture_message("Payment webhook received", level="info", 
                       context={"order_id": order_id})
    """
    with sentry_sdk.push_scope() as scope:
        if context:
            for key, value in context.items():
                scope.set_context(key, {"value": value})
        sentry_sdk.capture_message(message, level=level)


def set_user_context(user_id, email=None, username=None):
    """
    Set user context for error tracking
    
    Usage:
        from app.core.sentry import set_user_context
        
        @router.post("/login")
        def login(credentials):
            user = authenticate(credentials)
            set_user_context(user.id, user.email)
            return {"token": token}
    """
    sentry_sdk.set_user({
        "id": user_id,
        "email": email or "unknown",
        "username": username or "unknown"
    })


def clear_user_context():
    """Clear user context on logout"""
    sentry_sdk.set_user(None)
