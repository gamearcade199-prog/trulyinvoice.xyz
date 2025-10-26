-- =====================================================
-- 🔍 COMPLETE DIAGNOSTIC QUERY FOR 404 EYE ICON ISSUE
-- =====================================================
-- Run this in Supabase SQL Editor to diagnose the 404 problem
-- Copy the ENTIRE script and paste in Supabase SQL Editor
-- =====================================================

-- SECTION 1: CHECK TABLE STRUCTURE
-- =====================================================
SELECT 
  'INVOICES TABLE STRUCTURE' as diagnostic_section,
  column_name,
  data_type,
  is_nullable,
  column_default
FROM information_schema.columns
WHERE table_name = 'invoices'
ORDER BY ordinal_position;

-- SECTION 2: CHECK DOCUMENTS TABLE STRUCTURE
-- =====================================================
SELECT 
  'DOCUMENTS TABLE STRUCTURE' as diagnostic_section,
  column_name,
  data_type,
  is_nullable,
  column_default
FROM information_schema.columns
WHERE table_name = 'documents'
ORDER BY ordinal_position;

-- SECTION 3: COUNT TOTAL INVOICES
-- =====================================================
SELECT 
  'TOTAL INVOICES COUNT' as diagnostic,
  COUNT(*) as total_invoices,
  COUNT(DISTINCT user_id) as unique_users,
  COUNT(DISTINCT document_id) as invoices_with_documents
FROM invoices;

-- SECTION 4: SHOW ALL INVOICES WITH KEY DETAILS
-- =====================================================
SELECT 
  'ALL INVOICES IN DATABASE' as diagnostic,
  id as invoice_id,
  user_id,
  document_id,
  vendor_name,
  invoice_number,
  total_amount,
  payment_status,
  created_at,
  LENGTH(id::text) as id_length
FROM invoices
ORDER BY created_at DESC
LIMIT 100;

-- SECTION 5: CHECK INVOICES WITHOUT DOCUMENTS
-- =====================================================
SELECT 
  'INVOICES WITHOUT DOCUMENTS' as diagnostic,
  COUNT(*) as orphaned_invoices
FROM invoices
WHERE document_id IS NULL;

-- SECTION 6: SHOW ORPHANED INVOICES DETAILS
-- =====================================================
SELECT 
  'ORPHANED INVOICES (NO LINKED DOCUMENTS)' as diagnostic,
  id as invoice_id,
  vendor_name,
  invoice_number,
  user_id,
  created_at
FROM invoices
WHERE document_id IS NULL
LIMIT 50;

-- SECTION 7: CHECK DOCUMENTS WITHOUT INVOICES
-- =====================================================
SELECT 
  'DOCUMENTS IN DATABASE' as diagnostic,
  COUNT(*) as total_documents,
  COUNT(DISTINCT user_id) as docs_with_users
FROM documents;

-- SECTION 8: SHOW ALL DOCUMENTS
-- =====================================================
SELECT 
  'ALL DOCUMENTS IN DATABASE' as diagnostic,
  id as document_id,
  file_name,
  user_id,
  storage_path,
  status,
  created_at
FROM documents
ORDER BY created_at DESC
LIMIT 100;

-- SECTION 9: CHECK USERS IN SYSTEM
-- =====================================================
SELECT 
  'TOTAL USERS' as diagnostic,
  COUNT(*) as total_users,
  COUNT(DISTINCT id) as unique_user_ids
FROM users;

-- SECTION 10: SHOW ALL USERS AND THEIR INVOICES
-- =====================================================
SELECT 
  'USERS WITH INVOICE COUNTS' as diagnostic,
  u.id as user_id,
  u.email,
  COUNT(i.id) as invoice_count,
  MAX(i.created_at) as last_invoice_date
FROM users u
LEFT JOIN invoices i ON u.id = i.user_id
GROUP BY u.id, u.email
ORDER BY COUNT(i.id) DESC;

