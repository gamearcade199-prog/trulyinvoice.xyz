"""
Security Headers Middleware
FIX #8: Comprehensive Security Headers

Adds CSP, X-Frame-Options, HSTS, and other security headers
"""

from fastapi import FastAPI, Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
from app.core.config import settings


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """
    Add security headers to all responses
    
    Prevents:
    - Clickjacking (X-Frame-Options)
    - MIME type sniffing (X-Content-Type-Options)
    - XSS attacks (X-XSS-Protection, CSP)
    - Man-in-the-middle (HSTS)
    """
    
    async def dispatch(self, request: Request, call_next) -> Response:
        """Add security headers to response"""
        
        response = await call_next(request)
        
        # Content Security Policy
        # Restricts resources that can be loaded
        response.headers["Content-Security-Policy"] = (
            "default-src 'self'; "
            "script-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net; "
            "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; "
            "img-src 'self' data: https:; "
            "font-src 'self' https://fonts.gstatic.com; "
            "connect-src 'self' https://api.trulyinvoice.xyz; "
            "frame-ancestors 'none'; "
            "base-uri 'self'; "
            "form-action 'self'"
        )
        
        # Prevent browsers from MIME-sniffing
        response.headers["X-Content-Type-Options"] = "nosniff"
        
        # Prevent clickjacking attacks
        response.headers["X-Frame-Options"] = "DENY"
        
        # Enable browser XSS protection
        response.headers["X-XSS-Protection"] = "1; mode=block"
        
        # HTTP Strict Transport Security
        # Forces HTTPS in production
        if settings.ENVIRONMENT == "production":
            response.headers["Strict-Transport-Security"] = (
                "max-age=31536000; includeSubDomains; preload"
            )
        
        # Referrer Policy
        # Control how much referrer info is shared
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        
        # Feature Policy (now Permissions-Policy)
        # Restrict which browser features can be used
        response.headers["Permissions-Policy"] = (
            "accelerometer=(), "
            "ambient-light-sensor=(), "
            "autoplay=(), "
            "battery=(), "
            "camera=(), "
            "document-domain=(), "
            "encrypted-media=(), "
            "fullscreen=(), "
            "geolocation=(), "
            "gyroscope=(), "
            "magnetometer=(), "
            "microphone=(), "
            "midi=(), "
            "payment=(), "
            "picture-in-picture=(), "
            "sync-xhr=(), "
            "usb=(), "
            "vr=(), "
            "xr-spatial-tracking=()"
        )
        
        # Disable client caching for sensitive pages
        if self._is_sensitive_endpoint(request.url.path):
            response.headers["Cache-Control"] = (
                "no-store, no-cache, must-revalidate, proxy-revalidate"
            )
            response.headers["Pragma"] = "no-cache"
            response.headers["Expires"] = "0"
        
        return response
    
    @staticmethod
    def _is_sensitive_endpoint(path: str) -> bool:
        """Check if endpoint contains sensitive data"""
        sensitive_paths = [
            "/api/v1/auth/",
            "/api/v1/payments/",
            "/api/v1/subscriptions/",
            "/api/v1/account/",
        ]
        return any(path.startswith(p) for p in sensitive_paths)


class CORSEnhancedMiddleware(BaseHTTPMiddleware):
    """
    Enhanced CORS middleware with security checks
    
    Validates:
    - Origin is in whitelist
    - Methods are allowed
    - Headers are valid
    """
    
    async def dispatch(self, request: Request, call_next) -> Response:
        """Handle CORS with security validation"""
        
        origin = request.headers.get("origin", "")
        
        # Preflight request
        if request.method == "OPTIONS":
            return self._handle_preflight(origin)
        
        # Regular request
        response = await call_next(request)
        
        # Add CORS headers if origin is allowed
        if self._is_origin_allowed(origin):
            response.headers["Access-Control-Allow-Origin"] = origin
            response.headers["Access-Control-Allow-Credentials"] = "true"
            response.headers["Access-Control-Expose-Headers"] = (
                "Content-Length, X-RateLimit-Limit, X-RateLimit-Remaining"
            )
        
        return response
    
    def _handle_preflight(self, origin: str) -> Response:
        """Handle CORS preflight request"""
        
        if not self._is_origin_allowed(origin):
            return Response(status_code=403)
        
        return Response(
            status_code=200,
            headers={
                "Access-Control-Allow-Origin": origin,
                "Access-Control-Allow-Methods": (
                    "GET, POST, PUT, DELETE, PATCH, OPTIONS"
                ),
                "Access-Control-Allow-Headers": (
                    "Content-Type, Authorization, X-Requested-With"
                ),
                "Access-Control-Allow-Credentials": "true",
                "Access-Control-Max-Age": "3600",
            }
        )
    
    @staticmethod
    def _is_origin_allowed(origin: str) -> bool:
        """Check if origin is in whitelist"""
        allowed_origins = settings.ALLOWED_ORIGINS
        
        # Exact match or wildcard
        if origin in allowed_origins:
            return True
        
        # Allow localhost in development
        if settings.ENVIRONMENT != "production":
            if origin.startswith("http://localhost:"):
                return True
        
        return False


class RequestValidationMiddleware(BaseHTTPMiddleware):
    """
    Validate incoming requests for security issues
    
    Checks:
    - Content-Type is valid
    - Content-Length is reasonable
    - No suspicious patterns
    """
    
    async def dispatch(self, request: Request, call_next) -> Response:
        """Validate request before processing"""
        
        # Check Content-Type for POST/PUT/PATCH
        if request.method in ["POST", "PUT", "PATCH"]:
            content_type = request.headers.get("content-type", "")
            
            # Whitelist of allowed content types
            allowed_types = [
                "application/json",
                "multipart/form-data",
                "application/x-www-form-urlencoded",
            ]
            
            if content_type and not any(t in content_type for t in allowed_types):
                return Response(
                    status_code=415,
                    content={"error": "Unsupported Media Type"}
                )
        
        # Check Content-Length
        content_length = request.headers.get("content-length", "0")
        try:
            length = int(content_length)
            max_size = 10 * 1024 * 1024  # 10MB
            
            if length > max_size:
                return Response(
                    status_code=413,
                    content={"error": "Payload Too Large"}
                )
        except ValueError:
            pass
        
        # Check for suspicious headers
        user_agent = request.headers.get("user-agent", "").lower()
        if self._is_suspicious_user_agent(user_agent):
            # Log but don't block (could be legitimate bots)
            pass
        
        response = await call_next(request)
        return response
    
    @staticmethod
    def _is_suspicious_user_agent(user_agent: str) -> bool:
        """Check for suspicious user agents"""
        suspicious_patterns = [
            "sqlmap",
            "nikto",
            "nmap",
            "masscan",
            "nessus",
            "openvas",
        ]
        return any(pattern in user_agent for pattern in suspicious_patterns)


def add_security_middleware(app: FastAPI) -> None:
    """Add all security middleware to FastAPI app"""
    
    print("🔒 Adding security middleware...")
    
    # Order matters! Add in reverse order they should execute
    app.add_middleware(RequestValidationMiddleware)
    app.add_middleware(CORSEnhancedMiddleware)
    app.add_middleware(SecurityHeadersMiddleware)
    
    print("✅ Security middleware added")
