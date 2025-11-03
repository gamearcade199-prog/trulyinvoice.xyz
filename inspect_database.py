"""
Database Schema Inspector
Connects to Supabase and shows exact table structures
"""
import os
import sys
from dotenv import load_dotenv
from supabase import create_client, Client

# Add backend to path so we can import from it
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

# Load environment variables from backend directory
backend_env = os.path.join(os.path.dirname(__file__), 'backend', '.env')
if os.path.exists(backend_env):
    load_dotenv(backend_env)
else:
    load_dotenv()  # Try root directory

# Also try to load from backend config
try:
    from app.core.config import Settings
    settings = Settings()
    print(f"✅ Loaded settings from backend config")
except Exception as e:
    print(f"⚠️ Could not load backend settings: {e}")
    settings = None

def inspect_database():
    """Inspect the database schema and data"""
    
    # Initialize Supabase client - try multiple sources
    supabase_url = os.getenv("SUPABASE_URL")
    supabase_key = os.getenv("SUPABASE_SERVICE_ROLE_KEY") or os.getenv("SUPABASE_KEY")
    
    # Try to get from settings if available
    if settings:
        supabase_url = supabase_url or getattr(settings, 'SUPABASE_URL', None)
        supabase_key = supabase_key or getattr(settings, 'SUPABASE_KEY', None)
    
    if not supabase_url or not supabase_key:
        print("❌ ERROR: SUPABASE_URL or SUPABASE_SERVICE_ROLE_KEY not found")
        print("   Tried:")
        print("   - Environment variable SUPABASE_URL")
        print("   - Environment variable SUPABASE_SERVICE_ROLE_KEY")
        print("   - Environment variable SUPABASE_KEY")
        print("   - Backend .env file")
        print("   - Backend config settings")
        print(f"\n   Current SUPABASE_URL: {supabase_url}")
        print(f"   Current SUPABASE_KEY: {'Set' if supabase_key else 'Not set'}")
        return
    
    print(f"🔗 Connecting to: {supabase_url}")
    supabase: Client = create_client(supabase_url, supabase_key)
    
    print("\n" + "="*80)
    print("📊 DATABASE SCHEMA INSPECTION")
    print("="*80)
    
    # 1. Check subscriptions table structure
    print("\n1️⃣ SUBSCRIPTIONS TABLE STRUCTURE:")
    print("-" * 80)
    
    try:
        result = supabase.rpc('exec_sql', {
            'query': """
                SELECT 
                    column_name,
                    data_type,
                    is_nullable,
                    column_default
                FROM information_schema.columns
                WHERE table_schema = 'public' 
                AND table_name = 'subscriptions'
                ORDER BY ordinal_position;
            """
        }).execute()
        
        if result.data:
            print(f"{'Column Name':<30} {'Type':<20} {'Nullable':<10} {'Default'}")
            print("-" * 80)
            for col in result.data:
                print(f"{col['column_name']:<30} {col['data_type']:<20} {col['is_nullable']:<10} {str(col['column_default'])[:30]}")
        else:
            # Try direct query
            result = supabase.table('subscriptions').select('*').limit(1).execute()
            if result.data:
                print("✅ Table exists. Columns found:")
                for key in result.data[0].keys() if result.data else []:
                    print(f"   - {key}")
            else:
                print("📋 Table exists but is empty. Let me try another method...")
    except Exception as e:
        print(f"⚠️ RPC method failed: {e}")
        print("\nTrying direct table query...")
        try:
            result = supabase.table('subscriptions').select('*').limit(1).execute()
            if result.data and len(result.data) > 0:
                print("✅ Columns in subscriptions table:")
                for key in result.data[0].keys():
                    print(f"   - {key}")
            else:
                print("📋 Table is empty, fetching column metadata differently...")
                # Just show what we can access
                result = supabase.table('subscriptions').select('*').execute()
                print(f"   Result: {result}")
        except Exception as e2:
            print(f"❌ Error: {e2}")
    
    # 2. Check for the specific user
    print("\n\n2️⃣ USER CHECK: akibhusain830@gmail.com")
    print("-" * 80)
    
    try:
        # Try to get user from auth.users (might need service role)
        result = supabase.rpc('exec_sql', {
            'query': """
                SELECT id, email, created_at 
                FROM auth.users 
                WHERE email = 'akibhusain830@gmail.com';
            """
        }).execute()
        
        if result.data and len(result.data) > 0:
            user = result.data[0]
            print(f"✅ User found!")
            print(f"   Email: {user['email']}")
            print(f"   ID: {user['id']}")
            print(f"   Created: {user['created_at']}")
            user_id = user['id']
            
            # Check if user has subscription
            print("\n3️⃣ EXISTING SUBSCRIPTION:")
            print("-" * 80)
            sub_result = supabase.table('subscriptions').select('*').eq('user_id', user_id).execute()
            
            if sub_result.data and len(sub_result.data) > 0:
                sub = sub_result.data[0]
                print("✅ Subscription found:")
                for key, value in sub.items():
                    print(f"   {key}: {value}")
            else:
                print("📭 No subscription found for this user yet.")
        else:
            print("❌ User not found. Searching for similar emails...")
            result = supabase.rpc('exec_sql', {
                'query': "SELECT email FROM auth.users WHERE email LIKE '%akib%' LIMIT 5;"
            }).execute()
            if result.data:
                print("Similar emails found:")
                for row in result.data:
                    print(f"   - {row['email']}")
    except Exception as e:
        print(f"⚠️ Could not query auth.users directly: {e}")
        print("   This is normal - auth.users requires service role.")
    
    # 3. Show available plans
    print("\n\n4️⃣ AVAILABLE PLAN TIERS:")
    print("-" * 80)
    
    try:
        result = supabase.table('subscriptions').select('tier').execute()
        if result.data:
            tiers = set(sub['tier'] for sub in result.data if sub.get('tier'))
            if tiers:
                print("✅ Plans found in database:")
                for tier in sorted(tiers):
                    print(f"   - {tier}")
            else:
                print("📋 No tiers found yet (table might be empty)")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # 4. Show sample subscription data
    print("\n\n5️⃣ SAMPLE SUBSCRIPTION RECORDS (first 3):")
    print("-" * 80)
    
    try:
        result = supabase.table('subscriptions').select('*').limit(3).execute()
        if result.data and len(result.data) > 0:
            for idx, sub in enumerate(result.data, 1):
                print(f"\nRecord {idx}:")
                for key, value in sub.items():
                    print(f"   {key}: {value}")
        else:
            print("📋 No subscriptions found in database yet.")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print("\n" + "="*80)
    print("✅ INSPECTION COMPLETE")
    print("="*80)

if __name__ == "__main__":
    inspect_database()
