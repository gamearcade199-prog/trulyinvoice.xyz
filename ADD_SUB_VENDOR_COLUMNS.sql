-- ============================================================================
-- ADD SUB-VENDOR COLUMNS FOR CONSOLIDATED INVOICES
-- Run this in Supabase SQL Editor: https://supabase.com/dashboard/project/ldvwxqluaheuhbycdpwn/editor
-- ============================================================================

-- These columns track sub-vendors in consolidated invoices
-- Example: One invoice from distributor containing purchases from multiple manufacturers

-- Main invoice level: Track if this is a consolidated invoice
ALTER TABLE invoices ADD COLUMN IF NOT EXISTS is_consolidated BOOLEAN DEFAULT FALSE;
ALTER TABLE invoices ADD COLUMN IF NOT EXISTS sub_vendor_count INTEGER DEFAULT 0;

-- Add comments
COMMENT ON COLUMN invoices.is_consolidated IS 'True if invoice contains multiple sub-vendors/bills (consolidated billing report)';
COMMENT ON COLUMN invoices.sub_vendor_count IS 'Number of sub-vendors/bills in consolidated invoice (0 for regular invoices)';

-- Create index for quick filtering
CREATE INDEX IF NOT EXISTS idx_invoices_is_consolidated ON invoices(is_consolidated) WHERE is_consolidated = TRUE;

-- ============================================================================
-- NOTE: Line items already support sub-vendor fields through JSONB
-- ============================================================================
-- The line_items column is JSONB and can now store:
-- {
--   "line_items": [
--     {
--       "description": "...",
--       "amount": 100,
--       "sub_vendor": "PENNY BIG BAZAR",
--       "sub_bill_number": "OCT25-4761",
--       "sub_gstin": "01AEAPJ0354G1ZB"
--     }
--   ]
-- }

-- ============================================================================
-- SUCCESS MESSAGE
-- ============================================================================

DO $$
BEGIN
    RAISE NOTICE '✅ Added sub-vendor tracking columns!';
    RAISE NOTICE '✅ System can now handle consolidated invoices!';
    RAISE NOTICE 'ℹ️  Line items will automatically include sub_vendor, sub_bill_number, sub_gstin';
END $$;
