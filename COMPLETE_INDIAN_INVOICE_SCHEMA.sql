-- =====================================================
-- COMPLETE INDIAN INVOICE SCHEMA - ALL SCENARIOS
-- Supports: Retail, GST, Service, Manufacturing, E-commerce, 
--           Import/Export, B2B, B2C, Government, Healthcare, etc.
-- =====================================================
-- Run this ONCE in Supabase SQL Editor
-- Safe to run multiple times - only adds missing fields
-- =====================================================

-- Enable required extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm"; -- For fuzzy text search

-- =====================================================
-- STEP 1: ENSURE ALL BASE TABLES EXIST
-- =====================================================

-- 1. USERS TABLE (Authentication)
CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email VARCHAR(255) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Add optional user fields if they don't exist
DO $$ 
BEGIN
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'users' AND column_name = 'full_name') THEN
        ALTER TABLE users ADD COLUMN full_name VARCHAR(255);
    END IF;
    
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'users' AND column_name = 'company_name') THEN
        ALTER TABLE users ADD COLUMN company_name VARCHAR(255);
    END IF;
    
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'users' AND column_name = 'gstin') THEN
        ALTER TABLE users ADD COLUMN gstin VARCHAR(15);
    END IF;
    
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'users' AND column_name = 'pan') THEN
        ALTER TABLE users ADD COLUMN pan VARCHAR(10);
    END IF;
    
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'users' AND column_name = 'address') THEN
        ALTER TABLE users ADD COLUMN address TEXT;
    END IF;
    
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'users' AND column_name = 'phone') THEN
        ALTER TABLE users ADD COLUMN phone VARCHAR(20);
    END IF;
    
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'users' AND column_name = 'is_active') THEN
        ALTER TABLE users ADD COLUMN is_active BOOLEAN DEFAULT true;
    END IF;
    
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'users' AND column_name = 'is_verified') THEN
        ALTER TABLE users ADD COLUMN is_verified BOOLEAN DEFAULT false;
    END IF;
END $$;

-- Create indexes AFTER ensuring columns exist
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
CREATE INDEX IF NOT EXISTS idx_users_gstin ON users(gstin) WHERE gstin IS NOT NULL;

-- 2. DOCUMENTS TABLE (File Storage)
CREATE TABLE IF NOT EXISTS documents (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    file_name VARCHAR(255) NOT NULL,
    storage_path VARCHAR(500) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Add optional document fields if they don't exist
DO $$ 
BEGIN
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'documents' AND column_name = 'file_url') THEN
        ALTER TABLE documents ADD COLUMN file_url TEXT;
    END IF;
    
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'documents' AND column_name = 'file_size') THEN
        ALTER TABLE documents ADD COLUMN file_size INTEGER;
    END IF;
    
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'documents' AND column_name = 'mime_type') THEN
        ALTER TABLE documents ADD COLUMN mime_type VARCHAR(100);
    END IF;
    
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'documents' AND column_name = 'status') THEN
        ALTER TABLE documents ADD COLUMN status VARCHAR(50) DEFAULT 'uploaded';
    END IF;
    
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'documents' AND column_name = 'confidence_score') THEN
        ALTER TABLE documents ADD COLUMN confidence_score DECIMAL(5,4);
    END IF;
    
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'documents' AND column_name = 'processing_time_ms') THEN
        ALTER TABLE documents ADD COLUMN processing_time_ms INTEGER;
    END IF;
    
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'documents' AND column_name = 'error_message') THEN
        ALTER TABLE documents ADD COLUMN error_message TEXT;
    END IF;
END $$;

-- Create indexes AFTER ensuring columns exist
CREATE INDEX IF NOT EXISTS idx_documents_user_id ON documents(user_id);
CREATE INDEX IF NOT EXISTS idx_documents_status ON documents(status);

-- 3. CATEGORIES TABLE (Organization)
CREATE TABLE IF NOT EXISTS categories (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    color VARCHAR(7) DEFAULT '#6366f1',
    icon VARCHAR(50),
    is_default BOOLEAN DEFAULT false,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT unique_user_category UNIQUE (user_id, name)
);

