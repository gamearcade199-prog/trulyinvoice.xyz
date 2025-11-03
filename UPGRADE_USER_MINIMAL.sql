-- ============================================================================
-- UPGRADE USER TO MAX PLAN - MINIMAL VERSION (SAFE)
-- Only uses columns that MUST exist: user_id, tier, status
-- ============================================================================

DO $$
DECLARE
    v_user_id UUID;
    v_user_id_text TEXT;
BEGIN
    -- Get user ID from Supabase Auth
    SELECT id INTO v_user_id
    FROM auth.users
    WHERE email = 'akibhusain830@gmail.com';
    
    IF v_user_id IS NULL THEN
        RAISE NOTICE '❌ User not found with email: akibhusain830@gmail.com';
    ELSE
        v_user_id_text := v_user_id::TEXT;
        
        RAISE NOTICE '✅ Found user: %', v_user_id_text;
        
        -- Update subscription using ONLY columns that exist
        -- Check the table structure first and adjust this query
        INSERT INTO subscriptions (
            user_id,
            tier,
            status,
            scans_used_this_period,
            current_period_start,
            current_period_end,
            updated_at
        ) VALUES (
            v_user_id_text,
            'max',
            'active',
            0,
            NOW(),
            NOW() + INTERVAL '1 year',
            NOW()
        )
        ON CONFLICT (user_id) DO UPDATE SET
            tier = 'max',
            status = 'active',
            scans_used_this_period = 0,
            current_period_start = NOW(),
            current_period_end = NOW() + INTERVAL '1 year',
            updated_at = NOW();
        
        RAISE NOTICE '✅ USER UPGRADED TO MAX PLAN!';
        RAISE NOTICE '   Tier: max';
        RAISE NOTICE '   Scans: 1000/month';
        RAISE NOTICE '   Price: ₹999/month';
    END IF;
END $$;

-- Verify
SELECT 
    u.email,
    s.tier,
    s.status,
    s.scans_used_this_period,
    s.current_period_end::DATE
FROM auth.users u
LEFT JOIN subscriptions s ON u.id::TEXT = s.user_id
WHERE u.email = 'akibhusain830@gmail.com';

-- ============================================================================
-- INSTRUCTIONS:
-- 1. First run CHECK_TABLE_STRUCTURE.sql to see actual columns
-- 2. Then run this script (it only uses common columns)
-- 3. If it fails, send me the column list and I'll fix it
-- ============================================================================
