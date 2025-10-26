"""
Advanced Authentication Security Module
Industry-grade authentication with MFA, session management, and security features
"""

from fastapi import Request, HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import Optional, Dict, Tuple
import secrets
import hashlib
import re
import pyotp
from passlib.context import CryptContext

from app.core.database import get_db
# from app.models import User  # User model not needed with Supabase auth


# Password context with bcrypt
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
    bcrypt__rounds=12  # Industry standard
)


# Security bearer
security = HTTPBearer()


class PasswordPolicy:
    """
    Industry-grade password policy enforcement
    OWASP compliant password requirements
    """
    
    MIN_LENGTH = 8
    MAX_LENGTH = 128
    REQUIRE_UPPERCASE = True
    REQUIRE_LOWERCASE = True
    REQUIRE_DIGIT = True
    REQUIRE_SPECIAL = True
    SPECIAL_CHARS = "!@#$%^&*()_+-=[]{}|;:,.<>?"
    
    @classmethod
    def validate(cls, password: str) -> Tuple[bool, str]:
        """
        Validate password against policy
        
        Args:
            password: Password to validate
        
        Returns:
            Tuple of (is_valid: bool, message: str)
        """
        if len(password) < cls.MIN_LENGTH:
            return False, f"Password must be at least {cls.MIN_LENGTH} characters long"
        
        if len(password) > cls.MAX_LENGTH:
            return False, f"Password must not exceed {cls.MAX_LENGTH} characters"
        
        if cls.REQUIRE_UPPERCASE and not re.search(r'[A-Z]', password):
            return False, "Password must contain at least one uppercase letter"
        
        if cls.REQUIRE_LOWERCASE and not re.search(r'[a-z]', password):
            return False, "Password must contain at least one lowercase letter"
        
        if cls.REQUIRE_DIGIT and not re.search(r'\d', password):
            return False, "Password must contain at least one digit"
        
        if cls.REQUIRE_SPECIAL and not any(c in cls.SPECIAL_CHARS for c in password):
            return False, f"Password must contain at least one special character ({cls.SPECIAL_CHARS})"
        
        # Check for common patterns
        common_patterns = ['password', '12345', 'qwerty', 'abc123', 'letmein']
        password_lower = password.lower()
        if any(pattern in password_lower for pattern in common_patterns):
            return False, "Password contains common patterns and is not secure"
        
        return True, "Password meets all requirements"
    
    @classmethod
    def get_strength_score(cls, password: str) -> int:
        """
        Calculate password strength score (0-100)
        
        Args:
            password: Password to evaluate
        
        Returns:
            Strength score (0-100)
        """
        score = 0
        
        # Length bonus
        if len(password) >= 8:
            score += 20
        if len(password) >= 12:
            score += 10
        if len(password) >= 16:
            score += 10
        
        # Character variety
        if re.search(r'[a-z]', password):
            score += 10
        if re.search(r'[A-Z]', password):
            score += 10
        if re.search(r'\d', password):
            score += 10
        if any(c in cls.SPECIAL_CHARS for c in password):
            score += 10
        
        # Multiple of each type
        if len(re.findall(r'[a-z]', password)) >= 3:
            score += 5
        if len(re.findall(r'[A-Z]', password)) >= 3:
            score += 5
        if len(re.findall(r'\d', password)) >= 3:
            score += 5
        if len([c for c in password if c in cls.SPECIAL_CHARS]) >= 2:
            score += 5
        
        return min(100, score)


