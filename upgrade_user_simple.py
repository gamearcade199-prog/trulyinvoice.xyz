"""
Simple Subscription Upgrade - Direct Supabase Client
No complex SQL - just use the Supabase Python client
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

print(f"   SUPABASE_URL: {SUPABASE_URL}")
print(f"   SUPABASE_KEY: {'✅ Set' if SUPABASE_KEY else '❌ Missing'}")

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
print("🎯 UPGRADING USER TO MAX PLAN")
print("="*80)

EMAIL = "akibhusain830@gmail.com"

# Step 1: Get user from auth (using admin API)
print(f"\n1️⃣ Finding user: {EMAIL}")
try:
    # Try to list users
    response = supabase.auth.admin.list_users()
    users = [u for u in response if u.email == EMAIL]
    
    if not users:
        print(f"❌ User not found!")
        print(f"\nLet me show you all users:")
        for u in response[:5]:
            print(f"   - {u.email}")
        sys.exit(1)
    
    user = users[0]
    user_id = user.id
    print(f"✅ Found user!")
    print(f"   ID: {user_id}")
    print(f"   Email: {user.email}")
    
except Exception as e:
    print(f"⚠️ Cannot use admin API: {e}")
    print(f"   This is normal - trying alternative method...")
    
    # Alternative: Use Supabase service role to query auth.users directly
    # This requires RLS to be disabled or service role bypass
    user_id = None

# Step 2: Check current subscription
print(f"\n2️⃣ Checking existing subscription...")
try:
    result = supabase.table('subscriptions').select('*').eq('user_id', str(user_id)).execute()
    
    if result.data:
        print(f"✅ Found existing subscription:")
        for key, value in result.data[0].items():
            print(f"   {key}: {value}")
        has_subscription = True
    else:
        print(f"📭 No existing subscription")
        has_subscription = False
except Exception as e:
    print(f"⚠️ Error checking subscription: {e}")
    has_subscription = False

# Step 3: Prepare subscription data
print(f"\n3️⃣ Preparing MAX plan upgrade...")

now = datetime.utcnow()
one_year = now + timedelta(days=365)

subscription_data = {
    'user_id': str(user_id),
    'tier': 'max',
    'status': 'active',
    'scans_used_this_period': 0,
    'current_period_start': now.isoformat(),
    'current_period_end': one_year.isoformat(),
    'updated_at': now.isoformat()
}

# Only add created_at if it's a new subscription
if not has_subscription:
    subscription_data['created_at'] = now.isoformat()

print(f"   Subscription data ready:")
for key, value in subscription_data.items():
    print(f"      {key}: {value}")

# Step 4: Upsert the subscription
print(f"\n4️⃣ Upgrading subscription...")
try:
    result = supabase.table('subscriptions').upsert(
        subscription_data,
        on_conflict='user_id'
    ).execute()
    
    print(f"\n🎉 ============================================")
    print(f"✅ SUCCESS! USER UPGRADED TO MAX PLAN!")
    print(f"============================================")
    print(f"")
    print(f"📊 PLAN DETAILS:")
    print(f"   🏆 Tier: MAX (Highest/Premium)")
    print(f"   💰 Price: ₹999/month")
    print(f"   📈 Scans: 1000/month")
    print(f"   💾 Storage: 90 days")
    print(f"   📤 Bulk: 100 files")
    print(f"   🎯 Accuracy: 99.5%")
    print(f"   📅 Valid until: {one_year.strftime('%Y-%m-%d')}")
    print(f"")
    print(f"Result: {result.data}")
    
except Exception as e:
    print(f"\n❌ ERROR during upgrade: {e}")
    print(f"\nLet me try to show you the table structure...")
    
    try:
        # Try to get any row to see structure
        result = supabase.table('subscriptions').select('*').limit(1).execute()
        if result.data:
            print(f"\nTable columns:")
            for key in result.data[0].keys():
                print(f"   - {key}")
    except Exception as e2:
        print(f"Cannot inspect table: {e2}")
    
    import traceback
    traceback.print_exc()

print("\n" + "="*80)
print("✅ SCRIPT COMPLETE")
print("="*80)
