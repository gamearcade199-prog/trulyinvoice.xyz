import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import './globals.css'
import { ThemeProvider } from '@/components/ThemeProvider'
import GoogleAnalytics from '@/components/GoogleAnalytics'
import { TrackingWrapper } from '@/components/TrackingWrapper'
import seoConfig from '@/config/seo.config'
import { advancedSEOSchemas } from '@/config/seo.advanced'
import { Analytics } from '@vercel/analytics/react'
import { SpeedInsights } from '@vercel/speed-insights/next'
import { FAQSchema, SoftwareAppSchema, OrganizationSchema, LocalBusinessSchema } from '@/components/SeoSchemaMarkup'
import { Toaster } from 'react-hot-toast'

const inter = Inter({ 
  subsets: ['latin'],
  display: 'swap',
  preload: true,
})

// Comprehensive SEO Metadata for Invoice to Excel Converter
export const metadata: Metadata = {
  metadataBase: new URL('https://trulyinvoice.com'),
  
  // Basic metadata - Multi-Export Invoice Converter
  title: {
    default: 'TrulyInvoice - Convert Invoice to Excel, Tally, QuickBooks, Zoho Books | AI-Powered Converter',
    template: '%s | TrulyInvoice - Multi-Export Invoice Converter',
  },
  description: 'AI-powered invoice converter with high accuracy. Export to Excel, CSV, Tally ERP 9, QuickBooks India, Zoho Books. GST compliant, instant processing. Free plan available.',
  keywords: [
    'convert invoice to excel', 'invoice to excel converter', 'AI invoice extraction', 'pdf to excel converter', 'GST invoice to excel', 'indian invoice processing',
    'export invoice to tally', 'tally invoice import', 'quickbooks india integration', 'zoho books csv export', 'bulk csv export', 'accounting software export',
    'invoice to tally converter', 'quickbooks invoice import', 'zoho books integration', 'csv invoice export', 'erp invoice import'
  ],
  
  // Author and publisher
  authors: [{ name: 'TrulyInvoice Team' }],
  creator: 'TrulyInvoice',
  publisher: 'TrulyInvoice',
  
  // Application name
  applicationName: 'TrulyInvoice',
  
  // Canonical URL
  alternates: {
    canonical: 'https://trulyinvoice.com',
  },
  
  // Referrer policy
  referrer: 'origin-when-cross-origin',
  
  // Robots
  robots: {
    index: true,
    follow: true,
    googleBot: {
      index: true,
      follow: true,
      'max-video-preview': -1,
      'max-image-preview': 'large',
      'max-snippet': -1,
    },
  },
  
  // Open Graph (for Facebook, LinkedIn) - Multi-Export focus
  openGraph: {
    type: 'website',
    locale: 'en_IN',
    url: 'https://trulyinvoice.com',
    siteName: 'TrulyInvoice',
    title: 'Convert Invoice to Excel, Tally, QuickBooks, Zoho Books | AI-Powered Converter',
    description: 'Transform any invoice into Excel, Tally, QuickBooks, or Zoho Books with high accuracy. GST compliant, automatic processing. Free plan available.',
    images: [
      {
        url: '/og-image-india.jpg',
        width: 1200,
        height: 630,
        alt: 'TrulyInvoice - Convert Invoice to Excel, Tally, QuickBooks, Zoho Books',
      },
      {
        url: '/og-image-square.jpg',
        width: 1200,
        height: 1200,
        alt: 'TrulyInvoice Logo - Multi-Export Invoice Converter',
      },
    ],
  },
  
  // Twitter Card
  twitter: {
    card: 'summary_large_image',
    title: 'Convert Invoice to Excel, Tally, QuickBooks, Zoho | TrulyInvoice',
    description: 'AI-powered invoice converter with high accuracy. Export to Excel, Tally, QuickBooks, Zoho Books. GST compliant, instant processing.',
    creator: '@TrulyInvoice',
    images: ['/twitter-image.jpg'],
  },
  
  // Verification tags (replace with actual codes after Search Console setup)
  verification: {
    google: 'google-site-verification-code-here',
    yandex: 'yandex-verification-code-here',
  },
  
  // Icons and manifest
  icons: {
    icon: [
      { url: '/favicon-16x16.png', sizes: '16x16', type: 'image/png' },
      { url: '/favicon-32x32.png', sizes: '32x32', type: 'image/png' },
      { url: '/favicon-96x96.png', sizes: '96x96', type: 'image/png' },
    ],
    apple: [
      { url: '/apple-touch-icon.png', sizes: '180x180', type: 'image/png' },
    ],
    other: [
      {
        rel: 'mask-icon',
        url: '/safari-pinned-tab.svg',
        color: '#3b82f6',
      },
    ],
  },
  
  // Manifest
  manifest: '/site.webmanifest',
  
  // Category
  category: 'Business Software',
  
  // Other metadata
  other: {
    'msapplication-TileColor': '#3b82f6',
    'mobile-web-app-capable': 'yes',
    'apple-mobile-web-app-capable': 'yes',
    'apple-mobile-web-app-status-bar-style': 'default',
    'apple-mobile-web-app-title': 'TrulyInvoice',
    'format-detection': 'telephone=no',
    'theme-color': '#3b82f6',
  },
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  // JSON-LD Structured Data - Using Enhanced LocalBusiness Schema
  const organizationSchema = advancedSEOSchemas.enhancedLocalBusiness

  const breadcrumbSchema = {
    '@context': 'https://schema.org',
    '@type': 'BreadcrumbList',
    itemListElement: [
      {
        '@type': 'ListItem',
        position: 1,
        name: 'Home',
  item: 'https://trulyinvoice.com',
      },
      {
        '@type': 'ListItem',
        position: 2,
        name: 'Features',
  item: 'https://trulyinvoice.com/features',
      },
      {
        '@type': 'ListItem',
        position: 3,
        name: 'Pricing',
  item: 'https://trulyinvoice.com/pricing',
      },
    ],
  }

  return (
    <html lang="en-IN" suppressHydrationWarning>
      <head>
        {/* Google Analytics - Load in head for proper tracking */}
        <GoogleAnalytics />
        
        {/* Preconnect to important third-party origins */}
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin="anonymous" />
        <link rel="dns-prefetch" href="https://www.google-analytics.com" />
        
        {/* JSON-LD Structured Data */}
        <script
          type="application/ld+json"
          dangerouslySetInnerHTML={{ __html: JSON.stringify(organizationSchema) }}
        />
        <script
          type="application/ld+json"
          dangerouslySetInnerHTML={{ __html: JSON.stringify(breadcrumbSchema) }}
        />
        
        {/* Advanced SEO Schemas for Rich Snippets */}
        <script
          type="application/ld+json"
          dangerouslySetInnerHTML={{ __html: JSON.stringify(advancedSEOSchemas.aggregateRating) }}
        />
        <script
          type="application/ld+json"
          dangerouslySetInnerHTML={{ __html: JSON.stringify(advancedSEOSchemas.reviews) }}
        />
        
        {/* FAQ Schema removed from global layout - only loaded on /faq page */}
        <SoftwareAppSchema />
        <OrganizationSchema />
        
        {/* Alternate languages */}
  <link rel="alternate" hrefLang="en-IN" href="https://trulyinvoice.com" />
  <link rel="alternate" hrefLang="hi-IN" href="https://trulyinvoice.com/hi" />
        <link rel="alternate" hrefLang="x-default" href="https://trulyinvoice.in" />
        
        {/* Microsoft Clarity Analytics (optional) */}
        {/* <script type="text/javascript" dangerouslySetInnerHTML={{ __html: `
          (function(c,l,a,r,i,t,y){
            c[a]=c[a]||function(){(c[a].q=c[a].q||[]).push(arguments)};
            t=l.createElement(r);t.async=1;t.src="https://www.clarity.ms/tag/"+i;
            y=l.getElementsByTagName(r)[0];y.parentNode.insertBefore(t,y);
          })(window, document, "clarity", "script", "YOUR_CLARITY_ID");
        `}} /> */}
      </head>
      <body className={inter.className}>
        <TrackingWrapper />
        <ThemeProvider>
          {children}
        </ThemeProvider>
        <Toaster
          position="top-right"
          toastOptions={{
            duration: 4000,
            style: {
              background: '#fff',
              color: '#1f2937',
              border: '1px solid #e5e7eb',
            },
            success: {
              iconTheme: {
                primary: '#10b981',
                secondary: '#fff',
              },
            },
            error: {
              iconTheme: {
                primary: '#ef4444',
                secondary: '#fff',
              },
            },
          }}
        />
        <Analytics />
        <SpeedInsights />
      </body>
    </html>
  )
}
