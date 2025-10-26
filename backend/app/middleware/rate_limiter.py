"""
Rate Limiting Middleware
Implements robust rate limiting based on subscription tiers
"""

from fastapi import Request, HTTPException, status
from fastapi.responses import JSONResponse
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from typing import Callable, Optional
import time
from collections import defaultdict
from datetime import datetime, timedelta

from app.config.plans import get_rate_limits


# Initialize limiter with IP-based rate limiting
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["100/minute", "1000/hour"],
    storage_uri="memory://",  # Use in-memory storage (upgrade to Redis in production)
    strategy="fixed-window",
    config_filename=None  # Disable automatic .env file reading
)


# In-memory rate limit tracking (use Redis in production for distributed systems)
class RateLimitTracker:
    """Track rate limits per user"""
    
    def __init__(self):
        self.requests = defaultdict(list)
        self.cleanup_interval = 3600  # Cleanup every hour
        self.last_cleanup = time.time()
    
    def cleanup_old_requests(self):
        """Remove old request timestamps to prevent memory bloat"""
        current_time = time.time()
        
        if current_time - self.last_cleanup < self.cleanup_interval:
            return
        
        # Remove entries older than 1 day
        cutoff = current_time - 86400
        
        for key in list(self.requests.keys()):
            self.requests[key] = [ts for ts in self.requests[key] if ts > cutoff]
            
            # Remove empty entries
            if not self.requests[key]:
                del self.requests[key]
        
        self.last_cleanup = current_time
    
    def check_rate_limit(
        self, 
        user_id: str, 
        tier: str, 
        window: str
    ) -> tuple[bool, int, int]:
        """
        Check if rate limit is exceeded
        
        Args:
            user_id: User identifier
            tier: Subscription tier
            window: Time window ('minute', 'hour', 'day')
        
        Returns:
            Tuple of (allowed: bool, current_count: int, limit: int)
        """
        self.cleanup_old_requests()
        
        # Get rate limits for tier
        limits = get_rate_limits(tier)
        
        # Determine limit and window duration
        if window == 'minute':
            limit = limits["api_requests_per_minute"]
            window_seconds = 60
        elif window == 'hour':
            limit = limits["api_requests_per_hour"]
            window_seconds = 3600
        elif window == 'day':
            limit = limits["api_requests_per_day"]
            window_seconds = 86400
        else:
            return True, 0, 0
        
        # Get key for this user and window
        key = f"{user_id}:{window}"
        
        # Get current time
        current_time = time.time()
        cutoff_time = current_time - window_seconds
        
        # Filter requests within the window
        recent_requests = [ts for ts in self.requests[key] if ts > cutoff_time]
        self.requests[key] = recent_requests
        
        current_count = len(recent_requests)
        
        # Check if limit exceeded
        if current_count >= limit:
            return False, current_count, limit
        
        # Add current request
        self.requests[key].append(current_time)
        
        return True, current_count + 1, limit


# Global rate limit tracker
rate_limit_tracker = RateLimitTracker()


async def check_user_rate_limit(
    request: Request,
    user_id: str,
    tier: str
) -> None:
    """
    Check rate limits for a user based on their subscription tier
    
    Args:
        request: FastAPI request object
        user_id: User ID
        tier: Subscription tier
    
    Raises:
        HTTPException: If rate limit is exceeded
    """
    # Check all time windows
    for window in ['minute', 'hour', 'day']:
        allowed, current, limit = rate_limit_tracker.check_rate_limit(
            user_id, 
            tier, 
            window
        )
        
        if not allowed:
            # Calculate retry-after time
            if window == 'minute':
                retry_after = 60
            elif window == 'hour':
                retry_after = 3600
            else:
                retry_after = 86400
            
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail={
                    "error": "Rate limit exceeded",
                    "message": f"Too many requests. Limit: {limit} requests per {window}",
                    "current_usage": current,
                    "limit": limit,
                    "window": window,
                    "retry_after_seconds": retry_after,
                    "tier": tier,
                    "upgrade_message": "Upgrade your plan for higher rate limits"
                },
                headers={"Retry-After": str(retry_after)}
            )


