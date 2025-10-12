-- =====================================================
-- FLEXIBLE INVOICE SCHEMA FOR ALL INDIAN INVOICES
-- Optimized for various invoice formats across India
-- =====================================================
-- Run this in Supabase SQL Editor
-- =====================================================

-- =====================================================
-- UPDATED INVOICES TABLE (Flexible Schema)
-- =====================================================

-- First, check if invoices table exists and add missing columns
DO $$ 
BEGIN
    -- Add vendor_gstin if not exists
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'invoices' AND column_name = 'vendor_gstin'
    ) THEN
        ALTER TABLE invoices ADD COLUMN vendor_gstin VARCHAR(15);
    END IF;

    -- Add vendor_pan if not exists
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'invoices' AND column_name = 'vendor_pan'
    ) THEN
        ALTER TABLE invoices ADD COLUMN vendor_pan VARCHAR(10);
    END IF;

    -- Add vendor_email if not exists
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'invoices' AND column_name = 'vendor_email'
    ) THEN
        ALTER TABLE invoices ADD COLUMN vendor_email VARCHAR(255);
    END IF;

    -- Add vendor_phone if not exists
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'invoices' AND column_name = 'vendor_phone'
    ) THEN
        ALTER TABLE invoices ADD COLUMN vendor_phone VARCHAR(20);
    END IF;

    -- Add vendor_address if not exists
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'invoices' AND column_name = 'vendor_address'
    ) THEN
        ALTER TABLE invoices ADD COLUMN vendor_address TEXT;
    END IF;

    -- Add po_number if not exists
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'invoices' AND column_name = 'po_number'
    ) THEN
        ALTER TABLE invoices ADD COLUMN po_number VARCHAR(100);
    END IF;

    -- Add cess if not exists (for special taxes)
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'invoices' AND column_name = 'cess'
    ) THEN
        ALTER TABLE invoices ADD COLUMN cess DECIMAL(15,2) DEFAULT 0;
    END IF;

    -- Add discount if not exists
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'invoices' AND column_name = 'discount'
    ) THEN
        ALTER TABLE invoices ADD COLUMN discount DECIMAL(15,2) DEFAULT 0;
    END IF;

    -- Add payment_terms if not exists
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'invoices' AND column_name = 'payment_terms'
    ) THEN
        ALTER TABLE invoices ADD COLUMN payment_terms VARCHAR(255);
    END IF;

    -- Add payment_method if not exists
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'invoices' AND column_name = 'payment_method'
    ) THEN
        ALTER TABLE invoices ADD COLUMN payment_method VARCHAR(100);
    END IF;

    -- Add line_items JSONB if not exists
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'invoices' AND column_name = 'line_items'
    ) THEN
        ALTER TABLE invoices ADD COLUMN line_items JSONB DEFAULT '[]'::jsonb;
    END IF;

    -- Add raw_extracted_data JSONB if not exists (for debugging)
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'invoices' AND column_name = 'raw_extracted_data'
    ) THEN
        ALTER TABLE invoices ADD COLUMN raw_extracted_data JSONB;
    END IF;

    -- Add currency if not exists
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'invoices' AND column_name = 'currency'
    ) THEN
        ALTER TABLE invoices ADD COLUMN currency VARCHAR(10) DEFAULT 'INR';
    END IF;

    -- Add notes if not exists
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'invoices' AND column_name = 'notes'
    ) THEN
        ALTER TABLE invoices ADD COLUMN notes TEXT;
    END IF;

    -- Add tags if not exists
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'invoices' AND column_name = 'tags'
    ) THEN
        ALTER TABLE invoices ADD COLUMN tags TEXT[];
    END IF;

    -- Add hsn_code if not exists (for GST)
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'invoices' AND column_name = 'hsn_code'
    ) THEN
        ALTER TABLE invoices ADD COLUMN hsn_code VARCHAR(20);
    END IF;

    -- Add sac_code if not exists (for services)
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'invoices' AND column_name = 'sac_code'
    ) THEN
        ALTER TABLE invoices ADD COLUMN sac_code VARCHAR(20);
    END IF;

    -- Add place_of_supply if not exists (for GST)
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'invoices' AND column_name = 'place_of_supply'
    ) THEN
        ALTER TABLE invoices ADD COLUMN place_of_supply VARCHAR(100);
    END IF;

    -- Add reverse_charge if not exists (GST reverse charge mechanism)
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'invoices' AND column_name = 'reverse_charge'
    ) THEN
        ALTER TABLE invoices ADD COLUMN reverse_charge BOOLEAN DEFAULT false;
    END IF;

    -- Add shipping_charges if not exists
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'invoices' AND column_name = 'shipping_charges'
    ) THEN
        ALTER TABLE invoices ADD COLUMN shipping_charges DECIMAL(15,2) DEFAULT 0;
    END IF;

    -- Add tds_amount if not exists (Tax Deducted at Source)
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'invoices' AND column_name = 'tds_amount'
    ) THEN
        ALTER TABLE invoices ADD COLUMN tds_amount DECIMAL(15,2) DEFAULT 0;
    END IF;

    -- Add roundoff if not exists
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'invoices' AND column_name = 'roundoff'
    ) THEN
        ALTER TABLE invoices ADD COLUMN roundoff DECIMAL(15,2) DEFAULT 0;
    END IF;

