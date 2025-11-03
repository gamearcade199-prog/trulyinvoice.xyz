import psycopg2

DB_HOST = "db.ldvwxqluaheuhbycdpwn.supabase.co"
DB_PORT = "5432"
DB_NAME = "postgres"
DB_USER = "postgres"
DB_PASSWORD = "QDIXJSBJwyJOyTHt"

print("Adding missing razorpay_order_id column...")

conn = psycopg2.connect(
    host=DB_HOST, port=DB_PORT, database=DB_NAME, 
    user=DB_USER, password=DB_PASSWORD
)
conn.autocommit = True
cur = conn.cursor()

cur.execute("""
    ALTER TABLE subscriptions 
    ADD COLUMN IF NOT EXISTS razorpay_order_id VARCHAR(255)
""")

print("✅ Column added!")

# Reload the schema cache
cur.execute("NOTIFY pgrst, 'reload schema'")
print("✅ Schema cache reloaded!")

cur.close()
conn.close()

print("\n🎉 Fixed! Test again now.")
