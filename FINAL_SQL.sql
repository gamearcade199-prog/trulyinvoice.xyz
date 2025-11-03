-- ============================================================================
-- FINAL WORKING SQL - RUN THIS NOW
-- ============================================================================

-- Drop all existing policies
DROP POLICY IF EXISTS "Users can view own subscription" ON subscriptions;
DROP POLICY IF EXISTS "Users can insert own subscription" ON subscriptions;
DROP POLICY IF EXISTS "Users can update own subscription" ON subscriptions;
DROP POLICY IF EXISTS "Service role can manage all subscriptions" ON subscriptions;
DROP POLICY IF EXISTS "Service role can insert subscriptions" ON subscriptions;
DROP POLICY IF EXISTS "Allow backend to create subscriptions" ON subscriptions;
DROP POLICY IF EXISTS "Allow service role to insert subscriptions" ON subscriptions;
DROP POLICY IF EXISTS "Allow users to insert own subscription" ON subscriptions;
DROP POLICY IF EXISTS "Service role can delete subscriptions" ON subscriptions;
DROP POLICY IF EXISTS "service_role_all_access" ON subscriptions;
DROP POLICY IF EXISTS "users_select_own" ON subscriptions;
DROP POLICY IF EXISTS "users_insert_own" ON subscriptions;
DROP POLICY IF EXISTS "users_update_own" ON subscriptions;
DROP POLICY IF EXISTS "anon_select" ON subscriptions;
DROP POLICY IF EXISTS "service_role_select" ON subscriptions;
DROP POLICY IF EXISTS "service_role_insert" ON subscriptions;
DROP POLICY IF EXISTS "service_role_update" ON subscriptions;
DROP POLICY IF EXISTS "service_role_delete" ON subscriptions;
DROP POLICY IF EXISTS "authenticated_select_own" ON subscriptions;
DROP POLICY IF EXISTS "authenticated_insert_own" ON subscriptions;
DROP POLICY IF EXISTS "authenticated_update_own" ON subscriptions;
DROP POLICY IF EXISTS "block_anon_access" ON subscriptions;
DROP POLICY IF EXISTS "block_anon" ON subscriptions;

-- Enable RLS
ALTER TABLE subscriptions ENABLE ROW LEVEL SECURITY;

-- Grant permissions
GRANT ALL ON subscriptions TO service_role;
GRANT SELECT, INSERT, UPDATE ON subscriptions TO authenticated;

-- Create policies for service_role (backend)
DROP POLICY IF EXISTS "service_role_select" ON subscriptions;
CREATE POLICY "service_role_select" ON subscriptions FOR SELECT TO service_role USING (true);

DROP POLICY IF EXISTS "service_role_insert" ON subscriptions;
CREATE POLICY "service_role_insert" ON subscriptions FOR INSERT TO service_role WITH CHECK (true);

DROP POLICY IF EXISTS "service_role_update" ON subscriptions;
CREATE POLICY "service_role_update" ON subscriptions FOR UPDATE TO service_role USING (true) WITH CHECK (true);

DROP POLICY IF EXISTS "service_role_delete" ON subscriptions;
CREATE POLICY "service_role_delete" ON subscriptions FOR DELETE TO service_role USING (true);

-- Create policies for authenticated users
DROP POLICY IF EXISTS "authenticated_select_own" ON subscriptions;
CREATE POLICY "authenticated_select_own" ON subscriptions FOR SELECT TO authenticated USING (auth.uid() = user_id);

DROP POLICY IF EXISTS "authenticated_insert_own" ON subscriptions;
CREATE POLICY "authenticated_insert_own" ON subscriptions FOR INSERT TO authenticated WITH CHECK (auth.uid() = user_id);

DROP POLICY IF EXISTS "authenticated_update_own" ON subscriptions;
CREATE POLICY "authenticated_update_own" ON subscriptions FOR UPDATE TO authenticated USING (auth.uid() = user_id) WITH CHECK (auth.uid() = user_id);

-- Block anonymous
DROP POLICY IF EXISTS "block_anon" ON subscriptions;
CREATE POLICY "block_anon" ON subscriptions FOR ALL TO anon USING (false);

-- Create indexes
CREATE INDEX IF NOT EXISTS idx_subscriptions_user_id ON subscriptions(user_id);
CREATE INDEX IF NOT EXISTS idx_subscriptions_status ON subscriptions(status);
CREATE INDEX IF NOT EXISTS idx_subscriptions_tier ON subscriptions(tier);

-- Verify
DO $$
DECLARE
    policy_count INTEGER;
BEGIN
    SELECT COUNT(*) INTO policy_count FROM pg_policies WHERE tablename = 'subscriptions';
    RAISE NOTICE '============================================';
    RAISE NOTICE '✅ CONFIGURATION COMPLETE';
    RAISE NOTICE '============================================';
    RAISE NOTICE 'Policies created: %', policy_count;
    RAISE NOTICE '';
    RAISE NOTICE '✅ Backend can now create subscriptions';
    RAISE NOTICE '✅ Users can view/update their own data';
    RAISE NOTICE '✅ Anonymous access blocked';
    RAISE NOTICE '';
    RAISE NOTICE 'Test registration at /register';
    RAISE NOTICE '============================================';
END $$;

-- Show policies
SELECT policyname, cmd, roles::text FROM pg_policies WHERE tablename = 'subscriptions' ORDER BY policyname;
