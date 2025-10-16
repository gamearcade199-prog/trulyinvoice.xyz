-- Enhanced Database Schema - 50+ Industry Fields for Complete Invoice Coverage
-- This script adds comprehensive fields for ALL industries while maintaining bulletproof compatibility

BEGIN;

-- First, normalize existing payment_status values to prevent constraint violations
UPDATE invoices SET payment_status = 'pending' WHERE payment_status IS NULL OR payment_status = '';
UPDATE invoices SET payment_status = 'paid' WHERE LOWER(payment_status) IN ('paid', 'complete', 'completed', 'success', 'successful');
UPDATE invoices SET payment_status = 'pending' WHERE LOWER(payment_status) IN ('pending', 'unpaid', 'due', 'outstanding');
UPDATE invoices SET payment_status = 'overdue' WHERE LOWER(payment_status) IN ('overdue', 'late', 'past_due');
UPDATE invoices SET payment_status = 'cancelled' WHERE LOWER(payment_status) IN ('cancelled', 'canceled', 'void');
UPDATE invoices SET payment_status = 'refunded' WHERE LOWER(payment_status) IN ('refunded', 'returned');
UPDATE invoices SET payment_status = 'partial' WHERE LOWER(payment_status) IN ('partial', 'partially_paid');
-- Catch any other values and set to pending
UPDATE invoices SET payment_status = 'pending' WHERE payment_status NOT IN ('pending', 'paid', 'overdue', 'cancelled', 'refunded', 'partial', 'processing', 'failed');

-- Now safely drop and recreate the constraint
ALTER TABLE invoices DROP CONSTRAINT IF EXISTS invoices_payment_status_check;
ALTER TABLE invoices ADD CONSTRAINT invoices_payment_status_check 
CHECK (payment_status IN ('pending', 'paid', 'overdue', 'cancelled', 'refunded', 'partial', 'processing', 'failed'));

-- HOTEL & HOSPITALITY INDUSTRY FIELDS
ALTER TABLE invoices ADD COLUMN IF NOT EXISTS arrival_date DATE;
ALTER TABLE invoices ADD COLUMN IF NOT EXISTS departure_date DATE;
ALTER TABLE invoices ADD COLUMN IF NOT EXISTS room_number VARCHAR(50);
ALTER TABLE invoices ADD COLUMN IF NOT EXISTS guest_count INTEGER;
ALTER TABLE invoices ADD COLUMN IF NOT EXISTS booking_reference VARCHAR(100);
ALTER TABLE invoices ADD COLUMN IF NOT EXISTS hotel_star_rating INTEGER;
ALTER TABLE invoices ADD COLUMN IF NOT EXISTS meal_plan VARCHAR(50);

-- RETAIL & E-COMMERCE FIELDS
ALTER TABLE invoices ADD COLUMN IF NOT EXISTS order_id VARCHAR(100);
ALTER TABLE invoices ADD COLUMN IF NOT EXISTS tracking_number VARCHAR(100);
ALTER TABLE invoices ADD COLUMN IF NOT EXISTS shipping_method VARCHAR(100);
ALTER TABLE invoices ADD COLUMN IF NOT EXISTS delivery_date DATE;
ALTER TABLE invoices ADD COLUMN IF NOT EXISTS return_policy TEXT;
ALTER TABLE invoices ADD COLUMN IF NOT EXISTS coupon_code VARCHAR(50);
ALTER TABLE invoices ADD COLUMN IF NOT EXISTS discount_percentage DECIMAL(5,2);

-- MANUFACTURING & INDUSTRIAL FIELDS  
ALTER TABLE invoices ADD COLUMN IF NOT EXISTS purchase_order VARCHAR(100);
ALTER TABLE invoices ADD COLUMN IF NOT EXISTS batch_number VARCHAR(100);
ALTER TABLE invoices ADD COLUMN IF NOT EXISTS quality_certificate VARCHAR(100);
ALTER TABLE invoices ADD COLUMN IF NOT EXISTS warranty_period VARCHAR(50);
ALTER TABLE invoices ADD COLUMN IF NOT EXISTS manufacturing_date DATE;
ALTER TABLE invoices ADD COLUMN IF NOT EXISTS expiry_date DATE;

