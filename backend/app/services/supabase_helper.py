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
# ALWAYS use SERVICE_KEY for backend operations (bypasses RLS)
supabase_key = os.getenv("SUPABASE_SERVICE_KEY")

# Print warning if Supabase is not configured
if not supabase_url:
    print("⚠️ WARNING: SUPABASE_URL not configured - Supabase operations will fail")
    supabase_url = "https://placeholder.supabase.co"

if not supabase_key:
    print("⚠️ WARNING: SUPABASE_SERVICE_KEY not configured - using placeholder")
    print("   This will cause RLS policy errors!")
    supabase_key = "placeholder_key"
else:
    print(f"✅ Supabase configured with SERVICE_KEY (bypasses RLS)")

# Create official Supabase client (non-blocking, will fail gracefully at runtime if keys missing)
try:
    supabase: Client = create_client(
        supabase_url=supabase_url,
        supabase_key=supabase_key
    )
    print(f"✅ Supabase client initialized: {supabase_url}")
except Exception as e:
    print(f"⚠️ WARNING: Failed to initialize Supabase client: {e}")
    supabase = None
