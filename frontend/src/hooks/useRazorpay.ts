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
  const [processingPlan, setProcessingPlan] = useState<string | null>(null);

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
      alert('Razorpay SDK not loaded yet. Please wait a moment and try again.');
      return;
    }

    if (!plan || !plan.name || !plan.price) {
      console.error('❌ Invalid plan object:', plan);
      alert('Invalid plan selected. Please refresh and try again.');
      return;
    }

    setProcessingPlan(plan.name);

    try {
      // Get the current user session from Supabase
      const { data: { session }, error: sessionError } = await supabase.auth.getSession();
      if (sessionError || !session) {
        alert('You must be logged in to make a purchase.');
        setProcessingPlan(null);
        // Redirect to login page
        window.location.href = '/login';
        return;
      }
      const user = session.user;

      // Parse plan price - handle both '₹0' and '0' formats
      let amountInRupees = 0;
      if (plan.price && plan.price !== '₹0') {
        const priceString = plan.price.toString().replace('₹', '').trim();
        amountInRupees = parseInt(priceString) || 0;
      }

      // For free plan, don't attempt payment
      if (amountInRupees === 0) {
        alert('Free plan - use signup instead');
        window.location.href = '/register';
        setProcessingPlan(null);
        return;
      }

      console.log('💳 Processing payment:', {
        planName: plan.name,
        amountInRupees,
        billingCycle,
      });

      // Convert amount from rupees to paise (multiply by 100)
      const amountInPaise = amountInRupees * 100;

      if (amountInPaise <= 0) {
        console.error('❌ Invalid amount:', amountInPaise);
        alert('Invalid amount. Please try again.');
        setProcessingPlan(null);
        return;
      }

      const response = await fetch('/api/payments/create-order', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          tier: plan.name.toLowerCase(),
          amount: amountInPaise,
          currency: 'INR',
          planName: plan.name.toLowerCase(),
          billing_cycle: billingCycle,
        }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        console.error('❌ API error:', errorData);
        alert(`Payment error: ${errorData.error || 'Unknown error'}`);
        setProcessingPlan(null);
        return;
      }

      const order = await response.json();

      if (!order || !order.order_id || !order.key_id) {
        console.error('❌ Invalid order response:', order);
        alert('Failed to create order. Missing order details.');
        setProcessingPlan(null);
        return;
      }

      console.log('✅ Order created:', order.order_id);

      const options = {
        key: order.key_id, // ✅ CRITICAL: This must be set!
        amount: order.amount_paise,
        currency: order.currency,
        name: 'TrulyInvoice',
        description: `Subscription for ${plan.name} - ${billingCycle}`,
        order_id: order.order_id,
        handler: async (response: any) => {
          // After payment, verify it and then update the user's subscription
          try {
            console.log('✅ Payment successful, verifying...');
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
              alert('Payment verification failed. Please contact support.');
              console.error('Verification failed:', verificationResult);
            }
          } catch (err) {
            console.error('Payment verification error:', err);
            alert(`An error occurred: ${err instanceof Error ? err.message : 'Unknown error'}`);
          } finally {
            setProcessingPlan(null);
          }
        },
        modal: {
          ondismiss: () => {
            console.log('Payment modal dismissed');
            setProcessingPlan(null);
          }
        },
        prefill: {
          name: user.user_metadata?.full_name || 'User',
          email: user.email || '',
          contact: user.phone || '',
        },
        notes: {
          userId: user.id,
          planName: plan.name.toLowerCase(),
          billingCycle,
        },
        theme: {
          color: '#3b82f6',
        },
      };

      console.log('🔓 Opening Razorpay checkout with options:', options);
      const rzp = new window.Razorpay(options);
      rzp.open();
    } catch (error) {
      console.error('❌ Payment error:', error);
      alert(`Failed to initiate payment: ${error instanceof Error ? error.message : 'Unknown error'}`);
      setProcessingPlan(null);
    }
  };

  return { processPayment, isLoaded, processingPlan };
};

export default useRazorpay;
