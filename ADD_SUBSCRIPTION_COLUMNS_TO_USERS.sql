-- Add subscription columns to users table
ALTER TABLE users
ADD COLUMN plan TEXT DEFAULT 'Free',
ADD COLUMN subscription_status TEXT DEFAULT 'active',
ADD COLUMN plan_expiry_date TIMESTAMPTZ;

-- Create a function to get the current plan for a user
CREATE OR REPLACE FUNCTION get_user_plan(user_id_in uuid)
RETURNS TEXT AS $$
DECLARE
  current_plan TEXT;
BEGIN
  SELECT plan INTO current_plan FROM users WHERE id = user_id_in;
  RETURN current_plan;
END;
$$ LANGUAGE plpgsql;
