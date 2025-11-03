-- ============================================================================
-- DATABASE STRUCTURE SCAN
-- This will show us the exact structure and data types
-- ============================================================================

-- 1. Check auth.users table structure and data types
SELECT 
    column_name, 
    data_type, 
    udt_name,
    is_nullable
FROM information_schema.columns
WHERE table_schema = 'auth' 
  AND table_name = 'users'
ORDER BY ordinal_position;

-- 2. Check subscriptions table structure and data types
SELECT 
    column_name, 
    data_type, 
    udt_name,
    is_nullable,
    column_default
FROM information_schema.columns
WHERE table_schema = 'public' 
  AND table_name = 'subscriptions'
ORDER BY ordinal_position;

-- 3. Check what tier values exist in subscriptions
SELECT DISTINCT tier, COUNT(*) as count
FROM subscriptions
GROUP BY tier;

-- 4. Check for the specific user
SELECT 
    id,
    email,
    created_at
FROM auth.users
WHERE email = 'akibhusain830@gmail.com';

-- 5. Check if user has a subscription
SELECT 
    s.*
FROM subscriptions s
WHERE s.user_id IN (
    SELECT id::TEXT FROM auth.users WHERE email = 'akibhusain830@gmail.com'
);

-- 6. Check table constraints and foreign keys
SELECT
    tc.constraint_name,
    tc.constraint_type,
    kcu.column_name,
    ccu.table_name AS foreign_table_name,
    ccu.column_name AS foreign_column_name
FROM information_schema.table_constraints AS tc
JOIN information_schema.key_column_usage AS kcu
    ON tc.constraint_name = kcu.constraint_name
LEFT JOIN information_schema.constraint_column_usage AS ccu
    ON ccu.constraint_name = tc.constraint_name
WHERE tc.table_name = 'subscriptions';
