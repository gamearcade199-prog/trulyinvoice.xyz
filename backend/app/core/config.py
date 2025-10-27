"""
Application Configuration - Pydantic 2.1.x Compatible
CRITICAL FIX #4: Environment-Specific Configuration
"""

import os
from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    """Application settings - Pydantic 2.1.x compatible"""
    
    # App Info
    APP_NAME: str = "TrulyInvoice"
    APP_VERSION: str = "1.0.0"
    
    # Environment (development, staging, production)
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    DEBUG: bool = os.getenv("DEBUG", "false").lower() == "true"
    
    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://user:password@localhost/trulyinvoice")
    DATABASE_POOL_SIZE: int = int(os.getenv("DATABASE_POOL_SIZE", "10" if os.getenv("ENVIRONMENT") == "production" else "5"))
    DATABASE_MAX_OVERFLOW: int = int(os.getenv("DATABASE_MAX_OVERFLOW", "20" if os.getenv("ENVIRONMENT") == "production" else "10"))
    
    # Security
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 24 hours
    
    # Redis Configuration (CRITICAL FIX #3)
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    REDIS_DB: int = int(os.getenv("REDIS_DB", "0"))
    
    # Sentry Error Tracking (CRITICAL FIX #2)
    SENTRY_DSN: str = os.getenv("SENTRY_DSN", "")
    SENTRY_ENVIRONMENT: str = ENVIRONMENT
    SENTRY_TRACES_SAMPLE_RATE: float = 0.1 if ENVIRONMENT == "production" else 1.0
    SENTRY_PROFILES_SAMPLE_RATE: float = 0.1 if ENVIRONMENT == "production" else 0.1
    
    # Razorpay Configuration
    RAZORPAY_KEY_ID: str = os.getenv("RAZORPAY_KEY_ID", "rzp_test_dummy_key")
    RAZORPAY_KEY_SECRET: str = os.getenv("RAZORPAY_KEY_SECRET", "dummy_secret")
    RAZORPAY_WEBHOOK_SECRET: str = os.getenv("RAZORPAY_WEBHOOK_SECRET", "")
    
    # Google OAuth (for future implementation)
    GOOGLE_CLIENT_ID: str = os.getenv("GOOGLE_CLIENT_ID", "")
    GOOGLE_CLIENT_SECRET: str = os.getenv("GOOGLE_CLIENT_SECRET", "")
    
    # AI Services
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    GOOGLE_VISION_API_KEY: str = os.getenv("GOOGLE_VISION_API_KEY", "")
    GOOGLE_AI_API_KEY: str = os.getenv("GOOGLE_AI_API_KEY", "")  # Alternative AI key
    
    # Vision & OCR Configuration (Optional)
    VISION_API_ENABLED: str = os.getenv("VISION_API_ENABLED", "true")
    USE_GEMINI_FOR_OCR: str = os.getenv("USE_GEMINI_FOR_OCR", "false")
    GEMINI_OCR_MODEL: str = os.getenv("GEMINI_OCR_MODEL", "gemini-2.5-flash")
    GEMINI_FLASH_LITE_MODEL: str = os.getenv("GEMINI_FLASH_LITE_MODEL", "gemini-2.5-flash-lite")
    CONFIDENCE_THRESHOLD: float = float(os.getenv("CONFIDENCE_THRESHOLD", "0.85"))
    USE_VISION_FLASH_LITE_PIPELINE: str = os.getenv("USE_VISION_FLASH_LITE_PIPELINE", "false")
    USE_GEMINI_DUAL_PIPELINE: str = os.getenv("USE_GEMINI_DUAL_PIPELINE", "true")
    MAX_GEMINI_COST_PER_REQUEST: float = float(os.getenv("MAX_GEMINI_COST_PER_REQUEST", "0.10"))
    
    # Storage
    SUPABASE_URL: str = os.getenv("SUPABASE_URL", "")
    SUPABASE_KEY: str = os.getenv("SUPABASE_KEY", "")
    SUPABASE_SERVICE_KEY: str = os.getenv("SUPABASE_SERVICE_KEY", "")  # For backend operations
    
    # Environment & Debug
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    DEBUG: str = os.getenv("DEBUG", "false")  # Default false for production safety
    
    # Upload Configuration
    MAX_UPLOAD_SIZE: int = int(os.getenv("MAX_UPLOAD_SIZE", "10485760"))  # 10MB default
    ALLOWED_FILE_TYPES: str = os.getenv("ALLOWED_FILE_TYPES", "pdf,jpg,jpeg,png")
    
    # Upload Configuration
    MAX_UPLOAD_SIZE: int = int(os.getenv("MAX_UPLOAD_SIZE", "10485760"))  # 10MB default
    ALLOWED_FILE_TYPES: str = os.getenv("ALLOWED_FILE_TYPES", "pdf,jpg,jpeg,png")
    
    # Plan Limits
    STARTER_SCANS_LIMIT: int = int(os.getenv("STARTER_SCANS_LIMIT", "30"))
    PRO_SCANS_LIMIT: int = int(os.getenv("PRO_SCANS_LIMIT", "200"))
    BUSINESS_SCANS_LIMIT: int = int(os.getenv("BUSINESS_SCANS_LIMIT", "750"))
    
    # Data Retention
    STARTER_DATA_RETENTION_DAYS: int = int(os.getenv("STARTER_DATA_RETENTION_DAYS", "60"))
    PRO_DATA_RETENTION_DAYS: int = int(os.getenv("PRO_DATA_RETENTION_DAYS", "365"))
    BUSINESS_DATA_RETENTION_DAYS: int = int(os.getenv("BUSINESS_DATA_RETENTION_DAYS", "-1"))  # -1 = unlimited
    
    @property
    def ALLOWED_ORIGINS(self) -> list:
        return [origin.strip() for origin in self.ALLOWED_ORIGINS_STR.split(",")]
    
    def validate_production_config(self):
        """Validate production configuration on startup"""
        if self.ENVIRONMENT == "production":
            warnings = []
            
            # Check SECRET_KEY
            if self.SECRET_KEY == "your-secret-key-change-in-production":
                warnings.append("⚠️  WARNING: SECRET_KEY is using default value! Generate: python -c \"import secrets; print(secrets.token_urlsafe(32))\"")
            elif len(self.SECRET_KEY) < 32:
                warnings.append("⚠️  WARNING: SECRET_KEY should be at least 32 characters!")
            
            # Check JWT_SECRET_KEY
            if hasattr(self, 'JWT_SECRET_KEY'):
                if self.JWT_SECRET_KEY == "change-this-in-production-to-random-string":
                    warnings.append("⚠️  WARNING: JWT_SECRET_KEY is using default value!")
            
            # Print warnings but don't block startup
            if warnings:
                print("\n" + "="*80)
                print("🔒 SECURITY WARNINGS:")
                for warning in warnings:
                    print(f"   {warning}")
                print("="*80 + "\n")
    
    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "ignore"


# Create settings instance
settings = Settings()

# Validate production config on import
try:
    settings.validate_production_config()
    print(f"✅ Configuration loaded for {settings.ENVIRONMENT} environment")
except ValueError as e:
    print(f"❌ Configuration Error: {str(e)}")
    raise


settings = Settings()
