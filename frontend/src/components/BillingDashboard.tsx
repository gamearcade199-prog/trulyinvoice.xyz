'use client'

import { useState, useEffect } from 'react'
import { supabase } from '@/lib/supabase'
import { Loader2 } from 'lucide-react'
import Link from 'next/link'
import UsageWarning from '@/components/UsageWarning'
import UpgradeModal from '@/components/UpgradeModal'
import { useQuotaModal } from '@/hooks/useQuotaModal'
import toast from 'react-hot-toast'

export default function BillingDashboard() {
  const [subscription, setSubscription] = useState<any>(null)
  const [loading, setLoading] = useState(true)
  const [cancelling, setCancelling] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const { isModalOpen, showUpgradeModal, hideUpgradeModal } = useQuotaModal()

  useEffect(() => {
    fetchSubscription()
  }, [])

  async function fetchSubscription() {
    try {
      // Get the session first
      const { data: { session }, error: sessionError } = await supabase.auth.getSession()
      if (sessionError) throw sessionError
      if (!session) throw new Error('No session')

      // Call backend API instead of Edge Function
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/auth/subscription/${session.user.id}`, {
        headers: {
          'Authorization': `Bearer ${session.access_token}`,
          'Content-Type': 'application/json'
        }
      })
      
      if (!response.ok) {
        throw new Error(`Failed to fetch subscription: ${response.status}`)
      }
      
      const result = await response.json()
      
      // Backend returns { success: true, subscription: {...} }
      if (result.success && result.subscription) {
        setSubscription(result.subscription);
      } else {
        // No subscription found - user is on free plan
        setSubscription(null);
      }
      setError(null); // Clear any previous errors
    } catch (error) {
      console.error('Error fetching subscription:', error)
      setError(error instanceof Error ? error.message : 'Failed to load subscription')
    } finally {
      setLoading(false)
    }
  }

  async function handleCancel() {
    if (!window.confirm('Are you sure you want to cancel your subscription?')) {
      return
    }

    try {
      setCancelling(true)
      
      // Get current session
      const { data: { session }, error: sessionError } = await supabase.auth.getSession()
      if (sessionError) throw sessionError
      if (!session) throw new Error('No session')

      // Call backend API to cancel subscription
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/subscriptions/cancel`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${session.access_token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          user_id: session.user.id
        })
      })
      
      if (!response.ok) {
        throw new Error('Failed to cancel subscription')
      }
      
      toast.success('Subscription cancelled successfully')
      await fetchSubscription()
    } catch (error) {
      console.error('Error cancelling subscription:', error)
      toast.error('Failed to cancel subscription: ' + (error instanceof Error ? error.message : 'Unknown error'))
    } finally {
      setCancelling(false)
    }
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center py-12">
        <Loader2 className="w-8 h-8 animate-spin text-blue-600 dark:text-blue-400" />
      </div>
    );
  }

  if (error) {
    return (
      <div className="p-6 rounded-lg bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800">
        <h3 className="text-lg font-bold text-red-900 dark:text-red-200">Failed to load subscription</h3>
        <p className="text-sm text-red-600 dark:text-red-400">{error}</p>
        <button
          onClick={() => fetchSubscription()}
          className="mt-4 px-4 py-2 bg-red-100 dark:bg-red-900 text-red-900 dark:text-red-100 rounded-md hover:bg-red-200 dark:hover:bg-red-800"
        >
          Retry
        </button>
      </div>
    );
  }

  // Define plan details to match the public pricing page
  const planDetails: { [key: string]: { name: string; price: number; scans: number } } = {
    basic: { name: 'Basic', price: 149, scans: 80 },
    pro: { name: 'Pro', price: 299, scans: 200 },
    ultra: { name: 'Ultra', price: 599, scans: 500 },
    max: { name: 'Max', price: 999, scans: 1000 },
    // The 'free' plan is handled by the `else` block below
  };

  let displayData;

  if (subscription && subscription.tier && subscription.tier !== 'free') {
    // User has a paid subscription
    const details = planDetails[subscription.tier] || { name: 'Unknown Plan', price: 0, scans: 0 };
    displayData = {
      tier_name: details.name,
      scans_used: subscription.scans_used_this_period || 0,
      scans_limit: details.scans,
      price: details.price,
      period_end: subscription.current_period_end,
      tier: subscription.tier,
    };
  } else {
    // User is on the Free Plan (no subscription record or subscription.tier is 'free')
    displayData = {
      tier_name: 'Free Plan',
      scans_used: 0, // Assuming free users' scan count isn't tracked in the subscription table
      scans_limit: 10, // Match the 10 free scans from the pricing page
      price: 0,
      period_end: null,
      tier: 'free',
    };
  }

  const usagePercentage = displayData.scans_limit > 0 ? (displayData.scans_used / displayData.scans_limit) * 100 : 0;

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-xl font-bold text-gray-900 dark:text-white mb-4">Billing & Subscription</h2>
        <p className="text-gray-600 dark:text-gray-400 text-sm mb-6">Manage your subscription and payment methods.</p>
      </div>

      {/* Usage Warning Component */}
      <UsageWarning
        scansUsed={displayData.scans_used}
        scansLimit={displayData.scans_limit}
        currentPlan={displayData.tier}
        onUpgradeClick={() => showUpgradeModal('proactive_warning')}
      />

      {/* Current Plan Card */}
      <div className="relative overflow-hidden rounded-2xl bg-gradient-to-br from-blue-50 via-indigo-50 to-purple-50 dark:from-blue-950/50 dark:via-indigo-950/40 dark:to-purple-950/30 border border-blue-200 dark:border-blue-800/50 shadow-xl">
        {/* Decorative Background Elements */}
        <div className="absolute top-0 right-0 w-64 h-64 bg-gradient-to-br from-blue-400/10 to-purple-400/10 rounded-full blur-3xl"></div>
        <div className="absolute bottom-0 left-0 w-48 h-48 bg-gradient-to-tr from-indigo-400/10 to-blue-400/10 rounded-full blur-3xl"></div>
        
        <div className="relative p-8">
          {/* Header Section */}
          <div className="flex items-start justify-between mb-6">
            <div className="flex-1">
              <div className="flex items-center gap-3 mb-2">
                <h3 className="text-2xl font-bold text-gray-900 dark:text-white">
                  {displayData.tier_name}
                </h3>
                <span className={`
                  px-3 py-1 rounded-full text-xs font-bold shadow-sm
                  ${displayData.tier === 'free' 
                    ? 'bg-gray-600 text-white' 
                    : 'bg-gradient-to-r from-blue-600 to-indigo-600 text-white'
                  }
                `}>
                  {displayData.tier === 'free' ? 'Free' : 'Active'}
                </span>
              </div>
              <p className="text-sm text-gray-600 dark:text-gray-400 font-medium">
                {displayData.period_end 
                  ? `Renews ${new Date(displayData.period_end).toLocaleDateString('en-IN', { month: 'short', day: 'numeric', year: 'numeric' })}` 
                  : displayData.tier === 'free' ? 'Never expires' : 'Active subscription'}
              </p>
            </div>
            
            <div className="text-right">
              <p className="text-4xl font-bold bg-gradient-to-r from-blue-600 to-indigo-600 dark:from-blue-400 dark:to-indigo-400 bg-clip-text text-transparent">
                {displayData.tier === 'free' ? '₹0' : `₹${displayData.price}`}
              </p>
              <p className="text-sm text-gray-600 dark:text-gray-400 font-medium mt-1">
                per month
              </p>
            </div>
          </div>

          {/* Usage Stats */}
          <div className="mb-6">
            <div className="flex items-center justify-between mb-3">
              <div>
                <p className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                  Scans This Month
                </p>
                <div className="flex items-baseline gap-2">
                  <span className="text-3xl font-bold text-gray-900 dark:text-white">
                    {displayData.scans_used}
                  </span>
                  <span className="text-lg text-gray-500 dark:text-gray-400">
                    / {displayData.scans_limit}
                  </span>
                </div>
              </div>
              
              <div className="text-right">
                <div className={`
                  inline-flex items-center gap-2 px-4 py-2 rounded-xl shadow-sm
                  ${usagePercentage >= 90 
                    ? 'bg-red-100 dark:bg-red-900/40' 
                    : usagePercentage >= 80 
                    ? 'bg-amber-100 dark:bg-amber-900/40' 
                    : 'bg-emerald-100 dark:bg-emerald-900/40'
                  }
                `}>
                  <span className={`
                    text-2xl font-bold
                    ${usagePercentage >= 90 
                      ? 'text-red-600 dark:text-red-400' 
                      : usagePercentage >= 80 
                      ? 'text-amber-600 dark:text-amber-400' 
                      : 'text-emerald-600 dark:text-emerald-400'
                    }
                  `}>
                    {Math.round(usagePercentage)}%
                  </span>
                  <span className={`
                    text-xs font-medium
                    ${usagePercentage >= 90 
                      ? 'text-red-700 dark:text-red-300' 
                      : usagePercentage >= 80 
                      ? 'text-amber-700 dark:text-amber-300' 
                      : 'text-emerald-700 dark:text-emerald-300'
                    }
                  `}>
                    used
                  </span>
                </div>
              </div>
            </div>

            {/* Progress Bar */}
            <div className="relative w-full h-4 bg-gray-200/60 dark:bg-gray-800/60 rounded-full overflow-hidden shadow-inner backdrop-blur-sm">
              <div
                className={`
                  absolute inset-y-0 left-0 h-full transition-all duration-700 ease-out rounded-full shadow-sm
                  ${usagePercentage >= 90 
                    ? 'bg-gradient-to-r from-red-500 via-rose-500 to-red-600' 
                    : usagePercentage >= 80 
                    ? 'bg-gradient-to-r from-amber-500 via-yellow-500 to-orange-600' 
                    : 'bg-gradient-to-r from-blue-500 via-indigo-500 to-purple-600'
                  }
                `}
                style={{ width: `${usagePercentage}%` }}
              />
            </div>

            {/* Remaining Scans */}
            <p className="text-sm text-gray-600 dark:text-gray-400 mt-2 font-medium">
              {displayData.scans_limit - displayData.scans_used} scans remaining this period
            </p>
          </div>

          {/* Action Buttons */}
          <div className="flex flex-wrap gap-3">
            <Link 
              href="/pricing" 
              className="flex-1 min-w-[160px] px-6 py-3 bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700 text-white rounded-xl font-semibold transition-all shadow-lg shadow-blue-500/30 hover:shadow-xl hover:scale-105 active:scale-95 text-center"
            >
              {displayData.tier === 'free' ? '✨ Upgrade Plan' : '🔄 Change Plan'}
            </Link>
            
            {displayData.tier !== 'free' && (
              <button
                onClick={handleCancel}
                disabled={cancelling}
                className="px-6 py-3 bg-white dark:bg-gray-800 border-2 border-gray-300 dark:border-gray-600 text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-700 rounded-xl font-semibold transition-all disabled:opacity-50 disabled:cursor-not-allowed hover:scale-105 active:scale-95"
              >
                {cancelling ? (
                  <span className="flex items-center gap-2">
                    <Loader2 className="w-4 h-4 animate-spin" />
                    Cancelling...
                  </span>
                ) : (
                  'Cancel Subscription'
                )}
              </button>
            )}
          </div>
        </div>
      </div>

      {/* Payment Methods */}
      <div className="rounded-2xl bg-white dark:bg-gray-900/50 border border-gray-200 dark:border-gray-800 shadow-lg overflow-hidden">
        <div className="p-6 border-b border-gray-200 dark:border-gray-800">
          <h3 className="text-lg font-bold text-gray-900 dark:text-white">Payment Methods</h3>
          <p className="text-sm text-gray-600 dark:text-gray-400 mt-1">Manage your saved payment methods</p>
        </div>
        <div className="p-8 text-center">
          <div className="w-16 h-16 mx-auto mb-4 rounded-full bg-gray-100 dark:bg-gray-800 flex items-center justify-center">
            <svg className="w-8 h-8 text-gray-400 dark:text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 10h18M7 15h1m4 0h1m-7 4h12a3 3 0 003-3V8a3 3 0 00-3-3H6a3 3 0 00-3 3v8a3 3 0 003 3z" />
            </svg>
          </div>
          <p className="text-gray-600 dark:text-gray-400 mb-4 font-medium">No payment methods added yet</p>
          <button className="inline-flex items-center gap-2 px-5 py-2.5 bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700 text-white rounded-xl font-semibold shadow-lg shadow-blue-500/30 transition-all hover:scale-105 active:scale-95">
            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
            </svg>
            Add Payment Method
          </button>
        </div>
      </div>

      {/* Upgrade Modal */}
      <UpgradeModal
        isOpen={isModalOpen}
        onClose={hideUpgradeModal}
        currentPlan={displayData.tier}
        scansUsed={displayData.scans_used}
        scansLimit={displayData.scans_limit}
        reason="proactive_warning"
      />
    </div>
  );
}