CREATE INDEX IF NOT EXISTS idx_categories_user_id ON categories(user_id);

-- =====================================================
-- STEP 2: CREATE/UPDATE COMPREHENSIVE INVOICES TABLE
-- =====================================================

-- Create invoices table if not exists
CREATE TABLE IF NOT EXISTS invoices (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    document_id UUID REFERENCES documents(id) ON DELETE SET NULL,
    category_id UUID REFERENCES categories(id) ON DELETE SET NULL,
    
    -- Basic Invoice Information (ALWAYS REQUIRED)
    invoice_number VARCHAR(100) NOT NULL,
    invoice_date DATE NOT NULL,
    vendor_name VARCHAR(255) NOT NULL,
    total_amount DECIMAL(15,2) NOT NULL,
    
    -- Payment Status (ALWAYS INCLUDED)
    payment_status VARCHAR(50) DEFAULT 'unpaid',
    
    -- Timestamps (ALWAYS INCLUDED)
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =====================================================
-- STEP 3: ADD ALL OPTIONAL FIELDS (IF NOT EXISTS)
-- =====================================================

DO $$ 
BEGIN
    -- ============================================
    -- VENDOR INFORMATION (All Optional)
    -- ============================================
    
    -- Vendor GSTIN (GST invoices)
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'invoices' AND column_name = 'vendor_gstin') THEN
        ALTER TABLE invoices ADD COLUMN vendor_gstin VARCHAR(15);
    END IF;
    
    -- Vendor PAN (Tax purposes)
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'invoices' AND column_name = 'vendor_pan') THEN
        ALTER TABLE invoices ADD COLUMN vendor_pan VARCHAR(10);
    END IF;
    
    -- Vendor TAN (TDS purposes)
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'invoices' AND column_name = 'vendor_tan') THEN
        ALTER TABLE invoices ADD COLUMN vendor_tan VARCHAR(10);
    END IF;
    
    -- Vendor Email
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'invoices' AND column_name = 'vendor_email') THEN
        ALTER TABLE invoices ADD COLUMN vendor_email VARCHAR(255);
    END IF;
    
    -- Vendor Phone
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'invoices' AND column_name = 'vendor_phone') THEN
        ALTER TABLE invoices ADD COLUMN vendor_phone VARCHAR(20);
    END IF;
    
    -- Vendor Address
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'invoices' AND column_name = 'vendor_address') THEN
        ALTER TABLE invoices ADD COLUMN vendor_address TEXT;
    END IF;
    
    -- Vendor State (GST purposes)
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'invoices' AND column_name = 'vendor_state') THEN
        ALTER TABLE invoices ADD COLUMN vendor_state VARCHAR(100);
    END IF;
    
    -- Vendor PIN Code
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'invoices' AND column_name = 'vendor_pincode') THEN
        ALTER TABLE invoices ADD COLUMN vendor_pincode VARCHAR(10);
    END IF;
    
    -- Vendor Type (Registered/Unregistered/Composition)
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'invoices' AND column_name = 'vendor_type') THEN
        ALTER TABLE invoices ADD COLUMN vendor_type VARCHAR(50);
    END IF;
    
    -- ============================================
    -- CUSTOMER INFORMATION (B2B Invoices)
    -- ============================================
    
    -- Buyer/Customer Name
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'invoices' AND column_name = 'customer_name') THEN
        ALTER TABLE invoices ADD COLUMN customer_name VARCHAR(255);
    END IF;
    
    -- Customer GSTIN
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'invoices' AND column_name = 'customer_gstin') THEN
        ALTER TABLE invoices ADD COLUMN customer_gstin VARCHAR(15);
    END IF;
    
    -- Customer Address
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'invoices' AND column_name = 'customer_address') THEN
        ALTER TABLE invoices ADD COLUMN customer_address TEXT;
    END IF;
    
    -- Customer State
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'invoices' AND column_name = 'customer_state') THEN
        ALTER TABLE invoices ADD COLUMN customer_state VARCHAR(100);
    END IF;
    
    -- ============================================
    -- INVOICE DATES & REFERENCES
    -- ============================================
    
    -- Due Date
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'invoices' AND column_name = 'due_date') THEN
        ALTER TABLE invoices ADD COLUMN due_date DATE;
    END IF;
    
    -- Purchase Order Number
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'invoices' AND column_name = 'po_number') THEN
        ALTER TABLE invoices ADD COLUMN po_number VARCHAR(100);
    END IF;
    
    -- Purchase Order Date
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'invoices' AND column_name = 'po_date') THEN
        ALTER TABLE invoices ADD COLUMN po_date DATE;
    END IF;
    
    -- Challan/Delivery Note Number
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'invoices' AND column_name = 'challan_number') THEN
        ALTER TABLE invoices ADD COLUMN challan_number VARCHAR(100);
    END IF;
    
    -- E-way Bill Number (for goods transport)
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'invoices' AND column_name = 'eway_bill_number') THEN
        ALTER TABLE invoices ADD COLUMN eway_bill_number VARCHAR(50);
    END IF;
    
    -- LR Number (Lorry Receipt)
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'invoices' AND column_name = 'lr_number') THEN
        ALTER TABLE invoices ADD COLUMN lr_number VARCHAR(100);
    END IF;
    
    -- ============================================
    -- FINANCIAL AMOUNTS (All Optional)
    -- ============================================
    
    -- Subtotal (before tax)
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'invoices' AND column_name = 'subtotal') THEN
        ALTER TABLE invoices ADD COLUMN subtotal DECIMAL(15,2);
    END IF;
    
    -- Taxable Amount
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'invoices' AND column_name = 'taxable_amount') THEN
        ALTER TABLE invoices ADD COLUMN taxable_amount DECIMAL(15,2);
    END IF;
    
    -- ============================================
    -- GST TAX FIELDS (Indian GST System)
    -- ============================================
    
    -- CGST (Central GST - Intra-state)
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'invoices' AND column_name = 'cgst') THEN
        ALTER TABLE invoices ADD COLUMN cgst DECIMAL(15,2);
    END IF;
    
    -- SGST (State GST - Intra-state)
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'invoices' AND column_name = 'sgst') THEN
        ALTER TABLE invoices ADD COLUMN sgst DECIMAL(15,2);
    END IF;
    
    -- IGST (Integrated GST - Inter-state)
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'invoices' AND column_name = 'igst') THEN
        ALTER TABLE invoices ADD COLUMN igst DECIMAL(15,2);
    END IF;
    
    -- UGST (Union Territory GST)
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'invoices' AND column_name = 'ugst') THEN
        ALTER TABLE invoices ADD COLUMN ugst DECIMAL(15,2);
    END IF;
    
    -- CESS (Additional cess)
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'invoices' AND column_name = 'cess') THEN
        ALTER TABLE invoices ADD COLUMN cess DECIMAL(15,2);
    END IF;
    
    -- Total GST
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'invoices' AND column_name = 'total_gst') THEN
        ALTER TABLE invoices ADD COLUMN total_gst DECIMAL(15,2);
    END IF;
    
    -- ============================================
    -- OTHER TAXES (Non-GST)
    -- ============================================
    
    -- VAT (for old invoices pre-GST)
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'invoices' AND column_name = 'vat') THEN
        ALTER TABLE invoices ADD COLUMN vat DECIMAL(15,2);
    END IF;
    
    -- Service Tax (old regime)
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'invoices' AND column_name = 'service_tax') THEN
        ALTER TABLE invoices ADD COLUMN service_tax DECIMAL(15,2);
    END IF;
    
    -- TDS Amount (Tax Deducted at Source)
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'invoices' AND column_name = 'tds_amount') THEN
        ALTER TABLE invoices ADD COLUMN tds_amount DECIMAL(15,2);
    END IF;
    
    -- TDS Percentage
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'invoices' AND column_name = 'tds_percentage') THEN
        ALTER TABLE invoices ADD COLUMN tds_percentage DECIMAL(5,2);
    END IF;
    
    -- TCS (Tax Collected at Source)
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'invoices' AND column_name = 'tcs_amount') THEN
        ALTER TABLE invoices ADD COLUMN tcs_amount DECIMAL(15,2);
    END IF;
    
    -- ============================================
    -- DEDUCTIONS & CHARGES
    -- ============================================
    
    -- Discount Amount
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'invoices' AND column_name = 'discount') THEN
        ALTER TABLE invoices ADD COLUMN discount DECIMAL(15,2);
    END IF;
    
    -- Discount Percentage
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'invoices' AND column_name = 'discount_percentage') THEN
        ALTER TABLE invoices ADD COLUMN discount_percentage DECIMAL(5,2);
    END IF;
    
    -- Shipping/Freight Charges
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'invoices' AND column_name = 'shipping_charges') THEN
        ALTER TABLE invoices ADD COLUMN shipping_charges DECIMAL(15,2);
    END IF;
    
    -- Packing Charges
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'invoices' AND column_name = 'packing_charges') THEN
        ALTER TABLE invoices ADD COLUMN packing_charges DECIMAL(15,2);
    END IF;
    
    -- Handling Charges
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'invoices' AND column_name = 'handling_charges') THEN
        ALTER TABLE invoices ADD COLUMN handling_charges DECIMAL(15,2);
    END IF;
    
    -- Insurance Charges
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'invoices' AND column_name = 'insurance_charges') THEN
        ALTER TABLE invoices ADD COLUMN insurance_charges DECIMAL(15,2);
    END IF;
    
    -- Other Charges
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'invoices' AND column_name = 'other_charges') THEN
        ALTER TABLE invoices ADD COLUMN other_charges DECIMAL(15,2);
    END IF;
    
    -- Round Off
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'invoices' AND column_name = 'roundoff') THEN
        ALTER TABLE invoices ADD COLUMN roundoff DECIMAL(15,2);
    END IF;
    
    -- ============================================
    -- GST SPECIFIC FIELDS
    -- ============================================
    
    -- HSN Code (Harmonized System of Nomenclature - for goods)
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'invoices' AND column_name = 'hsn_code') THEN
        ALTER TABLE invoices ADD COLUMN hsn_code VARCHAR(20);
    END IF;
    
    -- SAC Code (Service Accounting Code - for services)
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'invoices' AND column_name = 'sac_code') THEN
        ALTER TABLE invoices ADD COLUMN sac_code VARCHAR(20);
    END IF;
    
    -- Place of Supply (State)
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'invoices' AND column_name = 'place_of_supply') THEN
        ALTER TABLE invoices ADD COLUMN place_of_supply VARCHAR(100);
    END IF;
    
    -- Reverse Charge Applicable (RCM)
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'invoices' AND column_name = 'reverse_charge') THEN
        ALTER TABLE invoices ADD COLUMN reverse_charge BOOLEAN DEFAULT false;
    END IF;
    
    -- Invoice Type (B2B, B2C, Export, SEZ, etc.)
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'invoices' AND column_name = 'invoice_type') THEN
        ALTER TABLE invoices ADD COLUMN invoice_type VARCHAR(50);
    END IF;
    
    -- Supply Type (Goods/Services/Both)
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'invoices' AND column_name = 'supply_type') THEN
        ALTER TABLE invoices ADD COLUMN supply_type VARCHAR(50);
    END IF;
    
    -- ============================================
    -- IMPORT/EXPORT FIELDS
    -- ============================================
    
    -- Bill of Entry Number (Import)
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'invoices' AND column_name = 'bill_of_entry') THEN
        ALTER TABLE invoices ADD COLUMN bill_of_entry VARCHAR(100);
    END IF;
    
    -- Bill of Entry Date
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'invoices' AND column_name = 'bill_of_entry_date') THEN
        ALTER TABLE invoices ADD COLUMN bill_of_entry_date DATE;
    END IF;
    
    -- Port Code (Import/Export)
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'invoices' AND column_name = 'port_code') THEN
        ALTER TABLE invoices ADD COLUMN port_code VARCHAR(50);
    END IF;
    
    -- Shipping Bill Number (Export)
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'invoices' AND column_name = 'shipping_bill_number') THEN
        ALTER TABLE invoices ADD COLUMN shipping_bill_number VARCHAR(100);
    END IF;
    
    -- Country of Origin
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'invoices' AND column_name = 'country_of_origin') THEN
        ALTER TABLE invoices ADD COLUMN country_of_origin VARCHAR(100);
    END IF;
    
    -- ============================================
    -- PAYMENT INFORMATION
    -- ============================================
    
    -- Payment Terms (Net 30, COD, etc.)
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'invoices' AND column_name = 'payment_terms') THEN
        ALTER TABLE invoices ADD COLUMN payment_terms VARCHAR(255);
    END IF;
    
    -- Payment Method (UPI, Cash, Card, etc.)
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'invoices' AND column_name = 'payment_method') THEN
        ALTER TABLE invoices ADD COLUMN payment_method VARCHAR(100);
    END IF;
    
    -- Payment Date
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'invoices' AND column_name = 'payment_date') THEN
        ALTER TABLE invoices ADD COLUMN payment_date DATE;
    END IF;
    
    -- Payment Reference (Transaction ID, Cheque No, etc.)
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'invoices' AND column_name = 'payment_reference') THEN
        ALTER TABLE invoices ADD COLUMN payment_reference VARCHAR(255);
    END IF;
    
    -- Bank Details
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'invoices' AND column_name = 'bank_details') THEN
        ALTER TABLE invoices ADD COLUMN bank_details TEXT;
    END IF;
    
    -- ============================================
    -- CURRENCY & EXCHANGE
    -- ============================================
    
    -- Currency Code
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'invoices' AND column_name = 'currency') THEN
        ALTER TABLE invoices ADD COLUMN currency VARCHAR(10) DEFAULT 'INR';
    END IF;
    
    -- Exchange Rate (for foreign currency)
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'invoices' AND column_name = 'exchange_rate') THEN
        ALTER TABLE invoices ADD COLUMN exchange_rate DECIMAL(15,4);
    END IF;
    
    -- Amount in Foreign Currency
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'invoices' AND column_name = 'foreign_currency_amount') THEN
        ALTER TABLE invoices ADD COLUMN foreign_currency_amount DECIMAL(15,2);
    END IF;
    
    -- ============================================
    -- FLEXIBLE DATA STORAGE
    -- ============================================
    
    -- Line Items (JSONB array for item details)
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'invoices' AND column_name = 'line_items') THEN
        ALTER TABLE invoices ADD COLUMN line_items JSONB DEFAULT '[]'::jsonb;
    END IF;
    
    -- Raw Extracted Data (AI output)
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'invoices' AND column_name = 'raw_extracted_data') THEN
        ALTER TABLE invoices ADD COLUMN raw_extracted_data JSONB;
    END IF;
    
    -- Additional Metadata
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'invoices' AND column_name = 'metadata') THEN
        ALTER TABLE invoices ADD COLUMN metadata JSONB;
    END IF;
    
    -- ============================================
    -- USER CUSTOMIZATION
    -- ============================================
    
    -- Notes/Comments
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'invoices' AND column_name = 'notes') THEN
        ALTER TABLE invoices ADD COLUMN notes TEXT;
    END IF;
    
    -- Tags (for organization)
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'invoices' AND column_name = 'tags') THEN
        ALTER TABLE invoices ADD COLUMN tags TEXT[];
    END IF;
    
    -- Attachments (additional files)
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'invoices' AND column_name = 'attachments') THEN
        ALTER TABLE invoices ADD COLUMN attachments JSONB;
    END IF;
    
    -- Is Starred/Favorite
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'invoices' AND column_name = 'is_starred') THEN
        ALTER TABLE invoices ADD COLUMN is_starred BOOLEAN DEFAULT false;
    END IF;
    
    -- Is Verified (manually verified by user)
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'invoices' AND column_name = 'is_verified') THEN
        ALTER TABLE invoices ADD COLUMN is_verified BOOLEAN DEFAULT false;
    END IF;
    
    -- ============================================
    -- SPECIAL INVOICE TYPES
    -- ============================================
    
    -- Credit Note Reference
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'invoices' AND column_name = 'credit_note_ref') THEN
        ALTER TABLE invoices ADD COLUMN credit_note_ref VARCHAR(100);
    END IF;
    
    -- Debit Note Reference
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'invoices' AND column_name = 'debit_note_ref') THEN
        ALTER TABLE invoices ADD COLUMN debit_note_ref VARCHAR(100);
    END IF;
    
    -- Original Invoice Reference (for returns)
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'invoices' AND column_name = 'original_invoice_ref') THEN
        ALTER TABLE invoices ADD COLUMN original_invoice_ref VARCHAR(100);
    END IF;
    
    -- Is Recurring Invoice
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'invoices' AND column_name = 'is_recurring') THEN
        ALTER TABLE invoices ADD COLUMN is_recurring BOOLEAN DEFAULT false;
    END IF;
    
    -- Recurring Frequency (monthly, quarterly, etc.)
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'invoices' AND column_name = 'recurring_frequency') THEN
        ALTER TABLE invoices ADD COLUMN recurring_frequency VARCHAR(50);
    END IF;

