import psycopg2
from psycopg2 import sql

# Database connection details
DB_HOST = "db.ldvwxqluaheuhbycdpwn.supabase.co"
DB_PORT = "5432"
DB_NAME = "postgres"
DB_USER = "postgres"
DB_PASSWORD = "QDIXJSBJwyJOyTHt"

print("🔌 Connecting to Supabase PostgreSQL...")

try:
    conn = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )
    conn.autocommit = True
    cur = conn.cursor()
    
    print("✅ Connected successfully!")
    print("\n" + "="*60)
    print("STEP 1: Getting all existing policies")
    print("="*60)
    
    # Get all existing policies
    cur.execute("""
        SELECT policyname FROM pg_policies 
        WHERE tablename = 'subscriptions' AND schemaname = 'public'
    """)
    policies = cur.fetchall()
    
    print(f"Found {len(policies)} existing policies:")
    for policy in policies:
        print(f"  - {policy[0]}")
    
    print("\n" + "="*60)
    print("STEP 2: Dropping ALL existing policies")
    print("="*60)
    
    # Drop all existing policies
    for policy in policies:
        policy_name = policy[0]
        drop_sql = f'DROP POLICY IF EXISTS "{policy_name}" ON subscriptions'
        print(f"Dropping: {policy_name}")
        cur.execute(drop_sql)
    
    print("✅ All old policies dropped!")
    
    print("\n" + "="*60)
    print("STEP 3: Creating new policies")
    print("="*60)
    
    # Enable RLS
    cur.execute("ALTER TABLE subscriptions ENABLE ROW LEVEL SECURITY")
    print("✅ RLS enabled")
    
    # Grant permissions
    cur.execute("GRANT ALL ON subscriptions TO service_role")
    cur.execute("GRANT SELECT, INSERT, UPDATE ON subscriptions TO authenticated")
    print("✅ Permissions granted")
    
    # Create service_role policies (for backend with SERVICE_KEY)
    policies_to_create = [
        ("service_role_select", "SELECT", "service_role", "true", None),
        ("service_role_insert", "INSERT", "service_role", None, "true"),
        ("service_role_update", "UPDATE", "service_role", "true", "true"),
        ("service_role_delete", "DELETE", "service_role", "true", None),
        ("authenticated_select_own", "SELECT", "authenticated", "auth.uid() = user_id", None),
        ("authenticated_insert_own", "INSERT", "authenticated", None, "auth.uid() = user_id"),
        ("authenticated_update_own", "UPDATE", "authenticated", "auth.uid() = user_id", "auth.uid() = user_id"),
        ("block_anon", "ALL", "anon", "false", None),
    ]
    
    for policy_name, command, role, using_clause, check_clause in policies_to_create:
        sql_parts = [f'CREATE POLICY "{policy_name}" ON subscriptions FOR {command} TO {role}']
        
        if using_clause:
            sql_parts.append(f"USING ({using_clause})")
        if check_clause:
            sql_parts.append(f"WITH CHECK ({check_clause})")
        
        policy_sql = " ".join(sql_parts)
        print(f"Creating: {policy_name}")
        cur.execute(policy_sql)
    
    print("✅ All new policies created!")
    
    print("\n" + "="*60)
    print("STEP 4: Creating indexes")
    print("="*60)
    
    indexes = [
        "CREATE INDEX IF NOT EXISTS idx_subscriptions_user_id ON subscriptions(user_id)",
        "CREATE INDEX IF NOT EXISTS idx_subscriptions_status ON subscriptions(status)",
        "CREATE INDEX IF NOT EXISTS idx_subscriptions_tier ON subscriptions(tier)"
    ]
    
    for idx_sql in indexes:
        cur.execute(idx_sql)
        print(f"✅ Index created")
    
    print("\n" + "="*60)
    print("STEP 5: Verifying configuration")
    print("="*60)
    
    # Verify policies
    cur.execute("""
        SELECT policyname, cmd, roles::text 
        FROM pg_policies 
        WHERE tablename = 'subscriptions' 
        ORDER BY policyname
    """)
    
    final_policies = cur.fetchall()
    print(f"\n✅ Total policies now: {len(final_policies)}")
    print("\nPolicy List:")
    for policy in final_policies:
        print(f"  📋 {policy[0]:<30} {policy[1]:<10} → {policy[2]}")
    
    print("\n" + "="*60)
    print("✅✅✅ CONFIGURATION COMPLETE! ✅✅✅")
    print("="*60)
    print("\n🎉 Backend can now create subscriptions!")
    print("🎉 Users can view/update their own data!")
    print("🎉 Anonymous access blocked!")
    print("\n🚀 TEST NOW: Go to http://localhost:3000/register")
    print("🚀 Use a NEW email address (not one that already exists)")
    print("="*60)
    
    cur.close()
    conn.close()
    
except Exception as e:
    print(f"\n❌ ERROR: {e}")
    import traceback
    traceback.print_exc()
