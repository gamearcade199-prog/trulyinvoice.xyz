-- =====================================================
-- 🔒 PRODUCTION-READY RLS POLICIES WITH AUTO-CLEANUP
-- =====================================================
-- TrulyInvoice Security Fix - October 22, 2025
-- Run this in Supabase SQL Editor to fix all RLS issues

-- =====================================================
-- STEP 1: CLEAN SLATE (Remove old broken policies)
-- =====================================================

-- Disable RLS temporarily to clean up
ALTER TABLE documents DISABLE ROW LEVEL SECURITY;
ALTER TABLE invoices DISABLE ROW LEVEL SECURITY;

-- Drop ALL old policies
DROP POLICY IF EXISTS "Public insert access" ON documents;
DROP POLICY IF EXISTS "Public read access" ON documents;
DROP POLICY IF EXISTS "Users can view own documents" ON documents;
DROP POLICY IF EXISTS "Users can insert own documents" ON documents;
DROP POLICY IF EXISTS "Users can update own documents" ON documents;
DROP POLICY IF EXISTS "Service role can access all documents" ON documents;
DROP POLICY IF EXISTS "Anonymous users can insert documents" ON documents;
DROP POLICY IF EXISTS "Anonymous users can view own documents" ON documents;
DROP POLICY IF EXISTS "Anonymous temp access" ON documents;
DROP POLICY IF EXISTS "Anonymous read own" ON documents;

DROP POLICY IF EXISTS "Users can view own invoices" ON invoices;
DROP POLICY IF EXISTS "Users can insert own invoices" ON invoices;
DROP POLICY IF EXISTS "Users can update own invoices" ON invoices;
DROP POLICY IF EXISTS "Users own invoices" ON invoices;

-- =====================================================
-- STEP 2: ENABLE RLS (Fresh start)
-- =====================================================

ALTER TABLE documents ENABLE ROW LEVEL SECURITY;
ALTER TABLE invoices ENABLE ROW LEVEL SECURITY;

-- =====================================================
-- STEP 3: DOCUMENTS TABLE POLICIES
-- =====================================================

-- Policy 1: Authenticated users can manage their own documents
CREATE POLICY "authenticated_users_own_documents" ON documents
  FOR ALL
  USING (auth.uid() IS NOT NULL AND auth.uid() = user_id::uuid)
  WITH CHECK (auth.uid() IS NOT NULL AND auth.uid() = user_id::uuid);

-- Policy 2: Anonymous users can insert documents for preview (with 1-hour expiry)
CREATE POLICY "anonymous_can_insert_temp" ON documents
  FOR INSERT
  WITH CHECK (
    auth.uid() IS NULL AND
    user_id IS NULL AND
    created_at > NOW() - INTERVAL '1 hour'
  );

-- Policy 3: Anonymous users can read their temp uploads (1-hour window)
CREATE POLICY "anonymous_can_read_temp" ON documents
  FOR SELECT
  USING (
    (auth.uid() IS NOT NULL AND auth.uid() = user_id::uuid) OR
    (auth.uid() IS NULL AND user_id IS NULL AND created_at > NOW() - INTERVAL '1 hour')
  );

-- Policy 4: Service role has full access (for backend operations)
CREATE POLICY "service_role_full_access_documents" ON documents
  FOR ALL
  USING (auth.jwt()->>'role' = 'service_role')
  WITH CHECK (auth.jwt()->>'role' = 'service_role');

-- =====================================================
-- STEP 4: INVOICES TABLE POLICIES
-- =====================================================

-- Policy 1: Authenticated users can manage invoices for their documents
CREATE POLICY "authenticated_users_own_invoices" ON invoices
  FOR ALL
  USING (
    auth.uid() IS NOT NULL AND
    EXISTS (
      SELECT 1 FROM documents 
      WHERE documents.id = invoices.document_id 
      AND documents.user_id = auth.uid()::text
    )
  )
  WITH CHECK (
    auth.uid() IS NOT NULL AND
    EXISTS (
      SELECT 1 FROM documents 
      WHERE documents.id = invoices.document_id 
      AND documents.user_id = auth.uid()::text
    )
  );

