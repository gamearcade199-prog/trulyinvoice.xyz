-- ============================================================================
-- CHECK EXISTING CONSTRAINTS
-- Run this first to see what constraints already exist
-- ============================================================================

-- Check existing constraints on subscriptions table
SELECT 
    conname AS constraint_name,
    contype AS constraint_type,
    pg_get_constraintdef(oid) AS constraint_definition
FROM pg_constraint
WHERE conrelid = 'subscriptions'::regclass
ORDER BY conname;

-- Check existing constraints on webhook_logs table
SELECT 
    conname AS constraint_name,
    contype AS constraint_type,
    pg_get_constraintdef(oid) AS constraint_definition
FROM pg_constraint
WHERE conrelid = 'webhook_logs'::regclass
ORDER BY conname;

-- Check for any invalid tier values
SELECT tier, COUNT(*) as count
FROM subscriptions
GROUP BY tier
ORDER BY count DESC;

-- Check for any invalid status values
SELECT status, COUNT(*) as count
FROM subscriptions
GROUP BY status
ORDER BY count DESC;
