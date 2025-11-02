-- ============================================================================
-- WEBHOOK LOGS TABLE MIGRATION
-- Creates table for tracking webhook events and retries
-- Run this in Supabase SQL Editor
-- URL: https://supabase.com/dashboard/project/ldvwxqluaheuhbycdpwn/sql
-- ============================================================================

-- Create webhook_logs table for tracking all webhook events
CREATE TABLE IF NOT EXISTS webhook_logs (
    id SERIAL PRIMARY KEY,
    event_id VARCHAR(255) UNIQUE NOT NULL,  -- Razorpay event ID for idempotency
    event_type VARCHAR(100) NOT NULL,        -- subscription.charged, etc.
    subscription_id VARCHAR(255),            -- Razorpay subscription ID
    user_id VARCHAR(255),                    -- User ID (extracted from notes)
    payload JSONB NOT NULL,                  -- Full webhook payload
    signature VARCHAR(255) NOT NULL,         -- Webhook signature
    status VARCHAR(50) NOT NULL DEFAULT 'pending',  -- pending, processed, failed, retrying
    attempt_count INTEGER NOT NULL DEFAULT 0,       -- Number of processing attempts
    last_attempt_at TIMESTAMP,               -- Last processing attempt
    error_message TEXT,                      -- Error details if failed
    processed_at TIMESTAMP,                  -- When successfully processed
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);

-- Create indexes for performance
CREATE INDEX IF NOT EXISTS idx_webhook_logs_event_id ON webhook_logs(event_id);
CREATE INDEX IF NOT EXISTS idx_webhook_logs_subscription_id ON webhook_logs(subscription_id) 
    WHERE subscription_id IS NOT NULL;
CREATE INDEX IF NOT EXISTS idx_webhook_logs_status ON webhook_logs(status);
CREATE INDEX IF NOT EXISTS idx_webhook_logs_created_at ON webhook_logs(created_at);
CREATE INDEX IF NOT EXISTS idx_webhook_logs_event_type ON webhook_logs(event_type);

-- Create function to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_webhook_logs_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Create trigger to auto-update updated_at
DROP TRIGGER IF EXISTS trigger_update_webhook_logs_updated_at ON webhook_logs;
CREATE TRIGGER trigger_update_webhook_logs_updated_at
    BEFORE UPDATE ON webhook_logs
    FOR EACH ROW
    EXECUTE FUNCTION update_webhook_logs_updated_at();

-- Verify migration
DO $$
BEGIN
    RAISE NOTICE '============================================';
    RAISE NOTICE 'WEBHOOK LOGS TABLE MIGRATION';
    RAISE NOTICE '============================================';
    
    IF EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'webhook_logs') THEN
        RAISE NOTICE '✅ webhook_logs table created successfully!';
    ELSE
        RAISE NOTICE '❌ webhook_logs table creation failed';
    END IF;
    
    RAISE NOTICE '============================================';
END $$;

-- ============================================================================
-- MIGRATION COMPLETE
-- webhook_logs table ready for webhook tracking and retry logic
-- ============================================================================
