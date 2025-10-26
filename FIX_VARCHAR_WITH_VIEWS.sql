-- ============================================================================
-- FIX: "value too long for type character varying(10)" Error
-- This script safely alters column types by temporarily dropping views
-- ============================================================================

-- STEP 1: Drop all views that depend on the columns we need to alter
-- ============================================================================
DROP VIEW IF EXISTS gst_invoices CASCADE;
DROP VIEW IF EXISTS invoice_essentials CASCADE;
DROP VIEW IF EXISTS overdue_invoices CASCADE;
DROP VIEW IF EXISTS monthly_invoice_summary CASCADE;

-- STEP 2: Alter the column types that are too short
-- ============================================================================

-- Fix currency column (was VARCHAR(10), needs to fit "Indian Rupee")
ALTER TABLE invoices ALTER COLUMN currency TYPE VARCHAR(50);

-- Fix vendor_pan column (was VARCHAR(10), needs to fit formatted PANs)
DO $$ 
BEGIN
    IF EXISTS (
        SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'invoices' AND column_name = 'vendor_pan'
    ) THEN
        ALTER TABLE invoices ALTER COLUMN vendor_pan TYPE VARCHAR(50);
    END IF;
END $$;

-- Fix vendor_tan column
DO $$ 
BEGIN
    IF EXISTS (
        SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'invoices' AND column_name = 'vendor_tan'
    ) THEN
        ALTER TABLE invoices ALTER COLUMN vendor_tan TYPE VARCHAR(50);
    END IF;
END $$;

-- Fix vendor_pincode column
DO $$ 
BEGIN
    IF EXISTS (
        SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'invoices' AND column_name = 'vendor_pincode'
    ) THEN
        ALTER TABLE invoices ALTER COLUMN vendor_pincode TYPE VARCHAR(20);
    END IF;
END $$;

-- Fix place_of_supply column (was causing the view error)
DO $$ 
BEGIN
    IF EXISTS (
        SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'invoices' AND column_name = 'place_of_supply'
    ) THEN
        ALTER TABLE invoices ALTER COLUMN place_of_supply TYPE VARCHAR(100);
    END IF;
END $$;

-- Fix payment_status column
DO $$ 
BEGIN
    IF EXISTS (
        SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'invoices' AND column_name = 'payment_status'
    ) THEN
        ALTER TABLE invoices ALTER COLUMN payment_status TYPE VARCHAR(50);
    END IF;
END $$;

-- Fix payment_method column
DO $$ 
BEGIN
    IF EXISTS (
        SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'invoices' AND column_name = 'payment_method'
    ) THEN
        ALTER TABLE invoices ALTER COLUMN payment_method TYPE VARCHAR(50);
    END IF;
END $$;

-- STEP 3: Recreate all the views
-- ============================================================================

-- View 1: Essential Invoice Fields (for performance)
CREATE VIEW invoice_essentials AS
SELECT 
    id, user_id, document_id, category_id,
    vendor_name, invoice_number, invoice_date, due_date,
    subtotal, cgst, sgst, igst, total_amount,
    payment_status, payment_date,
    created_at, updated_at
FROM invoices;

-- View 2: GST Invoices Only
CREATE VIEW gst_invoices AS
SELECT 
    id, user_id, vendor_name, vendor_gstin,
    invoice_number, invoice_date, place_of_supply,
    hsn_code, sac_code, invoice_type,
    subtotal, cgst, sgst, igst, cess, total_gst,
    total_amount, reverse_charge, created_at
FROM invoices
WHERE vendor_gstin IS NOT NULL 
   OR cgst IS NOT NULL 
   OR sgst IS NOT NULL 
   OR igst IS NOT NULL;

-- View 3: Overdue Invoices
CREATE VIEW overdue_invoices AS
SELECT 
    id, user_id, vendor_name, invoice_number,
    invoice_date, due_date, total_amount,
    CURRENT_DATE - due_date AS days_overdue
FROM invoices
WHERE payment_status = 'unpaid'
  AND due_date < CURRENT_DATE;

-- View 4: Monthly Summary
CREATE VIEW monthly_invoice_summary AS
SELECT 
    DATE_TRUNC('month', invoice_date) AS month,
    user_id,
    COUNT(*) AS total_invoices,
    SUM(CASE WHEN payment_status = 'paid' THEN 1 ELSE 0 END) AS paid_count,
    SUM(CASE WHEN payment_status = 'unpaid' THEN 1 ELSE 0 END) AS unpaid_count,
    SUM(total_amount) AS total_amount,
    SUM(CASE WHEN payment_status = 'paid' THEN total_amount ELSE 0 END) AS paid_amount,
    SUM(CASE WHEN payment_status = 'unpaid' THEN total_amount ELSE 0 END) AS unpaid_amount
FROM invoices
GROUP BY DATE_TRUNC('month', invoice_date), user_id;

-- STEP 4: Verify the changes
-- ============================================================================
SELECT 
    column_name,
    data_type,
    character_maximum_length
FROM information_schema.columns
WHERE table_name = 'invoices'
    AND column_name IN (
        'currency', 'vendor_pan', 'vendor_tan', 'vendor_pincode', 
        'place_of_supply', 'payment_status', 'payment_method'
    )
ORDER BY column_name;

-- Success message
SELECT '✅ All column sizes fixed! Views recreated successfully! Upload your invoice now.' AS status;