END $$;

-- =====================================================
-- STEP 4: CREATE COMPREHENSIVE INDEXES
-- =====================================================

-- Basic Indexes
CREATE INDEX IF NOT EXISTS idx_invoices_user_id ON invoices(user_id);
CREATE INDEX IF NOT EXISTS idx_invoices_document_id ON invoices(document_id);
CREATE INDEX IF NOT EXISTS idx_invoices_category_id ON invoices(category_id);

-- Search Indexes
CREATE INDEX IF NOT EXISTS idx_invoices_vendor_name ON invoices(vendor_name);
CREATE INDEX IF NOT EXISTS idx_invoices_invoice_number ON invoices(invoice_number);
CREATE INDEX IF NOT EXISTS idx_invoices_invoice_date ON invoices(invoice_date DESC);

-- Amount Indexes
CREATE INDEX IF NOT EXISTS idx_invoices_total_amount ON invoices(total_amount);
CREATE INDEX IF NOT EXISTS idx_invoices_payment_status ON invoices(payment_status);

-- GST Indexes
CREATE INDEX IF NOT EXISTS idx_invoices_vendor_gstin ON invoices(vendor_gstin);
CREATE INDEX IF NOT EXISTS idx_invoices_place_of_supply ON invoices(place_of_supply);
CREATE INDEX IF NOT EXISTS idx_invoices_hsn_code ON invoices(hsn_code);
CREATE INDEX IF NOT EXISTS idx_invoices_sac_code ON invoices(sac_code);
CREATE INDEX IF NOT EXISTS idx_invoices_invoice_type ON invoices(invoice_type);

