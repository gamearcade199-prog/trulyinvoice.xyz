import psycopg2
from datetime import datetime

DB_HOST = "db.ldvwxqluaheuhbycdpwn.supabase.co"
DB_PORT = "5432"
DB_NAME = "postgres"
DB_USER = "postgres"
DB_PASSWORD = "QDIXJSBJwyJOyTHt"

print("="*80)
print("🔍 CHECKING USER: akibhusain830@gmail.com")
print("="*80)

conn = psycopg2.connect(
    host=DB_HOST, port=DB_PORT, database=DB_NAME, 
    user=DB_USER, password=DB_PASSWORD
)
cur = conn.cursor()

# Get user ID from Supabase Auth
cur.execute("""
    SELECT id, email, created_at 
    FROM auth.users 
    WHERE email = 'akibhusain830@gmail.com'
""")
user = cur.fetchone()

if user:
    user_id, email, created_at = user
    print(f"\n✅ User Found in Auth:")
    print(f"   User ID: {user_id}")
    print(f"   Email: {email}")
    print(f"   Created: {created_at}")
    
    # Get subscription details
    cur.execute("""
        SELECT 
            id,
            user_id,
            tier,
            status,
            scans_used_this_period,
            current_period_start,
            current_period_end,
            razorpay_subscription_id,
            razorpay_customer_id,
            created_at,
            updated_at
        FROM subscriptions 
        WHERE user_id = %s
    """, (user_id,))
    
    subscription = cur.fetchone()
    
    if subscription:
        print(f"\n✅ Subscription Found:")
        print(f"   ID: {subscription[0]}")
        print(f"   Tier: {subscription[2].upper()}")
        print(f"   Status: {subscription[3].upper()}")
        print(f"   Scans Used: {subscription[4]}")
        print(f"   Period Start: {subscription[5]}")
        print(f"   Period End: {subscription[6]}")
        print(f"   Razorpay Sub ID: {subscription[7]}")
        print(f"   Razorpay Customer ID: {subscription[8]}")
        print(f"   Created: {subscription[9]}")
        print(f"   Updated: {subscription[10]}")
        
        # Check if MAX plan is active
        if subscription[2].lower() == 'max':
            print(f"\n🎉 MAX PLAN IS ACTIVE!")
            
            # Check if period is still valid
            period_end = subscription[6]
            if isinstance(period_end, str):
                from dateutil import parser
                period_end = parser.parse(period_end)
            
            if period_end and period_end > datetime.now():
                days_remaining = (period_end - datetime.now()).days
                print(f"   ✅ Plan is active for {days_remaining} more days")
                print(f"   ✅ Expires on: {period_end.strftime('%Y-%m-%d')}")
            else:
                print(f"   ⚠️  Plan has expired!")
                print(f"   Expired on: {period_end}")
        else:
            print(f"\n⚠️  Current plan is: {subscription[2].upper()} (NOT MAX)")
            print(f"   Expected: MAX")
    else:
        print(f"\n❌ No subscription found for user {user_id}")
        
    # Test API endpoint
    print(f"\n" + "="*80)
    print("Testing API Endpoint:")
    print("="*80)
    
    import requests
    response = requests.get(f"http://localhost:8000/api/auth/subscription/{user_id}", timeout=10)
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ API Response:")
        
        # Check if response has 'subscription' nested object
        if data.get('success') and data.get('subscription'):
            sub = data['subscription']
            print(f"   Tier: {sub.get('tier', 'N/A').upper()}")
            print(f"   Status: {sub.get('status', 'N/A').upper()}")
            print(f"   Scans Used: {sub.get('scans_used_this_period', 'N/A')}")
            print(f"   Scans Limit: {sub.get('scans_limit', 'N/A')}")
            print(f"   Scans Remaining: {sub.get('scans_remaining', 'N/A')}")
            print(f"   Period End: {sub.get('current_period_end', 'N/A')}")
            
            if sub.get('tier', '').lower() == 'max':
                print(f"\n🎉 MAX PLAN CONFIRMED IN API!")
                print(f"   ✅ You get 1000 scans per month")
                print(f"   ✅ Period end: {sub.get('current_period_end', 'N/A')}")
            else:
                print(f"\n⚠️  API shows tier as: {sub.get('tier', 'N/A')}")
        else:
            print(f"   ⚠️  Unexpected response format")
            print(f"   Response: {data}")
    else:
        print(f"❌ API Error: {response.status_code}")
        print(f"   Response: {response.text}")
    
else:
    print(f"\n❌ User not found in auth.users")

cur.close()
conn.close()

print("\n" + "="*80)
print("RECOMMENDATION:")
print("="*80)
print("To see this in the frontend:")
print("1. Go to http://localhost:3000/login")
print("2. Login with: akibhusain830@gmail.com")
print("3. Go to Settings or Billing page")
print("4. You should see MAX plan with 1000 scans/month")
print("="*80)
