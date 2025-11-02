-- ============================================================================
-- DATABASE CONSTRAINTS MIGRATION - FINAL VERSION
-- Matches actual models.py structure
-- ============================================================================
-- This migration adds proper constraints to ensure data integrity
-- Based on actual Subscription model columns (no scans_per_month, etc.)
-- ============================================================================

-- ============================================================================
-- SECTION 0: DROP ALL EXISTING CONSTRAINTS
-- ============================================================================
-- Drop all existing constraints first to avoid conflicts
ALTER TABLE subscriptions 
    DROP CONSTRAINT IF EXISTS subscriptions_tier_check CASCADE,
    DROP CONSTRAINT IF EXISTS check_subscriptions_tier CASCADE,
    DROP CONSTRAINT IF EXISTS subscriptions_status_check CASCADE,
    DROP CONSTRAINT IF EXISTS check_subscriptions_status CASCADE,
    DROP CONSTRAINT IF EXISTS subscriptions_scans_used_check CASCADE,
    DROP CONSTRAINT IF EXISTS check_subscriptions_scans_used CASCADE,
    DROP CONSTRAINT IF EXISTS subscriptions_payment_retry_check CASCADE,
    DROP CONSTRAINT IF EXISTS check_subscriptions_payment_retry CASCADE,
    DROP CONSTRAINT IF EXISTS subscriptions_user_id_fkey CASCADE,
    DROP CONSTRAINT IF EXISTS check_subscriptions_user_id CASCADE;

-- ============================================================================
-- SECTION 1: CLEAN INVALID DATA (Based on Actual Schema)
-- ============================================================================

-- 1.1 Fix invalid tier values (must be: free, basic, pro, ultra, max)
UPDATE subscriptions 
SET tier = 'free' 
WHERE tier NOT IN ('free', 'basic', 'pro', 'ultra', 'max')
   OR tier IS NULL;

-- 1.2 Fix invalid status values (must be: active, cancelled, expired)
UPDATE subscriptions 
SET status = 'active' 
WHERE status NOT IN ('active', 'cancelled', 'expired')
   OR status IS NULL;

-- 1.3 Fix negative scans_used_this_period
UPDATE subscriptions 
SET scans_used_this_period = 0 
WHERE scans_used_this_period < 0 
   OR scans_used_this_period IS NULL;

-- 1.4 Fix negative payment_retry_count
UPDATE subscriptions 
SET payment_retry_count = 0 
WHERE payment_retry_count < 0 
   OR payment_retry_count IS NULL;

-- ============================================================================
-- SECTION 2: ADD FOREIGN KEY CONSTRAINT
-- ============================================================================

-- User ID must reference auth.users (if using Supabase Auth)
-- Comment out if not using Supabase Auth
ALTER TABLE subscriptions
ADD CONSTRAINT subscriptions_user_id_fkey 
FOREIGN KEY (user_id) 
REFERENCES auth.users(id) 
ON DELETE CASCADE;

-- ============================================================================
-- SECTION 3: ADD TIER CHECK CONSTRAINT
-- ============================================================================

ALTER TABLE subscriptions
ADD CONSTRAINT check_subscriptions_tier 
CHECK (tier IN ('free', 'basic', 'pro', 'ultra', 'max'));

-- ============================================================================
-- SECTION 4: ADD STATUS CHECK CONSTRAINT
-- ============================================================================

ALTER TABLE subscriptions
ADD CONSTRAINT check_subscriptions_status 
CHECK (status IN ('active', 'cancelled', 'expired'));

-- ============================================================================
-- SECTION 5: ADD NON-NEGATIVE VALUE CONSTRAINTS
-- ============================================================================

-- Scans used must be non-negative
ALTER TABLE subscriptions
ADD CONSTRAINT check_subscriptions_scans_used 
CHECK (scans_used_this_period >= 0);

-- Payment retry count must be non-negative
ALTER TABLE subscriptions
ADD CONSTRAINT check_subscriptions_payment_retry 
CHECK (payment_retry_count >= 0);

-- ============================================================================
-- SECTION 6: ADD WEBHOOK_LOGS CONSTRAINTS (if table exists)
-- ============================================================================

-- Drop existing webhook_logs constraints first
DO $$ 
BEGIN
    IF EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'webhook_logs') THEN
        -- Drop existing constraints
        EXECUTE 'ALTER TABLE webhook_logs DROP CONSTRAINT IF EXISTS check_webhook_logs_event_type CASCADE';
        EXECUTE 'ALTER TABLE webhook_logs DROP CONSTRAINT IF EXISTS check_webhook_logs_status CASCADE';
        
        -- Add event type constraint
        EXECUTE 'ALTER TABLE webhook_logs
        ADD CONSTRAINT check_webhook_logs_event_type 
        CHECK (event_type IN (
            ''subscription.activated'',
            ''subscription.charged'',
            ''subscription.completed'',
            ''subscription.cancelled'',
            ''subscription.paused'',
            ''subscription.resumed'',
            ''payment.failed'',
            ''subscription.pending''
        ))';
        
        -- Add status constraint
        EXECUTE 'ALTER TABLE webhook_logs
        ADD CONSTRAINT check_webhook_logs_status 
        CHECK (status IN (''pending'', ''processed'', ''failed''))';
    END IF;
END $$;

-- ============================================================================
-- VERIFICATION QUERIES
-- ============================================================================

-- Check all constraints were added
SELECT 
    conname AS constraint_name,
    contype AS constraint_type,
    pg_get_constraintdef(oid) AS constraint_definition
FROM pg_constraint
WHERE conrelid = 'subscriptions'::regclass
ORDER BY conname;

-- Check data integrity
SELECT 
    COUNT(*) as total_subscriptions,
    COUNT(DISTINCT tier) as unique_tiers,
    COUNT(DISTINCT status) as unique_statuses,
    MIN(scans_used_this_period) as min_scans_used,
    MAX(scans_used_this_period) as max_scans_used,
    MIN(payment_retry_count) as min_retry_count,
    MAX(payment_retry_count) as max_retry_count
FROM subscriptions;

-- ============================================================================
-- COMPLETION MESSAGE
-- ============================================================================

SELECT '✅ DATABASE CONSTRAINTS MIGRATION COMPLETE!' as message,
       'All data integrity constraints have been successfully added.' as status,
       'Run the verification queries above to confirm.' as next_step;
