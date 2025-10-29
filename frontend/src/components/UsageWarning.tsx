'use client'

import { Zap, TrendingUp, Sparkles } from 'lucide-react'
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
        rounded-2xl p-5 border backdrop-blur-sm animate-in slide-in-from-top duration-300
        ${isUrgent
          ? 'bg-gradient-to-br from-red-50 via-rose-50 to-orange-50 dark:from-red-950/40 dark:via-rose-950/30 dark:to-orange-950/20 border-red-200 dark:border-red-800/50 shadow-lg shadow-red-100 dark:shadow-red-950/30'
          : 'bg-gradient-to-br from-amber-50 via-yellow-50 to-orange-50 dark:from-amber-950/40 dark:via-yellow-950/30 dark:to-orange-950/20 border-amber-200 dark:border-amber-800/50 shadow-lg shadow-amber-100 dark:shadow-amber-950/30'
        }
      `}
    >
      <div className="flex items-start gap-4">
        {/* Icon */}
        <div className={`
          p-3 rounded-xl flex-shrink-0 shadow-lg
          ${isUrgent 
            ? 'bg-gradient-to-br from-red-500 to-rose-600 dark:from-red-600 dark:to-rose-700' 
            : 'bg-gradient-to-br from-amber-500 to-orange-600 dark:from-amber-600 dark:to-orange-700'
          }
        `}>
          {isUrgent ? (
            <Zap className="w-6 h-6 text-white drop-shadow" fill="currentColor" />
          ) : (
            <Sparkles className="w-6 h-6 text-white drop-shadow" />
          )}
        </div>

        {/* Content */}
        <div className="flex-1">
          <div className="flex items-center gap-2 mb-2">
            <h4 className={`
              font-bold text-lg
              ${isUrgent 
                ? 'text-red-900 dark:text-red-100' 
                : 'text-amber-900 dark:text-amber-100'
              }
            `}>
              {isUrgent ? 'Almost Out of Scans!' : 'Running Low on Scans'}
            </h4>
            <span className={`
              px-2.5 py-0.5 rounded-full text-xs font-bold
              ${isUrgent
                ? 'bg-red-600 text-white'
                : 'bg-amber-600 text-white'
              }
            `}>
              {Math.round(percentage)}%
            </span>
          </div>
          
          <p className={`
            text-sm mb-4 leading-relaxed
            ${isUrgent 
              ? 'text-red-800 dark:text-red-200' 
              : 'text-amber-800 dark:text-amber-200'
            }
          `}>
            {isUrgent ? (
              <>
                Only <strong className="font-bold">{scansRemaining} scan{scansRemaining !== 1 ? 's' : ''}</strong> remaining this month. Upgrade now to keep processing invoices.
              </>
            ) : (
              <>
                You've used <strong className="font-bold">{scansUsed} of {scansLimit}</strong> scans. Consider upgrading for uninterrupted service.
              </>
            )}
          </p>

          {/* Progress Bar */}
          <div className="mb-4">
            <div className="flex justify-between text-xs font-medium mb-2">
              <span className={
                isUrgent 
                  ? 'text-red-700 dark:text-red-300' 
                  : 'text-amber-700 dark:text-amber-300'
              }>
                {scansUsed} used
              </span>
              <span className={
                isUrgent 
                  ? 'text-red-700 dark:text-red-300' 
                  : 'text-amber-700 dark:text-amber-300'
              }>
                {scansRemaining} left
              </span>
            </div>
            <div className={`
              relative w-full h-3 rounded-full overflow-hidden shadow-inner
              ${isUrgent 
                ? 'bg-red-200/60 dark:bg-red-950/60' 
                : 'bg-amber-200/60 dark:bg-amber-950/60'
              }
            `}>
              <div
                className={`
                  absolute inset-y-0 left-0 h-full transition-all duration-700 ease-out rounded-full shadow-sm
                  ${isUrgent 
                    ? 'bg-gradient-to-r from-red-500 via-rose-500 to-red-600' 
                    : 'bg-gradient-to-r from-amber-500 via-yellow-500 to-orange-600'
                  }
                `}
                style={{ width: `${percentage}%` }}
              />
            </div>
          </div>

          {/* Action Buttons */}
          <div className="flex flex-wrap gap-3">
            <button
              onClick={handleUpgradeClick}
              className={`
                px-5 py-2.5 rounded-xl font-semibold text-sm transition-all shadow-md hover:shadow-lg hover:scale-105 active:scale-95
                ${isUrgent
                  ? 'bg-gradient-to-r from-red-600 to-rose-600 hover:from-red-700 hover:to-rose-700 text-white'
                  : 'bg-gradient-to-r from-amber-600 to-orange-600 hover:from-amber-700 hover:to-orange-700 text-white'
                }
              `}
            >
              {isUrgent ? '⚡ Upgrade Now' : '✨ View Plans'}
            </button>

            <button
              onClick={() => router.push('/dashboard')}
              className={`
                px-5 py-2.5 rounded-xl font-semibold text-sm border-2 transition-all hover:scale-105 active:scale-95
                ${isUrgent
                  ? 'border-red-300 dark:border-red-700 text-red-700 dark:text-red-300 hover:bg-red-100/50 dark:hover:bg-red-950/50'
                  : 'border-amber-300 dark:border-amber-700 text-amber-700 dark:text-amber-300 hover:bg-amber-100/50 dark:hover:bg-amber-950/50'
                }
              `}
            >
              View Usage
            </button>
          </div>

          {/* Recommended Plan (for urgent cases) */}
          {isUrgent && currentPlan === 'free' && (
            <div className="mt-4 pt-4 border-t border-red-200/50 dark:border-red-800/50">
              <div className="flex items-center gap-2 text-sm">
                <TrendingUp className="w-4 h-4 text-red-600 dark:text-red-400 flex-shrink-0" />
                <span className="text-red-800 dark:text-red-200 font-medium">
                  Recommended: <strong>Basic Plan (₹149/mo)</strong> • 80 scans/month
                </span>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
