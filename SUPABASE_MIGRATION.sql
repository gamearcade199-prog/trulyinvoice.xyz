-- ============================================================================
-- SUPABASE DATABASE MIGRATION: ADD SUBSCRIPTION COLUMNS
-- Run this in Supabase SQL Editor
-- URL: https://supabase.com/dashboard/project/ldvwxqluaheuhbycdpwn/sql
-- ============================================================================

-- Step 1: Create subscriptions table if not exists (safe to run multiple times)
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
    auto_renew BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW(),
    cancelled_at TIMESTAMP,
    cancellation_reason TEXT
);

-- Step 2: Add new columns (only if they don't exist)
DO $$ 
BEGIN
    -- razorpay_plan_id
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.columns 
        WHERE table_name='subscriptions' AND column_name='razorpay_plan_id'
    ) THEN
        ALTER TABLE subscriptions ADD COLUMN razorpay_plan_id VARCHAR(255);
        RAISE NOTICE '✅ Added column: razorpay_plan_id';
    ELSE
        RAISE NOTICE '⏭️ Column already exists: razorpay_plan_id';
    END IF;

    -- next_billing_date
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.columns 
        WHERE table_name='subscriptions' AND column_name='next_billing_date'
    ) THEN
        ALTER TABLE subscriptions ADD COLUMN next_billing_date TIMESTAMP;
        RAISE NOTICE '✅ Added column: next_billing_date';
    ELSE
        RAISE NOTICE '⏭️ Column already exists: next_billing_date';
    END IF;

    -- last_payment_date
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.columns 
        WHERE table_name='subscriptions' AND column_name='last_payment_date'
    ) THEN
        ALTER TABLE subscriptions ADD COLUMN last_payment_date TIMESTAMP;
        RAISE NOTICE '✅ Added column: last_payment_date';
    ELSE
        RAISE NOTICE '⏭️ Column already exists: last_payment_date';
    END IF;

    -- payment_retry_count
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.columns 
        WHERE table_name='subscriptions' AND column_name='payment_retry_count'
    ) THEN
        ALTER TABLE subscriptions ADD COLUMN payment_retry_count INTEGER NOT NULL DEFAULT 0;
        RAISE NOTICE '✅ Added column: payment_retry_count';
    ELSE
        RAISE NOTICE '⏭️ Column already exists: payment_retry_count';
    END IF;

    -- last_payment_attempt
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.columns 
        WHERE table_name='subscriptions' AND column_name='last_payment_attempt'
    ) THEN
        ALTER TABLE subscriptions ADD COLUMN last_payment_attempt TIMESTAMP;
        RAISE NOTICE '✅ Added column: last_payment_attempt';
    ELSE
        RAISE NOTICE '⏭️ Column already exists: last_payment_attempt';
    END IF;

    -- grace_period_ends_at
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.columns 
        WHERE table_name='subscriptions' AND column_name='grace_period_ends_at'
    ) THEN
        ALTER TABLE subscriptions ADD COLUMN grace_period_ends_at TIMESTAMP;
        RAISE NOTICE '✅ Added column: grace_period_ends_at';
    ELSE
        RAISE NOTICE '⏭️ Column already exists: grace_period_ends_at';
    END IF;
END $$;

-- Step 3: Create indexes for performance
CREATE INDEX IF NOT EXISTS idx_user_id ON subscriptions(user_id);
CREATE INDEX IF NOT EXISTS idx_razorpay_subscription_id ON subscriptions(razorpay_subscription_id) 
    WHERE razorpay_subscription_id IS NOT NULL;
CREATE INDEX IF NOT EXISTS idx_next_billing_date ON subscriptions(next_billing_date) 
    WHERE next_billing_date IS NOT NULL;
CREATE INDEX IF NOT EXISTS idx_status ON subscriptions(status);
CREATE INDEX IF NOT EXISTS idx_tier ON subscriptions(tier);

-- Step 4: Create unique constraint on razorpay_subscription_id
DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM pg_constraint 
        WHERE conname = 'uq_razorpay_subscription_id'
    ) THEN
        ALTER TABLE subscriptions 
        ADD CONSTRAINT uq_razorpay_subscription_id 
        UNIQUE (razorpay_subscription_id);
        RAISE NOTICE '✅ Added unique constraint: uq_razorpay_subscription_id';
    ELSE
        RAISE NOTICE '⏭️ Constraint already exists: uq_razorpay_subscription_id';
    END IF;
EXCEPTION
    WHEN others THEN
        RAISE NOTICE '⚠️ Unique constraint creation skipped (may already exist)';
END $$;

-- Step 5: Verify migration
DO $$
DECLARE
    column_count INTEGER;
BEGIN
    SELECT COUNT(*) INTO column_count
    FROM information_schema.columns
    WHERE table_name = 'subscriptions'
    AND column_name IN (
        'razorpay_plan_id',
        'next_billing_date', 
        'last_payment_date',
        'payment_retry_count',
        'last_payment_attempt',
        'grace_period_ends_at'
    );
    
    RAISE NOTICE '============================================';
    RAISE NOTICE 'MIGRATION VERIFICATION';
    RAISE NOTICE '============================================';
    RAISE NOTICE 'New columns found: % / 6', column_count;
    
    IF column_count = 6 THEN
        RAISE NOTICE '✅ ALL COLUMNS ADDED SUCCESSFULLY!';
    ELSE
        RAISE NOTICE '⚠️ Some columns missing. Expected 6, found %', column_count;
    END IF;
    RAISE NOTICE '============================================';
END $$;

-- ============================================================================
-- MIGRATION COMPLETE
-- You should see success messages above
-- ============================================================================
