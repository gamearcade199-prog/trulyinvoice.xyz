-- 🛡️ DATABASE AUDIT TRIGGERS
-- Prevent invalid data from being saved to invoices table
-- Run this in Supabase SQL editor

BEGIN;

-- Drop existing triggers if any
DROP TRIGGER IF EXISTS tr_validate_invoice_before_insert ON invoices CASCADE;
DROP TRIGGER IF EXISTS tr_validate_invoice_before_update ON invoices CASCADE;
DROP FUNCTION IF EXISTS validate_invoice_on_insert() CASCADE;
DROP FUNCTION IF EXISTS validate_invoice_on_update() CASCADE;

-- ============ TRIGGER FUNCTION FOR INSERT ============
CREATE OR REPLACE FUNCTION validate_invoice_on_insert() RETURNS TRIGGER AS $$
BEGIN
    -- ============ REQUIRED FIELDS ============
    IF NEW.user_id IS NULL THEN
        RAISE EXCEPTION 'CRITICAL: user_id cannot be NULL (violates RLS security)';
    END IF;
    
    IF NEW.document_id IS NULL THEN
        RAISE EXCEPTION 'CRITICAL: document_id cannot be NULL (required for audit)';
    END IF;
    
    IF NEW.invoice_number IS NULL OR NEW.invoice_number = '' THEN
        RAISE EXCEPTION 'CRITICAL: invoice_number cannot be NULL or empty';
    END IF;
    
    IF NEW.vendor_name IS NULL OR NEW.vendor_name = '' THEN
        RAISE EXCEPTION 'CRITICAL: vendor_name cannot be NULL or empty';
    END IF;
    
    -- ============ FIELD LENGTH VALIDATION ============
    IF LENGTH(NEW.invoice_number) > 50 THEN
        RAISE EXCEPTION 'invoice_number too long (max 50 characters)';
    END IF;
    
    IF LENGTH(NEW.vendor_name) > 200 THEN
        RAISE EXCEPTION 'vendor_name too long (max 200 characters)';
    END IF;
    
    -- ============ NUMERIC FIELD VALIDATION ============
    IF NEW.total_amount IS NOT NULL AND NEW.total_amount < 0 THEN
        RAISE EXCEPTION 'total_amount cannot be negative: %', NEW.total_amount;
    END IF;
    
    IF NEW.total_amount IS NOT NULL AND NEW.total_amount > 999999999.99 THEN
        RAISE EXCEPTION 'total_amount exceeds maximum allowed value';
    END IF;
    
    -- ============ PAYMENT STATUS VALIDATION ============
    IF NEW.payment_status IS NOT NULL THEN
        IF NEW.payment_status NOT IN ('pending', 'paid', 'overdue', 'cancelled', 'refunded', 'partial', 'processing', 'failed') THEN
            RAISE EXCEPTION 'Invalid payment_status: %. Must be one of: pending, paid, overdue, cancelled, refunded, partial, processing, failed', NEW.payment_status;
        END IF;
    ELSE
        NEW.payment_status = 'pending'; -- Default
    END IF;
    
    -- ============ CONFIDENCE SCORE VALIDATION ============
    IF NEW.confidence_score IS NOT NULL AND (NEW.confidence_score < 0 OR NEW.confidence_score > 1) THEN
        RAISE EXCEPTION 'confidence_score out of range: % (must be 0-1)', NEW.confidence_score;
    END IF;
    
    IF NEW.vendor_confidence IS NOT NULL AND (NEW.vendor_confidence < 0 OR NEW.vendor_confidence > 1) THEN
        RAISE EXCEPTION 'vendor_confidence out of range: % (must be 0-1)', NEW.vendor_confidence;
    END IF;
    
    -- ============ DATE VALIDATION ============
    IF NEW.invoice_date IS NOT NULL AND NEW.due_date IS NOT NULL THEN
        IF NEW.due_date < NEW.invoice_date THEN
            RAISE EXCEPTION 'due_date cannot be before invoice_date';
        END IF;
    END IF;
    
    -- ============ AUTO-POPULATE TIMESTAMPS ============
    NEW.created_at = COALESCE(NEW.created_at, NOW());
    NEW.updated_at = COALESCE(NEW.updated_at, NOW());
    
    -- ============ TRIM WHITESPACE FROM STRING FIELDS ============
    NEW.invoice_number = TRIM(NEW.invoice_number);
    NEW.vendor_name = TRIM(NEW.vendor_name);
    IF NEW.customer_name IS NOT NULL THEN
        NEW.customer_name = TRIM(NEW.customer_name);
    END IF;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- ============ TRIGGER FUNCTION FOR UPDATE ============