-- Date Indexes
CREATE INDEX IF NOT EXISTS idx_invoices_due_date ON invoices(due_date);
CREATE INDEX IF NOT EXISTS idx_invoices_payment_date ON invoices(payment_date);
CREATE INDEX IF NOT EXISTS idx_invoices_created_at ON invoices(created_at DESC);

-- JSONB Indexes (for flexible data)
CREATE INDEX IF NOT EXISTS idx_invoices_line_items ON invoices USING GIN (line_items);
CREATE INDEX IF NOT EXISTS idx_invoices_tags ON invoices USING GIN (tags);
CREATE INDEX IF NOT EXISTS idx_invoices_raw_data ON invoices USING GIN (raw_extracted_data);
CREATE INDEX IF NOT EXISTS idx_invoices_metadata ON invoices USING GIN (metadata);

-- Full Text Search (for vendor names)
CREATE INDEX IF NOT EXISTS idx_invoices_vendor_name_trgm ON invoices USING gin (vendor_name gin_trgm_ops);

-- =====================================================
-- STEP 5: UPDATE CONSTRAINTS
-- =====================================================

-- Drop old payment_status constraint if exists
ALTER TABLE invoices DROP CONSTRAINT IF EXISTS invoices_payment_status_check;

-- Add comprehensive payment_status constraint
ALTER TABLE invoices ADD CONSTRAINT invoices_payment_status_check 
    CHECK (payment_status IN ('paid', 'unpaid', 'partial', 'overdue', 'pending', 'cancelled', 'refunded'));

