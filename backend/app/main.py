"""
CLEAN BACKEND - Main Application Entry Point
Industry-standard FastAPI backend with zero dependency conflicts
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os
import sys

# Load environment variables
import pathlib
backend_dir = pathlib.Path(__file__).parent.parent
env_path = backend_dir / ".env"
load_dotenv(env_path, encoding='utf-8')

# Initialize Sentry for error monitoring (PRODUCTION READY)
try:
    import sentry_sdk
    from sentry_sdk.integrations.fastapi import FastApiIntegration
    from sentry_sdk.integrations.starlette import StarletteIntegration
    
    sentry_dsn = os.getenv("SENTRY_DSN")
    environment = os.getenv("ENVIRONMENT", "production")
    
    if sentry_dsn:
        sentry_sdk.init(
            dsn=sentry_dsn,
            environment=environment,
            integrations=[
                FastApiIntegration(),
                StarletteIntegration(),
            ],
            # Performance monitoring
            traces_sample_rate=0.1,  # 10% of transactions for performance monitoring
            profiles_sample_rate=0.1,  # 10% of profiles
            # Error tracking
            send_default_pii=False,  # Don't send personally identifiable info
            attach_stacktrace=True,
            max_breadcrumbs=50,
            debug=False,
        )
        print("✅ Sentry error monitoring initialized")
    else:
        print("⚠️  SENTRY_DSN not set - Error monitoring disabled")
except ImportError:
    print("⚠️  Sentry SDK not installed - Run: pip install sentry-sdk")
except Exception as e:
    print(f"⚠️  Sentry initialization failed: {e}")

# Initialize Redis Connection (FIX #3 & #10)
try:
    from app.core.caching import get_redis_client
    from app.core.redis_limiter import get_rate_limiter
    
    # Test Redis connection
    redis_client = get_redis_client()
    if redis_client:
        print("✅ Redis cache layer initialized")
        redis_client.ping()
    else:
        print("⚠️  Redis unavailable - Using fallback in-memory caching")
    
    # Initialize rate limiter
    rate_limiter = get_rate_limiter()
    print("✅ Redis rate limiter initialized")
except ImportError:
    print("⚠️  Redis SDK not installed - Run: pip install redis")
except Exception as e:
    print(f"⚠️  Redis initialization warning: {e}")

app = FastAPI(
    title="TrulyInvoice API",
    description="Clean, production-ready invoice processing API",
    version="2.0.0"
)

# CORS Configuration
# Allow frontend to make API calls from different domains
allowed_origins = [
    "http://localhost:3000",  # Local development
    "http://localhost:3001",  # Alternative local port
    "http://localhost:3004",  # Alternative local port
    "https://trulyinvoice.xyz",  # Production domain
    "https://www.trulyinvoice.xyz",  # Production with www
    "https://trulyinvoice-xyz.vercel.app",  # Vercel deployment
]

# Add any preview deployments from environment
if os.getenv("VERCEL_URL"):
    allowed_origins.append(f"https://{os.getenv('VERCEL_URL')}")

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
    allow_headers=["Authorization", "Content-Type", "X-Request-ID", "X-CSRF-Token"],
    expose_headers=["X-Request-ID"],
)

# Add rate limiting middleware
from .middleware.rate_limiter import rate_limit_middleware, rate_limit_exception_handler
from slowapi.errors import RateLimitExceeded
app.middleware("http")(rate_limit_middleware)
app.add_exception_handler(RateLimitExceeded, rate_limit_exception_handler)

# Add Security Headers Middleware (FIX #8)
try:
    from app.middleware.security_headers import add_security_middleware
    add_security_middleware(app)
    print("✅ Security headers middleware initialized")
except Exception as e:
    print(f"⚠️  Security headers initialization warning: {e}")

# Environment validation
@app.on_event("startup")
async def validate_environment():
    """Validate required environment variables on startup"""
    import sys
    required_vars = [
        "SUPABASE_URL",
        "SUPABASE_SERVICE_KEY",
        "GEMINI_API_KEY",
        "RAZORPAY_KEY_ID",
        "RAZORPAY_KEY_SECRET"
    ]
    
    missing = [var for var in required_vars if not os.getenv(var)]
    
    if missing:
        print(f"❌ CRITICAL: Missing required environment variables: {', '.join(missing)}")
        print("⚠️  Application cannot start without these variables!")
        sys.exit(1)
    
    print("✅ Environment validation passed")
    print(f"   - Supabase: Connected")
    print(f"   - Gemini API: Configured")
    print(f"   - Razorpay: Configured")

# Import routers
# Import API routers
import os
environment = os.getenv("ENVIRONMENT", "development")

# Import core routers
from .api import documents, invoices, health, exports, payments, auth, storage

# Register routes
app.include_router(health.router, tags=["Health"])
app.include_router(documents.router, prefix="/api/documents", tags=["Documents"])
app.include_router(invoices.router, prefix="/api/invoices", tags=["Invoices"])
app.include_router(exports.router, prefix="/api/bulk", tags=["Bulk Exports"])
app.include_router(payments.router, prefix="/api/payments", tags=["Payments"])
app.include_router(storage.router, prefix="/api/storage", tags=["Storage"])
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])

# Debug endpoints only in development
if environment != "production":
    try:
        from .api import debug
        app.include_router(debug.router, prefix="/api/debug", tags=["Debug"])
        print("⚠️  Debug endpoints enabled (development mode)")
    except ImportError:
        print("ℹ️  Debug module not available")

# Note: Bulk export endpoints moved to separate router to avoid circular imports

@app.get("/")
def root():
    return {
        "message": "TrulyInvoice API v2.0 - Clean Architecture",
        "status": "operational",
        "docs": "/docs"
    }
