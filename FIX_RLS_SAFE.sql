-- =====================================================
-- SAFE FIX FOR UPLOAD ERROR - Run This Version
-- =====================================================
-- This version is safe to run multiple times
-- It will fix the "new row violates row-level security policy" error

-- ===== FIX DOCUMENTS TABLE =====

-- Drop ALL existing policies first (safe, won't error if not exists)
DROP POLICY IF EXISTS "Users can view own documents" ON documents;
DROP POLICY IF EXISTS "Users can insert own documents" ON documents;
DROP POLICY IF EXISTS "Users can update own documents" ON documents;
DROP POLICY IF EXISTS "Service role can access all documents" ON documents;
DROP POLICY IF EXISTS "Anonymous users can insert documents" ON documents;
DROP POLICY IF EXISTS "Anonymous users can view own documents" ON documents;
DROP POLICY IF EXISTS "Public read access" ON documents;
DROP POLICY IF EXISTS "Public insert access" ON documents;
DROP POLICY IF EXISTS "Service role full access" ON documents;

-- Ensure RLS is enabled
ALTER TABLE documents ENABLE ROW LEVEL SECURITY;

-- Create new policies
CREATE POLICY "Public insert access" ON documents
  FOR INSERT
  WITH CHECK (true);

CREATE POLICY "Public read access" ON documents
  FOR SELECT
  USING (true);

CREATE POLICY "Users can update own documents" ON documents
  FOR UPDATE
  USING (
    auth.uid() IS NOT NULL AND 
    auth.uid() = user_id::uuid
  );

CREATE POLICY "Service role full access" ON documents
  FOR ALL
  USING (auth.role() = 'service_role')
  WITH CHECK (auth.role() = 'service_role');

-- ===== FIX INVOICES TABLE =====

-- Drop ALL existing policies first
DROP POLICY IF EXISTS "Users can view own invoices" ON invoices;
DROP POLICY IF EXISTS "Users can insert own invoices" ON invoices;
DROP POLICY IF EXISTS "Users can update own invoices" ON invoices;
DROP POLICY IF EXISTS "Service role can access all invoices" ON invoices;
DROP POLICY IF EXISTS "Backend can create invoices" ON invoices;
DROP POLICY IF EXISTS "Public read access" ON invoices;
DROP POLICY IF EXISTS "Public insert access" ON invoices;
DROP POLICY IF EXISTS "Service role full access" ON invoices;

-- Ensure RLS is enabled
ALTER TABLE invoices ENABLE ROW LEVEL SECURITY;

-- Create new policies
CREATE POLICY "Public insert access" ON invoices
  FOR INSERT
  WITH CHECK (true);

CREATE POLICY "Public read access" ON invoices
  FOR SELECT
  USING (true);

CREATE POLICY "Users can update own invoices" ON invoices
  FOR UPDATE
  USING (
    EXISTS (
      SELECT 1 FROM documents 
      WHERE documents.id = invoices.document_id 
      AND documents.user_id::uuid = auth.uid()
    )
  );

CREATE POLICY "Service role full access" ON invoices
  FOR ALL
  USING (auth.role() = 'service_role')
  WITH CHECK (auth.role() = 'service_role');

-- ===== DONE! =====
-- You should see "Success. No rows returned"
-- Now go test the upload at trulyinvoice.xyz
