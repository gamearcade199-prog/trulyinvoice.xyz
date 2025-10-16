"""
Application Configuration
"""

import os
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings"""
    
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
    
    # Storage
    SUPABASE_URL: str = os.getenv("SUPABASE_URL", "")
    SUPABASE_KEY: str = os.getenv("SUPABASE_KEY", "")
    
    # CORS
    ALLOWED_ORIGINS: list = ["http://localhost:3000", "http://localhost:3001", "https://trulyinvoice.xyz"]
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
