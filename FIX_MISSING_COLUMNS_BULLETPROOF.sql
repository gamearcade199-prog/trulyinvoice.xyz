-- =====================================================
-- ADD MISSING INVOICE COLUMNS - BULLETPROOF EXTRACTOR SUPPORT
-- Run this in Supabase SQL Editor to fix column errors
-- Safe to run multiple times - only adds missing fields
-- =====================================================

DO $$ 
BEGIN
    -- ============================================
    -- BANKING FIELDS (Missing: account_number, bank_name, ifsc_code)
    -- ============================================
    
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'invoices' AND column_name = 'bank_name') THEN
        ALTER TABLE invoices ADD COLUMN bank_name VARCHAR(255);
        RAISE NOTICE 'Added bank_name column';
    END IF;
    
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'invoices' AND column_name = 'account_number') THEN
        ALTER TABLE invoices ADD COLUMN account_number VARCHAR(50);
        RAISE NOTICE 'Added account_number column';
    END IF;
    
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'invoices' AND column_name = 'ifsc_code') THEN
        ALTER TABLE invoices ADD COLUMN ifsc_code VARCHAR(15);
        RAISE NOTICE 'Added ifsc_code column';
    END IF;
    
    -- ============================================
    -- VENDOR EXTENDED FIELDS
    -- ============================================
    
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'invoices' AND column_name = 'vendor_pan') THEN
        ALTER TABLE invoices ADD COLUMN vendor_pan VARCHAR(10);
        RAISE NOTICE 'Added vendor_pan column';
    END IF;
    
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'invoices' AND column_name = 'vendor_phone') THEN
        ALTER TABLE invoices ADD COLUMN vendor_phone VARCHAR(20);
        RAISE NOTICE 'Added vendor_phone column';
    END IF;
    
    -- ============================================
    -- CUSTOMER FIELDS
    -- ============================================
    
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'invoices' AND column_name = 'customer_name') THEN
        ALTER TABLE invoices ADD COLUMN customer_name VARCHAR(255);
        RAISE NOTICE 'Added customer_name column';
    END IF;
    
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'invoices' AND column_name = 'customer_address') THEN
        ALTER TABLE invoices ADD COLUMN customer_address TEXT;
        RAISE NOTICE 'Added customer_address column';
    END IF;
    
    -- ============================================
    -- FINANCIAL FIELDS
    -- ============================================
    
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'invoices' AND column_name = 'subtotal') THEN
        ALTER TABLE invoices ADD COLUMN subtotal DECIMAL(15,2);
        RAISE NOTICE 'Added subtotal column';
    END IF;
    
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'invoices' AND column_name = 'taxable_value') THEN
        ALTER TABLE invoices ADD COLUMN taxable_value DECIMAL(15,2);
        RAISE NOTICE 'Added taxable_value column';
    END IF;
    
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'invoices' AND column_name = 'tax_amount') THEN
        ALTER TABLE invoices ADD COLUMN tax_amount DECIMAL(15,2);
        RAISE NOTICE 'Added tax_amount column';
    END IF;
    
    -- ============================================
    -- GST CODES
    -- ============================================
    
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'invoices' AND column_name = 'hsn_code') THEN
        ALTER TABLE invoices ADD COLUMN hsn_code VARCHAR(20);
        RAISE NOTICE 'Added hsn_code column';
    END IF;
    
    -- ============================================
    -- CURRENCY FIELD
    -- ============================================
    
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'invoices' AND column_name = 'currency') THEN
        ALTER TABLE invoices ADD COLUMN currency VARCHAR(10) DEFAULT 'INR';
        RAISE NOTICE 'Added currency column';
    END IF;
    
    -- ============================================
    -- ADDITIONAL VENDOR FIELDS THAT MIGHT BE EXTRACTED
    -- ============================================
    
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'invoices' AND column_name = 'vendor_tan') THEN
        ALTER TABLE invoices ADD COLUMN vendor_tan VARCHAR(10);
        RAISE NOTICE 'Added vendor_tan column';
    END IF;
    
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'invoices' AND column_name = 'vendor_state') THEN
        ALTER TABLE invoices ADD COLUMN vendor_state VARCHAR(100);
        RAISE NOTICE 'Added vendor_state column';
    END IF;
    
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'invoices' AND column_name = 'vendor_pincode') THEN
        ALTER TABLE invoices ADD COLUMN vendor_pincode VARCHAR(10);
        RAISE NOTICE 'Added vendor_pincode column';
    END IF;
    
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'invoices' AND column_name = 'vendor_type') THEN
        ALTER TABLE invoices ADD COLUMN vendor_type VARCHAR(50);
        RAISE NOTICE 'Added vendor_type column';
    END IF;
    
    -- ============================================
    -- CUSTOMER EXTENDED FIELDS
    -- ============================================
    
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'invoices' AND column_name = 'customer_gstin') THEN
        ALTER TABLE invoices ADD COLUMN customer_gstin VARCHAR(15);
        RAISE NOTICE 'Added customer_gstin column';
    END IF;
    
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'invoices' AND column_name = 'customer_state') THEN
        ALTER TABLE invoices ADD COLUMN customer_state VARCHAR(100);
        RAISE NOTICE 'Added customer_state column';
    END IF;
    
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'invoices' AND column_name = 'customer_phone') THEN
        ALTER TABLE invoices ADD COLUMN customer_phone VARCHAR(20);
        RAISE NOTICE 'Added customer_phone column';
    END IF;
    
    -- ============================================
    -- DATE FIELDS
    -- ============================================
    
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'invoices' AND column_name = 'due_date') THEN
        ALTER TABLE invoices ADD COLUMN due_date DATE;
        RAISE NOTICE 'Added due_date column';
    END IF;
    
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'invoices' AND column_name = 'po_number') THEN
        ALTER TABLE invoices ADD COLUMN po_number VARCHAR(100);
        RAISE NOTICE 'Added po_number column';
    END IF;
    
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'invoices' AND column_name = 'po_date') THEN
        ALTER TABLE invoices ADD COLUMN po_date DATE;
        RAISE NOTICE 'Added po_date column';
    END IF;
    
    -- ============================================
    -- ADDITIONAL FINANCIAL FIELDS
    -- ============================================
    
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'invoices' AND column_name = 'discount') THEN
        ALTER TABLE invoices ADD COLUMN discount DECIMAL(15,2);
        RAISE NOTICE 'Added discount column';
    END IF;
    
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'invoices' AND column_name = 'discount_percentage') THEN
        ALTER TABLE invoices ADD COLUMN discount_percentage DECIMAL(5,2);
        RAISE NOTICE 'Added discount_percentage column';
    END IF;
    
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'invoices' AND column_name = 'shipping_charges') THEN
        ALTER TABLE invoices ADD COLUMN shipping_charges DECIMAL(15,2);
        RAISE NOTICE 'Added shipping_charges column';
    END IF;
    
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'invoices' AND column_name = 'other_charges') THEN
        ALTER TABLE invoices ADD COLUMN other_charges DECIMAL(15,2);
        RAISE NOTICE 'Added other_charges column';
    END IF;
    
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'invoices' AND column_name = 'roundoff') THEN
        ALTER TABLE invoices ADD COLUMN roundoff DECIMAL(15,2);
        RAISE NOTICE 'Added roundoff column';
    END IF;
    
    -- ============================================
    -- OTHER TAX FIELDS
    -- ============================================
    
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'invoices' AND column_name = 'total_gst') THEN
        ALTER TABLE invoices ADD COLUMN total_gst DECIMAL(15,2);
        RAISE NOTICE 'Added total_gst column';
    END IF;
    
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'invoices' AND column_name = 'ugst') THEN
        ALTER TABLE invoices ADD COLUMN ugst DECIMAL(15,2);
        RAISE NOTICE 'Added ugst column';
    END IF;
    
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'invoices' AND column_name = 'cess') THEN
        ALTER TABLE invoices ADD COLUMN cess DECIMAL(15,2);
        RAISE NOTICE 'Added cess column';
    END IF;
    
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'invoices' AND column_name = 'vat') THEN
        ALTER TABLE invoices ADD COLUMN vat DECIMAL(15,2);
        RAISE NOTICE 'Added vat column';
    END IF;
    
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'invoices' AND column_name = 'service_tax') THEN
        ALTER TABLE invoices ADD COLUMN service_tax DECIMAL(15,2);
        RAISE NOTICE 'Added service_tax column';
    END IF;
    
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'invoices' AND column_name = 'tds_amount') THEN
        ALTER TABLE invoices ADD COLUMN tds_amount DECIMAL(15,2);
        RAISE NOTICE 'Added tds_amount column';
    END IF;
    
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'invoices' AND column_name = 'tds_percentage') THEN
        ALTER TABLE invoices ADD COLUMN tds_percentage DECIMAL(5,2);
        RAISE NOTICE 'Added tds_percentage column';
    END IF;
    
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'invoices' AND column_name = 'tcs_amount') THEN
        ALTER TABLE invoices ADD COLUMN tcs_amount DECIMAL(15,2);
        RAISE NOTICE 'Added tcs_amount column';
    END IF;
    
    -- ============================================
    -- GST SPECIFIC FIELDS
    -- ============================================
    
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'invoices' AND column_name = 'sac_code') THEN
        ALTER TABLE invoices ADD COLUMN sac_code VARCHAR(20);
        RAISE NOTICE 'Added sac_code column';
    END IF;
    
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'invoices' AND column_name = 'place_of_supply') THEN
        ALTER TABLE invoices ADD COLUMN place_of_supply VARCHAR(100);
        RAISE NOTICE 'Added place_of_supply column';
    END IF;
    
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'invoices' AND column_name = 'reverse_charge') THEN
        ALTER TABLE invoices ADD COLUMN reverse_charge BOOLEAN DEFAULT false;
        RAISE NOTICE 'Added reverse_charge column';
    END IF;
    
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'invoices' AND column_name = 'invoice_type') THEN
        ALTER TABLE invoices ADD COLUMN invoice_type VARCHAR(50);
        RAISE NOTICE 'Added invoice_type column';
    END IF;
    
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'invoices' AND column_name = 'supply_type') THEN
        ALTER TABLE invoices ADD COLUMN supply_type VARCHAR(50);
        RAISE NOTICE 'Added supply_type column';
    END IF;
    
    -- ============================================
    -- PAYMENT FIELDS
    -- ============================================
    
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'invoices' AND column_name = 'payment_method') THEN
        ALTER TABLE invoices ADD COLUMN payment_method VARCHAR(50);
        RAISE NOTICE 'Added payment_method column';
    END IF;
    
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'invoices' AND column_name = 'payment_terms') THEN
        ALTER TABLE invoices ADD COLUMN payment_terms VARCHAR(100);
        RAISE NOTICE 'Added payment_terms column';
    END IF;
    
    -- ============================================
    -- ADDITIONAL BANKING FIELDS
    -- ============================================
    
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'invoices' AND column_name = 'swift_code') THEN
        ALTER TABLE invoices ADD COLUMN swift_code VARCHAR(15);
        RAISE NOTICE 'Added swift_code column';
    END IF;
    
    -- ============================================
    -- IMPORT/EXPORT FIELDS
    -- ============================================
    
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'invoices' AND column_name = 'bill_of_entry') THEN
        ALTER TABLE invoices ADD COLUMN bill_of_entry VARCHAR(100);
        RAISE NOTICE 'Added bill_of_entry column';
    END IF;
    
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'invoices' AND column_name = 'bill_of_entry_date') THEN
        ALTER TABLE invoices ADD COLUMN bill_of_entry_date DATE;
        RAISE NOTICE 'Added bill_of_entry_date column';
    END IF;
    
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'invoices' AND column_name = 'port_code') THEN
        ALTER TABLE invoices ADD COLUMN port_code VARCHAR(10);
        RAISE NOTICE 'Added port_code column';
    END IF;

