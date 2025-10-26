-- =====================================================
-- TEMPORARY FIX: Relax RLS to allow backend reading
-- =====================================================
-- Run this in Supabase SQL Editor to allow the backend
-- API to fetch invoices without RLS blocking

-- Check current policies
SELECT policyname, cmd, qual 
FROM pg_policies 
WHERE tablename = 'invoices';

-- Drop restrictive policies temporarily
DROP POLICY IF EXISTS "Users can view own invoices" ON invoices;

-- Add new policy that allows backend (service_role) and public reads
CREATE POLICY "Allow backend and public read" ON invoices
  FOR SELECT
  USING (true);  -- Temporarily allow everyone to read

-- Keep other policies as-is
-- This means:
-- - Anyone can READ invoices
-- - Only service_role can INSERT/UPDATE
-- - Users with user_id set can update own

-- Verify
SELECT policyname, cmd, qual 
FROM pg_policies 
WHERE tablename = 'invoices'
ORDER BY cmd;

-- After Vercel deploys commit 9327073, you can make this more restrictive:
-- CREATE POLICY "Users can view own invoices" ON invoices
--   FOR SELECT
--   USING (auth.uid()::text = user_id OR auth.role() = 'service_role');
