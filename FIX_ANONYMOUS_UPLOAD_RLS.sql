-- =====================================================
-- FIX ANONYMOUS UPLOAD ISSUES - RLS POLICIES
-- =====================================================
-- This script allows uploads to work for both:
-- 1. Signed-in users
-- 2. Anonymous users (not signed in)
-- Run this in Supabase SQL Editor

-- ===== FIX DOCUMENTS TABLE =====

-- Disable RLS temporarily to clean up
ALTER TABLE documents DISABLE ROW LEVEL SECURITY;

-- Drop all existing policies
DROP POLICY IF EXISTS "Users can view own documents" ON documents;
DROP POLICY IF EXISTS "Users can insert own documents" ON documents;
DROP POLICY IF EXISTS "Users can update own documents" ON documents;
DROP POLICY IF EXISTS "Service role can access all documents" ON documents;
DROP POLICY IF EXISTS "Anonymous users can insert documents" ON documents;
DROP POLICY IF EXISTS "Anonymous users can view own documents" ON documents;
DROP POLICY IF EXISTS "Public read access" ON documents;
DROP POLICY IF EXISTS "Public insert access" ON documents;

-- Re-enable RLS
ALTER TABLE documents ENABLE ROW LEVEL SECURITY;

-- Policy 1: Allow ANYONE to insert documents (for demo uploads)
CREATE POLICY "Public insert access" ON documents
  FOR INSERT
  WITH CHECK (true);

-- Policy 2: Allow ANYONE to view documents (for demo)
-- In production, you may want to restrict this
CREATE POLICY "Public read access" ON documents
  FOR SELECT
  USING (true);

-- Policy 3: Users can update their own documents
CREATE POLICY "Users can update own documents" ON documents
  FOR UPDATE
  USING (
    auth.uid() IS NOT NULL AND 
    auth.uid() = user_id::uuid
  );

-- Policy 4: Service role has full access
DROP POLICY IF EXISTS "Service role full access" ON documents;
CREATE POLICY "Service role full access" ON documents
  FOR ALL
  USING (auth.role() = 'service_role')
  WITH CHECK (auth.role() = 'service_role');

-- ===== FIX INVOICES TABLE =====

-- Disable RLS temporarily
ALTER TABLE invoices DISABLE ROW LEVEL SECURITY;

-- Drop all existing policies
DROP POLICY IF EXISTS "Users can view own invoices" ON invoices;
DROP POLICY IF EXISTS "Users can insert own invoices" ON invoices;
DROP POLICY IF EXISTS "Users can update own invoices" ON invoices;
DROP POLICY IF EXISTS "Service role can access all invoices" ON invoices;
DROP POLICY IF EXISTS "Backend can create invoices" ON invoices;
DROP POLICY IF EXISTS "Public read access" ON invoices;
DROP POLICY IF EXISTS "Public insert access" ON invoices;

-- Re-enable RLS
ALTER TABLE invoices ENABLE ROW LEVEL SECURITY;

-- Policy 1: Allow ANYONE to insert invoices (backend processing)
CREATE POLICY "Public insert access" ON invoices
  FOR INSERT
  WITH CHECK (true);

-- Policy 2: Allow ANYONE to read invoices (for demo)
CREATE POLICY "Public read access" ON invoices
  FOR SELECT
  USING (true);

-- Policy 3: Users can update their own invoices
CREATE POLICY "Users can update own invoices" ON invoices
  FOR UPDATE
  USING (
    EXISTS (
      SELECT 1 FROM documents 
      WHERE documents.id = invoices.document_id 
      AND documents.user_id::uuid = auth.uid()
    )
  );

-- Policy 4: Service role has full access
DROP POLICY IF EXISTS "Service role full access" ON invoices;
CREATE POLICY "Service role full access" ON invoices
  FOR ALL
  USING (auth.role() = 'service_role')
  WITH CHECK (auth.role() = 'service_role');

-- ===== VERIFY POLICIES =====

-- Check documents policies
SELECT 
  schemaname,
  tablename,
  policyname,
  permissive,
  roles,
  cmd,
  qual,
  with_check
FROM pg_policies 
WHERE tablename = 'documents';

-- Check invoices policies
SELECT 
  schemaname,
  tablename,
  policyname,
  permissive,
  roles,
  cmd,
  qual,
  with_check
FROM pg_policies 
WHERE tablename = 'invoices';

-- =====================================================
-- IMPORTANT NOTES:
-- =====================================================
-- ⚠️ SECURITY WARNING:
-- These policies allow PUBLIC access for demo purposes
-- 
-- For PRODUCTION, you should:
-- 1. Require authentication for all uploads
-- 2. Add rate limiting
-- 3. Restrict view access to document owners only
-- 4. Add usage tracking and billing
-- 
-- To make it production-ready later, replace policies with:
-- - Authenticated users only can insert/view
-- - Anonymous uploads get stored in temp table
-- - Require sign-up to access processed invoices
-- =====================================================

-- Optional: Create a view for public invoices
CREATE OR REPLACE VIEW public_invoices AS
SELECT 
  i.id,
  i.invoice_number,
  i.invoice_date,
  i.total_amount,
  i.currency,
  i.vendor_name,
  i.created_at
FROM invoices i
WHERE i.created_at > NOW() - INTERVAL '24 hours';

-- Grant access to the view
GRANT SELECT ON public_invoices TO anon;
GRANT SELECT ON public_invoices TO authenticated;
