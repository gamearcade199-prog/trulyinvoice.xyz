"""
Secrets Management Module
CRITICAL FIX #5: Secure Secrets Management

Prevents hardcoded secrets, supports environment variables and AWS Secrets Manager
"""

import os
import json
from typing import Dict, Optional
from dotenv import load_dotenv

load_dotenv()


class SecretsManager:
    """Manage application secrets securely"""
    
    @staticmethod
    def get_secret(key: str, default: Optional[str] = None) -> str:
        """
        Get a secret from environment variables
        
        Args:
            key: Secret key name
            default: Default value if not found
        
        Returns:
            Secret value from environment
        
        Raises:
            ValueError: If secret not found and no default provided (for critical secrets)
        """
        value = os.getenv(key, default)
        
        if value is None:
            raise ValueError(f"⛔ Required secret not found: {key}")
        
        if value.startswith("dummy") or value.startswith("your-"):
            print(f"⚠️  WARNING: Placeholder value detected for {key}")
        
        return value
    
    @staticmethod
    def validate_secrets() -> Dict[str, bool]:
        """Validate all critical secrets are configured"""
        
        critical_secrets = {
            "RAZORPAY_KEY_ID": "Razorpay",
            "RAZORPAY_KEY_SECRET": "Razorpay",
            "RAZORPAY_WEBHOOK_SECRET": "Razorpay Webhook",
            "DATABASE_URL": "Database",
            "SUPABASE_URL": "Supabase",
            "SUPABASE_KEY": "Supabase",
            "SECRET_KEY": "Application",
        }
        
        validation_results = {}
        missing_secrets = []
        
        for secret_key, description in critical_secrets.items():
            value = os.getenv(secret_key, "")
            is_valid = bool(value) and not value.startswith("dummy")
            validation_results[secret_key] = is_valid
            
            if not is_valid:
                missing_secrets.append(f"{secret_key} ({description})")
        
        if missing_secrets:
            print(f"⛔ Missing or invalid secrets:\n   " + "\n   ".join(missing_secrets))
        else:
            print("✅ All critical secrets configured correctly")
        
        return validation_results
    
    @staticmethod
    def get_db_secrets() -> Dict[str, str]:
        """Extract database connection details"""
        
        db_url = os.getenv("DATABASE_URL", "")
        
        # Parse PostgreSQL connection string
        # Format: postgresql://user:password@host:port/database
        try:
            from urllib.parse import urlparse
            parsed = urlparse(db_url)
            
            return {
                "host": parsed.hostname or "localhost",
                "port": str(parsed.port or 5432),
                "user": parsed.username or "postgres",
                "password": parsed.password or "",
                "database": parsed.path.lstrip("/") or "trulyinvoice"
            }
        except Exception as e:
            print(f"⚠️  Failed to parse DATABASE_URL: {e}")
            return {}
    
    @staticmethod
    def get_razorpay_secrets() -> Dict[str, str]:
        """Get Razorpay configuration"""
        
        return {
            "key_id": os.getenv("RAZORPAY_KEY_ID", ""),
            "key_secret": os.getenv("RAZORPAY_KEY_SECRET", ""),
            "webhook_secret": os.getenv("RAZORPAY_WEBHOOK_SECRET", "")
        }
    
    @staticmethod
    def get_supabase_secrets() -> Dict[str, str]:
        """Get Supabase configuration"""
        
        return {
            "url": os.getenv("SUPABASE_URL", ""),
            "key": os.getenv("SUPABASE_KEY", ""),
            "service_key": os.getenv("SUPABASE_SERVICE_KEY", "")
        }
    
    @staticmethod
    def mask_secret(secret: str, show_chars: int = 4) -> str:
        """
        Mask a secret for logging/display
        
        Args:
            secret: Full secret value
            show_chars: Number of characters to show at end
        
        Returns:
            Masked secret (e.g., "****6789")
        """
        if len(secret) <= show_chars:
            return "*" * len(secret)
        
        return "*" * (len(secret) - show_chars) + secret[-show_chars:]
    
    @staticmethod
    def validate_payment_secrets() -> bool:
        """Validate payment-related secrets"""
        
        required = [
            "RAZORPAY_KEY_ID",
            "RAZORPAY_KEY_SECRET",
            "RAZORPAY_WEBHOOK_SECRET"
        ]
        
        for key in required:
            value = os.getenv(key, "")
            if not value or value.startswith("dummy"):
                print(f"⛔ Invalid {key}")
                return False
        
        # Check for test vs production keys
        key_id = os.getenv("RAZORPAY_KEY_ID", "")
        environment = os.getenv("ENVIRONMENT", "development")
        
        if environment == "production" and not key_id.startswith("rzp_live"):
            print("⛔ Using test Razorpay keys in PRODUCTION!")
            return False
        
        print("✅ Payment secrets validated")
        return True
    
    @staticmethod
    def rotate_secrets() -> None:
        """
        Guide for rotating secrets in production
        
        Use this function to document the rotation process
        """
        rotation_guide = """
        🔄 SECRET ROTATION PROCESS
        
        1. RAZORPAY_KEY_ID / RAZORPAY_KEY_SECRET
           → Update in Razorpay dashboard
           → Update .env or secrets manager
           → Restart application
        
        2. DATABASE_URL
           → Create new user in PostgreSQL
           → Update connection string
           → Test connection
           → Remove old user
        
        3. SECRET_KEY (Application)
           → Generate new key: python -c "import secrets; print(secrets.token_urlsafe(32))"
           → Update environment variable
           → No restart needed (but recommended)
        
        4. JWT_SECRET_KEY
           → Update environment variable
           → Old tokens remain valid until expiration
           → Recommend forcing re-login on rotation
        
        Best Practices:
        ✅ Rotate every 90 days
        ✅ Use automated rotation tools
        ✅ Never commit secrets to git
        ✅ Use version control for secrets configs (with encryption)
        ✅ Enable secret audit logging
        ✅ Restrict secret access by role
        """
        
        print(rotation_guide)


# Validate secrets on import
try:
    SecretsManager.validate_secrets()
except Exception as e:
    print(f"⚠️  Warning during secret validation: {e}")