-- =====================================================
-- STEP 6: CREATE USEFUL VIEWS
-- =====================================================

-- Drop existing views to recreate them safely
DROP VIEW IF EXISTS invoice_essentials CASCADE;
DROP VIEW IF EXISTS gst_invoices CASCADE;
DROP VIEW IF EXISTS overdue_invoices CASCADE;
DROP VIEW IF EXISTS monthly_invoice_summary CASCADE;

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
    user_id,
    DATE_TRUNC('month', invoice_date) AS month,
    COUNT(*) AS invoice_count,
    SUM(total_amount) AS total_amount,
    SUM(COALESCE(cgst, 0) + COALESCE(sgst, 0) + COALESCE(igst, 0)) AS total_gst,
    COUNT(CASE WHEN payment_status = 'paid' THEN 1 END) AS paid_count,
    COUNT(CASE WHEN payment_status = 'unpaid' THEN 1 END) AS unpaid_count
FROM invoices
GROUP BY user_id, DATE_TRUNC('month', invoice_date);

-- =====================================================
-- STEP 7: ADD HELPFUL COMMENTS
-- =====================================================

COMMENT ON TABLE invoices IS 'Comprehensive invoice storage for ALL Indian invoice types: Retail, GST, Service, Manufacturing, Import/Export, B2B, B2C, Government, Healthcare, etc.';

