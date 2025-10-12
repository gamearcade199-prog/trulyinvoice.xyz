-- =====================================================
-- SAFE TAX AMOUNT COLUMN FIX (handles existing triggers)
-- =====================================================
-- This safely adds tax_amount column without conflicts

-- Add tax_amount column if it doesn't exist
ALTER TABLE invoices ADD COLUMN IF NOT EXISTS tax_amount DECIMAL(15,2);

-- Update existing records to calculate tax_amount
UPDATE invoices 
SET tax_amount = COALESCE(cgst, 0) + COALESCE(sgst, 0) + COALESCE(igst, 0) + COALESCE(cess, 0)
WHERE tax_amount IS NULL;

-- The trigger already exists, so let's just verify the schema
-- Check what columns we have
SELECT column_name, data_type, is_nullable
FROM information_schema.columns 
WHERE table_name = 'invoices' 
AND column_name IN ('tax_amount', 'cgst', 'sgst', 'igst', 'total_amount', 'vendor_name', 'invoice_number')
ORDER BY column_name;

-- Check if we have any data
SELECT COUNT(*) as total_invoices FROM invoices;

-- Show sample data if any exists
SELECT id, vendor_name, total_amount, tax_amount, created_at
FROM invoices 
ORDER BY created_at DESC 
LIMIT 5;