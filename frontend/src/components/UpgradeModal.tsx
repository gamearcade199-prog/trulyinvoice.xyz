'use client'

import { useState } from 'react'
import { useRouter } from 'next/navigation'
import { X, Sparkles, Zap, CheckCircle2, TrendingUp } from 'lucide-react'

interface UpgradeModalProps {
  isOpen: boolean
  onClose: () => void
  currentPlan: string
  scansUsed: number
  scansLimit: number
  reason: 'quota_exceeded' | 'feature_locked' | 'proactive_warning'
}

interface PlanCardData {
  tier: string
  name: string
  price: number
  scans: number
  features: string[]
  badge?: string
  highlight?: boolean
}

const PLANS: PlanCardData[] = [
  {
    tier: 'basic',
    name: 'Basic Plan',
    price: 149,
    scans: 80,
    features: ['95% AI accuracy', '7-day storage', 'Bulk upload (5)'],
    badge: 'Most Popular'
  },
  {
    tier: 'pro',
    name: 'Pro Plan',
    price: 299,
    scans: 200,
    features: ['97% AI accuracy', '30-day storage', 'Bulk upload (10)'],
    badge: 'Best Value',
    highlight: true
  },
  {
    tier: 'ultra',
    name: 'Ultra Plan',
    price: 599,
    scans: 500,
    features: ['99% AI accuracy', '60-day storage', 'Bulk upload (50)']
  }
]

