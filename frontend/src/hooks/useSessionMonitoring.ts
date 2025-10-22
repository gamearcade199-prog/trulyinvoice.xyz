/**
 * Session Monitor Hook
 * Automatically manages session timeout monitoring across the app
 * Use this in your root layout or protected app wrapper
 */

'use client'

import { useEffect } from 'react'
import { useRouter } from 'next/navigation'
import { startSessionMonitoring, stopSessionMonitoring, onSessionTimeout } from '@/lib/supabase'

export function useSessionMonitoring() {
  const router = useRouter()

  useEffect(() => {
    // Start monitoring when component mounts
    console.log('🔒 Starting session monitoring')
    startSessionMonitoring()

    // Set callback for when session times out
    onSessionTimeout(() => {
      console.warn('⏱️ Session timeout - redirecting to login')
      router.push('/login')
    })

    // Cleanup on component unmount
    return () => {
      console.log('🔒 Stopping session monitoring')
      stopSessionMonitoring()
    }
  }, [router])
}
