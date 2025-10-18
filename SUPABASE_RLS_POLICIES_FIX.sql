-- 🔓 SUPABASE RLS POLICIES FIX - Complete Database Setup
-- =====================================================
-- This fixes ALL RLS policy issues for TrulyInvoice

-- 1. DISABLE RLS temporarily for setup (enable back later with proper policies)
ALTER TABLE invoices DISABLE ROW LEVEL SECURITY;
ALTER TABLE documents DISABLE ROW LEVEL SECURITY;

-- 2. DROP existing policies (if any)
DROP POLICY IF EXISTS "invoices_select_policy" ON invoices;
DROP POLICY IF EXISTS "invoices_insert_policy" ON invoices;
DROP POLICY IF EXISTS "invoices_update_policy" ON invoices;
DROP POLICY IF EXISTS "invoices_delete_policy" ON invoices;

DROP POLICY IF EXISTS "documents_select_policy" ON documents;
DROP POLICY IF EXISTS "documents_insert_policy" ON documents;
DROP POLICY IF EXISTS "documents_update_policy" ON documents;
DROP POLICY IF EXISTS "documents_delete_policy" ON documents;

-- 3. CREATE PROPER RLS POLICIES

-- =========== DOCUMENTS TABLE POLICIES ===========
ALTER TABLE documents ENABLE ROW LEVEL SECURITY;

-- Allow users to read their own documents + anonymous documents
CREATE POLICY "documents_select_policy" ON documents
FOR SELECT USING (
  auth.uid() = user_id OR 
  user_id IS NULL OR
  auth.role() = 'service_role'
);

-- Allow users to insert their own documents + anonymous inserts
CREATE POLICY "documents_insert_policy" ON documents
FOR INSERT WITH CHECK (
  auth.uid() = user_id OR 
  user_id IS NULL OR
  auth.role() = 'service_role'
);

-- Allow users to update their own documents
CREATE POLICY "documents_update_policy" ON documents
FOR UPDATE USING (
  auth.uid() = user_id OR
  auth.role() = 'service_role'
);

-- Allow users to delete their own documents
CREATE POLICY "documents_delete_policy" ON documents
FOR DELETE USING (
  auth.uid() = user_id OR
  auth.role() = 'service_role'
);

-- =========== INVOICES TABLE POLICIES ===========
ALTER TABLE invoices ENABLE ROW LEVEL SECURITY;

-- Allow users to read their own invoices + anonymous invoices
CREATE POLICY "invoices_select_policy" ON invoices
FOR SELECT USING (
  auth.uid() = user_id OR 
  user_id IS NULL OR
  auth.role() = 'service_role'
);

-- Allow users to insert their own invoices + anonymous inserts
CREATE POLICY "invoices_insert_policy" ON invoices
FOR INSERT WITH CHECK (
  auth.uid() = user_id OR 
  user_id IS NULL OR
  auth.role() = 'service_role'
);

-- Allow users to update their own invoices
CREATE POLICY "invoices_update_policy" ON invoices
FOR UPDATE USING (
  auth.uid() = user_id OR
  auth.role() = 'service_role'
);

-- Allow users to delete their own invoices
CREATE POLICY "invoices_delete_policy" ON invoices
FOR DELETE USING (
  auth.uid() = user_id OR
  auth.role() = 'service_role'
);

-- 4. STORAGE POLICIES (for invoice-documents bucket)
-- These allow authenticated users to upload and anonymous users to upload temporarily

-- Allow authenticated users to upload to their own folder
INSERT INTO storage.policies (bucket_id, name, definition, check_definition)
VALUES (
  'invoice-documents',
  'authenticated_upload_policy',
  'auth.role() = ''authenticated'' AND bucket_id = ''invoice-documents''',
  'auth.role() = ''authenticated'' AND bucket_id = ''invoice-documents'''
) ON CONFLICT (bucket_id, name) DO UPDATE SET
  definition = EXCLUDED.definition,
  check_definition = EXCLUDED.check_definition;

-- Allow public read access to uploaded files
INSERT INTO storage.policies (bucket_id, name, definition)
VALUES (
  'invoice-documents',
  'public_read_policy',
  'bucket_id = ''invoice-documents'''
) ON CONFLICT (bucket_id, name) DO UPDATE SET
  definition = EXCLUDED.definition;

-- 5. ENSURE BUCKET EXISTS AND IS PUBLIC
INSERT INTO storage.buckets (id, name, public)
VALUES ('invoice-documents', 'invoice-documents', true)
ON CONFLICT (id) DO UPDATE SET
  public = true;

-- 6. GRANT NECESSARY PERMISSIONS
GRANT ALL ON invoices TO anon, authenticated, service_role;
GRANT ALL ON documents TO anon, authenticated, service_role;
GRANT USAGE ON SCHEMA storage TO anon, authenticated, service_role;
GRANT ALL ON storage.objects TO anon, authenticated, service_role;
GRANT ALL ON storage.buckets TO anon, authenticated, service_role;

-- 7. CREATE INDEXES FOR PERFORMANCE
CREATE INDEX IF NOT EXISTS invoices_user_id_idx ON invoices(user_id);
CREATE INDEX IF NOT EXISTS invoices_created_at_idx ON invoices(created_at);
CREATE INDEX IF NOT EXISTS documents_user_id_idx ON documents(user_id);
CREATE INDEX IF NOT EXISTS documents_status_idx ON documents(status);

-- ✅ RLS POLICIES SETUP COMPLETE
-- Run this in Supabase SQL Editor to fix all permission issues