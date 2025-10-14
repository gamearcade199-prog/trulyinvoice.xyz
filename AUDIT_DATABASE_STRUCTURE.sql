-- ============================================================================
-- DATABASE STRUCTURE AUDIT SCRIPT
-- Run this to see your current database schema and identify issues
-- ============================================================================

-- 1. Check all invoices table columns and their sizes
-- ============================================================================
SELECT 
    column_name,
    data_type,
    CASE 
        WHEN data_type = 'character varying' THEN character_maximum_length
        WHEN data_type = 'numeric' THEN numeric_precision
        ELSE NULL
    END as max_length,
    is_nullable,
    column_default
FROM information_schema.columns
WHERE table_name = 'invoices'
ORDER BY ordinal_position;

-- 2. Find columns that might be too short (VARCHAR <= 10)
-- ============================================================================
SELECT 
    '⚠️ POTENTIAL ISSUE' as warning,
    column_name,
    data_type,
    character_maximum_length as current_size,
    CASE column_name
        WHEN 'currency' THEN 'Should be VARCHAR(50) to fit currency names'
        WHEN 'vendor_pan' THEN 'Should be VARCHAR(50) for formatted PANs'
        WHEN 'vendor_tan' THEN 'Should be VARCHAR(50) for formatted TANs'
        WHEN 'vendor_pincode' THEN 'Should be VARCHAR(20) for Indian pincodes'
        WHEN 'place_of_supply' THEN 'Should be VARCHAR(100) for state names'
        WHEN 'payment_status' THEN 'Should be VARCHAR(50) for status values'
        WHEN 'payment_method' THEN 'Should be VARCHAR(50) for method names'
        ELSE 'Check if this needs to be longer'
    END as recommendation
FROM information_schema.columns
WHERE table_name = 'invoices'
    AND data_type = 'character varying'
    AND character_maximum_length <= 10
ORDER BY character_maximum_length, column_name;

-- 3. Check all views that exist
-- ============================================================================
SELECT 
    table_name as view_name,
    view_definition
FROM information_schema.views
WHERE table_schema = 'public'
ORDER BY table_name;

-- 4. Check all indexes on invoices table
-- ============================================================================
SELECT
    indexname,
    indexdef
FROM pg_indexes
WHERE tablename = 'invoices'
ORDER BY indexname;

-- 5. Check foreign key constraints
-- ============================================================================
SELECT
    conname as constraint_name,
    contype as constraint_type,
    pg_get_constraintdef(c.oid) as definition
FROM pg_constraint c
JOIN pg_namespace n ON n.oid = c.connamespace
WHERE conrelid = 'invoices'::regclass
ORDER BY conname;

-- 6. Check table storage size
-- ============================================================================
SELECT
    pg_size_pretty(pg_total_relation_size('invoices')) as total_size,
    pg_size_pretty(pg_relation_size('invoices')) as table_size,
    pg_size_pretty(pg_total_relation_size('invoices') - pg_relation_size('invoices')) as indexes_size;

-- 7. Count records in invoices table
-- ============================================================================
SELECT 
    COUNT(*) as total_invoices,
    COUNT(CASE WHEN payment_status = 'paid' THEN 1 END) as paid_invoices,
    COUNT(CASE WHEN payment_status = 'unpaid' THEN 1 END) as unpaid_invoices,
    COUNT(CASE WHEN vendor_gstin IS NOT NULL THEN 1 END) as gst_invoices
FROM invoices;

-- 8. Check if required columns exist
-- ============================================================================
SELECT 
    CASE 
        WHEN EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name = 'invoices' AND column_name = 'currency') 
        THEN '✅ currency exists'
        ELSE '❌ currency missing'
    END as currency_check,
    CASE 
        WHEN EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name = 'invoices' AND column_name = 'place_of_supply') 
        THEN '✅ place_of_supply exists'
        ELSE '❌ place_of_supply missing'
    END as place_of_supply_check,
    CASE 
        WHEN EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name = 'invoices' AND column_name = 'vendor_gstin') 
        THEN '✅ vendor_gstin exists'
        ELSE '❌ vendor_gstin missing'
    END as vendor_gstin_check,
    CASE 
        WHEN EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name = 'invoices' AND column_name = 'line_items') 
        THEN '✅ line_items exists'
        ELSE '❌ line_items missing'
    END as line_items_check;

-- 9. Sample some data to see what's being stored
-- ============================================================================
SELECT 
    invoice_number,
    vendor_name,
    LENGTH(COALESCE(currency, '')) as currency_length,
    LENGTH(COALESCE(place_of_supply, '')) as place_of_supply_length,
    LENGTH(COALESCE(payment_status, '')) as payment_status_length,
    LENGTH(COALESCE(payment_method, '')) as payment_method_length,
    total_amount,
    created_at
FROM invoices
ORDER BY created_at DESC
LIMIT 5;

-- 10. Final recommendation
-- ============================================================================
SELECT '
📊 DATABASE AUDIT COMPLETE!

Check the results above to:
1. See which columns are too short (VARCHAR <= 10)
2. Identify which views exist that might block column changes
3. Verify all required columns exist
4. See sample data and field lengths

Next steps:
- If you see columns with character_maximum_length <= 10, run FIX_VARCHAR_WITH_VIEWS.sql
- Make sure all views are listed so we can recreate them after the fix
' as next_steps;