END $$;

-- =====================================================
-- CREATE INDEXES FOR PERFORMANCE
-- =====================================================

CREATE INDEX IF NOT EXISTS idx_invoices_vendor_gstin ON invoices(vendor_gstin) WHERE vendor_gstin IS NOT NULL;
CREATE INDEX IF NOT EXISTS idx_invoices_vendor_pan ON invoices(vendor_pan) WHERE vendor_pan IS NOT NULL;
CREATE INDEX IF NOT EXISTS idx_invoices_hsn_code ON invoices(hsn_code) WHERE hsn_code IS NOT NULL;
CREATE INDEX IF NOT EXISTS idx_invoices_currency ON invoices(currency);
CREATE INDEX IF NOT EXISTS idx_invoices_total_amount ON invoices(total_amount);
CREATE INDEX IF NOT EXISTS idx_invoices_payment_status ON invoices(payment_status);

-- =====================================================
-- SUCCESS MESSAGE
-- =====================================================

DO $$ 
BEGIN
    RAISE NOTICE '';
    RAISE NOTICE '✅ DATABASE SCHEMA UPDATE COMPLETE!';
    RAISE NOTICE '';
    RAISE NOTICE 'All missing columns have been added to support';
    RAISE NOTICE 'the bulletproof Gemini extractor.';
    RAISE NOTICE '';
    RAISE NOTICE 'You can now upload invoices without column errors!';
    RAISE NOTICE '';
END $$;