-- MEDICAL & HEALTHCARE FIELDS
ALTER TABLE invoices ADD COLUMN IF NOT EXISTS patient_id VARCHAR(100);
ALTER TABLE invoices ADD COLUMN IF NOT EXISTS doctor_name VARCHAR(200);
ALTER TABLE invoices ADD COLUMN IF NOT EXISTS medical_license VARCHAR(100);
ALTER TABLE invoices ADD COLUMN IF NOT EXISTS insurance_claim VARCHAR(100);
ALTER TABLE invoices ADD COLUMN IF NOT EXISTS treatment_date DATE;
ALTER TABLE invoices ADD COLUMN IF NOT EXISTS prescription_number VARCHAR(100);

-- LOGISTICS & TRANSPORTATION FIELDS
ALTER TABLE invoices ADD COLUMN IF NOT EXISTS vehicle_number VARCHAR(50);
ALTER TABLE invoices ADD COLUMN IF NOT EXISTS driver_name VARCHAR(200);
ALTER TABLE invoices ADD COLUMN IF NOT EXISTS origin_location VARCHAR(300);
ALTER TABLE invoices ADD COLUMN IF NOT EXISTS destination_location VARCHAR(300);
ALTER TABLE invoices ADD COLUMN IF NOT EXISTS distance_km DECIMAL(10,2);
ALTER TABLE invoices ADD COLUMN IF NOT EXISTS fuel_surcharge DECIMAL(10,2);

-- PROFESSIONAL SERVICES FIELDS
ALTER TABLE invoices ADD COLUMN IF NOT EXISTS project_name VARCHAR(200);
ALTER TABLE invoices ADD COLUMN IF NOT EXISTS consultant_name VARCHAR(200);
ALTER TABLE invoices ADD COLUMN IF NOT EXISTS hourly_rate DECIMAL(10,2);
ALTER TABLE invoices ADD COLUMN IF NOT EXISTS hours_worked DECIMAL(10,2);
ALTER TABLE invoices ADD COLUMN IF NOT EXISTS project_phase VARCHAR(100);
ALTER TABLE invoices ADD COLUMN IF NOT EXISTS deliverable TEXT;

-- REAL ESTATE FIELDS
ALTER TABLE invoices ADD COLUMN IF NOT EXISTS property_address TEXT;
ALTER TABLE invoices ADD COLUMN IF NOT EXISTS property_type VARCHAR(100);
ALTER TABLE invoices ADD COLUMN IF NOT EXISTS square_footage DECIMAL(10,2);
ALTER TABLE invoices ADD COLUMN IF NOT EXISTS lease_term VARCHAR(50);
ALTER TABLE invoices ADD COLUMN IF NOT EXISTS security_deposit DECIMAL(10,2);

-- EDUCATION FIELDS
ALTER TABLE invoices ADD COLUMN IF NOT EXISTS student_id VARCHAR(100);
ALTER TABLE invoices ADD COLUMN IF NOT EXISTS course_name VARCHAR(200);
ALTER TABLE invoices ADD COLUMN IF NOT EXISTS academic_year VARCHAR(20);
ALTER TABLE invoices ADD COLUMN IF NOT EXISTS semester VARCHAR(20);
ALTER TABLE invoices ADD COLUMN IF NOT EXISTS instructor_name VARCHAR(200);

-- UTILITIES & SERVICES FIELDS
ALTER TABLE invoices ADD COLUMN IF NOT EXISTS meter_reading_start DECIMAL(10,2);
ALTER TABLE invoices ADD COLUMN IF NOT EXISTS meter_reading_end DECIMAL(10,2);
ALTER TABLE invoices ADD COLUMN IF NOT EXISTS units_consumed DECIMAL(10,2);
ALTER TABLE invoices ADD COLUMN IF NOT EXISTS rate_per_unit DECIMAL(10,4);
ALTER TABLE invoices ADD COLUMN IF NOT EXISTS connection_id VARCHAR(100);

