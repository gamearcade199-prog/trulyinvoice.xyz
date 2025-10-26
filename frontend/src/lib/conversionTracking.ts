'use client'

import { useEffect } from 'react'
import { trackEvent, setUserProperties } from '@/components/GoogleAnalytics'

// Conversion tracking for invoice-to-excel business goals
export const conversionTracking = {
  // Track when user starts the invoice upload process
  trackUploadStart: () => {
    trackEvent('begin_upload', {
      event_category: 'conversion',
      event_label: 'invoice_upload_start',
      value: 1,
    })
  },

  // Track successful invoice processing
  trackProcessingComplete: (invoiceCount: number, processingTime: number) => {
    trackEvent('invoice_processed', {
      event_category: 'conversion',
      event_label: 'processing_complete',
      value: invoiceCount,
      custom_parameters: {
        processing_time_seconds: processingTime,
        invoice_count: invoiceCount,
      },
    })
  },

  // Track Excel export completion
  trackExportComplete: (format: string, invoiceCount: number) => {
    trackEvent('export_complete', {
      event_category: 'conversion',
      event_label: 'excel_export',
      value: invoiceCount,
      custom_parameters: {
        export_format: format,
        invoice_count: invoiceCount,
      },
    })
  },

  // Track pricing page engagement
  trackPricingView: () => {
    trackEvent('view_pricing', {
      event_category: 'engagement',
      event_label: 'pricing_page_view',
    })
  },

  // Track plan selection
  trackPlanSelect: (planName: string, price: number) => {
    trackEvent('select_plan', {
      event_category: 'conversion',
      event_label: 'plan_selection',
      value: price,
      custom_parameters: {
        plan_name: planName,
        plan_price: price,
        currency: 'INR',
      },
    })
  },

  // Track payment initiation
  trackPaymentStart: (planName: string, price: number) => {
    trackEvent('begin_checkout', {
      event_category: 'conversion',
      event_label: 'payment_start',
      value: price,
      custom_parameters: {
        plan_name: planName,
        currency: 'INR',
      },
    })
  },

  // Track successful payment
  trackPaymentComplete: (planName: string, price: number, transactionId: string) => {
    trackEvent('purchase', {
      event_category: 'conversion',
      event_label: 'payment_complete',
      transaction_id: transactionId,
      value: price,
      currency: 'INR',
      items: [{
        item_id: planName.toLowerCase(),
        item_name: `${planName} Plan`,
        price: price,
        quantity: 1,
        item_category: 'subscription',
      }],
    })

    // Set user properties for segmentation
    setUserProperties({
      plan_tier: planName.toLowerCase(),
      subscription_status: 'active',
      first_purchase_date: new Date().toISOString(),
    })
  },

  // Track user registration
  trackRegistration: (method: string = 'email') => {
    trackEvent('sign_up', {
      event_category: 'conversion',
      event_label: 'user_registration',
      method: method,
    })
  },

  // Track feature usage
  trackFeatureUsage: (featureName: string) => {
    trackEvent('feature_used', {
      event_category: 'engagement',
      event_label: featureName,
      custom_parameters: {
        feature_name: featureName,
      },
    })
  },

  // Track demo requests
  trackDemoRequest: (source: string) => {
    trackEvent('demo_request', {
      event_category: 'conversion',
      event_label: 'demo_requested',
      custom_parameters: {
        request_source: source,
      },
    })
  },

  // Track contact form submissions
  trackContactSubmit: (inquiryType: string) => {
    trackEvent('contact_submit', {
      event_category: 'engagement',
      event_label: 'contact_form',
      custom_parameters: {
        inquiry_type: inquiryType,
      },
    })
  },

  // Track newsletter signups
  trackNewsletterSignup: (source: string) => {
    trackEvent('newsletter_signup', {
      event_category: 'engagement',
      event_label: 'newsletter',
      custom_parameters: {
        signup_source: source,
      },
    })
  },

  // Track time spent on page
  trackTimeOnPage: (pageName: string, timeSpent: number) => {
    trackEvent('time_on_page', {
      event_category: 'engagement',
      event_label: pageName,
      value: timeSpent,
      custom_parameters: {
        time_spent_seconds: timeSpent,
        page_name: pageName,
      },
    })
  },

  // Track scroll depth
  trackScrollDepth: (depth: number, pageName: string) => {
    trackEvent('scroll_depth', {
      event_category: 'engagement',
      event_label: pageName,
      value: depth,
      custom_parameters: {
        scroll_percentage: depth,
        page_name: pageName,
      },
    })
  },
}

// Hook for automatic conversion tracking
export function useConversionTracking() {
  useEffect(() => {
    // Track time spent on page
    let startTime = Date.now()
    let scrollDepth = 0

    const trackTimeSpent = () => {
      const timeSpent = Math.floor((Date.now() - startTime) / 1000)
      if (timeSpent > 10) { // Only track if spent more than 10 seconds
        conversionTracking.trackTimeOnPage(window.location.pathname, timeSpent)
      }
    }

    const trackScroll = () => {
      const scrolled = Math.round(
        (window.scrollY / (document.documentElement.scrollHeight - window.innerHeight)) * 100
      )
      if (scrolled > scrollDepth) {
        scrollDepth = scrolled
        if (scrollDepth >= 25 && scrollDepth % 25 === 0) {
          conversionTracking.trackScrollDepth(scrollDepth, window.location.pathname)
        }
      }
    }

    // Add event listeners
    window.addEventListener('beforeunload', trackTimeSpent)
    window.addEventListener('scroll', trackScroll)

    return () => {
      window.removeEventListener('beforeunload', trackTimeSpent)
      window.removeEventListener('scroll', trackScroll)
      trackTimeSpent()
    }
  }, [])
}

export default conversionTracking