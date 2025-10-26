-- =====================================================
-- TrulyInvoice - Supabase Database Schema
-- =====================================================
-- Run this in Supabase SQL Editor
-- =====================================================

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- =====================================================
-- 1. USERS TABLE
-- =====================================================
CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email VARCHAR(255) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    full_name VARCHAR(255),
    company_name VARCHAR(255),
    is_active BOOLEAN DEFAULT true,
    is_verified BOOLEAN DEFAULT false,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Index for faster email lookups
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);

-- =====================================================
-- 2. SUBSCRIPTIONS TABLE
-- =====================================================
CREATE TABLE IF NOT EXISTS subscriptions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    tier VARCHAR(50) NOT NULL DEFAULT 'starter' CHECK (tier IN ('starter', 'pro', 'business')),
    status VARCHAR(50) DEFAULT 'active' CHECK (status IN ('active', 'cancelled', 'expired')),
    
    -- Usage tracking
    scans_used_this_period INTEGER DEFAULT 0,
    current_period_start TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    current_period_end TIMESTAMP DEFAULT CURRENT_TIMESTAMP + INTERVAL '1 month',
    
    -- Payment info
    razorpay_subscription_id VARCHAR(255),
    razorpay_customer_id VARCHAR(255),
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT unique_user_subscription UNIQUE (user_id)
);

-- Index for faster user lookups
CREATE INDEX IF NOT EXISTS idx_subscriptions_user_id ON subscriptions(user_id);
CREATE INDEX IF NOT EXISTS idx_subscriptions_tier ON subscriptions(tier);

-- =====================================================
-- 3. CATEGORIES TABLE (MOVED BEFORE INVOICES)
-- =====================================================
CREATE TABLE IF NOT EXISTS categories (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    color VARCHAR(7) DEFAULT '#6366f1',
    is_default BOOLEAN DEFAULT false,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT unique_user_category UNIQUE (user_id, name)
);

-- Index
CREATE INDEX IF NOT EXISTS idx_categories_user_id ON categories(user_id);

