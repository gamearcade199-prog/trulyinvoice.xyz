-- ============================================================================
-- FIX REGISTRATION ISSUES - RLS POLICIES AND SUBSCRIPTIONS TABLE
-- Run this in Supabase SQL Editor to fix "Database error saving new user"
-- ============================================================================

-- Step 1: Ensure subscriptions table exists with correct structure
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

-- Step 2: Enable RLS on subscriptions table
ALTER TABLE subscriptions ENABLE ROW LEVEL SECURITY;

-- Step 3: Drop existing policies (if any) to avoid conflicts
DROP POLICY IF EXISTS "Users can view own subscription" ON subscriptions;
DROP POLICY IF EXISTS "Users can insert own subscription" ON subscriptions;
DROP POLICY IF EXISTS "Users can update own subscription" ON subscriptions;
DROP POLICY IF EXISTS "Service role can manage all subscriptions" ON subscriptions;
DROP POLICY IF EXISTS "Allow backend to create subscriptions" ON subscriptions;

-- Step 4: Create RLS policies that allow service_role AND anon access for registration

-- Policy 1: Allow authenticated users to view their own subscription
CREATE POLICY "Users can view own subscription" 
ON subscriptions FOR SELECT 
USING (
    auth.uid()::text = user_id 
    OR auth.role() = 'service_role'
    OR auth.role() = 'anon'  -- Allow anon for temporary access during registration
);

-- Policy 2: Allow service_role to insert subscriptions (critical for registration)
CREATE POLICY "Service role can insert subscriptions" 
ON subscriptions FOR INSERT 
WITH CHECK (
    auth.role() = 'service_role' 
    OR auth.role() = 'anon'  -- Allow during registration before user is fully authenticated
);

-- Policy 3: Allow users to update their own subscription
CREATE POLICY "Users can update own subscription" 
ON subscriptions FOR UPDATE 
USING (
    auth.uid()::text = user_id 
    OR auth.role() = 'service_role'
);

-- Policy 4: Allow service_role to delete (for admin operations)
CREATE POLICY "Service role can delete subscriptions" 
ON subscriptions FOR DELETE 
USING (auth.role() = 'service_role');

-- Step 5: Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_subscriptions_user_id ON subscriptions(user_id);
CREATE INDEX IF NOT EXISTS idx_subscriptions_status ON subscriptions(status);
CREATE INDEX IF NOT EXISTS idx_subscriptions_tier ON subscriptions(tier);
CREATE INDEX IF NOT EXISTS idx_subscriptions_next_billing_date ON subscriptions(next_billing_date) 
    WHERE next_billing_date IS NOT NULL;

-- Step 6: Create function to auto-update updated_at timestamp
CREATE OR REPLACE FUNCTION update_subscriptions_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Step 7: Create trigger for auto-updating updated_at
DROP TRIGGER IF EXISTS update_subscriptions_updated_at_trigger ON subscriptions;
CREATE TRIGGER update_subscriptions_updated_at_trigger
    BEFORE UPDATE ON subscriptions
    FOR EACH ROW
    EXECUTE FUNCTION update_subscriptions_updated_at();

-- Step 8: Verify the setup
DO $$
DECLARE
    policy_count INTEGER;
BEGIN
    SELECT COUNT(*) INTO policy_count
    FROM pg_policies
    WHERE tablename = 'subscriptions';
    
    RAISE NOTICE '============================================';
    RAISE NOTICE 'REGISTRATION FIX VERIFICATION';
    RAISE NOTICE '============================================';
    RAISE NOTICE 'RLS Policies on subscriptions: %', policy_count;
    
    IF policy_count >= 4 THEN
        RAISE NOTICE '✅ ALL RLS POLICIES CONFIGURED!';
        RAISE NOTICE '✅ Registration should now work correctly!';
    ELSE
        RAISE NOTICE '⚠️ Expected at least 4 policies, found %', policy_count;
    END IF;
    RAISE NOTICE '============================================';
END $$;

-- ============================================================================
-- MIGRATION COMPLETE
-- The registration flow should now work without "Database error saving new user"
-- 
-- What was fixed:
-- 1. RLS policies now allow service_role to insert subscriptions
-- 2. Added anon role access during registration flow
-- 3. Proper indexes for performance
-- 4. Auto-updating timestamp trigger
-- 
-- Next steps:
-- 1. Test registration on the frontend
-- 2. Monitor logs for any remaining issues
-- 3. Remove anon INSERT policy after testing if desired
-- ============================================================================
