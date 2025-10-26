# Add Export Template Preference to Users Table

This SQL script adds an `export_template` column to the `users` table to store each user's preferred Excel export format.

## To Run This Script:

1. Go to your Supabase Dashboard
2. Navigate to SQL Editor
3. Copy and paste the following SQL:

```sql
-- Add export template preference to users table
ALTER TABLE users ADD COLUMN IF NOT EXISTS export_template VARCHAR(20) DEFAULT 'simple' CHECK (export_template IN ('simple', 'accountant', 'analyst', 'compliance'));

-- Update existing users to have 'simple' as default
UPDATE users SET export_template = 'simple' WHERE export_template IS NULL;

-- Add comment
COMMENT ON COLUMN users.export_template IS 'User preferred export template: simple (2 sheets), accountant (5 sheets), analyst, or compliance';
```

4. Click "Run" to execute the script

## What This Does:

- Adds an `export_template` column to the `users` table
- Sets the default value to 'simple' (2 sheets)
- Restricts values to valid template options
- Updates existing users to have the default preference
- Adds a descriptive comment

## Next Steps:

After running this SQL, you can update the frontend code to save/load preferences from the database instead of localStorage. For now, the app uses localStorage as a temporary solution.