-- 🔍 SUPABASE RLS DIAGNOSIS QUERIES
-- Run these queries ONE BY ONE in Supabase SQL Editor to identify the exact problem

-- 1. CHECK RLS STATUS ON ALL TABLES
SELECT 
    schemaname,
    tablename,
    rowsecurity as rls_enabled
FROM pg_tables 
WHERE schemaname = 'public'
ORDER BY tablename;

-- 2. CHECK ALL RLS POLICIES (THIS IS THE MAIN CULPRIT)
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
WHERE schemaname = 'public'
ORDER BY tablename, policyname;

-- 3. CHECK CURRENT USER AND ROLE
SELECT 
    current_user as current_user,
    session_user as session_user,
    current_role as current_role;

-- 4. CHECK AUTH.USERS TABLE ACCESS
SELECT COUNT(*) as user_count FROM auth.users;

-- 5. TEST INVOICE TABLE ACCESS
SELECT COUNT(*) as invoice_count FROM invoices LIMIT 1;

-- 6. CHECK TABLE STRUCTURE
SELECT 
    table_name,
    column_name,
    data_type,
    is_nullable,
    column_default
FROM information_schema.columns 
WHERE table_schema = 'public' 
    AND table_name IN ('invoices', 'invoice_items', 'profiles')
ORDER BY table_name, ordinal_position;

-- 7. CHECK FOR FOREIGN KEY CONSTRAINTS
SELECT
    tc.constraint_name,
    tc.table_name,
    kcu.column_name,
    ccu.table_name AS foreign_table_name,
    ccu.column_name AS foreign_column_name
FROM information_schema.table_constraints AS tc
JOIN information_schema.key_column_usage AS kcu
    ON tc.constraint_name = kcu.constraint_name
    AND tc.table_schema = kcu.table_schema
JOIN information_schema.constraint_column_usage AS ccu
    ON ccu.constraint_name = tc.constraint_name
    AND ccu.table_schema = tc.table_schema
WHERE tc.constraint_type = 'FOREIGN KEY'
    AND tc.table_schema = 'public'
    AND tc.table_name IN ('invoices', 'invoice_items');