COMMENT ON COLUMN invoices.vendor_gstin IS 'GST Identification Number (15 digits) - Required for GST invoices';
COMMENT ON COLUMN invoices.vendor_pan IS 'Permanent Account Number (10 chars) - For tax purposes';
COMMENT ON COLUMN invoices.vendor_tan IS 'Tax Deduction Account Number - For TDS';
COMMENT ON COLUMN invoices.cgst IS 'Central GST (intra-state) - Use with SGST';
COMMENT ON COLUMN invoices.sgst IS 'State GST (intra-state) - Use with CGST';
COMMENT ON COLUMN invoices.igst IS 'Integrated GST (inter-state) - Use alone, not with CGST/SGST';
COMMENT ON COLUMN invoices.ugst IS 'Union Territory GST - For UT transactions';
COMMENT ON COLUMN invoices.hsn_code IS 'Harmonized System Nomenclature - For goods';
COMMENT ON COLUMN invoices.sac_code IS 'Service Accounting Code - For services';
COMMENT ON COLUMN invoices.reverse_charge IS 'Reverse Charge Mechanism applicable';
COMMENT ON COLUMN invoices.invoice_type IS 'B2B, B2C, Export, SEZ, Deemed Export, etc.';
COMMENT ON COLUMN invoices.line_items IS 'Item-wise breakdown [{item, qty, rate, amount, hsn, tax}]';
COMMENT ON COLUMN invoices.raw_extracted_data IS 'Complete AI extraction output for debugging';
COMMENT ON COLUMN invoices.eway_bill_number IS 'E-way bill for goods transport above ₹50,000';
COMMENT ON COLUMN invoices.tds_amount IS 'Tax Deducted at Source amount';
COMMENT ON COLUMN invoices.tcs_amount IS 'Tax Collected at Source amount';

