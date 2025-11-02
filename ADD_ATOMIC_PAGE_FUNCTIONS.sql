-- ============================================
-- CRITICAL ROBUSTNESS FIXES FOR PAGE TRACKING
-- ============================================

-- 1. ATOMIC INCREMENT FUNCTION (Prevents Race Conditions)
CREATE OR REPLACE FUNCTION increment_page_usage(
  user_id_param UUID,
  pages_to_add INTEGER
)
RETURNS INTEGER AS $$
DECLARE
  new_usage INTEGER;
BEGIN
  -- Atomically increment pages_used_this_month
  UPDATE users
  SET pages_used_this_month = pages_used_this_month + pages_to_add
  WHERE id = user_id_param
  RETURNING pages_used_this_month INTO new_usage;
  
  -- Return the new usage count
  RETURN new_usage;
END;
$$ LANGUAGE plpgsql;

-- 2. RESERVE PAGE QUOTA FUNCTION (Pre-reserve before processing)
CREATE OR REPLACE FUNCTION reserve_page_quota(
  user_id_param UUID,
  pages_needed INTEGER,
  plan_limit INTEGER
)
RETURNS JSON AS $$
DECLARE
  current_usage INTEGER;
  new_usage INTEGER;
  pages_remaining INTEGER;
BEGIN
  -- Get current usage
  SELECT pages_used_this_month INTO current_usage
  FROM users WHERE id = user_id_param;
  
  -- If NULL, initialize to 0
  IF current_usage IS NULL THEN
    current_usage := 0;
  END IF;
  
  -- Calculate remaining pages
  pages_remaining := plan_limit - current_usage;
  
  -- Check if enough quota
  IF pages_remaining < pages_needed THEN
    RETURN json_build_object(
      'success', false,
      'error', 'insufficient_quota',
      'pages_needed', pages_needed,
      'pages_remaining', pages_remaining,
      'current_usage', current_usage
    );
  END IF;
  
  -- Atomically increment (reserve quota)
  UPDATE users
  SET pages_used_this_month = pages_used_this_month + pages_needed
  WHERE id = user_id_param
  RETURNING pages_used_this_month INTO new_usage;
  
  RETURN json_build_object(
    'success', true,
    'pages_reserved', pages_needed,
    'new_usage', new_usage,
    'pages_remaining', plan_limit - new_usage
  );
END;
$$ LANGUAGE plpgsql;

-- 3. ROLLBACK PAGE QUOTA FUNCTION (Rollback on processing failure)
CREATE OR REPLACE FUNCTION rollback_page_quota(
  user_id_param UUID,
  pages_to_rollback INTEGER
)
RETURNS INTEGER AS $$
DECLARE
  new_usage INTEGER;
BEGIN
  -- Atomically decrement, ensuring it doesn't go below 0
  UPDATE users
  SET pages_used_this_month = GREATEST(0, pages_used_this_month - pages_to_rollback)
  WHERE id = user_id_param
  RETURNING pages_used_this_month INTO new_usage;
  
  RETURN new_usage;
END;
$$ LANGUAGE plpgsql;

-- 4. CHECK AND RESET BILLING PERIOD (Auto-reset if expired)
CREATE OR REPLACE FUNCTION check_and_reset_billing_period(
  user_id_param UUID
)
RETURNS JSON AS $$
DECLARE
  billing_start TIMESTAMP;
  months_passed INTEGER;
  was_reset BOOLEAN := false;
BEGIN
  -- Get billing period start
  SELECT billing_period_start INTO billing_start
  FROM users WHERE id = user_id_param;
  
  -- If NULL, initialize to now
  IF billing_start IS NULL THEN
    UPDATE users
    SET billing_period_start = NOW(),
        pages_used_this_month = 0
    WHERE id = user_id_param;
    
    RETURN json_build_object(
      'was_reset', true,
      'reason', 'initialized',
      'new_period_start', NOW()
    );
  END IF;
  
  -- Calculate months passed
  months_passed := EXTRACT(YEAR FROM AGE(NOW(), billing_start)) * 12 +
                   EXTRACT(MONTH FROM AGE(NOW(), billing_start));
  
  -- If 1+ months passed, reset
  IF months_passed >= 1 THEN
    UPDATE users
    SET pages_used_this_month = 0,
        billing_period_start = NOW()
    WHERE id = user_id_param;
    
    was_reset := true;
  END IF;
  
  RETURN json_build_object(
    'was_reset', was_reset,
    'months_passed', months_passed,
    'new_period_start', CASE WHEN was_reset THEN NOW() ELSE billing_start END
  );
END;
$$ LANGUAGE plpgsql;

-- 5. GET USER QUOTA STATUS (All-in-one status check)
CREATE OR REPLACE FUNCTION get_user_quota_status(
  user_id_param UUID
)
RETURNS JSON AS $$
DECLARE
  user_plan TEXT;
  pages_used INTEGER;
  billing_start TIMESTAMP;
  plan_limit INTEGER;
  pages_remaining INTEGER;
BEGIN
  -- Get user data
  SELECT 
    plan,
    pages_used_this_month,
    billing_period_start
  INTO user_plan, pages_used, billing_start
  FROM users WHERE id = user_id_param;
  
  -- Initialize if NULL
  IF pages_used IS NULL THEN
    pages_used := 0;
  END IF;
  
  -- Determine plan limit
  plan_limit := CASE user_plan
    WHEN 'Free' THEN 10
    WHEN 'Basic' THEN 100
    WHEN 'Pro' THEN 500
    WHEN 'Ultra' THEN 2000
    WHEN 'Max' THEN 10000
    ELSE 10
  END;
  
  pages_remaining := plan_limit - pages_used;
  
  RETURN json_build_object(
    'plan', user_plan,
    'plan_limit', plan_limit,
    'pages_used', pages_used,
    'pages_remaining', pages_remaining,
    'billing_period_start', billing_start,
    'has_quota', pages_remaining > 0
  );
END;
$$ LANGUAGE plpgsql;

-- Grant execute permissions
GRANT EXECUTE ON FUNCTION increment_page_usage(UUID, INTEGER) TO authenticated;
GRANT EXECUTE ON FUNCTION reserve_page_quota(UUID, INTEGER, INTEGER) TO authenticated;
GRANT EXECUTE ON FUNCTION rollback_page_quota(UUID, INTEGER) TO authenticated;
GRANT EXECUTE ON FUNCTION check_and_reset_billing_period(UUID) TO authenticated;
GRANT EXECUTE ON FUNCTION get_user_quota_status(UUID) TO authenticated;

-- Create indexes for performance
CREATE INDEX IF NOT EXISTS idx_users_pages_used ON users(pages_used_this_month);
CREATE INDEX IF NOT EXISTS idx_users_plan_pages ON users(plan, pages_used_this_month);

COMMENT ON FUNCTION increment_page_usage IS 'Atomically increment page usage count (prevents race conditions)';
COMMENT ON FUNCTION reserve_page_quota IS 'Pre-reserve page quota before processing (prevents free retries on failure)';
COMMENT ON FUNCTION rollback_page_quota IS 'Rollback reserved quota if processing fails';
COMMENT ON FUNCTION check_and_reset_billing_period IS 'Check if billing period expired and auto-reset if needed';
COMMENT ON FUNCTION get_user_quota_status IS 'Get complete quota status for a user';
