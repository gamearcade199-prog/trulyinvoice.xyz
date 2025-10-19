import { NextRequest, NextResponse } from 'next/server';
import Razorpay from 'razorpay';

export async function POST(req: NextRequest) {
  const razorpay = new Razorpay({
    key_id: process.env.RAZORPAY_KEY_ID!,
    key_secret: process.env.RAZORPAY_KEY_SECRET!,
  });

  const { amount, currency, planName } = await req.json();

  const options = {
    amount,
    currency,
    receipt: `receipt_order_${new Date().getTime()}`,
    notes: {
      planName,
    },
  };

  try {
    const order = await razorpay.orders.create(options);
    return NextResponse.json(order);
  } catch (error) {
    return NextResponse.json({ error: 'Error creating order' }, { status: 500 });
  }
}
