-- ============================================================================
-- UPGRADE USER TO MAX PLAN (₹999 - HIGHEST TIER)
-- User: akibhusain830@gmail.com
-- Plan: max (1000 scans/month, 90 days storage)
-- ============================================================================

-- Step 0: Add missing columns if they don't exist (safe to run multiple times)
DO $$ 
BEGIN
    -- Add billing_cycle if it doesn't exist
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.columns 
        WHERE table_name='subscriptions' AND column_name='billing_cycle'
    ) THEN
        ALTER TABLE subscriptions ADD COLUMN billing_cycle VARCHAR(20) DEFAULT 'monthly';
        RAISE NOTICE '✅ Added billing_cycle column';
    END IF;

    -- Add auto_renew if it doesn't exist
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.columns 
        WHERE table_name='subscriptions' AND column_name='auto_renew'
    ) THEN
        ALTER TABLE subscriptions ADD COLUMN auto_renew BOOLEAN DEFAULT TRUE;
        RAISE NOTICE '✅ Added auto_renew column';
    END IF;
END $$;

-- Step 1: Find and upgrade the user
DO $$
DECLARE
    v_user_id UUID;
BEGIN
    -- Get user ID from Supabase Auth (UUID type)
    SELECT id INTO v_user_id
    FROM auth.users
    WHERE email = 'akibhusain830@gmail.com';
    
    IF v_user_id IS NULL THEN
        RAISE NOTICE '❌ User not found with email: akibhusain830@gmail.com';
        RAISE NOTICE '   Please ensure the user has registered.';
        RAISE NOTICE '   Run this to check: SELECT email FROM auth.users WHERE email LIKE ''%%akib%%'';';
    ELSE
        RAISE NOTICE '✅ Found user!';
        RAISE NOTICE '   📧 Email: akibhusain830@gmail.com';
        RAISE NOTICE '   🆔 User ID: %', v_user_id;
        
        -- Step 2: Update or insert subscription to MAX plan (user_id is UUID type)
        INSERT INTO subscriptions (
            user_id,
            tier,
            status,
            scans_used_this_period,
            current_period_start,
            current_period_end,
            created_at,
            updated_at
        ) VALUES (
            v_user_id,
            'max',
            'active',
            0,
            NOW(),
            NOW() + INTERVAL '1 year',
            NOW(),
            NOW()
        )
        ON CONFLICT (user_id) DO UPDATE SET
            tier = 'max',
            status = 'active',
            scans_used_this_period = 0,
            current_period_start = NOW(),
            current_period_end = NOW() + INTERVAL '1 year',
            updated_at = NOW();
        
        RAISE NOTICE '';
        RAISE NOTICE '🎉 ============================================';
        RAISE NOTICE '✅ USER UPGRADED TO MAX PLAN!';
        RAISE NOTICE '============================================';
        RAISE NOTICE '';
        RAISE NOTICE '📊 PLAN DETAILS:';
        RAISE NOTICE '   🏆 Tier: MAX (Highest/Premium)';
        RAISE NOTICE '   � Price: ₹999/month';
        RAISE NOTICE '   📈 Scans per month: 1000 (maximum)';
        RAISE NOTICE '   💾 Storage: 90 days';
        RAISE NOTICE '   📤 Bulk upload: 100 files at once';
        RAISE NOTICE '   🎯 AI Accuracy: 99.5%%';
        RAISE NOTICE '   💳 Billing: Yearly';
        RAISE NOTICE '   📅 Valid until: %', NOW() + INTERVAL '1 year';
        RAISE NOTICE '   🔄 Auto-renew: Enabled';
        RAISE NOTICE '';
        RAISE NOTICE '🎁 FEATURES UNLOCKED:';
        RAISE NOTICE '   ✅ 1000 invoice scans per month';
        RAISE NOTICE '   ✅ 99.5%% AI extraction accuracy';
        RAISE NOTICE '   ✅ Bulk upload up to 100 files';
        RAISE NOTICE '   ✅ Custom integrations';
        RAISE NOTICE '   ✅ 24/7 priority support';
        RAISE NOTICE '   ✅ 90-day data storage';
        RAISE NOTICE '   ✅ Custom workflows';
        RAISE NOTICE '   ✅ Excel & CSV exports';
        RAISE NOTICE '   ✅ Advanced GST validation';
        RAISE NOTICE '';
    END IF;
END $$;

-- Step 3: Verify the upgrade
SELECT 
    '✅ VERIFICATION' as status,
    u.email,
    s.tier,
    s.status,
    s.scans_used_this_period as scans_used,
    s.billing_cycle,
    s.current_period_start::DATE as period_start,
    s.current_period_end::DATE as period_end,
    s.auto_renew
FROM auth.users u
LEFT JOIN subscriptions s ON u.id = s.user_id
WHERE u.email = 'akibhusain830@gmail.com';

-- ============================================================================
-- MAX PLAN COMPLETE FEATURE LIST
-- ============================================================================
-- 💎 TIER: MAX (₹999/month)
-- ============================================================================
-- 
-- USAGE LIMITS:
-- ✅ 1000 invoice scans per month (HIGHEST)
-- ✅ 90 days data storage
-- ✅ 100 files bulk upload at once
-- 
-- AI & ACCURACY:
-- ✅ 99.5% AI extraction accuracy (BEST)
-- ✅ Advanced GST validation with real-time checks
-- ✅ Custom workflows and automation
-- 
-- EXPORTS:
-- ✅ Excel export with formulas
-- ✅ CSV export for ERPs
-- ✅ Custom export templates
-- ✅ Bulk export capability
-- 
-- SUPPORT:
-- ✅ 24/7 priority support
-- ✅ Dedicated account manager (on request)
-- ✅ Priority processing queue
-- ✅ Direct phone/chat support
-- 
-- INTEGRATIONS:
-- ✅ Custom API integrations
-- ✅ Tally integration
-- ✅ Zoho Books integration
-- ✅ QuickBooks integration
-- ✅ Custom webhook support
-- 
-- RATE LIMITS:
-- ✅ 200 API requests per minute
-- ✅ 5000 API requests per hour
-- ✅ 20000 API requests per day
-- 
-- ============================================================================
-- 🎉 CONGRATULATIONS! YOU NOW HAVE THE ULTIMATE PLAN! 🎉
-- ============================================================================

