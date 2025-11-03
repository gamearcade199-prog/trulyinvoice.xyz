-- Add missing columns to invoices table
-- These columns are being extracted by the enhanced OCR but don't exist in the database

-- Add paid_amount column
ALTER TABLE invoices ADD COLUMN IF NOT EXISTS paid_amount DECIMAL(15, 2);

-- Add balance column
ALTER TABLE invoices ADD COLUMN IF NOT EXISTS balance DECIMAL(15, 2);

-- Add balance_due column  
ALTER TABLE invoices ADD COLUMN IF NOT EXISTS balance_due DECIMAL(15, 2);

-- Add invoice_amount_in_words column
ALTER TABLE invoices ADD COLUMN IF NOT EXISTS invoice_amount_in_words TEXT;

-- Add irn_number column (Invoice Reference Number for GST)
ALTER TABLE invoices ADD COLUMN IF NOT EXISTS irn_number VARCHAR(100);

-- Add round_off column
ALTER TABLE invoices ADD COLUMN IF NOT EXISTS round_off DECIMAL(10, 2);

-- Add eway_bill column
ALTER TABLE invoices ADD COLUMN IF NOT EXISTS eway_bill VARCHAR(100);

-- Add comments for documentation
COMMENT ON COLUMN invoices.paid_amount IS 'Amount already paid towards this invoice';
COMMENT ON COLUMN invoices.balance IS 'Balance/remaining amount to be paid';
COMMENT ON COLUMN invoices.balance_due IS 'Same as balance - amount due/outstanding';
COMMENT ON COLUMN invoices.invoice_amount_in_words IS 'Total amount written in words (e.g., Sixty Six Thousand Eight Hundred Fifty Rupees Only)';
COMMENT ON COLUMN invoices.irn_number IS 'Invoice Reference Number (IRN) - unique GST system identifier';
COMMENT ON COLUMN invoices.round_off IS 'Round off adjustment amount (+ or -)';
COMMENT ON COLUMN invoices.eway_bill IS 'E-way bill number for goods transportation (alternative field name)';

-- Create indexes for frequently queried columns
CREATE INDEX IF NOT EXISTS idx_invoices_irn_number ON invoices(irn_number);
CREATE INDEX IF NOT EXISTS idx_invoices_balance_due ON invoices(balance_due) WHERE balance_due > 0;
