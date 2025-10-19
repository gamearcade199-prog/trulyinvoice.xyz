import { serve } from 'https://deno.land/std@0.168.0/http/server.ts'
import { createClient } from 'https://esm.sh/@supabase/supabase-js@2'

const corsHeaders = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Headers': 'authorization, x-client-info, apikey, content-type',
  'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
}

serve(async (req) => {
  // Handle CORS preflight requests
  if (req.method === 'OPTIONS') {
    return new Response('ok', { headers: corsHeaders })
  }

  try {
    // Get auth user
    const authorization = req.headers.get('Authorization')
    if (!authorization) {
      throw new Error('No authorization header')
    }

    // Create Supabase client
    const supabaseClient = createClient(
      Deno.env.get('SUPABASE_URL') ?? '',
      Deno.env.get('SUPABASE_ANON_KEY') ?? '',
      {
        global: {
          headers: { Authorization: authorization },
        },
      }
    )

    // Get user from auth header
    const {
      data: { user },
      error: userError,
    } = await supabaseClient.auth.getUser()

    if (userError) throw userError
    if (!user) throw new Error('No user found')

    // Get subscription data
    const { data: subscription, error: subscriptionError } = await supabaseClient
      .from('subscriptions')
      .select('*')
      .eq('user_id', user.id)
      .single()

    if (subscriptionError) throw subscriptionError

    // Get plan config
    const plans = {
      free: {
        name: 'Free',
        scans_per_month: 10,
        features: ['Basic extraction', 'Email support']
      },
      basic: {
        name: 'Basic',
        scans_per_month: 100,
        features: ['Advanced extraction', 'Priority support', 'Bulk upload']
      },
      pro: {
        name: 'Professional',
        scans_per_month: 500,
        features: ['Enterprise extraction', '24/7 support', 'Unlimited history']
      }
    }

    const planConfig = plans[subscription?.tier || 'free']

    // Calculate usage stats
    const scansUsed = subscription?.scans_used_this_period || 0
    const scansLimit = planConfig.scans_per_month
    const scansRemaining = Math.max(0, scansLimit - scansUsed)
    const usagePercentage = (scansUsed / scansLimit) * 100

    // Format response
    const response = {
      user_id: user.id,
      tier: subscription?.tier || 'free',
      tier_name: planConfig.name,
      status: subscription?.status || 'active',
      scans_used: scansUsed,
      scans_limit: scansLimit,
      scans_remaining: scansRemaining,
      usage_percentage: usagePercentage,
      period_start: subscription?.current_period_start || new Date().toISOString(),
      period_end: subscription?.current_period_end || new Date().toISOString(),
      features: planConfig.features,
      can_upgrade: true,
      can_downgrade: (subscription?.tier || 'free') !== 'free'
    }

    return new Response(
      JSON.stringify(response),
      { 
        headers: { 
          ...corsHeaders,
          'Content-Type': 'application/json'
        } 
      }
    )
  } catch (error) {
    return new Response(
      JSON.stringify({ error: error.message }),
      { 
        status: 400,
        headers: {
          ...corsHeaders,
          'Content-Type': 'application/json'
        }
      }
    )
  }
})