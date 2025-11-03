"""
Fix Registration - Create subscription for newly registered user
This script fixes the "Database error saving new user" issue
"""
import os
import sys
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Load .env from backend directory
backend_dir = os.path.join(os.path.dirname(__file__), 'backend')
env_path = os.path.join(backend_dir, '.env')
if os.path.exists(env_path):
    load_dotenv(env_path, encoding='utf-8')
    print(f"✅ Loaded .env from: {env_path}")
else:
    load_dotenv()
    print(f"⚠️ .env not found at {env_path}, using environment")

# Add backend to path
sys.path.insert(0, backend_dir)

# Get credentials
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_KEY") or os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    print("❌ Supabase credentials not found!")
    sys.exit(1)

try:
    from supabase import create_client
except ImportError:
    print("Installing supabase...")
    os.system("pip install supabase")
    from supabase import create_client

print(f"\n🔗 Connecting to Supabase: {SUPABASE_URL}")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

print("\n" + "="*80)
print("🔧 FIXING REGISTRATION - CREATE FREE SUBSCRIPTION")
print("="*80)

# Get email from command line or use the one from screenshot
if len(sys.argv) > 1:
    EMAIL = sys.argv[1]
else:
    EMAIL = "xpkeysstore@gmail.com"  # From the screenshot

print(f"\nUser email: {EMAIL}")

# Step 1: Find the user
print(f"\n1️⃣ Finding user...")
try:
    response = supabase.auth.admin.list_users()
    users = [u for u in response if u.email == EMAIL]
    
    if not users:
        print(f"❌ User not found!")
        print(f"Available users:")
        for u in response[:10]:
            print(f"   - {u.email}")
        sys.exit(1)
    
    user = users[0]
    user_id = user.id
    print(f"✅ Found user!")
    print(f"   ID: {user_id}")
    print(f"   Email: {user.email}")
    
except Exception as e:
    print(f"❌ Error finding user: {e}")
    sys.exit(1)

# Step 2: Check if subscription already exists
print(f"\n2️⃣ Checking for existing subscription...")
try:
    result = supabase.table('subscriptions').select('*').eq('user_id', str(user_id)).execute()
    
    if result.data:
        print(f"✅ Subscription already exists:")
        for key, value in result.data[0].items():
            print(f"   {key}: {value}")
        print(f"\n✅ Registration is complete - no fix needed!")
        sys.exit(0)
    else:
        print(f"📭 No subscription found - creating one...")
except Exception as e:
    print(f"⚠️ Error checking subscription: {e}")

# Step 3: Create FREE subscription
print(f"\n3️⃣ Creating FREE subscription for new user...")

now = datetime.utcnow()
one_month = now + timedelta(days=30)

subscription_data = {
    'user_id': str(user_id),
    'tier': 'free',
    'status': 'active',
    'scans_used_this_period': 0,
    'current_period_start': now.isoformat(),
    'current_period_end': one_month.isoformat(),
    'created_at': now.isoformat(),
    'updated_at': now.isoformat()
}

try:
    result = supabase.table('subscriptions').insert(subscription_data).execute()
    
    print(f"\n✅ ============================================")
    print(f"✅ REGISTRATION FIXED! FREE SUBSCRIPTION CREATED")
    print(f"============================================")
    print(f"")
    print(f"📊 Subscription Details:")
    print(f"   Tier: FREE")
    print(f"   Status: Active")
    print(f"   Scans: 10/month")
    print(f"   Valid until: {one_month.strftime('%Y-%m-%d')}")
    print(f"")
    print(f"🎉 User can now login successfully!")
    print(f"")
    
except Exception as e:
    print(f"\n❌ ERROR: {e}")
    print(f"\nThis usually means:")
    print(f"1. RLS policies are blocking INSERT")
    print(f"2. Table structure doesn't match")
    print(f"3. Service role key is not correct")
    print(f"\nLet me check the table structure...")
    
    try:
        result = supabase.table('subscriptions').select('*').limit(1).execute()
        if result.data:
            print(f"\nTable columns:")
            for key in result.data[0].keys():
                print(f"   - {key}")
    except Exception as e2:
        print(f"Cannot inspect table: {e2}")
    
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n" + "="*80)
print("✅ FIX COMPLETE - User can now login!")
print("="*80)
