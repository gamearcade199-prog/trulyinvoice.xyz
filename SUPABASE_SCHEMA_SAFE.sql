-- =====================================================
-- TrulyInvoice - Supabase Database Schema (SAFE VERSION)
-- =====================================================
-- This version uses DROP IF EXISTS to avoid errors
-- =====================================================

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- =====================================================
-- Drop existing triggers first
-- =====================================================
DROP TRIGGER IF EXISTS update_users_updated_at ON users;
DROP TRIGGER IF EXISTS update_subscriptions_updated_at ON subscriptions;
DROP TRIGGER IF EXISTS update_documents_updated_at ON documents;
DROP TRIGGER IF EXISTS update_invoices_updated_at ON invoices;
DROP TRIGGER IF EXISTS update_categories_updated_at ON categories;
DROP TRIGGER IF EXISTS create_user_default_categories ON users;
DROP TRIGGER IF EXISTS create_user_default_subscription ON users;

-- Drop existing functions
DROP FUNCTION IF EXISTS update_updated_at_column();
DROP FUNCTION IF EXISTS create_default_categories();
DROP FUNCTION IF EXISTS create_default_subscription();

-- =====================================================
-- Update documents table to add missing columns
-- =====================================================
ALTER TABLE documents 
    ADD COLUMN IF NOT EXISTS file_type VARCHAR(100),
    ADD COLUMN IF NOT EXISTS storage_path VARCHAR(500),
    ADD COLUMN IF NOT EXISTS file_url TEXT;

-- Remove NOT NULL constraints that might cause issues
ALTER TABLE documents 
    ALTER COLUMN file_path DROP NOT NULL;

-- Update column name if it exists with old name
DO $$ 
BEGIN
    IF EXISTS (
        SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'documents' AND column_name = 'file_path'
    ) THEN
        ALTER TABLE documents RENAME COLUMN file_path TO storage_path;
    END IF;
EXCEPTION WHEN OTHERS THEN
    -- Column might already be renamed, ignore error
    NULL;
END $$;

-- Update column name for mime_type
DO $$ 
BEGIN
    IF EXISTS (
        SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'documents' AND column_name = 'mime_type'
    ) THEN
        ALTER TABLE documents RENAME COLUMN mime_type TO file_type;
    END IF;
EXCEPTION WHEN OTHERS THEN
    -- Column might already be renamed, ignore error
    NULL;
END $$;

-- =====================================================
-- TRIGGERS FOR UPDATED_AT
-- =====================================================

-- Function to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Apply to all tables
CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON users
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_subscriptions_updated_at BEFORE UPDATE ON subscriptions
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_documents_updated_at BEFORE UPDATE ON documents
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_invoices_updated_at BEFORE UPDATE ON invoices
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_categories_updated_at BEFORE UPDATE ON categories
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- =====================================================
-- INSERT DEFAULT CATEGORIES FOR NEW USERS
-- =====================================================

-- Function to create default categories for new users
CREATE OR REPLACE FUNCTION create_default_categories()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO categories (user_id, name, description, color, is_default) VALUES
        (NEW.id, 'Office Supplies', 'Stationery, printer ink, etc.', '#3b82f6', true),
        (NEW.id, 'Software & SaaS', 'Software licenses and subscriptions', '#8b5cf6', true),
        (NEW.id, 'Travel & Transport', 'Business travel, fuel, cab rides', '#ec4899', true),
        (NEW.id, 'Utilities', 'Electricity, internet, phone bills', '#f59e0b', true),
        (NEW.id, 'Professional Services', 'Consultants, legal, accounting', '#10b981', true),
        (NEW.id, 'Marketing', 'Advertising, promotional materials', '#ef4444', true),
        (NEW.id, 'Equipment', 'Computers, furniture, machinery', '#6366f1', true),
        (NEW.id, 'Rent & Lease', 'Office rent, equipment lease', '#14b8a6', true),
        (NEW.id, 'Inventory', 'Raw materials, finished goods', '#f97316', true),
        (NEW.id, 'Other', 'Miscellaneous expenses', '#64748b', true)
    ON CONFLICT (user_id, name) DO NOTHING;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Trigger to create default categories when user is created
CREATE TRIGGER create_user_default_categories
    AFTER INSERT ON users
    FOR EACH ROW
    EXECUTE FUNCTION create_default_categories();

-- =====================================================
-- CREATE DEFAULT SUBSCRIPTION FOR NEW USERS
-- =====================================================

-- Function to create starter subscription for new users
CREATE OR REPLACE FUNCTION create_default_subscription()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO subscriptions (user_id, tier, status, scans_used_this_period, current_period_start, current_period_end)
    VALUES (
        NEW.id,
        'starter',
        'active',
        0,
        CURRENT_TIMESTAMP,
        CURRENT_TIMESTAMP + INTERVAL '1 month'
    )
    ON CONFLICT (user_id) DO NOTHING;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Trigger to create default subscription when user is created
CREATE TRIGGER create_user_default_subscription
    AFTER INSERT ON users
    FOR EACH ROW
    EXECUTE FUNCTION create_default_subscription();

-- =====================================================
-- COMPLETED!
-- =====================================================