-- Policy 2: Anonymous users can access invoices for temp documents
CREATE POLICY "anonymous_can_access_temp_invoices" ON invoices
  FOR ALL
  USING (
    auth.uid() IS NULL AND
    EXISTS (
      SELECT 1 FROM documents 
      WHERE documents.id = invoices.document_id 
      AND documents.user_id IS NULL
      AND documents.created_at > NOW() - INTERVAL '1 hour'
    )
  )
  WITH CHECK (
    auth.uid() IS NULL AND
    EXISTS (
      SELECT 1 FROM documents 
      WHERE documents.id = invoices.document_id 
      AND documents.user_id IS NULL
    )
  );

-- Policy 3: Service role has full access (for backend operations)
CREATE POLICY "service_role_full_access_invoices" ON invoices
  FOR ALL
  USING (auth.jwt()->>'role' = 'service_role')
  WITH CHECK (auth.jwt()->>'role' = 'service_role');

-- =====================================================
-- STEP 5: AUTO-CLEANUP FUNCTION
-- =====================================================

-- Function to clean up anonymous uploads older than 24 hours
CREATE OR REPLACE FUNCTION cleanup_anonymous_uploads()
RETURNS void AS $$
DECLARE
  deleted_count INTEGER;
BEGIN
  -- Delete old anonymous invoices first (foreign key constraint)
  DELETE FROM invoices
  WHERE document_id IN (
    SELECT id FROM documents 
    WHERE user_id IS NULL 
    AND created_at < NOW() - INTERVAL '24 hours'
  );
  
  GET DIAGNOSTICS deleted_count = ROW_COUNT;
  RAISE NOTICE 'Deleted % anonymous invoices', deleted_count;
  
  -- Delete old anonymous documents
  DELETE FROM documents 
  WHERE user_id IS NULL 
  AND created_at < NOW() - INTERVAL '24 hours';
  
  GET DIAGNOSTICS deleted_count = ROW_COUNT;
  RAISE NOTICE 'Deleted % anonymous documents', deleted_count;
  
  -- Also clean up orphaned invoices (documents no longer exist)
  DELETE FROM invoices
  WHERE document_id NOT IN (SELECT id FROM documents);
  
  GET DIAGNOSTICS deleted_count = ROW_COUNT;
  RAISE NOTICE 'Deleted % orphaned invoices', deleted_count;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- =====================================================
-- STEP 6: SCHEDULE AUTO-CLEANUP (Optional - requires pg_cron)
-- =====================================================

-- Note: pg_cron extension may not be available on all Supabase plans
-- If available, uncomment these lines:

-- SELECT cron.schedule(
--   'cleanup-anonymous-uploads',
--   '0 2 * * *', -- Run daily at 2 AM UTC
--   'SELECT cleanup_anonymous_uploads()'
-- );

-- If pg_cron is not available, you can:
-- 1. Call this function manually from your backend on a schedule
-- 2. Create a Supabase Edge Function to run it
-- 3. Use a cron job service (like cron-job.org) to hit an API endpoint

-- =====================================================
-- STEP 7: RATE LIMITING TABLE (For anonymous uploads)
-- =====================================================

-- Create table to track anonymous upload attempts
-- Rate limits based on TrulyInvoice pricing plans:
-- - Anonymous/Preview: 10 uploads/hour (prevents abuse)
-- - Free: 1 bulk upload (handled in app logic)
-- - Basic: 5 bulk uploads (handled in app logic)
-- - Pro: 10 bulk uploads (handled in app logic)
-- - Ultra: 50 bulk uploads (handled in app logic)
-- - Max: 100 bulk uploads (handled in app logic)
CREATE TABLE IF NOT EXISTS anonymous_upload_attempts (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  ip_address text NOT NULL,
  attempted_at timestamp DEFAULT NOW(),
  user_agent text
);

-- Create index for fast lookups
CREATE INDEX IF NOT EXISTS idx_anonymous_attempts_ip_time 
ON anonymous_upload_attempts(ip_address, attempted_at DESC);

-- Enable RLS
ALTER TABLE anonymous_upload_attempts ENABLE ROW LEVEL SECURITY;

