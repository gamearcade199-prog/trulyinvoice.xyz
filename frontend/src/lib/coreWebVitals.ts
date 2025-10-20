'use client'

import { useEffect } from 'react'

// Core Web Vitals tracking and optimization
export function useCoreWebVitals() {
  useEffect(() => {
    // Only run on client side
    if (typeof window === 'undefined') return

    // Track Largest Contentful Paint (LCP)
    const trackLCP = () => {
      try {
        if ('PerformanceObserver' in window) {
          const observer = new PerformanceObserver((list) => {
            const entries = list.getEntries()
            const lastEntry = entries[entries.length - 1]

            // Send LCP data to analytics
            if (window.gtag) {
              window.gtag('event', 'web_vitals', {
                event_category: 'Web Vitals',
                event_label: 'LCP',
                value: Math.round(lastEntry.startTime),
                custom_parameters: {
                  metric_value: Math.round(lastEntry.startTime),
                  metric_rating: getRating(lastEntry.startTime, 'LCP'),
                },
              })
            }
          })
          observer.observe({ entryTypes: ['largest-contentful-paint'] })
        }
      } catch (error) {
        console.warn('LCP tracking failed:', error)
      }
    }

    // Track First Input Delay (FID)
    const trackFID = () => {
      try {
        if ('PerformanceObserver' in window) {
          const observer = new PerformanceObserver((list) => {
            const entries = list.getEntries()
            entries.forEach((entry: any) => {
              if (window.gtag) {
                window.gtag('event', 'web_vitals', {
                  event_category: 'Web Vitals',
                  event_label: 'FID',
                  value: Math.round(entry.processingStart - entry.startTime),
                  custom_parameters: {
                    metric_value: Math.round(entry.processingStart - entry.startTime),
                    metric_rating: getRating(entry.processingStart - entry.startTime, 'FID'),
                  },
                })
              }
            })
          })
          observer.observe({ entryTypes: ['first-input'] })
        }
      } catch (error) {
        console.warn('FID tracking failed:', error)
      }
    }

    // Track Cumulative Layout Shift (CLS)
    const trackCLS = () => {
      try {
        let clsValue = 0
        if ('PerformanceObserver' in window) {
          const observer = new PerformanceObserver((list) => {
            const entries = list.getEntries()
            entries.forEach((entry: any) => {
              if (!entry.hadRecentInput) {
                clsValue += entry.value
              }
            })
          })
          observer.observe({ entryTypes: ['layout-shift'] })

          // Report CLS on page unload
          window.addEventListener('beforeunload', () => {
            if (window.gtag && clsValue > 0) {
              window.gtag('event', 'web_vitals', {
                event_category: 'Web Vitals',
                event_label: 'CLS',
                value: Math.round(clsValue * 1000),
                custom_parameters: {
                  metric_value: clsValue,
                  metric_rating: getRating(clsValue, 'CLS'),
                },
              })
            }
          })
        }
      } catch (error) {
        console.warn('CLS tracking failed:', error)
      }
    }

    // Track First Contentful Paint (FCP)
    const trackFCP = () => {
      try {
        if ('PerformanceObserver' in window) {
          const observer = new PerformanceObserver((list) => {
            const entries = list.getEntries()
            const lastEntry = entries[entries.length - 1]

            if (window.gtag) {
              window.gtag('event', 'web_vitals', {
                event_category: 'Web Vitals',
                event_label: 'FCP',
                value: Math.round(lastEntry.startTime),
                custom_parameters: {
                  metric_value: Math.round(lastEntry.startTime),
                  metric_rating: getRating(lastEntry.startTime, 'FCP'),
                },
              })
            }
          })
          observer.observe({ entryTypes: ['paint'] })
        }
      } catch (error) {
        console.warn('FCP tracking failed:', error)
      }
    }

    // Track Time to First Byte (TTFB)
    const trackTTFB = () => {
      try {
        if ('PerformanceObserver' in window) {
          const observer = new PerformanceObserver((list) => {
            const entries = list.getEntries()
            entries.forEach((entry: any) => {
              const ttfb = entry.responseStart - entry.requestStart

              if (window.gtag) {
                window.gtag('event', 'web_vitals', {
                  event_category: 'Web Vitals',
                  event_label: 'TTFB',
                  value: Math.round(ttfb),
                  custom_parameters: {
                    metric_value: Math.round(ttfb),
                    metric_rating: getRating(ttfb, 'TTFB'),
                  },
                })
              }
            })
          })
          observer.observe({ entryTypes: ['navigation'] })
        }
      } catch (error) {
        console.warn('TTFB tracking failed:', error)
      }
    }

    // Initialize all tracking
    trackLCP()
    trackFID()
    trackCLS()
    trackFCP()
    trackTTFB()

  }, [])
}

// Helper function to determine performance rating
function getRating(value: number, metric: string): 'good' | 'needs-improvement' | 'poor' {
  switch (metric) {
    case 'LCP':
      return value <= 2500 ? 'good' : value <= 4000 ? 'needs-improvement' : 'poor'
    case 'FID':
      return value <= 100 ? 'good' : value <= 300 ? 'needs-improvement' : 'poor'
    case 'CLS':
      return value <= 0.1 ? 'good' : value <= 0.25 ? 'needs-improvement' : 'poor'
    case 'FCP':
      return value <= 1800 ? 'good' : value <= 3000 ? 'needs-improvement' : 'poor'
    case 'TTFB':
      return value <= 800 ? 'good' : value <= 1800 ? 'needs-improvement' : 'poor'
    default:
      return 'needs-improvement'
  }
}

// Performance optimization utilities
export const performanceUtils = {
  // Lazy load images
  lazyLoadImage: (img: HTMLImageElement) => {
    const imageObserver = new IntersectionObserver((entries, observer) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          const lazyImage = entry.target as HTMLImageElement
          lazyImage.src = lazyImage.dataset.src || ''
          lazyImage.classList.remove('lazy')
          observer.unobserve(lazyImage)
        }
      })
    })
    imageObserver.observe(img)
  },

  // Preload critical resources
  preloadResource: (href: string, as: string, type?: string) => {
    const link = document.createElement('link')
    link.rel = 'preload'
    link.as = as
    link.href = href
    if (type) link.type = type
    document.head.appendChild(link)
  },

  // Defer non-critical JavaScript
  deferScript: (src: string, callback?: () => void) => {
    const script = document.createElement('script')
    script.src = src
    script.defer = true
    if (callback) {
      script.onload = callback
    }
    document.head.appendChild(script)
  },

  // Optimize font loading
  optimizeFonts: () => {
    // Add font-display: swap to existing font links
    const fontLinks = document.querySelectorAll('link[rel="stylesheet"][href*="font"]')
    fontLinks.forEach(link => {
      const href = link.getAttribute('href')
      if (href && !href.includes('display=swap')) {
        link.setAttribute('href', href + (href.includes('?') ? '&' : '?') + 'display=swap')
      }
    })
  },
}

export default useCoreWebVitals