-- Add missing critical columns to invoices table
-- These columns are needed for complete OCR extraction coverage

ALTER TABLE invoices
ADD COLUMN IF NOT EXISTS customer_pan VARCHAR(10),
ADD COLUMN IF NOT EXISTS customer_email VARCHAR(255),
ADD COLUMN IF NOT EXISTS reference_number VARCHAR(100),
ADD COLUMN IF NOT EXISTS bank_account VARCHAR(50);

-- Add comments for documentation
COMMENT ON COLUMN invoices.customer_pan IS 'Customer Permanent Account Number (India Tax ID)';
COMMENT ON COLUMN invoices.customer_email IS 'Customer contact email address';
COMMENT ON COLUMN invoices.reference_number IS 'External reference or tracking number';
COMMENT ON COLUMN invoices.bank_account IS 'Vendor bank account number for payments';

-- Verify columns were added
SELECT column_name, data_type 
FROM information_schema.columns 
WHERE table_name = 'invoices' 
  AND column_name IN ('customer_pan', 'customer_email', 'reference_number', 'bank_account')
ORDER BY column_name;
