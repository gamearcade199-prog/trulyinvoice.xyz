"""
Application Configuration - Pydantic 2.1.x Compatible
"""

import os
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings - Pydantic 2.1.x compatible"""
    
    # App Info
    APP_NAME: str = "TrulyInvoice"
    APP_VERSION: str = "1.0.0"
    
    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://user:password@localhost/trulyinvoice")
    
    # Security
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 24 hours
    
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
    
    # Plan Limits
    STARTER_SCANS_LIMIT: int = int(os.getenv("STARTER_SCANS_LIMIT", "30"))
    PRO_SCANS_LIMIT: int = int(os.getenv("PRO_SCANS_LIMIT", "200"))
    BUSINESS_SCANS_LIMIT: int = int(os.getenv("BUSINESS_SCANS_LIMIT", "750"))
    
    # Data Retention
    STARTER_DATA_RETENTION_DAYS: int = int(os.getenv("STARTER_DATA_RETENTION_DAYS", "60"))
    PRO_DATA_RETENTION_DAYS: int = int(os.getenv("PRO_DATA_RETENTION_DAYS", "365"))
    BUSINESS_DATA_RETENTION_DAYS: int = int(os.getenv("BUSINESS_DATA_RETENTION_DAYS", "-1"))  # -1 = unlimited
    
    # CORS
    ALLOWED_ORIGINS_STR: str = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000,http://localhost:3001,https://trulyinvoice.xyz")
    
    @property
    def ALLOWED_ORIGINS(self) -> list:
        return [origin.strip() for origin in self.ALLOWED_ORIGINS_STR.split(",")]
    
    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "ignore"


settings = Settings()
