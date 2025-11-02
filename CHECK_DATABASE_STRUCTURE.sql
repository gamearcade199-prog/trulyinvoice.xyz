-- ============================================================================
-- CHECK DATABASE STRUCTURE
-- Run this FIRST to see what columns actually exist
-- ============================================================================

-- 1. Check subscriptions table structure
SELECT 
    column_name,
    data_type,
    is_nullable,
    column_default
FROM information_schema.columns
WHERE table_name = 'subscriptions'
ORDER BY ordinal_position;

-- 2. Check webhook_logs table structure (if it exists)
SELECT 
    column_name,
    data_type,
    is_nullable,
    column_default
FROM information_schema.columns
WHERE table_name = 'webhook_logs'
ORDER BY ordinal_position;

-- 3. Check existing constraints
SELECT 
    conname AS constraint_name,
    contype AS constraint_type,
    pg_get_constraintdef(oid) AS constraint_definition
FROM pg_constraint
WHERE conrelid = 'subscriptions'::regclass
ORDER BY conname;

-- 4. Sample data from subscriptions
SELECT * FROM subscriptions LIMIT 5;

-- 5. Check unique tier values
SELECT DISTINCT tier FROM subscriptions ORDER BY tier;

-- 6. Check unique status values
SELECT DISTINCT status FROM subscriptions ORDER BY status;
