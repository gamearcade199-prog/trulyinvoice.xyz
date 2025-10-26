-- =====================================================
-- CRITICAL FIX: Add tax_amount column to invoices table
-- =====================================================
-- This resolves the mismatch between frontend and database

-- Add tax_amount column (what frontend expects)
ALTER TABLE invoices ADD COLUMN IF NOT EXISTS tax_amount DECIMAL(15,2);

-- Create a computed column that sums up all GST components
-- This ensures compatibility with both frontend and backend
UPDATE invoices 
SET tax_amount = COALESCE(cgst, 0) + COALESCE(sgst, 0) + COALESCE(igst, 0) + COALESCE(cess, 0)
WHERE tax_amount IS NULL;

-- Add a trigger to automatically calculate tax_amount when GST fields change
CREATE OR REPLACE FUNCTION calculate_tax_amount()
RETURNS TRIGGER AS $$
BEGIN
    NEW.tax_amount = COALESCE(NEW.cgst, 0) + COALESCE(NEW.sgst, 0) + COALESCE(NEW.igst, 0) + COALESCE(NEW.cess, 0);
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Apply trigger
DROP TRIGGER IF EXISTS trigger_calculate_tax_amount ON invoices;
CREATE TRIGGER trigger_calculate_tax_amount
    BEFORE INSERT OR UPDATE ON invoices
    FOR EACH ROW
    EXECUTE FUNCTION calculate_tax_amount();

-- Verify the fix
SELECT column_name, data_type 
FROM information_schema.columns 
WHERE table_name = 'invoices' 
AND column_name IN ('tax_amount', 'cgst', 'sgst', 'igst', 'total_amount')
ORDER BY column_name;