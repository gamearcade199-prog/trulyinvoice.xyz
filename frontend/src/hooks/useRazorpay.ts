'use client'

import { useState, useEffect } from 'react';

declare global {
  interface Window {
    Razorpay: any;
  }
}

const useRazorpay = () => {
  const [isLoaded, setIsLoaded] = useState(false);

  useEffect(() => {
    const script = document.createElement('script');
    script.src = 'https://checkout.razorpay.com/v1/checkout.js';
    script.async = true;
    script.onload = () => setIsLoaded(true);
    document.body.appendChild(script);

    return () => {
      document.body.removeChild(script);
    };
  }, []);

  const processPayment = async (plan: any, billingCycle: 'monthly' | 'yearly') => {
    if (!isLoaded) {
      alert('Razorpay SDK not loaded yet.');
      return;
    }

    const amount = billingCycle === 'yearly' && plan.price !== '₹0'
      ? Math.round(parseInt(plan.price.replace('₹', '')) * 12 * 0.8)
      : parseInt(plan.price.replace('₹', ''));

    const response = await fetch('/api/payments/create-order', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        amount: amount * 100, // Amount in paise
        currency: 'INR',
        planName: plan.name,
      }),
    });

    const order = await response.json();

    const options = {
      key: process.env.NEXT_PUBLIC_RAZORPAY_KEY_ID,
      amount: order.amount,
      currency: order.currency,
      name: 'TrulyInvoice',
      description: `Subscription for ${plan.name} - ${billingCycle}`,
      order_id: order.id,
      handler: async (response: any) => {
        const verificationResponse = await fetch('/api/payments/verify-payment', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            razorpay_order_id: response.razorpay_order_id,
            razorpay_payment_id: response.razorpay_payment_id,
            razorpay_signature: response.razorpay_signature,
          }),
        });

        const verificationResult = await verificationResponse.json();
        if (verificationResult.success) {
          alert('Payment successful!');
        } else {
          alert('Payment verification failed.');
        }
      },
      prefill: {
        name: 'Test User',
        email: 'test.user@example.com',
        contact: '9999999999',
      },
      notes: {
        address: 'Test Address',
      },
      theme: {
        color: '#3b82f6',
      },
    };

    const rzp = new window.Razorpay(options);
    rzp.open();
  };

  return { processPayment, isLoaded };
};

export default useRazorpay;
