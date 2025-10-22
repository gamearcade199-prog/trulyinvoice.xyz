/**
 * Session Timeout Warning Component
 * Displays when user has less than 5 minutes remaining in their session
 * Shows countdown timer and allows extending session or logging out
 */

'use client'

import React, { useState, useEffect } from 'react'
import { AlertTriangle, LogOut, RotateCcw } from 'lucide-react'
import {
  isSessionAboutToTimeout,
  getSessionTimeRemaining,
  resetActivityTimer,
  stopSessionMonitoring,
} from '@/lib/supabase'
import { useRouter } from 'next/navigation'

export function SessionTimeoutWarning() {
  const [showWarning, setShowWarning] = useState(false)
  const [timeRemaining, setTimeRemaining] = useState(0)
  const router = useRouter()

  useEffect(() => {
    // Check session status every 10 seconds
    const checkInterval = setInterval(() => {
      const remaining = getSessionTimeRemaining()
      setTimeRemaining(remaining)

      if (isSessionAboutToTimeout()) {
        setShowWarning(true)
      } else if (remaining <= 0) {
        // Session expired
        setShowWarning(false)
        handleLogout()
      } else {
        setShowWarning(false)
      }
    }, 10000)

    return () => clearInterval(checkInterval)
  }, [])

  const handleExtendSession = () => {
    resetActivityTimer()
    setShowWarning(false)
    console.log('✅ Session extended')
  }

  const handleLogout = async () => {
    stopSessionMonitoring()
    router.push('/login')
  }

  if (!showWarning) return null

  const minutes = Math.floor(timeRemaining / 60)
  const seconds = timeRemaining % 60

  return (
    <div className="fixed bottom-4 right-4 z-50 max-w-sm animate-in fade-in slide-in-from-bottom-4">
      <div className="bg-red-50 border-2 border-red-400 rounded-lg shadow-lg p-4">
        {/* Header */}
        <div className="flex items-center gap-2 mb-3">
          <AlertTriangle className="w-5 h-5 text-red-600" />
          <h3 className="font-semibold text-red-900">Session Expiring Soon</h3>
        </div>

        {/* Message */}
        <p className="text-sm text-red-800 mb-3">
          Your session will expire in{' '}
          <span className="font-bold">
            {minutes}:{seconds.toString().padStart(2, '0')}
          </span>
        </p>

        {/* Timer Progress Bar */}
        <div className="w-full bg-red-200 rounded-full h-2 mb-4 overflow-hidden">
          <div
            className="bg-red-600 h-full transition-all duration-1000"
            style={{
              width: `${(timeRemaining / (5 * 60)) * 100}%`,
              minWidth: timeRemaining > 0 ? '4px' : '0',
            }}
          />
        </div>

        {/* Actions */}
        <div className="flex gap-2">
          <button
            onClick={handleExtendSession}
            className="flex-1 flex items-center justify-center gap-2 bg-green-600 hover:bg-green-700 text-white px-3 py-2 rounded-md font-medium transition-colors"
          >
            <RotateCcw className="w-4 h-4" />
            Continue Working
          </button>
          <button
            onClick={handleLogout}
            className="flex-1 flex items-center justify-center gap-2 bg-red-600 hover:bg-red-700 text-white px-3 py-2 rounded-md font-medium transition-colors"
          >
            <LogOut className="w-4 h-4" />
            Log Out
          </button>
        </div>

        {/* Footer Message */}
        <p className="text-xs text-red-700 mt-3 text-center">
          Your account will be automatically logged out for security
        </p>
      </div>
    </div>
  )
}
