'use client'

import { useState, useEffect } from 'react';
import { supabase } from '@/lib/supabase'; // Import Supabase client

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

    // Get the current user session from Supabase
    const { data: { session }, error: sessionError } = await supabase.auth.getSession();
    if (sessionError || !session) {
      alert('You must be logged in to make a purchase.');
      // Optional: redirect to login page
      // window.location.href = '/login';
      return;
    }
    const user = session.user;

    const response = await fetch('/api/payments/create-order', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        tier: plan.name.toLowerCase(),
        billing_cycle: billingCycle,
      }),
    });

    const order = await response.json();

    const options = {
      key: order.key_id,
      amount: order.amount_paise,
      currency: order.currency,
      name: 'TrulyInvoice',
      description: `Subscription for ${plan.name} - ${billingCycle}`,
      order_id: order.order_id,
      handler: async (response: any) => {
        // After payment, verify it and then update the user's subscription
        try {
          const verificationResponse = await fetch('/api/payments/verify', {
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
            alert('Payment successful! Your subscription has been activated.');
            // Redirect to the dashboard
            window.location.href = '/dashboard/settings';
          } else {
            alert('Payment verification failed.');
          }
        } catch (err) {
          console.error('An error occurred during payment verification or subscription update:', err);
          alert(`An error occurred: ${err instanceof Error ? err.message : 'Unknown error'}`);
        }
      },
      prefill: {
        name: user.user_metadata?.full_name || 'New User',
        email: user.email,
        contact: user.phone || '',
      },
      notes: {
        userId: user.id,
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
