/**
 * Razorpay Payment Checkout Component
 * Handles Razorpay payment integration for subscription upgrades
 */

import { useEffect } from 'react'

interface RazorpayOptions {
  key: string
  amount: number
  currency: string
  name: string
  description: string
  order_id: string
  prefill?: {
    name?: string
    email?: string
    contact?: string
  }
  theme?: {
    color?: string
  }
  handler: (response: RazorpayResponse) => void
  modal?: {
    ondismiss?: () => void
  }
}

interface RazorpayResponse {
  razorpay_order_id: string
  razorpay_payment_id: string
  razorpay_signature: string
}

declare global {
  interface Window {
    Razorpay: any
  }
}

interface RazorpayCheckoutProps {
  amount: number // Amount in paise (100 paise = 1 rupee)
  currency: string // e.g., "INR"
  planName: string // e.g., "Basic Plan"
  planTier: string // e.g., "basic"
  billingCycle: 'monthly' | 'yearly'
  orderId: string // Razorpay order ID from backend
  razorpayKeyId: string // Razorpay key ID from backend
  userEmail: string
  userName: string
  onSuccess: (response: RazorpayResponse) => void
  onFailure: (error: any) => void
  onDismiss?: () => void
  autoOpen?: boolean
}

export default function RazorpayCheckout({
  amount,
  currency,
  planName,
  planTier,
  billingCycle,
  orderId,
  razorpayKeyId,
  userEmail,
  userName,
  onSuccess,
  onFailure,
  onDismiss,
  autoOpen = false
}: RazorpayCheckoutProps) {
  
  useEffect(() => {
    // Load Razorpay script
    const script = document.createElement('script')
    script.src = 'https://checkout.razorpay.com/v1/checkout.js'
    script.async = true
    
    script.onload = () => {
      if (autoOpen) {
        openRazorpayCheckout()
      }
    }
    
    script.onerror = () => {
      onFailure({ message: 'Failed to load Razorpay SDK' })
    }
    
    document.body.appendChild(script)
    
    return () => {
      document.body.removeChild(script)
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [autoOpen])
  
  const openRazorpayCheckout = () => {
    if (!window.Razorpay) {
      onFailure({ message: 'Razorpay SDK not loaded' })
      return
    }
    
    const options: RazorpayOptions = {
      key: razorpayKeyId,
      amount: amount,
      currency: currency,
      name: 'TrulyInvoice',
      description: `${planName} - ${billingCycle === 'monthly' ? 'Monthly' : 'Yearly'} Auto-Renewal Subscription`,
      order_id: orderId,
      prefill: {
        name: userName,
        email: userEmail
      },
      theme: {
        color: '#2563eb' // Blue-600
      },
      handler: (response: RazorpayResponse) => {
        // Payment successful
        onSuccess(response)
      },
      modal: {
        ondismiss: () => {
          // User closed the payment modal
          if (onDismiss) {
            onDismiss()
          }
        }
      }
    }
    
    try {
      const rzp = new window.Razorpay(options)
      
      rzp.on('payment.failed', function (response: any) {
        onFailure({
          code: response.error.code,
          description: response.error.description,
          source: response.error.source,
          step: response.error.step,
          reason: response.error.reason,
          metadata: response.error.metadata
        })
      })
      
      rzp.open()
    } catch (error) {
      onFailure(error)
    }
  }
  
  // Return null - this is a headless component
  return null
}

/**
 * Hook to use Razorpay checkout
 * Makes it easy to integrate payment flow into any component
 */
export function useRazorpay() {
  const createOrder = async (tier: string, billingCycle: 'monthly' | 'yearly') => {
    try {
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/payments/create-order`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        credentials: 'include', // Include auth cookies
        body: JSON.stringify({
          tier,
          billing_cycle: billingCycle
        })
      })
      
      if (!response.ok) {
        const error = await response.json()
        throw new Error(error.detail || 'Failed to create payment order')
      }
      
      return await response.json()
    } catch (error) {
      console.error('Error creating order:', error)
      throw error
    }
  }
  
  const verifyPayment = async (
    orderId: string,
    paymentId: string,
    signature: string
  ) => {
    try {
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/payments/verify`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        credentials: 'include', // Include auth cookies
        body: JSON.stringify({
          razorpay_order_id: orderId,
          razorpay_payment_id: paymentId,
          razorpay_signature: signature
        })
      })
      
      if (!response.ok) {
        const error = await response.json()
        throw new Error(error.detail || 'Payment verification failed')
      }
      
      return await response.json()
    } catch (error) {
      console.error('Error verifying payment:', error)
      throw error
    }
  }
  
  const getRazorpayConfig = async () => {
    try {
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/payments/config`, {
        credentials: 'include'
      })
      
      if (!response.ok) {
        throw new Error('Failed to get Razorpay config')
      }
      
      return await response.json()
    } catch (error) {
      console.error('Error getting Razorpay config:', error)
      throw error
    }
  }
  
  return {
    createOrder,
    verifyPayment,
    getRazorpayConfig
  }
}
