-- ============================================================================
-- VERIFY ALL CONSTRAINTS WERE ADDED SUCCESSFULLY
-- ============================================================================

-- 1. Check all constraints on subscriptions table
SELECT 
    conname AS constraint_name,
    contype AS constraint_type,
    CASE contype
        WHEN 'c' THEN 'CHECK'
        WHEN 'f' THEN 'FOREIGN KEY'
        WHEN 'p' THEN 'PRIMARY KEY'
        WHEN 'u' THEN 'UNIQUE'
    END AS constraint_description,
    pg_get_constraintdef(oid) AS constraint_definition
FROM pg_constraint
WHERE conrelid = 'subscriptions'::regclass
ORDER BY contype, conname;

-- 2. Check webhook_logs constraints (if table exists)
SELECT 
    conname AS constraint_name,
    contype AS constraint_type,
    pg_get_constraintdef(oid) AS constraint_definition
FROM pg_constraint
WHERE conrelid = 'webhook_logs'::regclass
ORDER BY conname;

-- 3. Test constraint enforcement - Try to insert invalid data
-- This should FAIL if constraints are working
DO $$
BEGIN
    -- Try invalid tier
    BEGIN
        INSERT INTO subscriptions (user_id, tier, status, scans_used_this_period, current_period_end)
        VALUES ('test-user-123', 'invalid_tier', 'active', 0, NOW() + INTERVAL '30 days');
        RAISE NOTICE '❌ CONSTRAINT FAILED: Invalid tier was accepted!';
    EXCEPTION WHEN check_violation THEN
        RAISE NOTICE '✅ CONSTRAINT WORKING: Invalid tier rejected correctly';
    END;
    
    -- Try invalid status
    BEGIN
        INSERT INTO subscriptions (user_id, tier, status, scans_used_this_period, current_period_end)
        VALUES ('test-user-456', 'free', 'invalid_status', 0, NOW() + INTERVAL '30 days');
        RAISE NOTICE '❌ CONSTRAINT FAILED: Invalid status was accepted!';
    EXCEPTION WHEN check_violation THEN
        RAISE NOTICE '✅ CONSTRAINT WORKING: Invalid status rejected correctly';
    END;
    
    -- Try negative scans
    BEGIN
        INSERT INTO subscriptions (user_id, tier, status, scans_used_this_period, current_period_end)
        VALUES ('test-user-789', 'free', 'active', -10, NOW() + INTERVAL '30 days');
        RAISE NOTICE '❌ CONSTRAINT FAILED: Negative scans accepted!';
    EXCEPTION WHEN check_violation THEN
        RAISE NOTICE '✅ CONSTRAINT WORKING: Negative scans rejected correctly';
    END;
END $$;

-- 4. Summary
SELECT 
    '✅ VERIFICATION COMPLETE!' as status,
    COUNT(*) as total_constraints
FROM pg_constraint
WHERE conrelid = 'subscriptions'::regclass;