class SessionManager:
    """
    Advanced session management with security features
    """
    
    # In-memory session store (use Redis in production)
    _sessions: Dict[str, Dict] = {}
    
    SESSION_TIMEOUT = 3600  # 1 hour
    MAX_SESSIONS_PER_USER = 5  # Prevent session exhaustion attacks
    
    @classmethod
    def create_session(cls, user_id: str, ip_address: str, user_agent: str) -> str:
        """
        Create new session
        
        Args:
            user_id: User ID
            ip_address: Client IP address
            user_agent: Client user agent
        
        Returns:
            Session token
        """
        # Clean up expired sessions
        cls._cleanup_expired_sessions()
        
        # Check session limit per user
        user_sessions = [s for s in cls._sessions.values() if s.get('user_id') == user_id]
        if len(user_sessions) >= cls.MAX_SESSIONS_PER_USER:
            # Remove oldest session
            oldest = min(user_sessions, key=lambda s: s['created_at'])
            del cls._sessions[oldest['token']]
        
        # Generate secure token
        token = secrets.token_urlsafe(32)
        
        # Store session
        cls._sessions[token] = {
            'token': token,
            'user_id': user_id,
            'ip_address': ip_address,
            'user_agent': user_agent,
            'created_at': datetime.utcnow(),
            'last_activity': datetime.utcnow(),
            'is_valid': True
        }
        
        return token
    
    @classmethod
    def validate_session(cls, token: str, ip_address: str, user_agent: str) -> Tuple[bool, Optional[str]]:
        """
        Validate session token
        
        Args:
            token: Session token
            ip_address: Client IP address
            user_agent: Client user agent
        
        Returns:
            Tuple of (is_valid: bool, user_id: Optional[str])
        """
        session = cls._sessions.get(token)
        
        if not session:
            return False, None
        
        # Check if expired
        if datetime.utcnow() - session['last_activity'] > timedelta(seconds=cls.SESSION_TIMEOUT):
            cls.invalidate_session(token)
            return False, None
        
        # Check IP address (optional - can be disabled for mobile users)
        # if session['ip_address'] != ip_address:
        #     return False, None
        
        # Update last activity
        session['last_activity'] = datetime.utcnow()
        
        return True, session['user_id']
    
    @classmethod
    def invalidate_session(cls, token: str) -> bool:
        """
        Invalidate session
        
        Args:
            token: Session token
        
        Returns:
            True if successful
        """
        if token in cls._sessions:
            del cls._sessions[token]
            return True
        return False
    
    @classmethod
    def invalidate_all_user_sessions(cls, user_id: str) -> int:
        """
        Invalidate all sessions for a user
        
        Args:
            user_id: User ID
        
        Returns:
            Number of sessions invalidated
        """
        tokens_to_remove = [
            token for token, session in cls._sessions.items()
            if session.get('user_id') == user_id
        ]
        
        for token in tokens_to_remove:
            del cls._sessions[token]
        
        return len(tokens_to_remove)
    
    @classmethod
    def _cleanup_expired_sessions(cls):
        """Remove expired sessions"""
        current_time = datetime.utcnow()
        expired_tokens = [
            token for token, session in cls._sessions.items()
            if current_time - session['last_activity'] > timedelta(seconds=cls.SESSION_TIMEOUT)
        ]
        
        for token in expired_tokens:
            del cls._sessions[token]


class MFAManager:
    """
    Multi-Factor Authentication Manager
    Supports TOTP (Time-based One-Time Password)
    """
    
    @staticmethod
    def generate_secret() -> str:
        """
        Generate MFA secret key
        
        Returns:
            Base32 encoded secret
        """
        return pyotp.random_base32()
    
    @staticmethod
    def get_qr_code_uri(secret: str, email: str, issuer: str = "TrulyInvoice") -> str:
        """
        Get QR code URI for authenticator apps
        
        Args:
            secret: MFA secret
            email: User email
            issuer: Service name
        
        Returns:
            OTP URI for QR code generation
        """
        totp = pyotp.TOTP(secret)
        return totp.provisioning_uri(name=email, issuer_name=issuer)
    
    @staticmethod
    def verify_code(secret: str, code: str) -> bool:
        """
        Verify TOTP code
        
        Args:
            secret: MFA secret
            code: 6-digit code from authenticator app
        
        Returns:
            True if code is valid
        """
        try:
            totp = pyotp.TOTP(secret)
            return totp.verify(code, valid_window=1)  # Allow 30s window
        except Exception:
            return False
    
    @staticmethod
    def generate_backup_codes(count: int = 10) -> list[str]:
        """
        Generate backup codes for MFA recovery
        
        Args:
            count: Number of backup codes to generate
        
        Returns:
            List of backup codes
        """
        codes = []
        for _ in range(count):
            code = secrets.token_hex(4).upper()  # 8-character hex code
            codes.append(f"{code[:4]}-{code[4:]}")  # Format: XXXX-XXXX
        return codes


