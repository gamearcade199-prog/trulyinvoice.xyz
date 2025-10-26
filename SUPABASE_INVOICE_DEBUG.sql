-- SUPABASE INVOICE DEBUGGING QUERIES
-- Run these in your Supabase SQL Editor to diagnose the issue

-- 0. FIRST: Check what columns actually exist in invoices table
SELECT column_name, data_type 
FROM information_schema.columns 
WHERE table_name = 'invoices' 
ORDER BY ordinal_position;

-- 1. Check if invoices table exists and has data
SELECT 
    COUNT(*) as total_invoices,
    COUNT(CASE WHEN user_id IS NOT NULL THEN 1 END) as user_invoices,
    COUNT(CASE WHEN user_id IS NULL THEN 1 END) as anonymous_invoices
FROM invoices;

-- 2. Check invoice ID formats and sample data
SELECT 
    id,
    file_name,
    status,
    user_id,
    created_at,
    LENGTH(id::text) as id_length,
    CASE 
        WHEN id::text ~ '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$' 
        THEN 'Valid UUID' 
        ELSE 'Invalid UUID' 
    END as id_format
FROM invoices 
ORDER BY created_at DESC 
LIMIT 10;

-- 3. Check specific invoice IDs from your 404 errors
-- Replace these with actual IDs from your console errors
SELECT * FROM invoices 
WHERE id IN (
    'f4f79498-cd99-4567-8901-074b15abcdef',  -- Replace with actual ID
    '2ee13a99-0766-4567-8901-fcba1b2abcdef', -- Replace with actual ID
    '5dc616f8-7f99-4567-8901-9c68cf2abcdef'  -- Replace with actual ID
);

-- 4. Check if RLS policies are blocking access
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

-- 5. Check table structure
SELECT 
    column_name,
    data_type,
    is_nullable,
    column_default
FROM information_schema.columns 
WHERE table_name = 'invoices' 
ORDER BY ordinal_position;

-- 6. Check recent invoices with all details
SELECT 
    i.id,
    i.file_name,
    i.status,
    i.user_id,
    i.created_at,
    i.extracted_data IS NOT NULL as has_extracted_data,
    d.file_name as document_name,
    d.storage_path
FROM invoices i
LEFT JOIN documents d ON i.document_id = d.id
ORDER BY i.created_at DESC
LIMIT 5;

-- 7. Test if anonymous access works (this should work if RLS is properly configured)
SELECT id, file_name, status FROM invoices WHERE user_id IS NULL LIMIT 3;

-- 8. Check if there are any invoices that might cause routing issues
SELECT 
    id,
    file_name,
    CASE 
        WHEN id IS NULL THEN 'NULL ID - PROBLEM!'
        WHEN id::text = '' THEN 'EMPTY ID - PROBLEM!'
        WHEN id::text LIKE '%/%' THEN 'SLASH IN ID - PROBLEM!'
        WHEN id::text LIKE '% %' THEN 'SPACE IN ID - PROBLEM!'
        ELSE 'ID looks OK'
    END as id_check
FROM invoices
WHERE id IS NULL 
   OR id::text = '' 
   OR id::text LIKE '%/%' 
   OR id::text LIKE '% %'
LIMIT 10;