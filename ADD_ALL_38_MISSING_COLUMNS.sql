-- ============================================================================
-- ADD ALL 38 MISSING COLUMNS TO INVOICES TABLE
-- Run this in Supabase SQL Editor: https://supabase.com/dashboard/project/ldvwxqluaheuhbycdpwn/editor
-- ============================================================================

-- CRITICAL COLUMNS (Priority 1 - Add these first!)
-- These are being extracted by AI but failing to save
ALTER TABLE invoices ADD COLUMN IF NOT EXISTS balance DECIMAL(15, 2);
ALTER TABLE invoices ADD COLUMN IF NOT EXISTS balance_due DECIMAL(15, 2);
ALTER TABLE invoices ADD COLUMN IF NOT EXISTS paid_amount DECIMAL(15, 2);
ALTER TABLE invoices ADD COLUMN IF NOT EXISTS customer_email VARCHAR(255);
ALTER TABLE invoices ADD COLUMN IF NOT EXISTS eway_bill VARCHAR(100);
ALTER TABLE invoices ADD COLUMN IF NOT EXISTS invoice_amount_in_words TEXT;
ALTER TABLE invoices ADD COLUMN IF NOT EXISTS irn_number VARCHAR(100);
ALTER TABLE invoices ADD COLUMN IF NOT EXISTS round_off DECIMAL(10, 2);

-- COMMON FIELDS (Priority 2)
ALTER TABLE invoices ADD COLUMN IF NOT EXISTS customer_pan VARCHAR(10);
ALTER TABLE invoices ADD COLUMN IF NOT EXISTS customer_pincode VARCHAR(10);
ALTER TABLE invoices ADD COLUMN IF NOT EXISTS vendor_cin VARCHAR(50);
ALTER TABLE invoices ADD COLUMN IF NOT EXISTS reference_number VARCHAR(100);
ALTER TABLE invoices ADD COLUMN IF NOT EXISTS order_number VARCHAR(100);
ALTER TABLE invoices ADD COLUMN IF NOT EXISTS order_date DATE;
ALTER TABLE invoices ADD COLUMN IF NOT EXISTS terms TEXT;

-- BANKING (Priority 2)
ALTER TABLE invoices ADD COLUMN IF NOT EXISTS bank_account VARCHAR(50);

-- SHIPPING/LOGISTICS (Priority 3)
ALTER TABLE invoices ADD COLUMN IF NOT EXISTS shipping_address TEXT;
ALTER TABLE invoices ADD COLUMN IF NOT EXISTS billing_address TEXT;
ALTER TABLE invoices ADD COLUMN IF NOT EXISTS ship_to_customer_name VARCHAR(255);
ALTER TABLE invoices ADD COLUMN IF NOT EXISTS ship_to_customer_address TEXT;
ALTER TABLE invoices ADD COLUMN IF NOT EXISTS ship_to_customer_state VARCHAR(100);
ALTER TABLE invoices ADD COLUMN IF NOT EXISTS ship_to_customer_phone VARCHAR(20);
ALTER TABLE invoices ADD COLUMN IF NOT EXISTS customer_gstin_ship_to VARCHAR(15);
ALTER TABLE invoices ADD COLUMN IF NOT EXISTS customer_po VARCHAR(100);
ALTER TABLE invoices ADD COLUMN IF NOT EXISTS customer_po_number VARCHAR(100);

-- TRANSPORT (Priority 3)
ALTER TABLE invoices ADD COLUMN IF NOT EXISTS delivery_number VARCHAR(100);
ALTER TABLE invoices ADD COLUMN IF NOT EXISTS delivery_note TEXT;
ALTER TABLE invoices ADD COLUMN IF NOT EXISTS eway_bill_date DATE;
ALTER TABLE invoices ADD COLUMN IF NOT EXISTS eway_bill_time TIME;
ALTER TABLE invoices ADD COLUMN IF NOT EXISTS vehicle_registration_number VARCHAR(50);
ALTER TABLE invoices ADD COLUMN IF NOT EXISTS mode_of_transport VARCHAR(50);
ALTER TABLE invoices ADD COLUMN IF NOT EXISTS transporter_name VARCHAR(255);
ALTER TABLE invoices ADD COLUMN IF NOT EXISTS lr_rr_number VARCHAR(50);
ALTER TABLE invoices ADD COLUMN IF NOT EXISTS lr_rr_date DATE;
ALTER TABLE invoices ADD COLUMN IF NOT EXISTS freight DECIMAL(10, 2);

-- ADDITIONAL (Priority 3)
ALTER TABLE invoices ADD COLUMN IF NOT EXISTS invoice_value_in_words TEXT;
ALTER TABLE invoices ADD COLUMN IF NOT EXISTS mrp_per_bag DECIMAL(10, 2);
ALTER TABLE invoices ADD COLUMN IF NOT EXISTS supplying_state VARCHAR(100);

-- ============================================================================
-- CREATE INDEXES FOR PERFORMANCE
-- ============================================================================

CREATE INDEX IF NOT EXISTS idx_invoices_customer_email ON invoices(customer_email);
CREATE INDEX IF NOT EXISTS idx_invoices_irn_number ON invoices(irn_number);
CREATE INDEX IF NOT EXISTS idx_invoices_eway_bill ON invoices(eway_bill);
CREATE INDEX IF NOT EXISTS idx_invoices_balance_due ON invoices(balance_due) WHERE balance_due > 0;
CREATE INDEX IF NOT EXISTS idx_invoices_reference_number ON invoices(reference_number);
CREATE INDEX IF NOT EXISTS idx_invoices_customer_pan ON invoices(customer_pan);

-- ============================================================================
-- ADD COMMENTS FOR DOCUMENTATION
-- ============================================================================

COMMENT ON COLUMN invoices.balance IS 'Balance amount remaining';
COMMENT ON COLUMN invoices.balance_due IS 'Amount due/outstanding';
COMMENT ON COLUMN invoices.paid_amount IS 'Amount already paid';
COMMENT ON COLUMN invoices.customer_email IS 'Customer email address';
COMMENT ON COLUMN invoices.customer_pan IS 'Customer PAN number';
COMMENT ON COLUMN invoices.eway_bill IS 'E-way bill number';
COMMENT ON COLUMN invoices.invoice_amount_in_words IS 'Invoice amount in words';
COMMENT ON COLUMN invoices.irn_number IS 'Invoice Reference Number (GST IRN)';
COMMENT ON COLUMN invoices.round_off IS 'Round off adjustment';
COMMENT ON COLUMN invoices.vendor_cin IS 'Vendor CIN (Corporate Identification Number)';
COMMENT ON COLUMN invoices.reference_number IS 'Reference/document number';
COMMENT ON COLUMN invoices.bank_account IS 'Bank account number';
COMMENT ON COLUMN invoices.shipping_address IS 'Shipping address';
COMMENT ON COLUMN invoices.billing_address IS 'Billing address';

-- ============================================================================
-- SUCCESS MESSAGE
-- ============================================================================

DO $$
BEGIN
    RAISE NOTICE '✅ Successfully added 38 missing columns to invoices table!';
    RAISE NOTICE '✅ Created 6 indexes for better query performance!';
    RAISE NOTICE '✅ System is now ready for enhanced OCR extraction!';
END $$;
