'use client'

import { Check, Zap, Crown, Rocket, Sparkles, ArrowLeft } from 'lucide-react'
import { useState } from 'react'
import Link from 'next/link'
import useRazorpay from '@/hooks/useRazorpay'

export default function PricingPage() {
  const [billingCycle, setBillingCycle] = useState<'monthly' | 'yearly'>('monthly')
  const { processPayment, isLoaded, processingPlan } = useRazorpay()

  const plans = [
    {
      name: 'Free',
      price: '₹0',
      scans: '10 scans',
      period: 'per month',
      icon: Zap,
      iconBg: 'bg-gradient-to-br from-gray-400 to-gray-500',
      borderGlow: '',
      unitCost: '₹0.00 per scan',
      features: [
        '10 scans per month',
        'Basic AI extraction',
        'PDF & Image support',
        'Bulk upload (1 invoice)',
        '1-day storage',
        'Email support',
      ],
      buttonText: 'Start Free',
      buttonStyle: 'bg-gray-600 hover:bg-gray-700 text-white',
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
      unitCost: '₹1.86 per scan',
      features: [
        '80 scans per month',
        '95% AI accuracy',
        'GST validation',
        'Bulk upload (5 invoices)',
        'Export to Excel/CSV',
        '7-day storage',
        'Priority support',
      ],
      buttonText: 'Get Started',
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
      unitCost: '₹1.50 per scan',
      features: [
        '200 scans per month',
        '99% AI accuracy',
        'Bulk upload (10 invoices)',
        'Custom export templates',
        '30-day storage',
        '24/7 priority support',
      ],
      buttonText: 'Get Started',
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
      unitCost: '₹1.20 per scan',
      features: [
        '500 scans per month',
        '99% AI accuracy',
        'Bulk upload (50 invoices)',
        'Advanced GST compliance',
        '60-day storage',
        'Dedicated support',
      ],
      buttonText: 'Get Started',
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
      unitCost: '₹1.00 per scan',
      features: [
        '1,000 scans per month',
        '99.5% AI accuracy',
        'Bulk upload (100 invoices)',
        'Custom integrations',
        '90-day storage',
        '24/7 priority support',
      ],
      buttonText: 'Get Started',
      buttonStyle: 'bg-gradient-to-r from-emerald-500 to-green-500 hover:from-emerald-600 hover:to-green-600 text-white shadow-lg hover:shadow-xl transition-all',
      popular: false,
    },
  ]

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 via-white to-blue-50 dark:from-gray-900 dark:via-gray-900 dark:to-gray-800">
      {/* Back Button */}
      <div className="container mx-auto px-4 pt-6">
        <Link
          href="/"
          className="inline-flex items-center gap-2 text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-white transition-colors group"
        >
          <ArrowLeft className="w-5 h-5 group-hover:-translate-x-1 transition-transform" />
          <span className="font-semibold">Back to Home</span>
        </Link>
      </div>

      <div className="container mx-auto px-4 py-12 md:py-16">
        {/* Header */}
        <div className="mb-12 text-center">
          <div className="inline-flex items-center gap-2 bg-blue-100 dark:bg-blue-900/30 text-blue-600 dark:text-blue-400 px-4 py-2 rounded-full text-sm font-semibold mb-4">
            <Sparkles className="w-4 h-4" />
            Simple & Transparent Pricing
          </div>
          <h1 className="text-4xl md:text-5xl font-bold bg-gradient-to-r from-gray-900 to-gray-600 dark:from-white dark:to-gray-300 bg-clip-text text-transparent mb-4">
            Pricing Plans - Choose the Perfect Plan for Invoice Conversion
          </h1>
          <p className="text-lg md:text-xl text-gray-600 dark:text-gray-400 max-w-2xl mx-auto">
            Select the perfect plan for your invoice processing needs. Upgrade or downgrade anytime.
          </p>
        </div>

        {/* Billing Toggle */}
        <div className="flex justify-center mb-12">
          <div className="bg-gray-50 dark:bg-gray-900 p-1.5 rounded-xl inline-flex shadow-lg border border-gray-200 dark:border-gray-800">
            <button
              onClick={() => setBillingCycle('monthly')}
              className={`px-6 md:px-8 py-3 rounded-lg font-semibold transition-all ${
                billingCycle === 'monthly'
                  ? 'bg-gradient-to-r from-blue-500 to-cyan-500 text-white shadow-md'
                  : 'text-gray-600 dark:text-gray-400 hover:text-gray-800 dark:hover:text-gray-200'
              }`}
            >
              Monthly
            </button>
            <button
              onClick={() => setBillingCycle('yearly')}
              className={`px-6 md:px-8 py-3 rounded-lg font-semibold transition-all ${
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
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-4 sm:gap-5 lg:gap-6 max-w-[90rem] mx-auto mb-16">
          {plans.map((plan) => {
            const Icon = plan.icon
            return (
              <div
                key={plan.name}
                className={`relative rounded-xl sm:rounded-2xl p-5 sm:p-7 transition-all duration-300 backdrop-blur-sm h-full flex flex-col ${
                  plan.popular
                    ? 'bg-white/90 dark:bg-gray-800/90 border-2 border-purple-500 dark:border-purple-400 lg:scale-110 lg:z-10'
                    : 'bg-white/70 dark:bg-gray-800/70 border border-gray-200/50 dark:border-gray-700/50 hover:scale-100 sm:hover:scale-[1.08]'
                } ${plan.borderGlow}`}
              >
                {/* Popular Badge */}
                {plan.popular && (
                  <div className="absolute -top-2 sm:-top-2.5 left-1/2 transform -translate-x-1/2">
                    <div className="bg-gradient-to-r from-purple-500 to-pink-500 text-white px-2.5 sm:px-3 py-0.5 sm:py-1 rounded-full text-[10px] sm:text-xs font-bold shadow-lg flex items-center gap-1">
                      <Sparkles className="w-2 sm:w-2.5 h-2 sm:h-2.5" />
                      <span>Popular</span>
                    </div>
                  </div>
                )}

                {/* Icon */}
                <div className="mb-4 sm:mb-5">
                  <div className={`w-12 sm:w-14 h-12 sm:h-14 ${plan.iconBg} rounded-xl sm:rounded-2xl flex items-center justify-center shadow-lg`}>
                    <Icon className="w-6 sm:w-7 h-6 sm:h-7 text-white" />
                  </div>
                </div>

                {/* Plan Name */}
                <h3 className="text-2xl sm:text-3xl font-bold text-gray-900 dark:text-white mb-2 sm:mb-3">
                  {plan.name}
                </h3>

                {/* Price */}
                <div className="mb-3 sm:mb-3.5">
                  <span className="text-3xl sm:text-4xl font-bold bg-gradient-to-r from-gray-900 to-gray-600 dark:from-white dark:to-gray-300 bg-clip-text text-transparent">
                    {billingCycle === 'yearly' && plan.price !== '₹0'
                      ? `₹${Math.round(parseInt(plan.price.replace('₹', '')) * 12 * 0.8)}`
                      : plan.price}
                  </span>
                  <span className="text-gray-500 dark:text-gray-400 ml-1 text-sm">
                    /{billingCycle === 'yearly' ? 'year' : 'month'}
                  </span>
                </div>

                {/* Scans */}
                <div className="mb-5 sm:mb-6">
                  <div className="inline-flex items-center gap-1.5 bg-gradient-to-r from-blue-50 to-cyan-50 dark:from-blue-900/30 dark:to-cyan-900/30 px-3 sm:px-4 py-1 sm:py-1.5 rounded-lg border border-blue-200 dark:border-blue-800 text-sm">
                    <span className="font-bold text-blue-600 dark:text-blue-400">
                      {plan.scans}
                    </span>
                    <span className="text-gray-600 dark:text-gray-400 hidden sm:inline">
                      {plan.period}
                    </span>
                  </div>
                </div>

                {/* CTA Button */}
                <button
                  onClick={() => {
                    if (plan.name === 'Free') {
                      window.location.href = '/register';
                    } else {
                      processPayment(plan, billingCycle);
                    }
                  }}
                  disabled={(!isLoaded && plan.name !== 'Free') || processingPlan === plan.name}
                  className={`w-full py-3 sm:py-3.5 px-4 sm:px-6 rounded-xl font-bold text-base transition-all duration-200 mb-5 sm:mb-6 block text-center ${
                    processingPlan === plan.name ? 'opacity-70 cursor-not-allowed' : ''
                  } ${plan.buttonStyle}`}
                >
                  {processingPlan === plan.name ? 'Processing...' : plan.buttonText}
                </button>

                {/* Features */}
                <div className="space-y-2 sm:space-y-3 flex-1">
                  <p className="text-sm font-bold text-gray-900 dark:text-white uppercase tracking-wide mb-3">
                    What&apos;s Included
                  </p>
                  {plan.features.map((feature, index) => (
                    <div key={index} className="flex items-start gap-2 sm:gap-2.5">
                      <div className="mt-0.5 flex-shrink-0">
                        <div className="w-4 sm:w-4.5 h-4 sm:h-4.5 rounded-full bg-green-100 dark:bg-green-900/30 flex items-center justify-center flex-shrink-0">
                          <Check className="w-2.5 sm:w-3 h-2.5 sm:h-3 text-green-600 dark:text-green-400 font-bold" />
                        </div>
                      </div>
                      <span className="text-sm text-gray-700 dark:text-gray-300 leading-relaxed">
                        {feature}
                      </span>
                    </div>
                  ))}
                </div>
              </div>
            )
          })}
        </div>

        {/* FAQ Section */}
        <div className="max-w-4xl mx-auto mb-16">
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
                  You can upgrade your plan anytime or purchase additional scans as needed. Unused scans don&apos;t roll over to the next month.
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
                  Yes! We offer a 14-day money-back guarantee if you&apos;re not satisfied with your plan.
                </p>
              </div>
            </div>
          </div>
        </div>

        {/* Related Links Section */}
        <div className="mb-16">
          <h2 className="text-3xl font-bold text-gray-900 dark:text-white mb-8 text-center">Learn More About TrulyInvoice</h2>
          <div className="grid md:grid-cols-3 gap-6">
            <Link 
              href="/"
              className="group p-6 bg-white dark:bg-gray-800 rounded-xl border border-gray-200 dark:border-gray-700 hover:border-blue-500 dark:hover:border-blue-500 transition-all hover:shadow-lg"
            >
              <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-2 group-hover:text-blue-600 dark:group-hover:text-blue-400 transition-colors">
                Home
              </h3>
              <p className="text-gray-600 dark:text-gray-400">
                Convert your invoices to Excel with our AI-powered solution.
              </p>
            </Link>

            <Link 
              href="/features"
              className="group p-6 bg-white dark:bg-gray-800 rounded-xl border border-gray-200 dark:border-gray-700 hover:border-blue-500 dark:hover:border-blue-500 transition-all hover:shadow-lg"
            >
              <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-2 group-hover:text-blue-600 dark:group-hover:text-blue-400 transition-colors">
                Features
              </h3>
              <p className="text-gray-600 dark:text-gray-400">
                Explore powerful AI-powered invoice processing capabilities.
              </p>
            </Link>

            <Link 
              href="/about"
              className="group p-6 bg-white dark:bg-gray-800 rounded-xl border border-gray-200 dark:border-gray-700 hover:border-blue-500 dark:hover:border-blue-500 transition-all hover:shadow-lg"
            >
              <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-2 group-hover:text-blue-600 dark:group-hover:text-blue-400 transition-colors">
                About Us
              </h3>
              <p className="text-gray-600 dark:text-gray-400">
                Discover our mission to revolutionize invoice processing.
              </p>
            </Link>
          </div>
        </div>

        {/* Contact Section */}
        <div className="text-center">
          <div className="inline-flex flex-col items-center gap-4 bg-gradient-to-r from-blue-500 to-purple-500 p-8 rounded-2xl shadow-2xl">
            <p className="text-white text-lg font-semibold">
              Need a custom plan for your enterprise?
            </p>
            <Link
              href="/contact"
              className="bg-white text-blue-600 hover:bg-gray-100 px-8 py-3 rounded-xl font-bold transition-all shadow-lg hover:shadow-xl hover:scale-105"
            >
              Contact Sales Team
            </Link>
          </div>
        </div>
      </div>
    </div>
  )
}