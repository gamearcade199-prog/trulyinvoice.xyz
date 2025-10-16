-- QUICK DIAGNOSIS QUERIES - RUN THESE IN SUPABASE SQL EDITOR

-- 1. Check actual table structure for INVOICES table
SELECT column_name, data_type 
FROM information_schema.columns 
WHERE table_name = 'invoices' 
ORDER BY ordinal_position;

-- 1b. If above returns nothing, check if table exists at all
SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';

-- 2. See actual invoice IDs and basic data (JUST ID and status first)
SELECT id, status, user_id, created_at::date as date_created
FROM invoices 
ORDER BY created_at DESC 
LIMIT 5;

-- 3. Check if there are any RLS policies blocking access
SELECT policyname, cmd, qual 
FROM pg_policies 
WHERE tablename = 'invoices';

-- 4. Test a simple count query
SELECT COUNT(*) as total_invoices FROM invoices;