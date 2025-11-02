"""
Create/Update Subscriptions Table in Supabase
Uses Supabase client to ensure table exists with all required columns
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.services.supabase_helper import supabase


def create_or_update_subscriptions_table():
    """Create or update subscriptions table in Supabase"""
    
    print("=" * 70)
    print("SUPABASE: CREATE/UPDATE SUBSCRIPTIONS TABLE")
    print("=" * 70)
    print()
    
    if not supabase:
        print("❌ Supabase client not initialized")
        print("Check SUPABASE_URL and SUPABASE_KEY environment variables")
        return False
    
    print("✅ Connected to Supabase")
    print()
    
    # SQL to create/update table
    sql = """
    -- Create subscriptions table if not exists
    CREATE TABLE IF NOT EXISTS subscriptions (
        id SERIAL PRIMARY KEY,
        user_id VARCHAR(255) NOT NULL UNIQUE,
        tier VARCHAR(50) NOT NULL DEFAULT 'free',
        status VARCHAR(50) NOT NULL DEFAULT 'active',
        scans_used_this_period INTEGER NOT NULL DEFAULT 0,
        billing_cycle VARCHAR(20) DEFAULT 'monthly',
        current_period_start TIMESTAMP NOT NULL DEFAULT NOW(),
        current_period_end TIMESTAMP NOT NULL,
        razorpay_order_id VARCHAR(255),
        razorpay_payment_id VARCHAR(255),
        razorpay_subscription_id VARCHAR(255),
        razorpay_plan_id VARCHAR(255),
        auto_renew BOOLEAN NOT NULL DEFAULT TRUE,
        next_billing_date TIMESTAMP,
        last_payment_date TIMESTAMP,
        payment_retry_count INTEGER NOT NULL DEFAULT 0,
        last_payment_attempt TIMESTAMP,
        grace_period_ends_at TIMESTAMP,
        created_at TIMESTAMP NOT NULL DEFAULT NOW(),
        updated_at TIMESTAMP NOT NULL DEFAULT NOW(),
        cancelled_at TIMESTAMP,
        cancellation_reason TEXT
    );

    -- Add columns if they don't exist (for existing tables)
    DO $$ 
    BEGIN
        -- razorpay_plan_id
        IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
                      WHERE table_name='subscriptions' AND column_name='razorpay_plan_id') THEN
            ALTER TABLE subscriptions ADD COLUMN razorpay_plan_id VARCHAR(255);
            RAISE NOTICE 'Added column: razorpay_plan_id';
        END IF;

        -- next_billing_date
        IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
                      WHERE table_name='subscriptions' AND column_name='next_billing_date') THEN
            ALTER TABLE subscriptions ADD COLUMN next_billing_date TIMESTAMP;
            RAISE NOTICE 'Added column: next_billing_date';
        END IF;

        -- last_payment_date
        IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
                      WHERE table_name='subscriptions' AND column_name='last_payment_date') THEN
            ALTER TABLE subscriptions ADD COLUMN last_payment_date TIMESTAMP;
            RAISE NOTICE 'Added column: last_payment_date';
        END IF;

        -- payment_retry_count
        IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
                      WHERE table_name='subscriptions' AND column_name='payment_retry_count') THEN
            ALTER TABLE subscriptions ADD COLUMN payment_retry_count INTEGER NOT NULL DEFAULT 0;
            RAISE NOTICE 'Added column: payment_retry_count';
        END IF;

        -- last_payment_attempt
        IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
                      WHERE table_name='subscriptions' AND column_name='last_payment_attempt') THEN
            ALTER TABLE subscriptions ADD COLUMN last_payment_attempt TIMESTAMP;
            RAISE NOTICE 'Added column: last_payment_attempt';
        END IF;

        -- grace_period_ends_at
        IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
                      WHERE table_name='subscriptions' AND column_name='grace_period_ends_at') THEN
            ALTER TABLE subscriptions ADD COLUMN grace_period_ends_at TIMESTAMP;
            RAISE NOTICE 'Added column: grace_period_ends_at';
        END IF;
    END $$;

    -- Create indexes
    CREATE INDEX IF NOT EXISTS idx_user_id ON subscriptions(user_id);
    CREATE INDEX IF NOT EXISTS idx_razorpay_subscription_id ON subscriptions(razorpay_subscription_id) WHERE razorpay_subscription_id IS NOT NULL;
    CREATE INDEX IF NOT EXISTS idx_next_billing_date ON subscriptions(next_billing_date) WHERE next_billing_date IS NOT NULL;
    CREATE INDEX IF NOT EXISTS idx_status ON subscriptions(status);
    CREATE INDEX IF NOT EXISTS idx_tier ON subscriptions(tier);

    -- Create unique constraint on razorpay_subscription_id
    DO $$
    BEGIN
        IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'uq_razorpay_subscription_id') THEN
            ALTER TABLE subscriptions 
            ADD CONSTRAINT uq_razorpay_subscription_id 
            UNIQUE (razorpay_subscription_id);
            RAISE NOTICE 'Added unique constraint: uq_razorpay_subscription_id';
        END IF;
    EXCEPTION
        WHEN duplicate_table THEN
            RAISE NOTICE 'Unique constraint already exists';
    END $$;
    """
    
    print("📝 Executing SQL migration...")
    print()
    
    try:
        # Execute via Supabase RPC or direct SQL
        result = supabase.rpc('exec_sql', {'sql': sql}).execute()
        
        print("✅ Migration executed successfully!")
        print()
        return True
    
    except Exception as e:
        # If RPC doesn't exist, print SQL for manual execution
        print(f"⚠️ Could not execute automatically: {str(e)}")
        print()
        print("=" * 70)
        print("MANUAL MIGRATION REQUIRED")
        print("=" * 70)
        print()
        print("Please execute this SQL in Supabase SQL Editor:")
        print("https://supabase.com/dashboard/project/ldvwxqluaheuhbycdpwn/sql")
        print()
        print(sql)
        print()
        print("=" * 70)
        return False


if __name__ == "__main__":
    try:
        create_or_update_subscriptions_table()
    
    except KeyboardInterrupt:
        print("\n❌ Cancelled by user")
        sys.exit(1)
    
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
