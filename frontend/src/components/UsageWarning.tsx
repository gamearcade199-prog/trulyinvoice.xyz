'use client'

import { AlertCircle, Zap, TrendingUp } from 'lucide-react'
import { useRouter } from 'next/navigation'

interface UsageWarningProps {
  scansUsed: number
  scansLimit: number
  currentPlan: string
  onUpgradeClick?: () => void
}

export default function UsageWarning({
  scansUsed,
  scansLimit,
  currentPlan,
  onUpgradeClick
}: UsageWarningProps) {
  const router = useRouter()
  const percentage = (scansUsed / scansLimit) * 100
  
  // Don't show warning if below 80%
  if (percentage < 80) return null

  const isUrgent = percentage >= 90
  const scansRemaining = scansLimit - scansUsed

  const handleUpgradeClick = () => {
    if (onUpgradeClick) {
      onUpgradeClick()
    } else {
      router.push('/pricing')
    }
  }

  return (
    <div
      className={`
        rounded-xl p-4 border-2 mb-6 animate-in slide-in-from-top duration-300
        ${isUrgent
          ? 'bg-red-50 dark:bg-red-900/20 border-red-300 dark:border-red-800'
          : 'bg-yellow-50 dark:bg-yellow-900/20 border-yellow-300 dark:border-yellow-800'
        }
      `}
    >
      <div className="flex items-start gap-3">
        {/* Icon */}
        <div className={`
          p-2 rounded-lg flex-shrink-0
          ${isUrgent 
            ? 'bg-red-100 dark:bg-red-900/40' 
            : 'bg-yellow-100 dark:bg-yellow-900/40'
          }
        `}>
          {isUrgent ? (
            <Zap className="w-5 h-5 text-red-600 dark:text-red-400" />
          ) : (
            <AlertCircle className="w-5 h-5 text-yellow-600 dark:text-yellow-400" />
          )}
        </div>

        {/* Content */}
        <div className="flex-1">
          <h4 className={`
            font-bold text-lg mb-1
            ${isUrgent 
              ? 'text-red-900 dark:text-red-100' 
              : 'text-yellow-900 dark:text-yellow-100'
            }
          `}>
            {isUrgent ? '🚨 Last scan remaining!' : '⚠️ Running low on scans'}
          </h4>
          
          <p className={`
            text-sm mb-3
            ${isUrgent 
              ? 'text-red-800 dark:text-red-200' 
              : 'text-yellow-800 dark:text-yellow-200'
            }
          `}>
            {isUrgent ? (
              <>
                You have only <strong>{scansRemaining} scan{scansRemaining !== 1 ? 's' : ''}</strong> left on your {currentPlan} plan.
                Upgrade now to avoid interruption.
              </>
            ) : (
              <>
                You've used <strong>{scansUsed} of {scansLimit} scans</strong> this month.
                Consider upgrading to continue processing without limits.
              </>
            )}
          </p>

          {/* Progress Bar */}
          <div className="mb-3">
            <div className="flex justify-between text-xs mb-1">
              <span className={
                isUrgent 
                  ? 'text-red-700 dark:text-red-300' 
                  : 'text-yellow-700 dark:text-yellow-300'
              }>
                {scansUsed} used
              </span>
              <span className={
                isUrgent 
                  ? 'text-red-700 dark:text-red-300' 
                  : 'text-yellow-700 dark:text-yellow-300'
              }>
                {scansRemaining} remaining
              </span>
            </div>
            <div className={`
              w-full h-2 rounded-full overflow-hidden
              ${isUrgent 
                ? 'bg-red-200 dark:bg-red-900/40' 
                : 'bg-yellow-200 dark:bg-yellow-900/40'
              }
            `}>
              <div
                className={`
                  h-full transition-all duration-500 rounded-full
                  ${isUrgent 
                    ? 'bg-gradient-to-r from-red-500 to-red-600' 
                    : 'bg-gradient-to-r from-yellow-500 to-yellow-600'
                  }
                `}
                style={{ width: `${percentage}%` }}
              />
            </div>
          </div>

          {/* Action Buttons */}
          <div className="flex flex-wrap gap-2">
            <button
              onClick={handleUpgradeClick}
              className={`
                px-4 py-2 rounded-lg font-semibold text-sm transition-all
                ${isUrgent
                  ? 'bg-gradient-to-r from-red-600 to-red-700 hover:from-red-700 hover:to-red-800 text-white shadow-lg shadow-red-500/30'
                  : 'bg-gradient-to-r from-yellow-600 to-yellow-700 hover:from-yellow-700 hover:to-yellow-800 text-white shadow-lg shadow-yellow-500/30'
                }
              `}
            >
              {isUrgent ? '⚡ Upgrade Now' : '🚀 View Plans'}
            </button>

            <button
              onClick={() => router.push('/dashboard')}
              className={`
                px-4 py-2 rounded-lg font-semibold text-sm border-2 transition-all
                ${isUrgent
                  ? 'border-red-300 dark:border-red-700 text-red-700 dark:text-red-300 hover:bg-red-100 dark:hover:bg-red-900/40'
                  : 'border-yellow-300 dark:border-yellow-700 text-yellow-700 dark:text-yellow-300 hover:bg-yellow-100 dark:hover:bg-yellow-900/40'
                }
              `}
            >
              View Usage
            </button>
          </div>
        </div>

        {/* Stats Badge (Desktop only) */}
        <div className="hidden sm:block">
          <div className={`
            px-4 py-3 rounded-lg text-center min-w-[100px]
            ${isUrgent 
              ? 'bg-red-100 dark:bg-red-900/40' 
              : 'bg-yellow-100 dark:bg-yellow-900/40'
            }
          `}>
            <div className={`
              text-2xl font-bold
              ${isUrgent 
                ? 'text-red-600 dark:text-red-400' 
                : 'text-yellow-600 dark:text-yellow-400'
              }
            `}>
              {Math.round(percentage)}%
            </div>
            <div className={`
              text-xs
              ${isUrgent 
                ? 'text-red-700 dark:text-red-300' 
                : 'text-yellow-700 dark:text-yellow-300'
              }
            `}>
              used
            </div>
          </div>
        </div>
      </div>

      {/* Recommended Plan (for urgent cases) */}
      {isUrgent && currentPlan === 'free' && (
        <div className="mt-3 pt-3 border-t border-red-200 dark:border-red-800">
          <div className="flex items-center gap-2 text-sm">
            <TrendingUp className="w-4 h-4 text-red-600 dark:text-red-400" />
            <span className="text-red-800 dark:text-red-200 font-medium">
              💡 Recommended: Upgrade to <strong>Basic Plan (₹149/mo)</strong> for 80 scans/month
            </span>
          </div>
        </div>
      )}
    </div>
  )
}
