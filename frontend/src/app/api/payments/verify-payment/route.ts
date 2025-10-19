import { NextRequest, NextResponse } from 'next/server';
import crypto from 'crypto';
import { supabase } from '@/lib/supabase';

export async function POST(req: NextRequest) {
  const { razorpay_order_id, razorpay_payment_id, razorpay_signature, planName } = await req.json();

  const body = `${razorpay_order_id}|${razorpay_payment_id}`;

  const expectedSignature = crypto
    .createHmac('sha256', process.env.RAZORPAY_KEY_SECRET!)
    .update(body.toString())
    .digest('hex');

  if (expectedSignature === razorpay_signature) {
    const { data: { user } } = await supabase.auth.getUser();

    if (user) {
      const { error } = await supabase
        .from('users')
        .update({
          plan: planName,
          subscription_status: 'active',
          plan_expiry_date: new Date(new Date().setMonth(new Date().getMonth() + 1)),
        })
        .eq('id', user.id);

      if (error) {
        return NextResponse.json({ success: false, error: 'Failed to update user plan' }, { status: 500 });
      }
    }

    return NextResponse.json({ success: true });
  } else {
    return NextResponse.json({ success: false }, { status: 400 });
  }
}