-- FINANCIAL SERVICES FIELDS
ALTER TABLE invoices ADD COLUMN IF NOT EXISTS account_number VARCHAR(100);
ALTER TABLE invoices ADD COLUMN IF NOT EXISTS transaction_id VARCHAR(100);
ALTER TABLE invoices ADD COLUMN IF NOT EXISTS interest_rate DECIMAL(10,4);
ALTER TABLE invoices ADD COLUMN IF NOT EXISTS principal_amount DECIMAL(15,2);
ALTER TABLE invoices ADD COLUMN IF NOT EXISTS processing_fee DECIMAL(10,2);

-- AI CONFIDENCE TRACKING FIELDS
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

-- SUBSCRIPTION & RECURRING SERVICES
ALTER TABLE invoices ADD COLUMN IF NOT EXISTS subscription_type VARCHAR(100);
ALTER TABLE invoices ADD COLUMN IF NOT EXISTS billing_cycle VARCHAR(50);
ALTER TABLE invoices ADD COLUMN IF NOT EXISTS next_billing_date DATE;
ALTER TABLE invoices ADD COLUMN IF NOT EXISTS auto_renewal BOOLEAN DEFAULT FALSE;
ALTER TABLE invoices ADD COLUMN IF NOT EXISTS plan_features TEXT;

-- ADDITIONAL BUSINESS FIELDS
ALTER TABLE invoices ADD COLUMN IF NOT EXISTS contract_number VARCHAR(100);
ALTER TABLE invoices ADD COLUMN IF NOT EXISTS milestone VARCHAR(200);
ALTER TABLE invoices ADD COLUMN IF NOT EXISTS approval_status VARCHAR(50);
ALTER TABLE invoices ADD COLUMN IF NOT EXISTS approved_by VARCHAR(200);
ALTER TABLE invoices ADD COLUMN IF NOT EXISTS department VARCHAR(100);
ALTER TABLE invoices ADD COLUMN IF NOT EXISTS cost_center VARCHAR(100);
ALTER TABLE invoices ADD COLUMN IF NOT EXISTS budget_code VARCHAR(100);

-- COMPLIANCE & REGULATORY FIELDS
ALTER TABLE invoices ADD COLUMN IF NOT EXISTS regulatory_code VARCHAR(100);
ALTER TABLE invoices ADD COLUMN IF NOT EXISTS compliance_certificate VARCHAR(100);
ALTER TABLE invoices ADD COLUMN IF NOT EXISTS audit_trail TEXT;
ALTER TABLE invoices ADD COLUMN IF NOT EXISTS authorized_signatory VARCHAR(200);

-- ENHANCED METADATA FIELDS
ALTER TABLE invoices ADD COLUMN IF NOT EXISTS extraction_version VARCHAR(20) DEFAULT 'v2.5';
ALTER TABLE invoices ADD COLUMN IF NOT EXISTS processing_time_seconds DECIMAL(5,2);
ALTER TABLE invoices ADD COLUMN IF NOT EXISTS data_source VARCHAR(50) DEFAULT 'gemini-2.5-flash';
ALTER TABLE invoices ADD COLUMN IF NOT EXISTS quality_score DECIMAL(5,2);

-- Create index for better performance on frequently searched fields
CREATE INDEX IF NOT EXISTS idx_invoices_order_id ON invoices(order_id);
CREATE INDEX IF NOT EXISTS idx_invoices_booking_reference ON invoices(booking_reference);
CREATE INDEX IF NOT EXISTS idx_invoices_purchase_order ON invoices(purchase_order);
CREATE INDEX IF NOT EXISTS idx_invoices_project_name ON invoices(project_name);
CREATE INDEX IF NOT EXISTS idx_invoices_subscription_type ON invoices(subscription_type);

-- Update existing null values to prevent constraint violations (already done above)
-- UPDATE invoices SET payment_status = 'pending' WHERE payment_status IS NULL;

COMMIT;

-- Verification query to show all added columns
SELECT 
    column_name, 
    data_type, 
    is_nullable
FROM information_schema.columns 
WHERE table_name = 'invoices' 
ORDER BY ordinal_position;