import psycopg2

DB_HOST = "db.ldvwxqluaheuhbycdpwn.supabase.co"
DB_PORT = "5432"
DB_NAME = "postgres"
DB_USER = "postgres"
DB_PASSWORD = "QDIXJSBJwyJOyTHt"

print("Adding all missing columns...")

conn = psycopg2.connect(
    host=DB_HOST, port=DB_PORT, database=DB_NAME, 
    user=DB_USER, password=DB_PASSWORD
)
conn.autocommit = True
cur = conn.cursor()

# Add both missing columns
columns_to_add = [
    "razorpay_order_id VARCHAR(255)",
    "razorpay_payment_id VARCHAR(255)"
]

for col in columns_to_add:
    try:
        col_name = col.split()[0]
        cur.execute(f"ALTER TABLE subscriptions ADD COLUMN IF NOT EXISTS {col}")
        print(f"✅ Added: {col_name}")
    except Exception as e:
        print(f"⚠️ {col_name}: {e}")

# Reload schema
cur.execute("NOTIFY pgrst, 'reload schema'")
print("\n✅ Schema cache reloaded!")

# Verify all columns
cur.execute("""
    SELECT column_name 
    FROM information_schema.columns
    WHERE table_schema = 'public' AND table_name = 'subscriptions'
    AND column_name LIKE '%razorpay%'
    ORDER BY column_name
""")
razorpay_cols = cur.fetchall()
print("\nRazorpay columns in subscriptions table:")
for col in razorpay_cols:
    print(f"   • {col[0]}")

cur.close()
conn.close()

print("\n🎉 All columns added! Test registration now.")
