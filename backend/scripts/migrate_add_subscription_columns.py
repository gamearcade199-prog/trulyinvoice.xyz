"""
Database Migration: Add Subscription Columns
Adds columns needed for Razorpay Subscriptions API integration
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from sqlalchemy import text
from app.core.database import engine


def run_migration():
    """Add subscription-related columns to subscriptions table"""
    
    print("=" * 70)
    print("DATABASE MIGRATION: ADD SUBSCRIPTION COLUMNS")
    print("=" * 70)
    print()
    
    migrations = [
        {
            "name": "Add razorpay_plan_id column",
            "sql": """
                ALTER TABLE subscriptions 
                ADD COLUMN IF NOT EXISTS razorpay_plan_id VARCHAR(255);
            """,
            "rollback": "ALTER TABLE subscriptions DROP COLUMN IF EXISTS razorpay_plan_id;"
        },
        {
            "name": "Add unique constraint to razorpay_subscription_id",
            "sql": """
                CREATE UNIQUE INDEX IF NOT EXISTS idx_unique_razorpay_subscription_id 
                ON subscriptions(razorpay_subscription_id) 
                WHERE razorpay_subscription_id IS NOT NULL;
            """,
            "rollback": "DROP INDEX IF EXISTS idx_unique_razorpay_subscription_id;"
        },
        {
            "name": "Add next_billing_date column",
            "sql": """
                ALTER TABLE subscriptions 
                ADD COLUMN IF NOT EXISTS next_billing_date TIMESTAMP;
            """,
            "rollback": "ALTER TABLE subscriptions DROP COLUMN IF EXISTS next_billing_date;"
        },
        {
            "name": "Add last_payment_date column",
            "sql": """
                ALTER TABLE subscriptions 
                ADD COLUMN IF NOT EXISTS last_payment_date TIMESTAMP;
            """,
            "rollback": "ALTER TABLE subscriptions DROP COLUMN IF EXISTS last_payment_date;"
        },
        {
            "name": "Add payment_retry_count column",
            "sql": """
                ALTER TABLE subscriptions 
                ADD COLUMN IF NOT EXISTS payment_retry_count INTEGER DEFAULT 0;
            """,
            "rollback": "ALTER TABLE subscriptions DROP COLUMN IF EXISTS payment_retry_count;"
        },
        {
            "name": "Add last_payment_attempt column",
            "sql": """
                ALTER TABLE subscriptions 
                ADD COLUMN IF NOT EXISTS last_payment_attempt TIMESTAMP;
            """,
            "rollback": "ALTER TABLE subscriptions DROP COLUMN IF EXISTS last_payment_attempt;"
        },
        {
            "name": "Add grace_period_ends_at column",
            "sql": """
                ALTER TABLE subscriptions 
                ADD COLUMN IF NOT EXISTS grace_period_ends_at TIMESTAMP;
            """,
            "rollback": "ALTER TABLE subscriptions DROP COLUMN IF EXISTS grace_period_ends_at;"
        },
        {
            "name": "Add index on next_billing_date",
            "sql": """
                CREATE INDEX IF NOT EXISTS idx_next_billing_date 
                ON subscriptions(next_billing_date) 
                WHERE next_billing_date IS NOT NULL;
            """,
            "rollback": "DROP INDEX IF EXISTS idx_next_billing_date;"
        },
        {
            "name": "Add index on razorpay_subscription_id",
            "sql": """
                CREATE INDEX IF NOT EXISTS idx_razorpay_subscription_id 
                ON subscriptions(razorpay_subscription_id) 
                WHERE razorpay_subscription_id IS NOT NULL;
            """,
            "rollback": "DROP INDEX IF EXISTS idx_razorpay_subscription_id;"
        }
    ]
    
    print("📋 Migration Plan:")
    for i, migration in enumerate(migrations, 1):
        print(f"   {i}. {migration['name']}")
    print()
    
    response = input("Proceed with migration? (yes/no): ")
    if response.lower() != 'yes':
        print("❌ Migration cancelled")
        return False
    
    print()
    print("🚀 Running migrations...")
    print()
    
    successful = []
    failed = []
    
    with engine.connect() as connection:
        for migration in migrations:
            try:
                print(f"⏳ {migration['name']}...", end=" ")
                
                # Execute migration
                connection.execute(text(migration['sql']))
                connection.commit()
                
                print("✅")
                successful.append(migration['name'])
            
            except Exception as e:
                print(f"❌")
                print(f"   Error: {str(e)}")
                failed.append({
                    "name": migration['name'],
                    "error": str(e)
                })
    
    # Summary
    print()
    print("=" * 70)
    print("MIGRATION SUMMARY")
    print("=" * 70)
    print()
    
    if successful:
        print(f"✅ Successful: {len(successful)}/{len(migrations)}")
        for name in successful:
            print(f"   - {name}")
        print()
    
    if failed:
        print(f"❌ Failed: {len(failed)}/{len(migrations)}")
        for failure in failed:
            print(f"   - {failure['name']}")
            print(f"     Error: {failure['error']}")
        print()
    
    if not failed:
        print("=" * 70)
        print("🎉 ALL MIGRATIONS SUCCESSFUL!")
        print("=" * 70)
        print()
        print("Database is now ready for Razorpay Subscriptions!")
        print()
        return True
    else:
        print("⚠️ Some migrations failed. Please check errors above.")
        return False


def verify_schema():
    """Verify the schema has all required columns"""
    
    print("🔍 Verifying database schema...")
    print()
    
    with engine.connect() as connection:
        # Get column names
        result = connection.execute(text("""
            SELECT column_name, data_type, is_nullable
            FROM information_schema.columns
            WHERE table_name = 'subscriptions'
            ORDER BY ordinal_position;
        """))
        
        columns = {}
        for row in result:
            columns[row[0]] = {
                "type": row[1],
                "nullable": row[2] == "YES"
            }
        
        # Check required columns
        required_columns = [
            "razorpay_subscription_id",
            "razorpay_plan_id",
            "next_billing_date",
            "last_payment_date",
            "payment_retry_count",
            "last_payment_attempt",
            "grace_period_ends_at",
            "auto_renew"
        ]
        
        print("Required Columns:")
        all_present = True
        for col in required_columns:
            if col in columns:
                print(f"   ✅ {col}: {columns[col]['type']}")
            else:
                print(f"   ❌ {col}: MISSING")
                all_present = False
        
        print()
        
        if all_present:
            print("✅ All required columns present!")
        else:
            print("❌ Some columns missing!")
        
        return all_present


if __name__ == "__main__":
    try:
        print()
        success = run_migration()
        
        if success:
            print()
            verify_schema()
        
        sys.exit(0 if success else 1)
    
    except KeyboardInterrupt:
        print("\n❌ Migration cancelled by user")
        sys.exit(1)
    
    except Exception as e:
        print(f"\n❌ Migration failed: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