export default function UpgradeModal({
  isOpen,
  onClose,
  currentPlan,
  scansUsed,
  scansLimit,
  reason
}: UpgradeModalProps) {
  const router = useRouter()
  const [selectedPlan, setSelectedPlan] = useState<string>('')

  if (!isOpen) return null

  const handleUpgrade = (tier: string) => {
    // Close modal and navigate to pricing page with pre-selected plan
    onClose()
    router.push(`/pricing?plan=${tier}&upgrade=true`)
  }

  const getTitle = () => {
    switch (reason) {
      case 'quota_exceeded':
        return '🚀 Upgrade to Continue Processing'
      case 'feature_locked':
        return '✨ Unlock Premium Features'
      case 'proactive_warning':
        return '⚠️ Running Low on Scans'
      default:
        return '🚀 Upgrade Your Plan'
    }
  }

  const getDescription = () => {
    switch (reason) {
      case 'quota_exceeded':
        return `You've used all ${scansLimit} scans this month. Upgrade to continue processing invoices without interruption.`
      case 'feature_locked':
        return 'Unlock advanced features like bulk upload, extended storage, and higher accuracy with a premium plan.'
      case 'proactive_warning':
        return `You've used ${scansUsed} of ${scansLimit} scans. Consider upgrading to avoid hitting your limit.`
      default:
        return 'Choose a plan that fits your needs and start processing more invoices today.'
    }
  }

  // Filter plans based on current plan
  const availablePlans = PLANS.filter(plan => {
    const tierOrder = ['free', 'basic', 'pro', 'ultra', 'max']
    const currentIndex = tierOrder.indexOf(currentPlan.toLowerCase())
    const planIndex = tierOrder.indexOf(plan.tier)
    return planIndex > currentIndex
  })

  return (
    <>
      {/* Backdrop */}
      <div 
        className="fixed inset-0 bg-black/50 backdrop-blur-sm z-50 animate-in fade-in duration-200"
        onClick={onClose}
      />

      {/* Modal */}
      <div className="fixed inset-0 z-50 flex items-center justify-center p-3 sm:p-4 pointer-events-none">
        <div 
          className="bg-white dark:bg-gray-900 rounded-xl sm:rounded-2xl shadow-2xl max-w-4xl w-full max-h-[90vh] overflow-y-auto pointer-events-auto animate-in zoom-in-95 duration-200"
          onClick={(e) => e.stopPropagation()}
        >
          {/* Header */}
          <div className="sticky top-0 bg-gradient-to-r from-blue-600 to-purple-600 text-white p-4 sm:p-6 rounded-t-xl sm:rounded-t-2xl">
            <button
              onClick={onClose}
              className="absolute top-3 right-3 sm:top-4 sm:right-4 p-2 hover:bg-white/20 rounded-full transition-colors min-w-[44px] min-h-[44px] flex items-center justify-center"
            >
              <X className="w-5 h-5" />
            </button>

            <div className="flex items-center gap-2 sm:gap-3 mb-2 pr-10 sm:pr-0">
              {reason === 'quota_exceeded' && <Zap className="w-6 h-6 sm:w-8 sm:h-8 flex-shrink-0" />}
              {reason === 'feature_locked' && <Sparkles className="w-6 h-6 sm:w-8 sm:h-8 flex-shrink-0" />}
              {reason === 'proactive_warning' && <TrendingUp className="w-6 h-6 sm:w-8 sm:h-8 flex-shrink-0" />}
              <h2 className="text-lg sm:text-2xl md:text-3xl font-bold leading-tight">
                {getTitle()}
              </h2>
            </div>
            
            <p className="text-blue-100 text-xs sm:text-sm md:text-base leading-relaxed">
              {getDescription()}
            </p>

            {/* Current Usage Badge */}
            <div className="mt-3 sm:mt-4 inline-flex items-center gap-1.5 sm:gap-2 bg-white/20 rounded-full px-3 py-1.5 sm:px-4 sm:py-2 text-xs sm:text-sm">
              <span className="font-semibold whitespace-nowrap">Current: {currentPlan}</span>
              <span>•</span>
              <span className="whitespace-nowrap">{scansUsed} / {scansLimit} scans used</span>
            </div>
          </div>

          {/* Plans Grid */}
          <div className="p-4 sm:p-6">
            <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
              Choose Your New Plan
            </h3>

            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3 sm:gap-4">
              {availablePlans.map((plan) => (
                <div
                  key={plan.tier}
                  className={`
                    relative border-2 rounded-lg sm:rounded-xl p-4 sm:p-6 cursor-pointer transition-all
                    ${plan.highlight 
                      ? 'border-blue-500 bg-blue-50 dark:bg-blue-900/20' 
                      : 'border-gray-200 dark:border-gray-700 hover:border-blue-400'
                    }
                    ${selectedPlan === plan.tier ? 'ring-4 ring-blue-500 ring-opacity-50' : ''}
                  `}
                  onClick={() => setSelectedPlan(plan.tier)}
                >
                  {/* Badge */}
                  {plan.badge && (
                    <div className="absolute -top-2.5 sm:-top-3 left-1/2 -translate-x-1/2 bg-gradient-to-r from-blue-600 to-purple-600 text-white text-[10px] sm:text-xs font-bold px-2.5 py-0.5 sm:px-3 sm:py-1 rounded-full whitespace-nowrap">
                      {plan.badge}
                    </div>
                  )}

                  {/* Plan Name */}
                  <h4 className="text-base sm:text-xl font-bold text-gray-900 dark:text-white mb-2 mt-2 sm:mt-0">
                    {plan.name}
                  </h4>

                  {/* Price */}
                  <div className="mb-3 sm:mb-4">
                    <span className="text-2xl sm:text-3xl font-bold text-blue-600 dark:text-blue-400">
                      ₹{plan.price}
                    </span>
                    <span className="text-gray-600 dark:text-gray-400 text-xs sm:text-sm">/month</span>
                  </div>

                  {/* Scans */}
                  <div className="bg-white dark:bg-gray-800 rounded-lg p-2.5 sm:p-3 mb-3 sm:mb-4 border border-gray-200 dark:border-gray-700">
                    <div className="text-xl sm:text-2xl font-bold text-gray-900 dark:text-white">
                      {plan.scans} scans
                    </div>
                    <div className="text-xs sm:text-sm text-gray-600 dark:text-gray-400">
                      per month
                    </div>
                  </div>

                  {/* Features */}
                  <ul className="space-y-1.5 sm:space-y-2 mb-3 sm:mb-4">
                    {plan.features.map((feature, idx) => (
                      <li key={idx} className="flex items-start gap-2 text-xs sm:text-sm">
                        <CheckCircle2 className="w-3.5 h-3.5 sm:w-4 sm:h-4 text-green-500 flex-shrink-0 mt-0.5" />
                        <span className="text-gray-700 dark:text-gray-300 leading-tight">{feature}</span>
                      </li>
                    ))}
                  </ul>

                  {/* Select Button */}
                  <button
                    onClick={(e) => {
                      e.stopPropagation()
                      handleUpgrade(plan.tier)
                    }}
                    className={`
                      w-full py-2.5 sm:py-3 rounded-lg font-semibold transition-all text-sm sm:text-base min-h-[44px]
                      ${plan.highlight
                        ? 'bg-gradient-to-r from-blue-600 to-purple-600 text-white hover:from-blue-700 hover:to-purple-700'
                        : 'bg-gray-200 dark:bg-gray-700 text-gray-900 dark:text-white hover:bg-gray-300 dark:hover:bg-gray-600'
                      }
                    `}
                  >
                    Upgrade to {plan.name}
                  </button>
                </div>
              ))}
            </div>

            {/* View All Plans Link */}
            <div className="mt-4 sm:mt-6 text-center">
              <button
                onClick={() => {
                  onClose()
                  router.push('/pricing')
                }}
                className="text-blue-600 dark:text-blue-400 hover:underline font-medium text-sm sm:text-base min-h-[44px] inline-flex items-center justify-center px-4"
              >
                View All Plans & Features →
              </button>
            </div>
          </div>

          {/* Footer */}
          <div className="bg-gray-50 dark:bg-gray-800 p-4 sm:p-6 rounded-b-xl sm:rounded-b-2xl border-t border-gray-200 dark:border-gray-700">
            <div className="flex flex-col sm:flex-row items-center justify-between gap-3 sm:gap-4">
              <div className="text-xs sm:text-sm text-gray-600 dark:text-gray-400 text-center sm:text-left">
                ✅ Instant activation • 💳 Secure payment • 🔄 Cancel anytime
              </div>
              
              <button
                onClick={onClose}
                className="w-full sm:w-auto px-6 py-2.5 border border-gray-300 dark:border-gray-600 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors text-gray-700 dark:text-gray-300 text-sm sm:text-base min-h-[44px]"
              >
                Maybe Later
              </button>
            </div>
          </div>
        </div>
      </div>
    </>
  )
}
