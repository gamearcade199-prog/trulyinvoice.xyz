'use client'

import { useCoreWebVitals } from '@/lib/coreWebVitals'
import { useConversionTracking } from '@/lib/conversionTracking'

export function TrackingWrapper() {
  // Initialize Core Web Vitals tracking
  useCoreWebVitals()

  // Initialize conversion tracking
  useConversionTracking()

  return null
}