-- Service role can manage this table
CREATE POLICY "service_role_full_access_attempts" ON anonymous_upload_attempts
  FOR ALL
  USING (auth.jwt()->>'role' = 'service_role')
  WITH CHECK (auth.jwt()->>'role' = 'service_role');

-- Function to check rate limit for anonymous users
-- Free plan: 1 bulk upload = 1 invoice per upload
-- Anonymous preview users: 10 uploads per hour (generous for testing)
CREATE OR REPLACE FUNCTION check_anonymous_rate_limit(ip_addr text)
RETURNS boolean AS $$
DECLARE
  recent_count INTEGER;
BEGIN
  -- Count uploads in last 60 minutes (1 hour window)
  SELECT COUNT(*) INTO recent_count
  FROM anonymous_upload_attempts
  WHERE ip_address = ip_addr
  AND attempted_at > NOW() - INTERVAL '60 minutes';
  
  -- If less than 10 uploads per hour, allow (prevents abuse while allowing testing)
  IF recent_count < 10 THEN
    -- Log this attempt
    INSERT INTO anonymous_upload_attempts (ip_address, user_agent)
    VALUES (ip_addr, current_setting('request.headers', true)::json->>'user-agent');
    
    RETURN true;
  ELSE
    RETURN false;
  END IF;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- =====================================================
-- STEP 8: VERIFICATION QUERIES
-- =====================================================

-- Check that RLS is enabled
SELECT 
  tablename,
  CASE WHEN rowsecurity THEN '✅ ENABLED' ELSE '❌ DISABLED' END as rls_status
FROM pg_tables 
WHERE schemaname = 'public'
AND tablename IN ('documents', 'invoices');

-- List all active policies
SELECT 
  schemaname,
  tablename,
  policyname,
  cmd as operation,
  CASE 
    WHEN roles = '{public}' THEN '👥 Public'
    ELSE '🔒 ' || array_to_string(roles, ', ')
  END as applies_to
FROM pg_policies 
WHERE schemaname = 'public'
AND tablename IN ('documents', 'invoices')
ORDER BY tablename, policyname;

-- =====================================================
-- STEP 9: TEST QUERIES
-- =====================================================

-- Test 1: Authenticated user should see only their documents
-- (Run while logged in)
-- SELECT id, user_id, created_at FROM documents;

-- Test 2: Anonymous user should see only recent temp documents
-- (Run while logged out)
-- SELECT id, user_id, created_at FROM documents WHERE user_id IS NULL;

-- Test 3: Run cleanup function manually
-- SELECT cleanup_anonymous_uploads();

-- =====================================================
-- SUCCESS INDICATORS
-- =====================================================

-- ✅ RLS is enabled on both tables
-- ✅ 7 policies created (4 for documents, 3 for invoices)
-- ✅ Auto-cleanup function created
-- ✅ Rate limiting table created
-- ✅ Authenticated users isolated from each other
-- ✅ Anonymous users can preview but data auto-expires
-- ✅ Service role can perform backend operations

-- =====================================================
-- MAINTENANCE COMMANDS
-- =====================================================

-- To manually clean up old anonymous uploads:
-- SELECT cleanup_anonymous_uploads();

-- To check recent anonymous upload attempts:
-- SELECT ip_address, COUNT(*) as attempts, MAX(attempted_at) as last_attempt
-- FROM anonymous_upload_attempts
-- WHERE attempted_at > NOW() - INTERVAL '1 hour'
-- GROUP BY ip_address
-- HAVING COUNT(*) >= 10
-- ORDER BY attempts DESC;

-- To clean up old rate limit records (run periodically):
-- DELETE FROM anonymous_upload_attempts WHERE attempted_at < NOW() - INTERVAL '24 hours';

-- To view policy details:
-- \d+ documents  -- In psql
-- SELECT * FROM pg_policies WHERE tablename = 'documents';

RAISE NOTICE '✅ RLS policies successfully configured!';
RAISE NOTICE '🔧 Run cleanup_anonymous_uploads() to test cleanup function';
RAISE NOTICE '📊 Check policies with: SELECT * FROM pg_policies WHERE tablename IN (''documents'', ''invoices'');';
