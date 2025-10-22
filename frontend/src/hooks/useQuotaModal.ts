'use client'

import { useState, useCallback } from 'react'
import { useRouter } from 'next/navigation'

interface QuotaState {
  scansUsed: number
  scansLimit: number
  currentPlan: string
  scansRemaining: number
  usagePercentage: number
}

interface UseQuotaModalReturn {
  isModalOpen: boolean
  showUpgradeModal: (reason?: 'quota_exceeded' | 'feature_locked' | 'proactive_warning') => void
  hideUpgradeModal: () => void
  handleQuotaError: (error: any) => boolean
  quotaState: QuotaState | null
  modalReason: 'quota_exceeded' | 'feature_locked' | 'proactive_warning'
}

export function useQuotaModal(initialQuotaState?: QuotaState): UseQuotaModalReturn {
  const [isModalOpen, setIsModalOpen] = useState(false)
  const [modalReason, setModalReason] = useState<'quota_exceeded' | 'feature_locked' | 'proactive_warning'>('quota_exceeded')
  const [quotaState, setQuotaState] = useState<QuotaState | null>(initialQuotaState || null)
  const router = useRouter()

  const showUpgradeModal = useCallback((reason: 'quota_exceeded' | 'feature_locked' | 'proactive_warning' = 'quota_exceeded') => {
    setModalReason(reason)
    setIsModalOpen(true)
  }, [])

  const hideUpgradeModal = useCallback(() => {
    setIsModalOpen(false)
  }, [])

  const handleQuotaError = useCallback((error: any) => {
    // Check if error is a quota exceeded error (HTTP 429)
    if (error?.status === 429 || error?.response?.status === 429) {
      // Try to extract quota information from error
      const errorDetail = error?.detail || error?.response?.data?.detail || ''
      const match = errorDetail.match(/Used: (\d+)\/(\d+)/)
      
      if (match) {
        const scansUsed = parseInt(match[1], 10)
        const scansLimit = parseInt(match[2], 10)
        
        setQuotaState({
          scansUsed,
          scansLimit,
          currentPlan: 'free', // Default, should be fetched from user data
          scansRemaining: scansLimit - scansUsed,
          usagePercentage: (scansUsed / scansLimit) * 100
        })
      }
      
      showUpgradeModal('quota_exceeded')
      return true
    }
    
    return false
  }, [showUpgradeModal])

  return {
    isModalOpen,
    showUpgradeModal,
    hideUpgradeModal,
    handleQuotaError,
    quotaState,
    modalReason
  }
}

// Custom error class for quota exceeded errors
export class QuotaExceededError extends Error {
  status: number
  scansUsed: number
  scansLimit: number

  constructor(message: string, scansUsed?: number, scansLimit?: number) {
    super(message)
    this.name = 'QuotaExceededError'
    this.status = 429
    this.scansUsed = scansUsed || 0
    this.scansLimit = scansLimit || 0
  }
}

// Helper function to check if error is quota related
export function isQuotaError(error: any): boolean {
  return (
    error instanceof QuotaExceededError ||
    error?.status === 429 ||
    error?.response?.status === 429 ||
    (error?.message && error.message.includes('scan limit exceeded'))
  )
}

// Helper function to parse quota info from error
export function parseQuotaError(error: any): { scansUsed: number; scansLimit: number } | null {
  const errorDetail = error?.detail || error?.response?.data?.detail || error?.message || ''
  const match = errorDetail.match(/Used: (\d+)\/(\d+)/)
  
  if (match) {
    return {
      scansUsed: parseInt(match[1], 10),
      scansLimit: parseInt(match[2], 10)
    }
  }
  
  return null
}
