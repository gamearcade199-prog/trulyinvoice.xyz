-- ============================================================================
-- DATABASE CONSTRAINTS MIGRATION
-- Adds foreign keys and check constraints for data integrity
-- Run this in Supabase SQL Editor
-- URL: https://supabase.com/dashboard/project/ldvwxqluaheuhbycdpwn/sql
-- ============================================================================

-- ============================================================================
-- 0. DROP ALL EXISTING CONSTRAINTS FIRST
-- ============================================================================

-- Drop all existing check constraints that might conflict
ALTER TABLE subscriptions DROP CONSTRAINT IF EXISTS subscriptions_tier_check;
ALTER TABLE subscriptions DROP CONSTRAINT IF EXISTS subscriptions_status_check;
ALTER TABLE subscriptions DROP CONSTRAINT IF EXISTS subscriptions_scans_used_this_period_check;
ALTER TABLE subscriptions DROP CONSTRAINT IF EXISTS subscriptions_scans_per_month_check;
ALTER TABLE subscriptions DROP CONSTRAINT IF EXISTS subscriptions_payment_retry_count_check;
ALTER TABLE subscriptions DROP CONSTRAINT IF EXISTS check_subscriptions_tier;
ALTER TABLE subscriptions DROP CONSTRAINT IF EXISTS check_subscriptions_status;
ALTER TABLE subscriptions DROP CONSTRAINT IF EXISTS check_subscriptions_scans_used_positive;
ALTER TABLE subscriptions DROP CONSTRAINT IF EXISTS check_subscriptions_scans_per_month_positive;
ALTER TABLE subscriptions DROP CONSTRAINT IF EXISTS check_subscriptions_retry_count_positive;
ALTER TABLE subscriptions DROP CONSTRAINT IF EXISTS fk_subscriptions_user_id;

ALTER TABLE webhook_logs DROP CONSTRAINT IF EXISTS webhook_logs_status_check;
ALTER TABLE webhook_logs DROP CONSTRAINT IF EXISTS webhook_logs_attempt_count_check;
ALTER TABLE webhook_logs DROP CONSTRAINT IF EXISTS check_webhook_logs_status;
ALTER TABLE webhook_logs DROP CONSTRAINT IF EXISTS check_webhook_logs_attempt_count_positive;

-- ============================================================================
-- 1. DATA CLEANUP - Fix existing invalid data before adding constraints
-- ============================================================================

-- Check for invalid tier values
DO $$
DECLARE
    invalid_count INTEGER;
BEGIN
    SELECT COUNT(*) INTO invalid_count
    FROM subscriptions
    WHERE tier NOT IN ('free', 'basic', 'pro', 'ultra', 'max');
    
    IF invalid_count > 0 THEN
        RAISE NOTICE '⚠️  Found % subscription(s) with invalid tier values', invalid_count;
        RAISE NOTICE '🔧 Fixing invalid tier values...';
        
        -- Update any invalid tiers to 'free' (or your preferred default)
        UPDATE subscriptions
        SET tier = 'free'
        WHERE tier NOT IN ('free', 'basic', 'pro', 'ultra', 'max');
        
        RAISE NOTICE '✅ Fixed % subscription(s)', invalid_count;
    ELSE
        RAISE NOTICE '✅ All tier values are valid';
    END IF;
END $$;

-- Check for invalid status values
DO $$
DECLARE
    invalid_count INTEGER;
BEGIN
    SELECT COUNT(*) INTO invalid_count
    FROM subscriptions
    WHERE status NOT IN ('active', 'pending', 'cancelled', 'past_due', 'paused', 'completed');
    
    IF invalid_count > 0 THEN
        RAISE NOTICE '⚠️  Found % subscription(s) with invalid status values', invalid_count;
        RAISE NOTICE '🔧 Fixing invalid status values...';
        
        -- Update any invalid statuses to 'active' (or your preferred default)
        UPDATE subscriptions
        SET status = 'active'
        WHERE status NOT IN ('active', 'pending', 'cancelled', 'past_due', 'paused', 'completed');
        
        RAISE NOTICE '✅ Fixed % subscription(s)', invalid_count;
    ELSE
        RAISE NOTICE '✅ All status values are valid';
    END IF;
END $$;

-- Check for negative scan values
DO $$
DECLARE
    invalid_count INTEGER;
BEGIN
    SELECT COUNT(*) INTO invalid_count
    FROM subscriptions
    WHERE scans_used_this_period < 0 OR scans_per_month < 0;
    
    IF invalid_count > 0 THEN
        RAISE NOTICE '⚠️  Found % subscription(s) with negative scan values', invalid_count;
        RAISE NOTICE '🔧 Fixing negative scan values...';
        
        UPDATE subscriptions
        SET scans_used_this_period = 0
        WHERE scans_used_this_period < 0;
        
        UPDATE subscriptions
        SET scans_per_month = 0
        WHERE scans_per_month < 0;
        
        RAISE NOTICE '✅ Fixed % subscription(s)', invalid_count;
    ELSE
        RAISE NOTICE '✅ All scan values are valid';
    END IF;
END $$;

-- Check for negative retry counts
DO $$
DECLARE
    invalid_count INTEGER;
BEGIN
    SELECT COUNT(*) INTO invalid_count
    FROM subscriptions
    WHERE payment_retry_count < 0;
    
    IF invalid_count > 0 THEN
        RAISE NOTICE '⚠️  Found % subscription(s) with negative retry counts', invalid_count;
        RAISE NOTICE '🔧 Fixing negative retry counts...';
        
        UPDATE subscriptions
        SET payment_retry_count = 0
        WHERE payment_retry_count < 0;
        
        RAISE NOTICE '✅ Fixed % subscription(s)', invalid_count;
    ELSE
        RAISE NOTICE '✅ All retry counts are valid';
    END IF;
