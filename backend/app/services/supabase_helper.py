"""
Supabase Helper - Using official Supabase Python client
"""
import os
from dotenv import load_dotenv
from supabase import create_client, Client

# Load environment variables with UTF-8 encoding
backend_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
env_path = os.path.join(backend_dir, ".env")
load_dotenv(env_path, encoding='utf-8')

# Get environment variables with fallbacks for deployment
supabase_url = os.getenv("SUPABASE_URL")
# Try SERVICE_KEY first (for backend), fallback to SUPABASE_KEY (for client)
supabase_key = os.getenv("SUPABASE_SERVICE_KEY") or os.getenv("SUPABASE_KEY")

# Print warning if Supabase is not configured
if not supabase_url:
    print("⚠️ WARNING: SUPABASE_URL not configured - Supabase operations will fail")
    supabase_url = "https://placeholder.supabase.co"

if not supabase_key:
    print("⚠️ WARNING: SUPABASE_SERVICE_KEY or SUPABASE_KEY not configured - using placeholder")
    supabase_key = "placeholder_key"

# Create official Supabase client (non-blocking, will fail gracefully at runtime if keys missing)
try:
    supabase: Client = create_client(
        supabase_url=supabase_url,
        supabase_key=supabase_key
    )
except Exception as e:
    print(f"⚠️ WARNING: Failed to initialize Supabase client: {e}")
    supabase = None
