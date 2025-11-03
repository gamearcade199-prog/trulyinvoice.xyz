import psycopg2

DB_HOST = "db.ldvwxqluaheuhbycdpwn.supabase.co"
DB_PORT = "5432"
DB_NAME = "postgres"
DB_USER = "postgres"
DB_PASSWORD = "QDIXJSBJwyJOyTHt"

print("🔍 Checking what's blocking Supabase Auth signup...")

conn = psycopg2.connect(
    host=DB_HOST, port=DB_PORT, database=DB_NAME, 
    user=DB_USER, password=DB_PASSWORD
)
conn.autocommit = True
cur = conn.cursor()

print("\n1️⃣ Checking auth.users table policies:")
cur.execute("""
    SELECT schemaname, tablename, policyname, cmd, roles::text 
    FROM pg_policies 
    WHERE schemaname = 'auth' AND tablename = 'users'
    ORDER BY policyname
""")
auth_policies = cur.fetchall()
if auth_policies:
    for policy in auth_policies:
        print(f"   📋 {policy[2]} - {policy[3]} - {policy[4]}")
else:
    print("   ✅ No policies on auth.users")

print("\n2️⃣ Checking auth schema permissions:")
cur.execute("""
    SELECT grantee, privilege_type 
    FROM information_schema.role_table_grants 
    WHERE table_schema = 'auth' AND table_name = 'users'
    AND grantee IN ('service_role', 'supabase_auth_admin', 'authenticated', 'anon')
    ORDER BY grantee, privilege_type
""")
perms = cur.fetchall()
for perm in perms:
    print(f"   🔐 {perm[0]}: {perm[1]}")

print("\n3️⃣ Checking if RLS is enabled on auth.users:")
cur.execute("""
    SELECT tablename, rowsecurity 
    FROM pg_tables 
    WHERE schemaname = 'auth' AND tablename = 'users'
""")
rls_status = cur.fetchone()
if rls_status:
    print(f"   RLS Status: {'ENABLED ⚠️' if rls_status[1] else 'DISABLED ✅'}")

print("\n4️⃣ Checking triggers on auth.users:")
cur.execute("""
    SELECT tgname, tgtype, proname
    FROM pg_trigger t
    JOIN pg_proc p ON t.tgfoid = p.oid
    JOIN pg_class c ON t.tgrelid = c.oid
    JOIN pg_namespace n ON c.relnamespace = n.oid
    WHERE n.nspname = 'auth' AND c.relname = 'users'
    AND NOT tgisinternal
""")
triggers = cur.fetchall()
if triggers:
    for trigger in triggers:
        print(f"   ⚡ {trigger[0]} -> {trigger[2]}")
else:
    print("   ✅ No custom triggers")

print("\n5️⃣ Checking subscriptions table setup:")
cur.execute("""
    SELECT column_name, data_type, is_nullable, column_default
    FROM information_schema.columns
    WHERE table_schema = 'public' AND table_name = 'subscriptions'
    ORDER BY ordinal_position
""")
cols = cur.fetchall()
print("   Columns:")
for col in cols:
    print(f"      • {col[0]} ({col[1]}) nullable={col[2]} default={col[3]}")

print("\n6️⃣ Looking for any foreign key constraints:")
cur.execute("""
    SELECT
        tc.constraint_name,
        tc.table_name,
        kcu.column_name,
        ccu.table_name AS foreign_table_name,
        ccu.column_name AS foreign_column_name
    FROM information_schema.table_constraints AS tc
    JOIN information_schema.key_column_usage AS kcu
        ON tc.constraint_name = kcu.constraint_name
    JOIN information_schema.constraint_column_usage AS ccu
        ON ccu.constraint_name = tc.constraint_name
    WHERE tc.constraint_type = 'FOREIGN KEY'
        AND tc.table_schema = 'public'
        AND tc.table_name = 'subscriptions'
""")
fks = cur.fetchall()
if fks:
    for fk in fks:
        print(f"   🔗 {fk[0]}: {fk[1]}.{fk[2]} -> {fk[3]}.{fk[4]}")
else:
    print("   ✅ No foreign keys to auth.users")

cur.close()
conn.close()

print("\n" + "="*60)
print("Analysis complete. Looking for the issue...")
print("="*60)
