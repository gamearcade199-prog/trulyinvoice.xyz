'use client'

import { useEffect, Suspense } from 'react'
import { usePathname, useSearchParams } from 'next/navigation'
import { trackingConfig } from '@/lib/analytics'

declare global {
  interface Window {
    gtag: (...args: any[]) => void
    dataLayer: any[]
  }
}

// Inner component that uses useSearchParams
function GoogleAnalyticsInner() {
  const pathname = usePathname()
  const searchParams = useSearchParams()

  useEffect(() => {
    if (!trackingConfig.googleAnalyticsId || trackingConfig.googleAnalyticsId === 'G-XXXXXXXXXX') {
      return
    }

    const url = pathname + (searchParams?.toString() ? `?${searchParams.toString()}` : '')

    // Track page view
    if (window.gtag) {
      window.gtag('config', trackingConfig.googleAnalyticsId, {
        page_path: url,
        page_title: document.title,
      })
    }
  }, [pathname, searchParams])

  return null
}

// Main component wrapped in Suspense
export default function GoogleAnalytics() {
  // Don't render anything if GA ID is not configured
  if (!trackingConfig.googleAnalyticsId || trackingConfig.googleAnalyticsId === 'G-XXXXXXXXXX') {
    return null
  }

  return (
    <>
      {/* Google Analytics Script */}
      <script
        async
        src={`https://www.googletagmanager.com/gtag/js?id=${trackingConfig.googleAnalyticsId}`}
      />
      <script
        dangerouslySetInnerHTML={{
          __html: `
            window.dataLayer = window.dataLayer || [];
            function gtag(){dataLayer.push(arguments);}
            gtag('js', new Date());
            gtag('config', '${trackingConfig.googleAnalyticsId}', {
              page_path: window.location.pathname,
              send_page_view: true,
              anonymize_ip: true,
              cookie_flags: 'SameSite=None;Secure',
            });
          `,
        }}
      />
      
      {/* Wrap the tracking component in Suspense */}
      <Suspense fallback={null}>
        <GoogleAnalyticsInner />
      </Suspense>
    </>
  )
}

// Export tracking functions for use in components
export function trackEvent(eventName: string, eventParams?: Record<string, any>) {
  if (typeof window !== 'undefined' && window.gtag) {
    window.gtag('event', eventName, eventParams)
  }
}

export function trackPageView(url: string) {
  if (typeof window !== 'undefined' && window.gtag && trackingConfig.googleAnalyticsId) {
    window.gtag('config', trackingConfig.googleAnalyticsId, {
      page_path: url,
    })
  }
}

export function setUserProperties(properties: Record<string, any>) {
  if (typeof window !== 'undefined' && window.gtag) {
    window.gtag('set', 'user_properties', properties)
  }
}
