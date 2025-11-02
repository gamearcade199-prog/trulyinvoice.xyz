-- Add page tracking columns to users table
-- This enables the 1 page = 1 scan quota system

-- Add columns for monthly page tracking
ALTER TABLE users 
ADD COLUMN IF NOT EXISTS pages_used_this_month INTEGER DEFAULT 0,
ADD COLUMN IF NOT EXISTS billing_period_start TIMESTAMP DEFAULT NOW();

-- Add index for faster queries
CREATE INDEX IF NOT EXISTS idx_users_billing_period ON users(billing_period_start);

-- Create function to reset monthly page usage
CREATE OR REPLACE FUNCTION reset_monthly_page_usage()
RETURNS void AS $$
BEGIN
  UPDATE users 
  SET pages_used_this_month = 0,
      billing_period_start = NOW()
  WHERE billing_period_start < NOW() - INTERVAL '1 month';
  
  RAISE NOTICE 'Monthly page usage reset for % users', 
    (SELECT COUNT(*) FROM users WHERE billing_period_start >= NOW() - INTERVAL '1 month');
END;
$$ LANGUAGE plpgsql;

-- Optional: Schedule monthly reset via pg_cron extension
-- Uncomment if pg_cron is installed:
-- SELECT cron.schedule('reset-monthly-pages', '0 0 1 * *', 'SELECT reset_monthly_page_usage()');

-- Or run manually once per month:
-- SELECT reset_monthly_page_usage();

COMMENT ON COLUMN users.pages_used_this_month IS 'Number of PDF pages processed this billing month (1 page = 1 scan)';
COMMENT ON COLUMN users.billing_period_start IS 'Start date of current billing period for page quota tracking';