END $$;

-- ============================================================================
-- 2. FOREIGN KEY CONSTRAINTS
-- ============================================================================

-- Add foreign key constraint for user_id
-- Ensures every subscription belongs to a valid user
ALTER TABLE subscriptions 
DROP CONSTRAINT IF EXISTS fk_subscriptions_user_id;

ALTER TABLE subscriptions 
ADD CONSTRAINT fk_subscriptions_user_id 
FOREIGN KEY (user_id) 
REFERENCES auth.users(id) 
ON DELETE CASCADE;  -- Delete subscriptions when user is deleted

-- ============================================================================
-- 3. CHECK CONSTRAINTS - Subscription Tier
-- ============================================================================

-- Ensure tier is one of the valid values
ALTER TABLE subscriptions
ADD CONSTRAINT check_subscriptions_tier 
CHECK (tier IN ('free', 'basic', 'pro', 'ultra', 'max'));

-- ============================================================================
-- 4. CHECK CONSTRAINTS - Subscription Status
-- ============================================================================

-- Ensure status is one of the valid values
ALTER TABLE subscriptions
ADD CONSTRAINT check_subscriptions_status 
CHECK (status IN ('active', 'pending', 'cancelled', 'past_due', 'paused', 'completed'));

-- ============================================================================
-- 5. CHECK CONSTRAINTS - Scan Limits
-- ============================================================================

-- Ensure scans_used_this_period is not negative
ALTER TABLE subscriptions
ADD CONSTRAINT check_subscriptions_scans_used_positive 
CHECK (scans_used_this_period >= 0);

-- Ensure scans_per_month is not negative
ALTER TABLE subscriptions
ADD CONSTRAINT check_subscriptions_scans_per_month_positive 
CHECK (scans_per_month >= 0);

-- ============================================================================
-- 6. CHECK CONSTRAINTS - Payment Retry Count
-- ============================================================================

-- Ensure payment_retry_count is not negative
ALTER TABLE subscriptions
ADD CONSTRAINT check_subscriptions_retry_count_positive 
CHECK (payment_retry_count >= 0);

-- ============================================================================
-- 7. CHECK CONSTRAINTS - Webhook Logs Status
-- ============================================================================

-- Ensure webhook_logs status is valid
ALTER TABLE webhook_logs
ADD CONSTRAINT check_webhook_logs_status 
CHECK (status IN ('pending', 'processed', 'failed', 'retrying'));

-- Ensure attempt_count is not negative
ALTER TABLE webhook_logs
ADD CONSTRAINT check_webhook_logs_attempt_count_positive 
CHECK (attempt_count >= 0);

-- ============================================================================
-- VERIFICATION
-- ============================================================================

DO $$
DECLARE
    constraint_count INTEGER;
BEGIN
    RAISE NOTICE '============================================';
    RAISE NOTICE 'DATABASE CONSTRAINTS MIGRATION';
    RAISE NOTICE '============================================';
    
    -- Count constraints on subscriptions table
    SELECT COUNT(*) INTO constraint_count
    FROM information_schema.table_constraints
    WHERE table_name = 'subscriptions'
    AND constraint_type IN ('FOREIGN KEY', 'CHECK');
    
    RAISE NOTICE '✅ Subscriptions table: % constraints added', constraint_count;
    
    -- Count constraints on webhook_logs table
    SELECT COUNT(*) INTO constraint_count
    FROM information_schema.table_constraints
    WHERE table_name = 'webhook_logs'
    AND constraint_type = 'CHECK';
    
    RAISE NOTICE '✅ Webhook_logs table: % constraints added', constraint_count;
    
    RAISE NOTICE '============================================';
    RAISE NOTICE '✅ CONSTRAINTS MIGRATION COMPLETE';
    RAISE NOTICE '============================================';
    
    -- List all constraints for verification
    RAISE NOTICE '';
    RAISE NOTICE '📋 Subscriptions Constraints:';
    RAISE NOTICE '   - fk_subscriptions_user_id (Foreign Key)';
    RAISE NOTICE '   - check_subscriptions_tier';
    RAISE NOTICE '   - check_subscriptions_status';
    RAISE NOTICE '   - check_subscriptions_scans_used_positive';
    RAISE NOTICE '   - check_subscriptions_scans_per_month_positive';
    RAISE NOTICE '   - check_subscriptions_retry_count_positive';
    RAISE NOTICE '';
    RAISE NOTICE '📋 Webhook_logs Constraints:';
    RAISE NOTICE '   - check_webhook_logs_status';
    RAISE NOTICE '   - check_webhook_logs_attempt_count_positive';
    
END $$;

-- ============================================================================
-- TEST CONSTRAINTS (Optional - Comment out if you want to skip)
-- ============================================================================

-- Test 1: Try to insert invalid tier (should fail)
-- INSERT INTO subscriptions (user_id, tier, scans_per_month) 
-- VALUES ('test-user-id', 'invalid_tier', 100);

-- Test 2: Try to insert negative scans_used_this_period (should fail)
-- INSERT INTO subscriptions (user_id, tier, scans_per_month, scans_used_this_period) 
-- VALUES ('test-user-id', 'basic', 100, -5);

-- Test 3: Try to insert invalid status (should fail)
-- INSERT INTO subscriptions (user_id, tier, scans_per_month, status) 
-- VALUES ('test-user-id', 'basic', 100, 'invalid_status');

-- ============================================================================
-- MIGRATION COMPLETE
-- All constraints added successfully
-- Data integrity enforced at database level
-- ============================================================================
