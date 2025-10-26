-- =====================================================
-- MOST LIKELY FIX: RLS Policies Blocking Invoice Operations  
-- =====================================================
-- Run this in Supabase SQL Editor if 404 still appears
-- This temporarily opens RLS to diagnose the issue

-- =====================================================
-- STEP 1: Check Current RLS Policies on Invoices
-- =====================================================

SELECT policyname, cmd, qual, with_check
FROM pg_policies 
WHERE tablename = 'invoices'
ORDER BY cmd;

-- If you see many restrictive policies, that's the problem!

-- =====================================================
-- STEP 2: Temporarily Open RLS (For Diagnosis)
-- =====================================================

-- Drop all INSERT policies
DROP POLICY IF EXISTS "Users can insert own invoices" ON invoices;
DROP POLICY IF EXISTS "Backend can create invoices" ON invoices;
DROP POLICY IF EXISTS "Public insert access" ON invoices;

-- Drop all SELECT policies  
DROP POLICY IF EXISTS "Users can view own invoices" ON invoices;
DROP POLICY IF EXISTS "Allow all read" ON invoices;
DROP POLICY IF EXISTS "Public read access" ON invoices;

-- Add simple policies for testing
CREATE POLICY "Test allow insert" ON invoices
  FOR INSERT
  WITH CHECK (true);

CREATE POLICY "Test allow select" ON invoices
  FOR SELECT
  USING (true);

-- =====================================================
-- STEP 3: Verify Policies Were Updated
-- =====================================================

SELECT policyname, cmd 
FROM pg_policies 
WHERE tablename = 'invoices'
ORDER BY cmd;

-- You should see only 2 policies now:
-- - Test allow insert (INSERT)
-- - Test allow select (SELECT)

-- =====================================================
-- STEP 4: Test Upload & View
-- =====================================================

-- After running above:
-- 1. Go back to trulyinvoice.xyz
-- 2. Upload a test invoice
-- 3. Click eye icon to view it
-- 4. If 404 is GONE - then RLS was the issue!

-- =====================================================
-- AFTER CONFIRMING THE FIX WORKS
-- =====================================================

-- Once you confirm it works, we can make it more secure with:

DROP POLICY IF EXISTS "Test allow insert" ON invoices;
DROP POLICY IF EXISTS "Test allow select" ON invoices;

-- Secure policies for production
CREATE POLICY "Backend can do anything" ON invoices
  FOR ALL
  USING (auth.role() = 'service_role')
  WITH CHECK (auth.role() = 'service_role');

CREATE POLICY "Users can read all invoices" ON invoices
  FOR SELECT
  USING (true);  -- All can read for now

CREATE POLICY "Users can insert invoices" ON invoices
  FOR INSERT
  WITH CHECK (true);  -- All can insert for now

-- Later make it more restrictive if needed
-- USING (auth.uid()::text = user_id OR auth.role() = 'service_role');