class SecurityHeaders:
    """
    Security headers middleware
    Implements OWASP security headers
    """
    
    @staticmethod
    def add_security_headers(response):
        """Add security headers to response"""
        
        # Prevent clickjacking
        response.headers["X-Frame-Options"] = "DENY"
        
        # Prevent MIME sniffing
        response.headers["X-Content-Type-Options"] = "nosniff"
        
        # XSS Protection
        response.headers["X-XSS-Protection"] = "1; mode=block"
        
        # Strict Transport Security (HTTPS only)
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        
        # Content Security Policy
        response.headers["Content-Security-Policy"] = (
            "default-src 'self'; "
            "script-src 'self' 'unsafe-inline' 'unsafe-eval'; "
            "style-src 'self' 'unsafe-inline'; "
            "img-src 'self' data: https:; "
            "font-src 'self' data:; "
            "connect-src 'self'"
        )
        
        # Referrer Policy
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        
        # Permissions Policy
        response.headers["Permissions-Policy"] = (
            "geolocation=(), "
            "microphone=(), "
            "camera=(), "
            "payment=()"
        )
        
        return response


class LoginAttemptTracker:
    """
    Track and prevent brute force login attempts
    """
    
    # In-memory store (use Redis in production)
    _attempts: Dict[str, list] = {}
    
    MAX_ATTEMPTS = 5
    LOCKOUT_DURATION = 900  # 15 minutes
    ATTEMPT_WINDOW = 300  # 5 minutes
    
    @classmethod
    def record_attempt(cls, identifier: str, success: bool):
        """
        Record login attempt
        
        Args:
            identifier: IP address or email
            success: Whether attempt was successful
        """
        if identifier not in cls._attempts:
            cls._attempts[identifier] = []
        
        cls._attempts[identifier].append({
            'timestamp': datetime.utcnow(),
            'success': success
        })
        
        # Clean old attempts
        cls._cleanup_old_attempts(identifier)
    
    @classmethod
    def is_locked_out(cls, identifier: str) -> Tuple[bool, int]:
        """
        Check if identifier is locked out
        
        Args:
            identifier: IP address or email
        
        Returns:
            Tuple of (is_locked: bool, seconds_remaining: int)
        """
        if identifier not in cls._attempts:
            return False, 0
        
        cls._cleanup_old_attempts(identifier)
        
        # Get failed attempts in window
        recent_failures = [
            a for a in cls._attempts[identifier]
            if not a['success']
        ]
        
        if len(recent_failures) < cls.MAX_ATTEMPTS:
            return False, 0
        
        # Check if still in lockout period
        last_failure = max(recent_failures, key=lambda a: a['timestamp'])
        lockout_end = last_failure['timestamp'] + timedelta(seconds=cls.LOCKOUT_DURATION)
        
        if datetime.utcnow() < lockout_end:
            seconds_remaining = int((lockout_end - datetime.utcnow()).total_seconds())
            return True, seconds_remaining
        
        # Lockout expired, reset
        cls._attempts[identifier] = []
        return False, 0
    
    @classmethod
    def _cleanup_old_attempts(cls, identifier: str):
        """Remove attempts outside the window"""
        if identifier not in cls._attempts:
            return
        
        cutoff = datetime.utcnow() - timedelta(seconds=cls.ATTEMPT_WINDOW)
        cls._attempts[identifier] = [
            a for a in cls._attempts[identifier]
            if a['timestamp'] > cutoff
        ]


# Helper functions
def hash_password(password: str) -> str:
    """Hash password using bcrypt"""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify password against hash"""
    return pwd_context.verify(plain_password, hashed_password)


def get_client_ip(request: Request) -> str:
    """Get client IP address from request"""
    # Check for proxy headers
    forwarded = request.headers.get("X-Forwarded-For")
    if forwarded:
        return forwarded.split(",")[0].strip()
    
    real_ip = request.headers.get("X-Real-IP")
    if real_ip:
        return real_ip
    
    # Fallback to direct connection
    if request.client:
        return request.client.host
    
    return "unknown"


def get_user_agent(request: Request) -> str:
    """Get user agent from request"""
    return request.headers.get("User-Agent", "unknown")