-- =====================================================
-- STEP 8: CREATE TRIGGERS
-- =====================================================

-- Function to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger for invoices
DROP TRIGGER IF EXISTS update_invoices_updated_at ON invoices;
CREATE TRIGGER update_invoices_updated_at
    BEFORE UPDATE ON invoices
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Trigger for users
DROP TRIGGER IF EXISTS update_users_updated_at ON users;
CREATE TRIGGER update_users_updated_at
    BEFORE UPDATE ON users
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Trigger for documents
DROP TRIGGER IF EXISTS update_documents_updated_at ON documents;
CREATE TRIGGER update_documents_updated_at
    BEFORE UPDATE ON documents
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Trigger for categories
DROP TRIGGER IF EXISTS update_categories_updated_at ON categories;
CREATE TRIGGER update_categories_updated_at
    BEFORE UPDATE ON categories
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- =====================================================
-- STEP 9: SUCCESS MESSAGE
-- =====================================================

DO $$ 
BEGIN
    RAISE NOTICE '';
    RAISE NOTICE '========================================';
    RAISE NOTICE '✅ COMPLETE INDIAN INVOICE SCHEMA READY!';
    RAISE NOTICE '========================================';
    RAISE NOTICE '';
    RAISE NOTICE '📊 TABLES CREATED/UPDATED:';
    RAISE NOTICE '   - users';
    RAISE NOTICE '   - documents';
    RAISE NOTICE '   - categories';
    RAISE NOTICE '   - invoices (75+ fields)';
    RAISE NOTICE '';
    RAISE NOTICE '🏷️ INVOICE FIELDS (75+ Total):';
    RAISE NOTICE '   REQUIRED: 4 fields (invoice_number, date, vendor_name, total_amount)';
    RAISE NOTICE '   OPTIONAL: 71+ fields';
    RAISE NOTICE '';
    RAISE NOTICE '✅ SUPPORTED INVOICE TYPES:';
    RAISE NOTICE '   - ✅ Simple Retail Bills (4 fields)';
    RAISE NOTICE '   - ✅ Restaurant Bills (5-7 fields)';
    RAISE NOTICE '   - ✅ GST Invoices Intra-State (CGST+SGST)';
    RAISE NOTICE '   - ✅ GST Invoices Inter-State (IGST)';
    RAISE NOTICE '   - ✅ Service Invoices (SAC code)';
    RAISE NOTICE '   - ✅ Manufacturing Invoices (HSN code)';
    RAISE NOTICE '   - ✅ E-commerce Invoices';
    RAISE NOTICE '   - ✅ Import Invoices (Bill of Entry)';
    RAISE NOTICE '   - ✅ Export Invoices (Shipping Bill)';
    RAISE NOTICE '   - ✅ B2B Invoices (with PO, Challan)';
    RAISE NOTICE '   - ✅ B2C Invoices';
    RAISE NOTICE '   - ✅ Government Invoices';
    RAISE NOTICE '   - ✅ Healthcare Invoices';
    RAISE NOTICE '   - ✅ Transport Invoices (E-way Bill, LR)';
    RAISE NOTICE '   - ✅ Credit/Debit Notes';
    RAISE NOTICE '   - ✅ Recurring Invoices';
    RAISE NOTICE '   - ✅ Pre-GST Invoices (VAT, Service Tax)';
    RAISE NOTICE '';
    RAISE NOTICE '📈 INDEXES: 20+ indexes for fast queries';
    RAISE NOTICE '👁️ VIEWS: 4 helpful views created';
    RAISE NOTICE '🔔 TRIGGERS: Auto-update timestamps';
    RAISE NOTICE '';
    RAISE NOTICE '========================================';
    RAISE NOTICE '🚀 YOUR DATABASE IS NOW FUTURE-PROOF!';
    RAISE NOTICE '========================================';
    RAISE NOTICE '';
    RAISE NOTICE '💡 NEXT STEPS:';
    RAISE NOTICE '1. Your intelligent AI extractor will only save fields that exist';
    RAISE NOTICE '2. Simple bills = 4 fields saved';
    RAISE NOTICE '3. Complex invoices = 20-30 fields saved';
    RAISE NOTICE '4. NO empty columns cluttering your database!';
    RAISE NOTICE '';
END $$;
