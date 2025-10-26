import { serve } from 'https://deno.land/std@0.168.0/http/server.ts';
import { createClient } from 'https://esm.sh/@supabase/supabase-js@2';

// Define allowed origins for CORS
const allowedOrigins = [
  'https://www.trulyinvoice.xyz',
  'https://trulyinvoice.xyz',
  'http://localhost:3000',
];

serve(async (req) => {
  // Handle CORS preflight requests
  const origin = req.headers.get('Origin') || '';
  const corsHeaders = {
    'Access-Control-Allow-Origin': allowedOrigins.includes(origin) ? origin : allowedOrigins[0],
    'Access-Control-Allow-Headers': 'authorization, x-client-info, apikey, content-type',
  };
  if (req.method === 'OPTIONS') {
    return new Response('ok', { headers: corsHeaders });
  }

  try {
    // Create a Supabase client with the user's auth token
    const supabaseClient = createClient(
      Deno.env.get('SUPABASE_URL') ?? '',
      Deno.env.get('SUPABASE_ANON_KEY') ?? '',
      { global: { headers: { Authorization: req.headers.get('Authorization')! } } }
    );

    // Get the user from the session
    const { data: { user }, error: userError } = await supabaseClient.auth.getUser();
    if (userError) throw userError;
    if (!user) throw new Error('User not found');

    // Get the plan details from the request body
    const { planId, billingCycle } = await req.json();
    if (!planId || !billingCycle) {
      throw new Error('planId and billingCycle are required.');
    }

    const periodEnd = new Date();
    if (billingCycle === 'monthly') {
      periodEnd.setMonth(periodEnd.getMonth() + 1);
    } else if (billingCycle === 'yearly') {
      periodEnd.setFullYear(periodEnd.getFullYear() + 1);
    } else {
      throw new Error('Invalid billing cycle.');
    }

    // Use 'upsert' to create a new subscription or update an existing one
    const { data, error } = await supabaseClient
      .from('subscriptions')
      .upsert({
        user_id: user.id,
        tier: planId,
        status: 'active',
        scans_used_this_period: 0, // Reset scan count on new/updated plan
        current_period_start: new Date().toISOString(),
        current_period_end: periodEnd.toISOString(),
      })
      .select()
      .single();

    if (error) {
      console.error('Supabase DB error:', error);
      throw error;
    }

    return new Response(JSON.stringify({ success: true, subscription: data }), {
      headers: { ...corsHeaders, 'Content-Type': 'application/json' },
      status: 200,
    });

  } catch (error) {
    return new Response(JSON.stringify({ error: error.message }), {
      headers: { ...corsHeaders, 'Content-Type': 'application/json' },
      status: 400,
    });
  }
});
