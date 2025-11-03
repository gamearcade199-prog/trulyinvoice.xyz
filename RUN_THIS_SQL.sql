-- ============================================================================
-- FINAL SQL FIX - RUN THIS IN SUPABASE SQL EDITOR
-- ============================================================================
-- Copy this entire file and paste into Supabase SQL Editor, then click RUN
-- ============================================================================

-- Step 1: Check table structure
DO $$
BEGIN
    IF EXISTS (
        SELECT 1 FROM information_schema.columns
        WHERE table_name = 'subscriptions'
        AND column_name = 'user_id'
        AND data_type = 'uuid'
    ) THEN
        RAISE NOTICE '✅ user_id is UUID type (correct)';
    ELSE
        RAISE NOTICE '⚠️ user_id is not UUID - this may cause issues';
    END IF;
END $$;

-- Step 2: Drop ALL existing RLS policies
DROP POLICY IF EXISTS "Users can view own subscription" ON subscriptions;
DROP POLICY IF EXISTS "Users can insert own subscription" ON subscriptions;
DROP POLICY IF EXISTS "Users can update own subscription" ON subscriptions;
DROP POLICY IF EXISTS "Service role can manage all subscriptions" ON subscriptions;
DROP POLICY IF EXISTS "Service role can insert subscriptions" ON subscriptions;
DROP POLICY IF EXISTS "Allow backend to create subscriptions" ON subscriptions;
DROP POLICY IF EXISTS "Allow service role to insert subscriptions" ON subscriptions;
DROP POLICY IF EXISTS "Allow users to insert own subscription" ON subscriptions;
DROP POLICY IF EXISTS "Service role can delete subscriptions" ON subscriptions;

-- Step 3: Enable RLS
ALTER TABLE subscriptions ENABLE ROW LEVEL SECURITY;

-- Step 4: Create new policies
CREATE POLICY "service_role_all_access"
ON subscriptions
AS PERMISSIVE
FOR ALL
TO service_role
USING (true)
WITH CHECK (true);

CREATE POLICY "users_select_own"
ON subscriptions
AS PERMISSIVE
FOR SELECT
TO authenticated
USING (auth.uid() = user_id);

CREATE POLICY "users_insert_own"
ON subscriptions
AS PERMISSIVE
FOR INSERT
TO authenticated
WITH CHECK (auth.uid() = user_id);

CREATE POLICY "users_update_own"
ON subscriptions
AS PERMISSIVE
FOR UPDATE
TO authenticated
USING (auth.uid() = user_id)
WITH CHECK (auth.uid() = user_id);

CREATE POLICY "anon_select"
ON subscriptions
AS PERMISSIVE
FOR SELECT
TO anon
USING (false);

-- Step 5: Create indexes
CREATE INDEX IF NOT EXISTS idx_subscriptions_user_id ON subscriptions(user_id);
CREATE INDEX IF NOT EXISTS idx_subscriptions_status ON subscriptions(status);
CREATE INDEX IF NOT EXISTS idx_subscriptions_tier ON subscriptions(tier);

-- Step 6: Verification
DO $$
DECLARE
    policy_count INTEGER;
BEGIN
    SELECT COUNT(*) INTO policy_count
    FROM pg_policies
    WHERE tablename = 'subscriptions';
    
    RAISE NOTICE '';
    RAISE NOTICE '============================================';
    RAISE NOTICE '✅ CONFIGURATION COMPLETE';
    RAISE NOTICE '============================================';
    RAISE NOTICE 'Policies created: %', policy_count;
    RAISE NOTICE '';
    RAISE NOTICE '✅ service_role_all_access - Backend can do everything';
    RAISE NOTICE '✅ users_select_own - Users can view own subscription';
    RAISE NOTICE '✅ users_insert_own - Users can create subscription';
    RAISE NOTICE '✅ users_update_own - Users can update subscription';
    RAISE NOTICE '✅ anon_select - Public access blocked';
    RAISE NOTICE '';
    RAISE NOTICE '🎉 Registration should now work!';
    RAISE NOTICE '';
    RAISE NOTICE 'Test: Go to /register and create a new account';
    RAISE NOTICE '';
    RAISE NOTICE '============================================';
END $$;

-- Step 7: Show all policies
SELECT 
    policyname,
    cmd,
    roles::text
FROM pg_policies
WHERE tablename = 'subscriptions'
ORDER BY policyname;
