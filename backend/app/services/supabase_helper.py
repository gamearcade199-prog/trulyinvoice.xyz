"""
Supabase Helper - Using official Supabase Python client
"""
import os
from supabase import create_client, Client

# Create official Supabase client
supabase: Client = create_client(
    supabase_url=os.getenv("SUPABASE_URL"),
    supabase_key=os.getenv("SUPABASE_SERVICE_KEY")
)
