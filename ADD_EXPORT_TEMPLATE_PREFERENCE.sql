-- Add export template preference to users table
ALTER TABLE users ADD COLUMN IF NOT EXISTS export_template VARCHAR(20) DEFAULT 'simple' CHECK (export_template IN ('simple', 'accountant', 'analyst', 'compliance'));

-- Update existing users to have 'simple' as default
UPDATE users SET export_template = 'simple' WHERE export_template IS NULL;

-- Add comment
COMMENT ON COLUMN users.export_template IS 'User preferred export template: simple (2 sheets), accountant (5 sheets), analyst, or compliance';