END $$;

-- =====================================================
-- CREATE INDEXES FOR BETTER PERFORMANCE
-- =====================================================

CREATE INDEX IF NOT EXISTS idx_invoices_vendor_gstin ON invoices(vendor_gstin);
CREATE INDEX IF NOT EXISTS idx_invoices_place_of_supply ON invoices(place_of_supply);
CREATE INDEX IF NOT EXISTS idx_invoices_hsn_code ON invoices(hsn_code);
CREATE INDEX IF NOT EXISTS idx_invoices_tags ON invoices USING GIN (tags);
CREATE INDEX IF NOT EXISTS idx_invoices_raw_data ON invoices USING GIN (raw_extracted_data);

-- =====================================================
-- UPDATE PAYMENT STATUS CHECK CONSTRAINT
-- =====================================================

-- Drop old constraint if exists
ALTER TABLE invoices DROP CONSTRAINT IF EXISTS invoices_payment_status_check;

-- Add new constraint with more options
ALTER TABLE invoices ADD CONSTRAINT invoices_payment_status_check 
    CHECK (payment_status IN ('paid', 'unpaid', 'partial', 'overdue', 'pending', 'cancelled'));

-- =====================================================
-- CREATE VIEW FOR COMMON INVOICE FIELDS ONLY
-- =====================================================

CREATE OR REPLACE VIEW invoice_essentials AS
SELECT 
    id,
    user_id,
    document_id,
    vendor_name,
    invoice_number,
    invoice_date,
    due_date,
    subtotal,
    cgst,
    sgst,
    igst,
    total_amount,
    payment_status,
    created_at,
    updated_at
FROM invoices;

-- =====================================================
-- CREATE VIEW FOR GST-SPECIFIC INVOICES
-- =====================================================

CREATE OR REPLACE VIEW gst_invoices AS
SELECT 
    id,
    user_id,
    vendor_name,
    vendor_gstin,
    invoice_number,
    invoice_date,
    place_of_supply,
    hsn_code,
    sac_code,
    subtotal,
    cgst,
    sgst,
    igst,
    cess,
    total_amount,
    reverse_charge,
    created_at
FROM invoices
WHERE vendor_gstin IS NOT NULL OR cgst > 0 OR sgst > 0 OR igst > 0;

-- =====================================================
-- COMMENTS FOR DOCUMENTATION
-- =====================================================

COMMENT ON TABLE invoices IS 'Flexible invoice storage supporting various Indian invoice formats (GST, non-GST, retail, wholesale, service, etc.)';

COMMENT ON COLUMN invoices.vendor_gstin IS 'GST Identification Number (15 digits) - Optional for non-GST invoices';
COMMENT ON COLUMN invoices.vendor_pan IS 'Permanent Account Number (10 chars) - Optional';
COMMENT ON COLUMN invoices.cgst IS 'Central GST (for intra-state) - 0 if not applicable';
COMMENT ON COLUMN invoices.sgst IS 'State GST (for intra-state) - 0 if not applicable';
COMMENT ON COLUMN invoices.igst IS 'Integrated GST (for inter-state) - 0 if not applicable';
COMMENT ON COLUMN invoices.cess IS 'Additional cess (e.g., luxury cess) - 0 if not applicable';
COMMENT ON COLUMN invoices.hsn_code IS 'Harmonized System of Nomenclature (for goods) - Optional';
COMMENT ON COLUMN invoices.sac_code IS 'Service Accounting Code (for services) - Optional';
COMMENT ON COLUMN invoices.line_items IS 'Detailed item breakdown stored as JSON array';
COMMENT ON COLUMN invoices.raw_extracted_data IS 'Complete AI extraction output for debugging and reprocessing';
COMMENT ON COLUMN invoices.reverse_charge IS 'GST reverse charge mechanism applicable - false by default';
COMMENT ON COLUMN invoices.tds_amount IS 'Tax Deducted at Source - 0 if not applicable';

-- =====================================================
-- SUCCESS MESSAGE
-- =====================================================

DO $$ 
BEGIN
    RAISE NOTICE '✅ Flexible invoice schema updated successfully!';
    RAISE NOTICE '📊 Supports: GST, non-GST, retail, wholesale, service invoices';
    RAISE NOTICE '🔧 All optional fields - only save what exists in uploaded invoice';
END $$;
