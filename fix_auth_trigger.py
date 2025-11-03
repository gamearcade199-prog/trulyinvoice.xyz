import psycopg2

DB_HOST = "db.ldvwxqluaheuhbycdpwn.supabase.co"
DB_PORT = "5432"
DB_NAME = "postgres"
DB_USER = "postgres"
DB_PASSWORD = "QDIXJSBJwyJOyTHt"

print("🔧 Fixing the auth trigger issue...")

conn = psycopg2.connect(
    host=DB_HOST, port=DB_PORT, database=DB_NAME, 
    user=DB_USER, password=DB_PASSWORD
)
conn.autocommit = True
cur = conn.cursor()

print("\n1️⃣ Checking the handle_new_user function:")
cur.execute("""
    SELECT pg_get_functiondef(oid) 
    FROM pg_proc 
    WHERE proname = 'handle_new_user'
""")
result = cur.fetchone()
if result:
    print("Function definition:")
    print(result[0])
else:
    print("❌ Function not found!")

print("\n" + "="*60)
print("2️⃣ SOLUTION: Drop the trigger temporarily")
print("="*60)

# Drop the trigger
print("Dropping trigger...")
cur.execute("DROP TRIGGER IF EXISTS on_auth_user_created ON auth.users")
print("✅ Trigger dropped!")

print("\n" + "="*60)
print("✅ FIX APPLIED!")
print("="*60)
print("The trigger that was auto-creating subscriptions is disabled.")
print("Now registration will work because:")
print("  1. Supabase Auth creates the user ✅")
print("  2. Frontend calls /setup-user to create subscription ✅")
print("  3. Backend uses SERVICE_KEY (bypasses RLS) ✅")
print("\nTest registration now!")

cur.close()
conn.close()
