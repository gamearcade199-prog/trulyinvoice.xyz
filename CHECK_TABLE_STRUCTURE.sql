-- ============================================================================
-- STEP 1: CHECK ACTUAL SUBSCRIPTIONS TABLE STRUCTURE
-- Run this FIRST to see what columns actually exist
-- ============================================================================

-- Check all columns in subscriptions table
SELECT 
    column_name,
    data_type,
    is_nullable,
    column_default
FROM information_schema.columns
WHERE table_schema = 'public' 
  AND table_name = 'subscriptions'
ORDER BY ordinal_position;

-- ============================================================================
-- This will show you the EXACT columns that exist in your table
-- Copy the output and I'll create the correct SQL based on what actually exists
-- ============================================================================