async def rate_limit_middleware(request: Request, call_next: Callable):
    """
    Middleware to apply rate limiting to all requests
    
    Args:
        request: FastAPI request object
        call_next: Next middleware/handler
    
    Returns:
        Response from the next handler
    """
    # Skip rate limiting for certain paths
    skip_paths = ["/health", "/docs", "/openapi.json", "/redoc"]
    
    if any(request.url.path.startswith(path) for path in skip_paths):
        return await call_next(request)
    
    # Get user info from request (if authenticated)
    user_id = getattr(request.state, "user_id", None)
    
    if user_id:
        # Get user's subscription tier from request state
        # (should be set by authentication middleware)
        tier = getattr(request.state, "user_tier", "free")
        
        try:
            await check_user_rate_limit(request, user_id, tier)
        except HTTPException as e:
            return JSONResponse(
                status_code=e.status_code,
                content=e.detail,
                headers=e.headers
            )
    
    # Continue with request
    response = await call_next(request)
    
    # Add rate limit headers
    if user_id:
        tier = getattr(request.state, "user_tier", "free")
        limits = get_rate_limits(tier)
        
        # Add informational headers
        response.headers["X-RateLimit-Limit-Minute"] = str(limits["api_requests_per_minute"])
        response.headers["X-RateLimit-Limit-Hour"] = str(limits["api_requests_per_hour"])
        response.headers["X-RateLimit-Limit-Day"] = str(limits["api_requests_per_day"])
    
    return response


# Rate limit exception handler
async def rate_limit_exception_handler(request: Request, exc: RateLimitExceeded):
    """
    Custom exception handler for rate limit exceeded errors
    
    Args:
        request: FastAPI request object
        exc: RateLimitExceeded exception
    
    Returns:
        JSON response with rate limit information
    """
    return JSONResponse(
        status_code=status.HTTP_429_TOO_MANY_REQUESTS,
        content={
            "error": "Rate limit exceeded",
            "message": str(exc),
            "detail": "You have exceeded the rate limit. Please try again later.",
            "upgrade_message": "Upgrade your plan for higher rate limits at /pricing"
        },
        headers={"Retry-After": "60"}
    )


# Decorator for applying rate limits to specific endpoints
def rate_limit(tier_override: Optional[str] = None):
    """
    Decorator to apply rate limiting to specific endpoints
    
    Args:
        tier_override: Override the user's tier for testing
    
    Usage:
        @router.post("/upload")
        @rate_limit()
        async def upload_invoice(...):
            ...
    """
    def decorator(func: Callable):
        async def wrapper(*args, **kwargs):
            request = None
            
            # Find request object in args or kwargs
            for arg in args:
                if isinstance(arg, Request):
                    request = arg
                    break
            
            if not request:
                request = kwargs.get('request')
            
            if request:
                user_id = getattr(request.state, "user_id", None)
                
                if user_id:
                    tier = tier_override or getattr(request.state, "user_tier", "free")
                    await check_user_rate_limit(request, user_id, tier)
            
            return await func(*args, **kwargs)
        
        return wrapper
    
    return decorator


# Per-endpoint rate limit configurations
ENDPOINT_LIMITS = {
    "/api/documents/upload": {
        "free": "10/hour",
        "basic": "50/hour",
        "pro": "200/hour",
        "ultra": "500/hour",
        "max": "1000/hour"
    },
    "/api/documents/batch-process": {
        "free": "5/day",
        "basic": "20/day",
        "pro": "100/day",
        "ultra": "500/day",
        "max": "2000/day"
    },
    "/api/invoices/export": {
        "free": "10/day",
        "basic": "50/day",
        "pro": "200/day",
        "ultra": "1000/day",
        "max": "5000/day"
    }
}


def get_endpoint_limit(endpoint: str, tier: str) -> Optional[str]:
    """
    Get rate limit string for a specific endpoint and tier
    
    Args:
        endpoint: API endpoint path
        tier: Subscription tier
    
    Returns:
        Rate limit string (e.g., "100/hour") or None
    """
    if endpoint in ENDPOINT_LIMITS:
        return ENDPOINT_LIMITS[endpoint].get(tier)
    
    return None


# Advanced rate limiting with burst allowance
class BurstRateLimiter:
    """
    Advanced rate limiter with burst allowance
    Allows short bursts while maintaining average rate
    """
    
    def __init__(self):
        self.buckets = defaultdict(lambda: {"tokens": 0, "last_update": time.time()})
    
    def check_limit(
        self, 
        key: str, 
        rate: int, 
        per_seconds: int, 
        burst: Optional[int] = None
    ) -> tuple[bool, float]:
        """
        Token bucket algorithm for rate limiting
        
        Args:
            key: Unique key for this limiter
            rate: Number of requests allowed
            per_seconds: Time window in seconds
            burst: Maximum burst size (defaults to rate)
        
        Returns:
            Tuple of (allowed: bool, wait_time: float)
        """
        if burst is None:
            burst = rate
        
        bucket = self.buckets[key]
        current_time = time.time()
        
        # Calculate tokens to add based on time elapsed
        time_elapsed = current_time - bucket["last_update"]
        tokens_to_add = (time_elapsed / per_seconds) * rate
        
        # Update bucket
        bucket["tokens"] = min(burst, bucket["tokens"] + tokens_to_add)
        bucket["last_update"] = current_time
        
        # Check if request can be processed
        if bucket["tokens"] >= 1:
            bucket["tokens"] -= 1
            return True, 0.0
        
        # Calculate wait time
        wait_time = (1 - bucket["tokens"]) * (per_seconds / rate)
        
        return False, wait_time


