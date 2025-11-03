"""
Direct Database Inspector - Uses raw psycopg2 to inspect tables
"""
import os
import sys

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

try:
    from app.core.config import Settings
    settings = Settings()
    DATABASE_URL = settings.DATABASE_URL
    print(f"✅ Loaded DATABASE_URL from backend config")
except Exception as e:
    DATABASE_URL = os.getenv("DATABASE_URL")
    print(f"⚠️ Could not load settings, using env: {e}")

if not DATABASE_URL:
    print("❌ DATABASE_URL not found!")
    sys.exit(1)

try:
    import psycopg2
except ImportError:
    print("❌ psycopg2 not installed. Installing...")
    os.system("pip install psycopg2-binary")
    import psycopg2

print(f"\n🔗 Connecting to database...")
print(f"   URL: {DATABASE_URL[:50]}...")

try:
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()
    
    print("\n" + "="*80)
    print("📊 DATABASE INSPECTION - RAW SQL")
    print("="*80)
    
    # 1. Check subscriptions table structure
    print("\n1️⃣ SUBSCRIPTIONS TABLE COLUMNS:")
    print("-" * 80)
    
    cursor.execute("""
        SELECT 
            column_name,
            data_type,
            is_nullable,
            column_default
        FROM information_schema.columns
        WHERE table_schema = 'public' 
        AND table_name = 'subscriptions'
        ORDER BY ordinal_position;
    """)
    
    columns = cursor.fetchall()
    if columns:
        print(f"{'Column Name':<30} {'Type':<20} {'Nullable':<10} {'Default'}")
        print("-" * 80)
        for col in columns:
            default_val = str(col[3])[:30] if col[3] else 'None'
            print(f"{col[0]:<30} {col[1]:<20} {col[2]:<10} {default_val}")
    else:
        print("❌ Subscriptions table not found!")
    
    # 2. Check for constraints
    print("\n\n2️⃣ SUBSCRIPTIONS TABLE CONSTRAINTS:")
    print("-" * 80)
    
    cursor.execute("""
        SELECT
            con.conname AS constraint_name,
            con.contype AS constraint_type,
            col.column_name
        FROM pg_constraint con
        JOIN pg_class cls ON con.conrelid = cls.oid
        JOIN information_schema.columns col ON col.table_name = cls.relname
        WHERE cls.relname = 'subscriptions'
        AND col.table_schema = 'public'
        ORDER BY con.conname;
    """)
    
    constraints = cursor.fetchall()
    if constraints:
        for constraint in constraints:
            type_map = {'p': 'PRIMARY KEY', 'f': 'FOREIGN KEY', 'u': 'UNIQUE', 'c': 'CHECK'}
            print(f"   {constraint[0]}: {type_map.get(constraint[1], constraint[1])} on {constraint[2]}")
    else:
        print("   No constraints found")
    
    # 3. Check auth.users table structure
    print("\n\n3️⃣ AUTH.USERS TABLE COLUMNS:")
    print("-" * 80)
    
    cursor.execute("""
        SELECT 
            column_name,
            data_type
        FROM information_schema.columns
        WHERE table_schema = 'auth' 
        AND table_name = 'users'
        ORDER BY ordinal_position;
    """)
    
    auth_columns = cursor.fetchall()
    if auth_columns:
        for col in auth_columns:
            print(f"   {col[0]:<30} {col[1]}")
    else:
        print("   ⚠️ Cannot access auth.users (normal for RLS)")
    
    # 4. Search for the user
    print("\n\n4️⃣ SEARCHING FOR USER: akibhusain830@gmail.com")
    print("-" * 80)
    
    try:
        cursor.execute("""
            SELECT id, email, created_at, confirmed_at
            FROM auth.users
            WHERE email = 'akibhusain830@gmail.com';
        """)
        
        user = cursor.fetchone()
        if user:
            print(f"✅ User found!")
            print(f"   ID: {user[0]}")
            print(f"   Email: {user[1]}")
            print(f"   Created: {user[2]}")
            print(f"   Confirmed: {user[3]}")
            user_id = user[0]
            
            # Check subscription
            print("\n   Checking for existing subscription...")
            cursor.execute("""
                SELECT * FROM subscriptions WHERE user_id = %s;
            """, (str(user_id),))
            
            sub = cursor.fetchone()
            if sub:
                print(f"   ✅ Has subscription: {sub}")
            else:
                print(f"   📭 No subscription found")
        else:
            print("❌ User not found!")
            
            # Search for similar
            cursor.execute("""
                SELECT email FROM auth.users WHERE email LIKE %s LIMIT 5;
            """, ('%akib%',))
            
            similar = cursor.fetchall()
            if similar:
                print("\n   Similar emails:")
                for email in similar:
                    print(f"      - {email[0]}")
    except Exception as e:
        print(f"   ⚠️ Cannot query auth.users: {e}")
    
    # 5. Count existing subscriptions
    print("\n\n5️⃣ EXISTING SUBSCRIPTIONS:")
    print("-" * 80)
    
    cursor.execute("SELECT COUNT(*) FROM subscriptions;")
    count = cursor.fetchone()[0]
    print(f"   Total subscriptions: {count}")
    
    if count > 0:
        cursor.execute("SELECT DISTINCT tier FROM subscriptions;")
        tiers = cursor.fetchall()
        print(f"   Tiers in use:")
        for tier in tiers:
            print(f"      - {tier[0]}")
    
    print("\n" + "="*80)
    print("✅ INSPECTION COMPLETE")
    print("="*80)
    
    cursor.close()
    conn.close()
    
except Exception as e:
    print(f"\n❌ ERROR: {e}")
    import traceback
    traceback.print_exc()