-- =====================================================
-- 4. DOCUMENTS TABLE
-- =====================================================
CREATE TABLE IF NOT EXISTS documents (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    
    -- File info
    filename VARCHAR(255) NOT NULL,
    file_path VARCHAR(500) NOT NULL,
    file_size INTEGER,
    mime_type VARCHAR(100),
    
    -- Processing status
    status VARCHAR(50) DEFAULT 'uploaded' CHECK (status IN ('uploaded', 'processing', 'completed', 'failed')),
    
    -- AI extraction metadata
    confidence_score DECIMAL(5,4),
    used_fallback_model BOOLEAN DEFAULT false,
    processing_time_ms INTEGER,
    error_message TEXT,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes
CREATE INDEX IF NOT EXISTS idx_documents_user_id ON documents(user_id);
CREATE INDEX IF NOT EXISTS idx_documents_status ON documents(status);
CREATE INDEX IF NOT EXISTS idx_documents_created_at ON documents(created_at DESC);

-- =====================================================
-- 5. INVOICES TABLE
-- =====================================================
CREATE TABLE IF NOT EXISTS invoices (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    document_id UUID REFERENCES documents(id) ON DELETE SET NULL,
    
    -- Vendor Information
    vendor_name VARCHAR(255),
    vendor_address TEXT,
    vendor_gstin VARCHAR(15),
    vendor_pan VARCHAR(10),
    vendor_email VARCHAR(255),
    vendor_phone VARCHAR(20),
    
    -- Invoice Details
    invoice_number VARCHAR(100),
    invoice_date DATE,
    due_date DATE,
    po_number VARCHAR(100),
    
    -- Financial Information
    subtotal DECIMAL(15,2),
    cgst DECIMAL(15,2),
    sgst DECIMAL(15,2),
    igst DECIMAL(15,2),
    cess DECIMAL(15,2),
    discount DECIMAL(15,2),
    total_amount DECIMAL(15,2) NOT NULL,
    
    -- Currency
    currency VARCHAR(10) DEFAULT 'INR',
    
    -- Payment Information
    payment_terms VARCHAR(255),
    payment_status VARCHAR(50) DEFAULT 'unpaid' CHECK (payment_status IN ('paid', 'unpaid', 'partial', 'overdue')),
    payment_method VARCHAR(100),
    
    -- Line Items (stored as JSONB for flexibility)
    line_items JSONB DEFAULT '[]'::jsonb,
    
    -- Raw extracted data (for debugging and reprocessing)
    raw_extracted_data JSONB,
    
    -- Notes
    notes TEXT,
    
    -- Metadata
    category_id UUID REFERENCES categories(id) ON DELETE SET NULL,
    tags TEXT[],
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for better query performance
CREATE INDEX IF NOT EXISTS idx_invoices_user_id ON invoices(user_id);
CREATE INDEX IF NOT EXISTS idx_invoices_vendor_name ON invoices(vendor_name);
CREATE INDEX IF NOT EXISTS idx_invoices_invoice_number ON invoices(invoice_number);
CREATE INDEX IF NOT EXISTS idx_invoices_invoice_date ON invoices(invoice_date DESC);
CREATE INDEX IF NOT EXISTS idx_invoices_total_amount ON invoices(total_amount);
CREATE INDEX IF NOT EXISTS idx_invoices_payment_status ON invoices(payment_status);
CREATE INDEX IF NOT EXISTS idx_invoices_category_id ON invoices(category_id);
CREATE INDEX IF NOT EXISTS idx_invoices_line_items ON invoices USING GIN (line_items);

-- =====================================================
-- 6. USAGE LOGS TABLE (for analytics & debugging)
-- =====================================================
CREATE TABLE IF NOT EXISTS usage_logs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    action VARCHAR(100) NOT NULL,
    resource_type VARCHAR(50),
    resource_id UUID,
    metadata JSONB,
    ip_address INET,
    user_agent TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes
CREATE INDEX IF NOT EXISTS idx_usage_logs_user_id ON usage_logs(user_id);
CREATE INDEX IF NOT EXISTS idx_usage_logs_action ON usage_logs(action);
CREATE INDEX IF NOT EXISTS idx_usage_logs_created_at ON usage_logs(created_at DESC);

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
        (NEW.id, 'Other', 'Miscellaneous expenses', '#64748b', true);
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
    );
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Trigger to create default subscription when user is created
CREATE TRIGGER create_user_default_subscription
    AFTER INSERT ON users
    FOR EACH ROW
    EXECUTE FUNCTION create_default_subscription();

-- =====================================================
-- ROW LEVEL SECURITY (RLS) - IMPORTANT FOR SUPABASE
-- =====================================================

-- Enable RLS on all tables
ALTER TABLE users ENABLE ROW LEVEL SECURITY;
ALTER TABLE subscriptions ENABLE ROW LEVEL SECURITY;
ALTER TABLE documents ENABLE ROW LEVEL SECURITY;
ALTER TABLE invoices ENABLE ROW LEVEL SECURITY;
ALTER TABLE categories ENABLE ROW LEVEL SECURITY;
ALTER TABLE usage_logs ENABLE ROW LEVEL SECURITY;

-- Users can only see their own data
CREATE POLICY "Users can view own data" ON users
    FOR SELECT USING (auth.uid() = id);

CREATE POLICY "Users can update own data" ON users
    FOR UPDATE USING (auth.uid() = id);

-- Subscriptions policies
CREATE POLICY "Users can view own subscription" ON subscriptions
    FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users can update own subscription" ON subscriptions
    FOR UPDATE USING (auth.uid() = user_id);

-- Documents policies
CREATE POLICY "Users can view own documents" ON documents
    FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users can insert own documents" ON documents
    FOR INSERT WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update own documents" ON documents
    FOR UPDATE USING (auth.uid() = user_id);

CREATE POLICY "Users can delete own documents" ON documents
    FOR DELETE USING (auth.uid() = user_id);

-- Invoices policies
CREATE POLICY "Users can view own invoices" ON invoices
    FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users can insert own invoices" ON invoices
    FOR INSERT WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update own invoices" ON invoices
    FOR UPDATE USING (auth.uid() = user_id);

CREATE POLICY "Users can delete own invoices" ON invoices
    FOR DELETE USING (auth.uid() = user_id);

-- Categories policies
CREATE POLICY "Users can view own categories" ON categories
    FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users can insert own categories" ON categories
    FOR INSERT WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update own categories" ON categories
    FOR UPDATE USING (auth.uid() = user_id);

CREATE POLICY "Users can delete own categories" ON categories
    FOR DELETE USING (auth.uid() = user_id);

-- Usage logs policies
CREATE POLICY "Users can view own logs" ON usage_logs
    FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users can insert own logs" ON usage_logs
    FOR INSERT WITH CHECK (auth.uid() = user_id);

-- =====================================================
-- STORAGE BUCKET FOR DOCUMENTS (Run in Supabase Dashboard)
-- =====================================================

-- Note: This needs to be done via Supabase Dashboard > Storage
-- Create a bucket named: "invoice-documents"
-- Set it to private (not public)
-- Then apply this storage policy:

/*
-- Storage policies (apply after creating bucket in dashboard)
CREATE POLICY "Users can upload own documents" ON storage.objects
    FOR INSERT WITH CHECK (
        bucket_id = 'invoice-documents' AND
        auth.uid()::text = (storage.foldername(name))[1]
    );

CREATE POLICY "Users can view own documents" ON storage.objects
    FOR SELECT USING (
        bucket_id = 'invoice-documents' AND
        auth.uid()::text = (storage.foldername(name))[1]
    );

CREATE POLICY "Users can delete own documents" ON storage.objects
    FOR DELETE USING (
        bucket_id = 'invoice-documents' AND
        auth.uid()::text = (storage.foldername(name))[1]
    );
*/

-- =====================================================
-- HELPER VIEWS FOR ANALYTICS
-- =====================================================

-- Monthly invoice summary per user
CREATE OR REPLACE VIEW monthly_invoice_summary AS
SELECT 
    user_id,
    DATE_TRUNC('month', invoice_date) as month,
    COUNT(*) as invoice_count,
    SUM(total_amount) as total_amount,
    AVG(total_amount) as avg_amount,
    COUNT(CASE WHEN payment_status = 'paid' THEN 1 END) as paid_count,
    COUNT(CASE WHEN payment_status = 'unpaid' THEN 1 END) as unpaid_count
FROM invoices
WHERE invoice_date IS NOT NULL
GROUP BY user_id, DATE_TRUNC('month', invoice_date);

-- User subscription usage summary
CREATE OR REPLACE VIEW user_subscription_usage AS
SELECT 
    u.id as user_id,
    u.email,
    u.full_name,
    s.tier,
    s.scans_used_this_period,
    CASE 
        WHEN s.tier = 'starter' THEN 30
        WHEN s.tier = 'pro' THEN 200
        WHEN s.tier = 'business' THEN 750
    END as scan_limit,
    s.current_period_start,
    s.current_period_end,
    COUNT(d.id) as total_documents
FROM users u
LEFT JOIN subscriptions s ON u.id = s.user_id
LEFT JOIN documents d ON u.id = d.user_id
GROUP BY u.id, u.email, u.full_name, s.tier, s.scans_used_this_period, s.current_period_start, s.current_period_end;

-- =====================================================
-- COMPLETED!
-- =====================================================
-- Your database schema is now ready!
-- 
-- Next steps:
-- 1. Go to Supabase Dashboard > SQL Editor
-- 2. Paste and run this entire SQL script
-- 3. Go to Storage and create bucket "invoice-documents"
-- 4. Update your .env file with Supabase credentials
-- =====================================================
