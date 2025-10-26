import { NextRequest, NextResponse } from 'next/server';
import Razorpay from 'razorpay';

const PLAN_PRICES: Record<string, number> = {
  'free': 0,
  'basic': 14900, // ₹149 in paise
  'pro': 29900,   // ₹299 in paise
  'ultra': 59900, // ₹599 in paise
  'max': 99900,   // ₹999 in paise
};

export async function POST(req: NextRequest) {
  try {
    const razorpay = new Razorpay({
      key_id: process.env.NEXT_PUBLIC_RAZORPAY_KEY_ID || process.env.RAZORPAY_KEY_ID!,
      key_secret: process.env.RAZORPAY_KEY_SECRET!,
    });

    const body = await req.json();
    const { tier, billing_cycle, amount, currency, planName } = body;

    // Support both old and new request formats
    let finalAmount = amount;
    let finalCurrency = currency || 'INR';
    let finalPlanName = planName || tier;

    // If tier is provided (new format), calculate amount
    if (tier && !amount) {
      const basePrice = PLAN_PRICES[tier.toLowerCase()] || 0;
      
      if (basePrice === 0) {
        return NextResponse.json({ 
          error: 'Cannot create order for free plan' 
        }, { status: 400 });
      }

      // Apply yearly discount if applicable
      if (billing_cycle === 'yearly') {
        finalAmount = Math.round(basePrice * 12 * 0.8); // 20% discount
      } else {
        finalAmount = basePrice;
      }
    }

    if (!finalAmount || finalAmount <= 0) {
      return NextResponse.json({ 
        error: 'Invalid amount' 
      }, { status: 400 });
    }

    const options = {
      amount: finalAmount,
      currency: finalCurrency,
      receipt: `receipt_order_${new Date().getTime()}`,
      notes: {
        plan_name: finalPlanName.toLowerCase(),
        billing_cycle: billing_cycle || 'monthly',
      },
    };

    const order = await razorpay.orders.create(options);
    
    // Return order details with key_id for client
    return NextResponse.json({
      order_id: order.id,
      amount_paise: order.amount,
      currency: order.currency,
      key_id: process.env.NEXT_PUBLIC_RAZORPAY_KEY_ID || process.env.RAZORPAY_KEY_ID,
    });
  } catch (error) {
    console.error('Payment order error:', error);
    return NextResponse.json({ 
      error: 'Error creating order',
      details: error instanceof Error ? error.message : 'Unknown error'
    }, { status: 500 });
  }
}