-- SECTION 11: CHECK FOR DATA TYPE ISSUES
-- =====================================================
SELECT 
  'INVOICES WITH DATA ISSUES' as diagnostic,
  id,
  vendor_name,
  CASE 
    WHEN id IS NULL THEN 'NULL ID'
    WHEN vendor_name IS NULL OR vendor_name = '' THEN 'MISSING VENDOR'
    WHEN invoice_number IS NULL OR invoice_number = '' THEN 'MISSING INVOICE #'
    WHEN total_amount IS NULL THEN 'MISSING TOTAL'
    WHEN payment_status IS NULL OR payment_status = '' THEN 'MISSING STATUS'
    ELSE 'OK'
  END as data_status
FROM invoices
WHERE id IS NULL 
   OR vendor_name IS NULL 
   OR invoice_number IS NULL 
   OR total_amount IS NULL
   OR payment_status IS NULL;

-- SECTION 12: TEST QUERY SIMILAR TO BACKEND
-- =====================================================
-- This is what your backend is running
-- Replace UUID below with an invoice ID from the list above
SELECT 
  'BACKEND QUERY TEST' as diagnostic,
  *
FROM invoices
WHERE id = 'REPLACE_WITH_ACTUAL_UUID_HERE'
LIMIT 1;

-- SECTION 13: CHECK RECENT INVOICES (LAST 24 HOURS)
-- =====================================================
SELECT 
  'RECENT INVOICES (LAST 24 HOURS)' as diagnostic,
  id,
  vendor_name,
  invoice_number,
  total_amount,
  user_id,
  created_at
FROM invoices
WHERE created_at > NOW() - INTERVAL '24 hours'
ORDER BY created_at DESC;

-- SECTION 14: CHECK FOR DUPLICATE IDS
-- =====================================================
SELECT 
  'DUPLICATE INVOICE IDS' as diagnostic,
  id,
  COUNT(*) as duplicate_count
FROM invoices
GROUP BY id
HAVING COUNT(*) > 1;

-- SECTION 15: SHOW FULL INVOICE DETAILS (FIRST INVOICE)
-- =====================================================
SELECT 
  'FIRST INVOICE FULL DETAILS' as diagnostic,
  i.*,
  d.file_name,
  d.file_url,
  d.storage_path,
  u.email as user_email
FROM invoices i
LEFT JOIN documents d ON i.document_id = d.id
LEFT JOIN users u ON i.user_id = u.id
ORDER BY i.created_at DESC
LIMIT 1;

-- SECTION 16: CHECK RLS POLICIES
-- =====================================================
SELECT 
  'RLS POLICIES ON INVOICES TABLE' as diagnostic,
  policyname,
  permissive,
  roles,
  qual as policy_condition,
  with_check
FROM pg_policies
WHERE tablename = 'invoices';

-- SECTION 17: DATABASE SIZE INFO
-- =====================================================
SELECT 
  'DATABASE SIZE INFORMATION' as diagnostic,
  schemaname,
  tablename,
  pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) as table_size
FROM pg_tables
WHERE schemaname NOT IN ('pg_catalog', 'information_schema')
  AND tablename IN ('invoices', 'documents', 'users')
ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC;

-- SECTION 18: INVOICES GROUPED BY STATUS
-- =====================================================
SELECT 
  'INVOICES BY PAYMENT STATUS' as diagnostic,
  payment_status,
  COUNT(*) as count
FROM invoices
GROUP BY payment_status
ORDER BY count DESC;

-- SECTION 19: CHECK FOR NULL USER_ID (ANONYMOUS UPLOADS)
-- =====================================================
SELECT 
  'INVOICES WITH NULL USER_ID (ANONYMOUS)' as diagnostic,
  COUNT(*) as anonymous_invoices
FROM invoices
WHERE user_id IS NULL;

-- SECTION 20: SHOW ALL DATA - COMPLETE DUMP
-- =====================================================
SELECT 
  'COMPLETE DATA DUMP' as diagnostic,
  'INVOICES' as table_name,
  jsonb_agg(to_jsonb(row)) as data
FROM (
  SELECT 
    i.id,
    i.user_id,
    i.document_id,
    i.vendor_name,
    i.invoice_number,
    i.total_amount,
    i.payment_status,
    i.created_at,
    d.file_name,
    d.file_url
  FROM invoices i
  LEFT JOIN documents d ON i.document_id = d.id
  LIMIT 50
) as row;
