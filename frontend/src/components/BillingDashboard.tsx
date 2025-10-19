'use client'

import { useState, useEffect } from 'react'
import { supabase } from '@/lib/supabase'
import { Loader2 } from 'lucide-react'
import Link from 'next/link'

export default function BillingDashboard() {
  const [subscription, setSubscription] = useState<any>(null)
  const [loading, setLoading] = useState(true)
  const [cancelling, setCancelling] = useState(false)

  useEffect(() => {
    fetchSubscription()
  }, [])

  async function fetchSubscription() {
    try {
      const { data, error } = await supabase.functions.invoke('get-subscription-status')
      if (error) throw error
      setSubscription(data)
    } catch (error) {
      console.error('Error fetching subscription:', error)
    } finally {
      setLoading(false)
    }
  }

  async function handleCancel() {
    if (window.confirm('Are you sure you want to cancel your subscription?')) {
      try {
        setCancelling(true)
        const { error } = await supabase.functions.invoke('cancel-subscription')
        if (error) throw error
        await fetchSubscription()
      } catch (error) {
        console.error('Error cancelling subscription:', error)
        alert('Failed to cancel subscription.')
      } finally {
        setCancelling(false)
      }
    }
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center py-12">
        <Loader2 className="w-8 h-8 animate-spin text-blue-600 dark:text-blue-400" />
      </div>
    )
  }

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-xl font-bold text-gray-900 dark:text-white mb-4">Billing & Subscription</h2>
        <p className="text-gray-600 dark:text-gray-400 text-sm mb-6">Manage your subscription and payment methods.</p>
      </div>

      <div className="p-6 rounded-lg bg-gradient-to-br from-blue-50 to-purple-50 dark:from-blue-900/20 dark:to-purple-900/20 border border-blue-200 dark:border-blue-800">
        <div className="flex items-center justify-between mb-4">
          <div>
            <h3 className="text-lg font-bold text-gray-900 dark:text-white">{subscription.tier_name}</h3>
            <p className="text-sm text-gray-600 dark:text-gray-400">
              {subscription.scans_used} / {subscription.scans_limit} scans used
            </p>
          </div>
          <div className="text-right">
            <p className="text-3xl font-bold text-gray-900 dark:text-white">
              {subscription.tier === 'free' ? 'Free' : `₹${subscription.price}`}
            </p>
            <p className="text-sm text-gray-600 dark:text-gray-400">
              Renews on {new Date(subscription.period_end).toLocaleDateString()}
            </p>
          </div>
        </div>
        <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2.5">
          <div
            className="bg-blue-600 h-2.5 rounded-full"
            style={{ width: `${subscription.usage_percentage}%` }}
          ></div>
        </div>
        <div className="flex justify-between mt-4">
          <Link href="/pricing" className="px-6 py-2.5 bg-blue-600 hover:bg-blue-700 dark:bg-blue-500 dark:hover:bg-blue-600 text-white rounded-lg font-semibold transition-colors">
            Upgrade Plan
          </Link>
          {subscription.tier !== 'free' && (
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
    </div>
  )
}
