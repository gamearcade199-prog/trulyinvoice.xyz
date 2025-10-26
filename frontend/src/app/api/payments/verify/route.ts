import { NextRequest, NextResponse } from 'next/server';
import crypto from 'crypto';
import { supabase } from '@/lib/supabase';

export async function POST(req: NextRequest) {
  try {
    const body = await req.json();
    const { razorpay_order_id, razorpay_payment_id, razorpay_signature } = body;

    if (!razorpay_order_id || !razorpay_payment_id || !razorpay_signature) {
      return NextResponse.json(
        { success: false, error: 'Missing payment parameters' },
        { status: 400 }
      );
    }

    const signatureBody = `${razorpay_order_id}|${razorpay_payment_id}`;

    const expectedSignature = crypto
      .createHmac('sha256', process.env.RAZORPAY_KEY_SECRET!)
      .update(signatureBody.toString())
      .digest('hex');

    if (expectedSignature === razorpay_signature) {
      const { data: { user } } = await supabase.auth.getUser();

      if (user) {
        try {
          // Fetch order from Razorpay to get plan information
          const razorpayResponse = await fetch(`https://api.razorpay.com/v1/orders/${razorpay_order_id}`, {
            method: 'GET',
            headers: {
              'Authorization': `Basic ${Buffer.from(`${process.env.RAZORPAY_KEY_ID}:${process.env.RAZORPAY_KEY_SECRET}`).toString('base64')}`,
            },
          });

          if (!razorpayResponse.ok) {
            return NextResponse.json(
              { success: false, error: 'Failed to fetch order from Razorpay' },
              { status: 500 }
            );
          }

          const orderData = await razorpayResponse.json();
          const planName = orderData.notes?.plan_name || 'basic';

          const { error: updateError } = await supabase
            .from('users')
            .update({
              plan: planName,
              subscription_status: 'active',
              plan_expiry_date: new Date(new Date().setMonth(new Date().getMonth() + 1)),
            })
            .eq('id', user.id);

          if (updateError) {
            console.error('Update error:', updateError);
            return NextResponse.json(
              { success: false, error: 'Failed to update user plan' },
              { status: 500 }
            );
          }

          return NextResponse.json({ success: true, message: 'Payment verified successfully' });
        } catch (error) {
          console.error('Payment verification error:', error);
          return NextResponse.json(
            { success: false, error: 'Error during verification process' },
            { status: 500 }
          );
        }
      } else {
        return NextResponse.json(
          { success: false, error: 'User not found' },
          { status: 401 }
        );
      }
    } else {
      return NextResponse.json(
        { success: false, error: 'Signature verification failed' },
        { status: 400 }
      );
    }
  } catch (error) {
    console.error('Request parsing error:', error);
    return NextResponse.json(
      { success: false, error: 'Invalid request format' },
      { status: 400 }
    );
  }
}

