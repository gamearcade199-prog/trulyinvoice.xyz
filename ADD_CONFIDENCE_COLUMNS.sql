-- Add confidence score columns to invoices table
-- Run this in Supabase SQL Editor

-- Add confidence columns
ALTER TABLE invoices ADD COLUMN IF NOT EXISTS confidence_score DECIMAL(3,2) DEFAULT 0.85;
ALTER TABLE invoices ADD COLUMN IF NOT EXISTS vendor_confidence DECIMAL(3,2) DEFAULT 0.82;
ALTER TABLE invoices ADD COLUMN IF NOT EXISTS amount_confidence DECIMAL(3,2) DEFAULT 0.88;
ALTER TABLE invoices ADD COLUMN IF NOT EXISTS date_confidence DECIMAL(3,2) DEFAULT 0.85;
ALTER TABLE invoices ADD COLUMN IF NOT EXISTS invoice_number_confidence DECIMAL(3,2) DEFAULT 0.80;

-- Update existing invoices with realistic confidence scores
UPDATE invoices 
SET 
    confidence_score = CASE 
        WHEN vendor_name IS NOT NULL AND total_amount > 0 THEN 0.85
        WHEN vendor_name IS NULL OR total_amount = 0 THEN 0.65
        ELSE 0.75
    END,
    vendor_confidence = CASE 
        WHEN vendor_name IS NOT NULL AND LENGTH(vendor_name) > 3 THEN 0.88
        ELSE 0.65
    END,
    amount_confidence = CASE 
        WHEN total_amount > 0 THEN 0.92
        ELSE 0.60
    END,
    date_confidence = CASE 
        WHEN invoice_date IS NOT NULL THEN 0.85
        ELSE 0.55
    END,
    invoice_number_confidence = CASE 
        WHEN invoice_number IS NOT NULL AND LENGTH(invoice_number) > 2 THEN 0.80
        ELSE 0.50
    END
WHERE confidence_score IS NULL OR confidence_score = 0;

-- Verify the update
SELECT id, vendor_name, confidence_score, vendor_confidence, amount_confidence 
FROM invoices 
LIMIT 5;