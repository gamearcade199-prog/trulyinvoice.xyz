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
supabase_key = os.getenv("SUPABASE_SERVICE_KEY")

# Validate required environment variables
if not supabase_url:
    raise ValueError("SUPABASE_URL environment variable is required")

if not supabase_key:
    raise ValueError("SUPABASE_SERVICE_KEY environment variable is required")

# Create official Supabase client
supabase: Client = create_client(
    supabase_url=supabase_url,
    supabase_key=supabase_key
)
