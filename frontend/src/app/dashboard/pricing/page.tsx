'use client'

import { Check, Zap, Crown, Rocket, X, Sparkles, Loader2 } from 'lucide-react'
import { useState } from 'react'
import DashboardLayout from '@/components/DashboardLayout'
import RazorpayCheckout, { useRazorpay } from '@/components/RazorpayCheckout'
import { supabase } from '@/lib/supabase'

export default function PricingPage() {
  const [billingCycle, setBillingCycle] = useState<'monthly' | 'yearly'>('monthly')
  const [processingPlan, setProcessingPlan] = useState<string | null>(null)
  const [showPayment, setShowPayment] = useState(false)
  const [paymentData, setPaymentData] = useState<any>(null)
  const [userEmail, setUserEmail] = useState('')
  const [userName, setUserName] = useState('')
  
  const { createOrder, verifyPayment, getRazorpayConfig } = useRazorpay()
  
  // Get user data on mount
  useState(() => {
    const getUserData = async () => {
      const { data: { user } } = await supabase.auth.getUser()
      if (user) {
        setUserEmail(user.email || '')
        setUserName(user.user_metadata?.full_name || user.email || '')
      }
    }
    getUserData()
  })
  
  const handleUpgrade = async (planTier: string, planName: string) => {
    if (planTier === 'free') return // Can't upgrade to free
    
    setProcessingPlan(planTier)
    
    try {
      // Step 1: Create payment order
      const orderData = await createOrder(planTier, billingCycle)
      
      // Step 2: Get Razorpay config
      const config = await getRazorpayConfig()
      
      // Step 3: Prepare payment data
      setPaymentData({
        orderId: orderData.order_id,
        amount: orderData.amount,
        currency: orderData.currency,
        razorpayKeyId: config.key_id,
        planName: planName,
        planTier: planTier
      })
      
      // Step 4: Show Razorpay checkout
      setShowPayment(true)
      setProcessingPlan(null)
    } catch (error: any) {
      console.error('Error creating order:', error)
      alert(error.message || 'Failed to initiate payment. Please try again.')
      setProcessingPlan(null)
    }
  }
  
  const handlePaymentSuccess = async (response: any) => {
    setShowPayment(false)
    setProcessingPlan('verifying')
    
    try {
      // Verify payment with backend
      const verificationResult = await verifyPayment(
        response.razorpay_order_id,
        response.razorpay_payment_id,
        response.razorpay_signature
      )
      
      // Show success message
      alert(`Payment successful! Your ${verificationResult.subscription.tier} plan is now active.`)
      
      // Reload page to show updated plan
      window.location.reload()
    } catch (error: any) {
      console.error('Payment verification failed:', error)
      alert('Payment verification failed. Please contact support.')
    } finally {
      setProcessingPlan(null)
    }
  }
  
  const handlePaymentFailure = (error: any) => {
    setShowPayment(false)
    setProcessingPlan(null)
    console.error('Payment failed:', error)
    alert(error.description || 'Payment failed. Please try again.')
  }
  
  const handlePaymentDismiss = () => {
    setShowPayment(false)
    setProcessingPlan(null)
  }

  const plans = [
    {
      name: 'Free',
      price: '₹0',
      scans: '10 scans',
      period: 'per month',
      icon: Zap,
      iconBg: 'bg-gradient-to-br from-gray-400 to-gray-500',
      borderGlow: '',
      features: [
        '10 scans per month',
        'Basic AI extraction',
        'PDF & Image support',
        'Bulk upload (1 invoice)',
        '1-day storage',
        'Email support',
      ],
      limitations: [],
      buttonText: 'Current Plan',
      buttonStyle: 'bg-gray-200 dark:bg-gray-700 text-gray-600 dark:text-gray-400 cursor-not-allowed border border-gray-300 dark:border-gray-600',
      popular: false,
    },
    {
      name: 'Basic',
      price: '₹149',
      scans: '80 scans',
      period: 'per month',
      icon: Check,
      iconBg: 'bg-gradient-to-br from-blue-500 to-cyan-500',
      borderGlow: 'hover:shadow-lg hover:shadow-blue-500/20',
      features: [
        '80 scans per month',
        '95% AI accuracy',
        'GST validation',
        'Bulk upload (5 invoices)',
        'Export to Excel/CSV',
        '7-day storage',
        'Priority support',
      ],
      limitations: [],
      buttonText: 'Upgrade to Basic',
      buttonStyle: 'bg-gradient-to-r from-blue-500 to-cyan-500 hover:from-blue-600 hover:to-cyan-600 text-white shadow-md hover:shadow-lg transition-all',
      popular: false,
    },
    {
      name: 'Pro',
      price: '₹299',
      scans: '200 scans',
      period: 'per month',
      icon: Crown,
      iconBg: 'bg-gradient-to-br from-purple-500 to-pink-500',
      borderGlow: 'shadow-xl shadow-purple-500/30',
      features: [
        '200 scans per month',
        '98% AI accuracy',
        'Bulk upload (10 invoices)',
        'Custom export templates',
        '30-day storage',
        '24/7 priority support',
      ],
      limitations: [],
      buttonText: 'Upgrade to Pro',
      buttonStyle: 'bg-gradient-to-r from-purple-500 to-pink-500 hover:from-purple-600 hover:to-pink-600 text-white shadow-lg hover:shadow-xl transition-all',
      popular: true,
    },
    {
      name: 'Ultra',
      price: '₹599',
      scans: '500 scans',
      period: 'per month',
      icon: Rocket,
      iconBg: 'bg-gradient-to-br from-orange-500 to-red-500',
      borderGlow: 'hover:shadow-xl hover:shadow-orange-500/30',
      features: [
        '500 scans per month',
        '99% AI accuracy',
        'Bulk upload (50 invoices)',
        'Advanced GST compliance',
        '60-day storage',
        'Dedicated support',
      ],
      limitations: [],
      buttonText: 'Upgrade to Ultra',
      buttonStyle: 'bg-gradient-to-r from-orange-500 to-red-500 hover:from-orange-600 hover:to-red-600 text-white shadow-lg hover:shadow-xl transition-all',
      popular: false,
    },
    {
      name: 'Max',
      price: '₹999',
      scans: '1000 scans',
      period: 'per month',
      icon: Sparkles,
      iconBg: 'bg-gradient-to-br from-emerald-500 to-green-500',
      borderGlow: 'hover:shadow-xl hover:shadow-emerald-500/30',
      features: [
        '1,000 scans per month',
        '99.5% AI accuracy',
        'Bulk upload (100 invoices)',
        'Custom integrations',
        '90-day storage',
        '24/7 priority support',
      ],
      limitations: [],
      buttonText: 'Upgrade to Max',
      buttonStyle: 'bg-gradient-to-r from-emerald-500 to-green-500 hover:from-emerald-600 hover:to-green-600 text-white shadow-lg hover:shadow-xl transition-all',
      popular: false,
    },
  ]

  return (
    <DashboardLayout>
      <div className="max-w-7xl mx-auto bg-gradient-to-br from-gray-50 via-white to-blue-50 dark:from-gray-900 dark:via-gray-900 dark:to-gray-800 -m-6 p-6 rounded-xl">
        {/* Header */}
        <div className="mb-12 text-center">
          <div className="inline-flex items-center gap-2 bg-blue-100 dark:bg-blue-900/30 text-blue-600 dark:text-blue-400 px-4 py-2 rounded-full text-sm font-semibold mb-4">
            <Sparkles className="w-4 h-4" />
            Simple & Transparent Pricing
          </div>
          <h1 className="text-5xl font-bold bg-gradient-to-r from-gray-900 to-gray-600 dark:from-white dark:to-gray-300 bg-clip-text text-transparent mb-4">
            Dashboard Pricing - Upgrade Your Invoice Processing Plan
          </h1>
          <p className="text-xl text-gray-600 dark:text-gray-400 max-w-2xl mx-auto">
            Select the perfect plan for your invoice processing needs. Upgrade or downgrade anytime.
          </p>
        </div>

      {/* Billing Toggle */}
      <div className="flex justify-center mb-16">
        <div className="bg-gray-50 dark:bg-gray-900 p-1.5 rounded-xl inline-flex shadow-lg border border-gray-200 dark:border-gray-800">
          <button
            onClick={() => setBillingCycle('monthly')}
            className={`px-8 py-3 rounded-lg font-semibold transition-all ${
              billingCycle === 'monthly'
                ? 'bg-gradient-to-r from-blue-500 to-cyan-500 text-white shadow-md'
                : 'text-gray-600 dark:text-gray-400 hover:text-gray-800 dark:hover:text-gray-200'
            }`}
          >
            Monthly
          </button>
          <button
            onClick={() => setBillingCycle('yearly')}
            className={`px-8 py-3 rounded-lg font-semibold transition-all ${
              billingCycle === 'yearly'
                ? 'bg-gradient-to-r from-blue-500 to-cyan-500 text-white shadow-md'
                : 'text-gray-600 dark:text-gray-400 hover:text-gray-800 dark:hover:text-gray-200'
            }`}
          >
            Yearly
            <span className="ml-2 text-xs bg-green-100 dark:bg-green-900/50 text-green-600 dark:text-green-400 px-2 py-1 rounded-full font-bold">
              Save 20%
            </span>
          </button>
        </div>
      </div>

      {/* Pricing Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-4 gap-6 max-w-7xl mx-auto">
        {plans.map((plan) => {
          const Icon = plan.icon
          return (
            <div
              key={plan.name}
              className={`relative rounded-2xl p-8 transition-all duration-300 backdrop-blur-sm ${
                plan.popular
                  ? 'bg-white/90 dark:bg-gray-800/90 border-2 border-purple-500 dark:border-purple-400 scale-105 z-10'
                  : 'bg-white/70 dark:bg-gray-800/70 border border-gray-200/50 dark:border-gray-700/50 hover:scale-105'
              } ${plan.borderGlow}`}
            >
              {/* Popular Badge */}
              {plan.popular && (
                <div className="absolute -top-5 left-1/2 transform -translate-x-1/2">
                  <div className="bg-gradient-to-r from-purple-500 to-pink-500 text-white px-6 py-2 rounded-full text-sm font-bold shadow-xl flex items-center gap-2">
                    <Sparkles className="w-4 h-4" />
                    Most Popular
                  </div>
                </div>
              )}

              {/* Icon */}
              <div className="mb-6">
                <div className={`w-16 h-16 ${plan.iconBg} rounded-2xl flex items-center justify-center shadow-lg`}>
                  <Icon className="w-8 h-8 text-white" />
                </div>
              </div>

              {/* Plan Name */}
              <h3 className="text-3xl font-bold text-gray-900 dark:text-white mb-3">
                {plan.name}
              </h3>

              {/* Price */}
              <div className="mb-3">
                <span className="text-5xl font-bold bg-gradient-to-r from-gray-900 to-gray-600 dark:from-white dark:to-gray-300 bg-clip-text text-transparent">
                  {billingCycle === 'yearly' && plan.price !== '₹0'
                    ? `₹${Math.round(parseInt(plan.price.replace('₹', '')) * 12 * 0.8)}`
                    : plan.price}
                </span>
                <span className="text-gray-500 dark:text-gray-400 ml-2 text-lg">
                  /{billingCycle === 'yearly' ? 'year' : 'month'}
                </span>
              </div>

              {/* Scans */}
              <div className="mb-8">
                <div className="inline-flex items-center gap-2 bg-gradient-to-r from-blue-50 to-cyan-50 dark:from-blue-900/30 dark:to-cyan-900/30 px-4 py-2 rounded-lg border border-blue-200 dark:border-blue-800">
                  <span className="text-lg font-bold text-blue-600 dark:text-blue-400">
                    {plan.scans}
                  </span>
                  <span className="text-sm text-gray-600 dark:text-gray-400">
                    {plan.period}
                  </span>
                </div>
              </div>

              {/* CTA Button */}
              <button
                className={`w-full py-4 px-6 rounded-xl font-bold text-lg transition-all duration-200 mb-8 ${plan.buttonStyle} flex items-center justify-center gap-2`}
                disabled={plan.name === 'Free' || processingPlan !== null}
                onClick={() => handleUpgrade(plan.name.toLowerCase(), plan.name)}
              >
                {processingPlan === plan.name.toLowerCase() ? (
                  <>
                    <Loader2 className="w-5 h-5 animate-spin" />
                    Processing...
                  </>
                ) : (
                  plan.buttonText
                )}
              </button>

              {/* Features */}
              <div className="space-y-4">
                <p className="text-sm font-bold text-gray-900 dark:text-white uppercase tracking-wide">
                  What's Included
                </p>
                {plan.features.map((feature, index) => (
                  <div key={index} className="flex items-start gap-3">
                    <div className="mt-0.5 flex-shrink-0">
                      <div className="w-5 h-5 rounded-full bg-green-100 dark:bg-green-900/30 flex items-center justify-center">
                        <Check className="w-3 h-3 text-green-600 dark:text-green-400 font-bold" />
                      </div>
                    </div>
                    <span className="text-sm text-gray-700 dark:text-gray-300 leading-relaxed">
                      {feature}
                    </span>
                  </div>
                ))}
              </div>

              {/* Limitations (if any) */}
              {plan.limitations.length > 0 && (
                <div className="mt-6 pt-6 border-t border-gray-200 dark:border-gray-800">
                  <p className="text-xs font-bold text-gray-500 dark:text-gray-400 uppercase tracking-wide mb-3">
                    Limitations
                  </p>
                  {plan.limitations.map((limitation, index) => (
                    <div key={index} className="flex items-start gap-3 mb-3">
                      <div className="mt-0.5">
                        <X className="w-4 h-4 text-gray-400 dark:text-gray-600" />
                      </div>
                      <span className="text-sm text-gray-500 dark:text-gray-500">
                        {limitation}
                      </span>
                    </div>
                  ))}
                </div>
              )}
            </div>
          )
        })}
      </div>

      {/* FAQ Section */}
      <div className="mt-20 max-w-7xl mx-auto">
        <div className="bg-white/80 dark:bg-gray-800/80 backdrop-blur-sm rounded-3xl p-10 border border-gray-200/50 dark:border-gray-700/50 shadow-xl">
          <div className="text-center mb-10">
            <h2 className="text-3xl font-bold text-gray-900 dark:text-white mb-3">
              Frequently Asked Questions
            </h2>
            <p className="text-gray-600 dark:text-gray-400">
              Everything you need to know about our pricing plans
            </p>
          </div>
          <div className="grid md:grid-cols-2 gap-8">
            <div className="bg-gradient-to-br from-blue-50 to-cyan-50 dark:from-blue-900/20 dark:to-cyan-900/20 p-6 rounded-2xl border border-blue-200/50 dark:border-blue-800/50">
              <h3 className="font-bold text-gray-900 dark:text-white mb-3 text-lg">
                What happens if I exceed my scan limit?
              </h3>
              <p className="text-gray-600 dark:text-gray-400">
                You can upgrade your plan anytime or purchase additional scans as needed. Unused scans don't roll over to the next month.
              </p>
            </div>
            <div className="bg-gradient-to-br from-purple-50 to-pink-50 dark:from-purple-900/20 dark:to-pink-900/20 p-6 rounded-2xl border border-purple-200/50 dark:border-purple-800/50">
              <h3 className="font-bold text-gray-900 dark:text-white mb-3 text-lg">
                Can I change plans later?
              </h3>
              <p className="text-gray-600 dark:text-gray-400">
                Yes! You can upgrade or downgrade your plan at any time. Changes take effect immediately.
              </p>
            </div>
            <div className="bg-gradient-to-br from-green-50 to-emerald-50 dark:from-green-900/20 dark:to-emerald-900/20 p-6 rounded-2xl border border-green-200/50 dark:border-green-800/50">
              <h3 className="font-bold text-gray-900 dark:text-white mb-3 text-lg">
                What payment methods do you accept?
              </h3>
              <p className="text-gray-600 dark:text-gray-400">
                We accept UPI, credit/debit cards, net banking, and all major payment methods through our secure payment gateway.
              </p>
            </div>
            <div className="bg-gradient-to-br from-orange-50 to-red-50 dark:from-orange-900/20 dark:to-red-900/20 p-6 rounded-2xl border border-orange-200/50 dark:border-orange-800/50">
              <h3 className="font-bold text-gray-900 dark:text-white mb-3 text-lg">
                Is there a refund policy?
              </h3>
              <p className="text-gray-600 dark:text-gray-400">
                Yes! We offer a 14-day money-back guarantee if you're not satisfied with your plan.
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* Contact Section */}
      <div className="mt-12 text-center">
        <div className="inline-flex flex-col items-center gap-4 bg-gradient-to-r from-blue-500 to-purple-500 p-8 rounded-2xl shadow-2xl">
          <p className="text-white text-lg font-semibold">
            Need a custom plan for your enterprise?
          </p>
          <a 
            href="/dashboard/support" 
            className="bg-white text-blue-600 hover:bg-gray-100 px-8 py-3 rounded-xl font-bold transition-all shadow-lg hover:shadow-xl hover:scale-105"
          >
            Contact Sales Team
          </a>
        </div>
      </div>
      </div>
      
      {/* Razorpay Checkout */}
      {showPayment && paymentData && (
        <RazorpayCheckout
          amount={paymentData.amount}
          currency={paymentData.currency}
          planName={paymentData.planName}
          planTier={paymentData.planTier}
          billingCycle={billingCycle}
          orderId={paymentData.orderId}
          razorpayKeyId={paymentData.razorpayKeyId}
          userEmail={userEmail}
          userName={userName}
          onSuccess={handlePaymentSuccess}
          onFailure={handlePaymentFailure}
          onDismiss={handlePaymentDismiss}
          autoOpen={true}
        />
      )}
    </DashboardLayout>
  )
}