# Global burst rate limiter
burst_limiter = BurstRateLimiter()


# Authentication-specific rate limiting
class AuthenticationRateLimiter:
    """
    Specialized rate limiter for authentication endpoints.
    
    Security Features:
    - 5 failed attempts per minute per IP
    - Exponential backoff (5s, 10s, 30s, 60s, 300s)
    - IP-based blocking for repeated violations
    - Failed login tracking with email
    """
    
    def __init__(self):
        # Track failed attempts per IP: {ip: {"attempts": int, "last_attempt": datetime, "emails": [str]}}
        self.failed_attempts: dict = defaultdict(lambda: {
            "attempts": 0,
            "last_attempt": None,
            "emails": [],
            "blocked_until": None
        })
    
    def check_login_allowed(self, client_ip: str) -> tuple[bool, Optional[str]]:
        """
        Check if login from this IP is allowed.
        
        Args:
            client_ip: Client IP address
        
        Returns:
            (allowed: bool, error_message: Optional[str])
        """
        now = datetime.utcnow()
        attempts_data = self.failed_attempts[client_ip]
        
        # Check if IP is currently blocked
        if attempts_data["blocked_until"] and now < attempts_data["blocked_until"]:
            remaining = (attempts_data["blocked_until"] - now).total_seconds()
            return False, f"Too many failed login attempts. Try again in {int(remaining)} seconds."
        
        # Reset if outside window
        if attempts_data["last_attempt"] is None or \
           (now - attempts_data["last_attempt"]).total_seconds() > 60:
            attempts_data["attempts"] = 0
            attempts_data["last_attempt"] = None
            attempts_data["blocked_until"] = None
        
        return True, None
    
    def record_failed_login(self, client_ip: str, email: str):
        """
        Record a failed login attempt.
        
        Args:
            client_ip: Client IP address
            email: Email of failed login
        """
        now = datetime.utcnow()
        attempts_data = self.failed_attempts[client_ip]
        
        # Reset if outside window
        if attempts_data["last_attempt"] is None or \
           (now - attempts_data["last_attempt"]).total_seconds() > 60:
            attempts_data["attempts"] = 0
            attempts_data["emails"] = []
            attempts_data["blocked_until"] = None
        
        # Increment attempts
        attempts_data["attempts"] += 1
        attempts_data["last_attempt"] = now
        
        # Track email for this attempt
        if email not in attempts_data["emails"]:
            attempts_data["emails"].append(email)
        
        print(f"🚨 Failed login: {client_ip} ({email}) - Attempt {attempts_data['attempts']}/5")
        
        # Block if exceeded
        if attempts_data["attempts"] >= 5:
            # Exponential backoff: 5s, 10s, 30s, 60s, 300s
            violations = len([ip for ip, data in self.failed_attempts.items() 
                            if data.get("blocked_until") and data["blocked_until"] > now])
            backoff = min(5 * (2 ** (violations % 5)), 300)
            
            attempts_data["blocked_until"] = now + timedelta(seconds=backoff)
            print(f"🔒 IP blocked: {client_ip} for {backoff} seconds")
    
    def record_successful_login(self, client_ip: str):
        """
        Clear failed attempts after successful login.
        
        Args:
            client_ip: Client IP address
        """
        if client_ip in self.failed_attempts:
            del self.failed_attempts[client_ip]
            print(f"✅ Login successful: {client_ip} - attempts cleared")


# Global auth rate limiter
auth_rate_limiter = AuthenticationRateLimiter()


def check_login_rate_limit(client_ip: str) -> tuple[bool, Optional[str]]:
    """
    Check if login attempt should be allowed.
    
    Args:
        client_ip: Client IP address
    
    Returns:
        (allowed: bool, error_message: Optional[str])
    """
    return auth_rate_limiter.check_login_allowed(client_ip)


def record_failed_login_attempt(client_ip: str, email: str):
    """
    Record a failed login attempt.
    
    Args:
        client_ip: Client IP address
        email: Email that failed to log in
    """
    auth_rate_limiter.record_failed_login(client_ip, email)


def record_successful_login(client_ip: str):
    """
    Clear rate limit after successful login.
    
    Args:
        client_ip: Client IP address
    """
    auth_rate_limiter.record_successful_login(client_ip)