CREATE OR REPLACE FUNCTION validate_invoice_on_update() RETURNS TRIGGER AS $$
BEGIN
    -- ============ PREVENT CRITICAL FIELD CHANGES ============
    IF OLD.user_id != NEW.user_id THEN
        RAISE EXCEPTION 'Cannot change user_id after invoice creation (data security violation)';
    END IF;
    
    IF OLD.document_id != NEW.document_id THEN
        RAISE EXCEPTION 'Cannot change document_id after invoice creation (audit trail violation)';
    END IF;
    
    IF OLD.created_at != NEW.created_at THEN
        RAISE EXCEPTION 'Cannot modify created_at timestamp';
    END IF;
    
    -- ============ VALIDATE NEW VALUES ============
    IF NEW.invoice_number IS NULL OR NEW.invoice_number = '' THEN
        RAISE EXCEPTION 'invoice_number cannot be set to NULL or empty';
    END IF;
    
    IF NEW.vendor_name IS NULL OR NEW.vendor_name = '' THEN
        RAISE EXCEPTION 'vendor_name cannot be set to NULL or empty';
    END IF;
    
    -- ============ NUMERIC VALIDATION ============
    IF NEW.total_amount IS NOT NULL AND NEW.total_amount < 0 THEN
        RAISE EXCEPTION 'total_amount cannot be negative: %', NEW.total_amount;
    END IF;
    
    -- ============ PAYMENT STATUS VALIDATION ============
    IF NEW.payment_status IS NOT NULL THEN
        IF NEW.payment_status NOT IN ('pending', 'paid', 'overdue', 'cancelled', 'refunded', 'partial', 'processing', 'failed') THEN
            RAISE EXCEPTION 'Invalid payment_status: %', NEW.payment_status;
        END IF;
    END IF;
    
    -- ============ UPDATE TIMESTAMP ============
    NEW.updated_at = NOW();
    
    -- ============ TRIM WHITESPACE ============
    NEW.invoice_number = TRIM(NEW.invoice_number);
    NEW.vendor_name = TRIM(NEW.vendor_name);
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- ============ CREATE TRIGGERS ============
CREATE TRIGGER tr_validate_invoice_before_insert
BEFORE INSERT ON invoices
FOR EACH ROW
EXECUTE FUNCTION validate_invoice_on_insert();

CREATE TRIGGER tr_validate_invoice_before_update
BEFORE UPDATE ON invoices
FOR EACH ROW
EXECUTE FUNCTION validate_invoice_on_update();

-- ============ LOG TABLE FOR AUDIT TRAIL ============
CREATE TABLE IF NOT EXISTS invoice_validation_logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    invoice_id UUID REFERENCES invoices(id) ON DELETE CASCADE,
    validation_type VARCHAR(50), -- 'insert', 'update', 'export'
    is_valid BOOLEAN NOT NULL,
    error_message TEXT,
    warnings TEXT,
    data_snapshot JSONB,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Create index for quick lookups
CREATE INDEX IF NOT EXISTS idx_validation_logs_invoice ON invoice_validation_logs(invoice_id);
CREATE INDEX IF NOT EXISTS idx_validation_logs_created ON invoice_validation_logs(created_at);

-- Enable RLS for audit logs
ALTER TABLE invoice_validation_logs ENABLE ROW LEVEL SECURITY;

-- Policy: Users can only see their own validation logs
CREATE POLICY "Users see own validation logs"
ON invoice_validation_logs FOR SELECT
USING (
    EXISTS (
        SELECT 1 FROM invoices 
        WHERE invoices.id = invoice_validation_logs.invoice_id 
        AND invoices.user_id = auth.uid()
    )
);

COMMIT;
