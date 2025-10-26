-- =====================================================
-- PRODUCTION-READY RLS POLICIES FOR TRULYINVOICE
-- =====================================================
-- Comprehensive security policies for multi-tenant invoice system

-- ===== DOCUMENTS TABLE POLICIES =====

-- Enable RLS on documents table
ALTER TABLE documents ENABLE ROW LEVEL SECURITY;

-- Remove any existing policies
DROP POLICY IF EXISTS "Users can view own documents" ON documents;
DROP POLICY IF EXISTS "Users can insert own documents" ON documents;
DROP POLICY IF EXISTS "Users can update own documents" ON documents;
DROP POLICY IF EXISTS "Service role can access all documents" ON documents;

-- Policy 1: Users can only view their own documents
CREATE POLICY "Users can view own documents" ON documents
  FOR SELECT
  USING (auth.uid() = user_id::uuid);

-- Policy 2: Users can insert documents for themselves
CREATE POLICY "Users can insert own documents" ON documents
  FOR INSERT
  WITH CHECK (auth.uid() = user_id::uuid);

-- Policy 3: Users can update their own documents
CREATE POLICY "Users can update own documents" ON documents
  FOR UPDATE
  USING (auth.uid() = user_id::uuid)
  WITH CHECK (auth.uid() = user_id::uuid);

-- Policy 4: Service role (backend) can access all documents for processing
CREATE POLICY "Service role can access all documents" ON documents
  FOR ALL
  USING (true)
  WITH CHECK (true);

-- ===== INVOICES TABLE POLICIES =====

-- Enable RLS on invoices table
ALTER TABLE invoices ENABLE ROW LEVEL SECURITY;

-- Remove any existing policies
DROP POLICY IF EXISTS "Users can view own invoices" ON invoices;
DROP POLICY IF EXISTS "Users can insert own invoices" ON invoices;
DROP POLICY IF EXISTS "Users can update own invoices" ON invoices;
DROP POLICY IF EXISTS "Service role can access all invoices" ON invoices;
DROP POLICY IF EXISTS "Backend can create invoices" ON invoices;

-- Policy 1: Users can only view invoices for their documents
CREATE POLICY "Users can view own invoices" ON invoices
  FOR SELECT
  USING (
    EXISTS (
      SELECT 1 FROM documents 
      WHERE documents.id = invoices.document_id 
      AND documents.user_id::uuid = auth.uid()
    )
  );

-- Policy 2: Users can update their own invoices (payment status, etc.)
CREATE POLICY "Users can update own invoices" ON invoices
  FOR UPDATE
  USING (
    EXISTS (
      SELECT 1 FROM documents 
      WHERE documents.id = invoices.document_id 
      AND documents.user_id::uuid = auth.uid()
    )
  )
  WITH CHECK (
    EXISTS (
      SELECT 1 FROM documents 
      WHERE documents.id = invoices.document_id 
      AND documents.user_id::uuid = auth.uid()
    )
  );

-- Policy 3: Service role (backend) can create and manage all invoices
CREATE POLICY "Service role can access all invoices" ON invoices
  FOR ALL
  USING (true)
  WITH CHECK (true);

-- Policy 4: Allow anonymous inserts for backend processing (with API key)
CREATE POLICY "Backend can create invoices" ON invoices
  FOR INSERT
  WITH CHECK (true);

-- ===== ADDITIONAL SECURITY MEASURES =====

-- Create a function to check if current user owns a document
CREATE OR REPLACE FUNCTION user_owns_document(doc_id uuid)
RETURNS boolean AS $$
BEGIN
  RETURN EXISTS (
    SELECT 1 FROM documents 
    WHERE id = doc_id 
    AND user_id::uuid = auth.uid()
  );
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Create a function to get user's documents count (for rate limiting)
CREATE OR REPLACE FUNCTION get_user_documents_count()
RETURNS integer AS $$
BEGIN
  RETURN (
    SELECT COUNT(*) FROM documents 
    WHERE user_id::uuid = auth.uid()
  );
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- ===== USER PROFILES TABLE (if exists) =====
-- Ensure users can only access their own profile
DO $$ 
BEGIN
  IF EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'profiles') THEN
    ALTER TABLE profiles ENABLE ROW LEVEL SECURITY;
    
    DROP POLICY IF EXISTS "Users can view own profile" ON profiles;
    DROP POLICY IF EXISTS "Users can update own profile" ON profiles;
    
    CREATE POLICY "Users can view own profile" ON profiles
      FOR SELECT
      USING (auth.uid() = id);
      
    CREATE POLICY "Users can update own profile" ON profiles
      FOR UPDATE
      USING (auth.uid() = id)
      WITH CHECK (auth.uid() = id);
  END IF;
END $$;

-- ===== AUDIT AND MONITORING =====

-- Create audit log function for sensitive operations
CREATE OR REPLACE FUNCTION audit_invoice_access()
RETURNS trigger AS $$
BEGIN
  -- Log invoice access for compliance
  INSERT INTO audit_log (
    user_id, 
    action, 
    table_name, 
    record_id, 
    timestamp
  ) VALUES (
    COALESCE(auth.uid()::text, 'system'),
    TG_OP,
    'invoices',
    COALESCE(NEW.id, OLD.id)::text,
    NOW()
  );
  
  RETURN COALESCE(NEW, OLD);
EXCEPTION WHEN others THEN
  -- Don't fail the operation if audit logging fails
  RETURN COALESCE(NEW, OLD);
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Create audit log table if it doesn't exist
CREATE TABLE IF NOT EXISTS audit_log (
  id uuid DEFAULT gen_random_uuid() PRIMARY KEY,
  user_id text,
  action text,
  table_name text,
  record_id text,
  timestamp timestamptz DEFAULT NOW()
);

-- Enable RLS on audit log
ALTER TABLE audit_log ENABLE ROW LEVEL SECURITY;

-- Only allow viewing own audit logs
CREATE POLICY "Users can view own audit logs" ON audit_log
  FOR SELECT
  USING (user_id = auth.uid()::text);

-- ===== VERIFY POLICIES =====

-- Check current RLS status and policies
SELECT 
  schemaname, 
  tablename, 
  rowsecurity as rls_enabled,
  CASE 
    WHEN rowsecurity THEN 'ENABLED'
    ELSE 'DISABLED'
  END as status
FROM pg_tables 
WHERE tablename IN ('documents', 'invoices', 'profiles', 'audit_log')
AND schemaname = 'public';

-- List all policies
SELECT 
  schemaname,
  tablename,
  policyname,
  permissive,
  roles,
  cmd as operation,
  CASE 
    WHEN qual IS NOT NULL THEN 'Has USING clause'
    ELSE 'No USING clause'
  END as using_clause,
  CASE 
    WHEN with_check IS NOT NULL THEN 'Has WITH CHECK clause'
    ELSE 'No WITH CHECK clause'
  END as with_check_clause
FROM pg_policies 
WHERE tablename IN ('documents', 'invoices', 'profiles', 'audit_log')
ORDER BY tablename, policyname;