'use client'

import { useState, useEffect } from 'react'
import { supabase } from '@/lib/supabase'
import { Loader2 } from 'lucide-react'
import Link from 'next/link'
import UsageWarning from '@/components/UsageWarning'
import UpgradeModal from '@/components/UpgradeModal'
import { useQuotaModal } from '@/hooks/useQuotaModal'

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

      // Call the function with proper auth
      const { data, error } = await supabase.functions.invoke('get-subscription-status', {
        headers: {
          Authorization: `Bearer ${session.access_token}`
        }
      })
      
      if (error) {
        // If the function itself throws an error (e.g., network issue)
        throw error;
      }
      
      // data can be null if no subscription exists, which is a valid state.
      // We set the subscription state to whatever is returned (data or null).
      setSubscription(data);
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

      const { error } = await supabase.functions.invoke('cancel-subscription', {
        headers: {
          Authorization: `Bearer ${session.access_token}`
        }
      })
      
      if (error) throw error
      
      await fetchSubscription()
    } catch (error) {
      console.error('Error cancelling subscription:', error)
      alert('Failed to cancel subscription: ' + (error instanceof Error ? error.message : 'Unknown error'))
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

      <div className="p-6 rounded-lg bg-gradient-to-br from-blue-50 to-purple-50 dark:from-blue-900/20 dark:to-purple-900/20 border border-blue-200 dark:border-blue-800">
        <div className="flex items-center justify-between mb-4">
          <div>
            <h3 className="text-lg font-bold text-gray-900 dark:text-white">{displayData.tier_name}</h3>
            <p className="text-sm text-gray-600 dark:text-gray-400">
              {displayData.scans_used} / {displayData.scans_limit} scans used
            </p>
          </div>
          <div className="text-right">
            <p className="text-3xl font-bold text-gray-900 dark:text-white">
              {displayData.tier === 'free' ? 'Free' : `₹${displayData.price}`}
            </p>
            <p className="text-sm text-gray-600 dark:text-gray-400">
              {displayData.period_end ? `Renews on ${new Date(displayData.period_end).toLocaleDateString()}` : 'Your free plan does not expire.'}
            </p>
          </div>
        </div>
        <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2.5">
          <div
            className="bg-blue-600 h-2.5 rounded-full"
            style={{ width: `${usagePercentage}%` }}
          ></div>
        </div>
        <div className="flex justify-between mt-4">
          <Link href="/pricing" className="px-6 py-2.5 bg-blue-600 hover:bg-blue-700 dark:bg-blue-500 dark:hover:bg-blue-600 text-white rounded-lg font-semibold transition-colors">
            {displayData.tier === 'free' ? 'Upgrade Plan' : 'Change Plan'}
          </Link>
          {displayData.tier !== 'free' && (
            <button
              onClick={handleCancel}
              disabled={cancelling}
              className="px-6 py-2.5 bg-red-600 hover:bg-red-700 dark:bg-red-500 dark:hover:bg-red-600 text-white rounded-lg font-semibold transition-colors disabled:opacity-50"
            >
              {cancelling ? 'Cancelling...' : 'Cancel Subscription'}
            </button>
          )}
        </div>
      </div>

      <div>
        <h3 className="font-semibold text-gray-900 dark:text-white mb-3">Payment Methods</h3>
        <div className="p-4 rounded-lg border border-gray-200 dark:border-gray-800 text-center">
          <p className="text-gray-500 dark:text-gray-400">No payment methods added</p>
          <button className="mt-2 text-blue-600 dark:text-blue-400 hover:text-blue-700 dark:hover:text-blue-300 font-semibold">
            + Add Payment Method
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
