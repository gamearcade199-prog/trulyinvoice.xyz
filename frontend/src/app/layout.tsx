import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import './globals.css'
import { ThemeProvider } from '@/components/ThemeProvider'
import GoogleAnalytics from '@/components/GoogleAnalytics'
import seoConfig from '@/config/seo.config'
import { Analytics } from '@vercel/analytics/react'
import { SpeedInsights } from '@vercel/speed-insights/next'

const inter = Inter({ 
  subsets: ['latin'],
  display: 'swap',
  preload: true,
})

// Comprehensive SEO Metadata for Indian Market
export const metadata: Metadata = {
  metadataBase: new URL('https://trulyinvoice.xyz'),
  
  // Basic metadata
  title: {
    default: 'Invoice Management Software India | AI-Powered GST Invoicing',
    template: '%s | TrulyInvoice - GST Invoice Management India',
  },
  description: 'AI-powered invoice management for Indian businesses. 99% accuracy, GST compliant, automatic data extraction. Process 1000+ invoices/month. Free plan available.',
  keywords: ['invoice management software india', 'gst invoice software', 'ai invoice extraction', 'invoice ocr india', 'gst compliant invoice software'],
  
  // Author and publisher
  authors: [{ name: 'TrulyInvoice Team' }],
  creator: 'TrulyInvoice',
  publisher: 'TrulyInvoice',
  
  // Application name
  applicationName: 'TrulyInvoice',
  
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
  
  // Open Graph (for Facebook, LinkedIn)
  openGraph: {
    type: 'website',
    locale: 'en_IN',
    url: 'https://trulyinvoice.xyz',
    siteName: 'TrulyInvoice',
    title: 'Best Invoice Management Software for Indian Businesses',
    description: 'AI-powered invoice management. 99% accuracy, GST compliant, Excel export in 1 click.',
    images: [
      {
        url: '/og-image-india.jpg',
        width: 1200,
        height: 630,
        alt: 'TrulyInvoice - AI Invoice Management India',
      },
      {
        url: '/og-image-square.jpg',
        width: 1200,
        height: 1200,
        alt: 'TrulyInvoice Logo',
      },
    ],
  },
  
  // Twitter Card
  twitter: {
    card: 'summary_large_image',
    title: 'AI Invoice Management for India | TrulyInvoice',
    description: 'Process 1000+ invoices/month with 99% accuracy. GST compliant, automatic extraction.',
    creator: '@TrulyInvoice',
    images: ['/twitter-image.jpg'],
  },
  
  // Verification tags (replace with actual codes after Search Console setup)
  verification: {
    google: 'your-google-verification-code',
    yandex: 'your-yandex-verification-code',
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
  },
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  // JSON-LD Structured Data for rich snippets
  const organizationSchema = {
    '@context': 'https://schema.org',
    '@type': 'SoftwareApplication',
    name: 'TrulyInvoice',
    applicationCategory: 'BusinessApplication',
    operatingSystem: 'Web Browser, iOS, Android',
    offers: {
      '@type': 'AggregateOffer',
      priceCurrency: 'INR',
      lowPrice: '0',
      highPrice: '999',
      offerCount: '4',
    },
    aggregateRating: {
      '@type': 'AggregateRating',
      ratingValue: '4.8',
      ratingCount: '1247',
      bestRating: '5',
      worstRating: '1',
    },
    author: {
      '@type': 'Organization',
      name: 'TrulyInvoice',
  url: 'https://trulyinvoice.xyz',
    },
    publisher: {
      '@type': 'Organization',
      name: 'TrulyInvoice',
      logo: {
        '@type': 'ImageObject',
  url: 'https://trulyinvoice.xyz/logo.png',
      },
    },
    description: 'AI-powered invoice management software for Indian businesses with GST compliance',
    softwareVersion: '1.0',
  screenshot: 'https://trulyinvoice.xyz/screenshot.jpg',
  image: 'https://trulyinvoice.xyz/og-image-india.jpg',
  url: 'https://trulyinvoice.xyz',
    inLanguage: 'en-IN',
    areaServed: {
      '@type': 'Country',
      name: 'India',
    },
    audience: {
      '@type': 'BusinessAudience',
      audienceType: 'Small and Medium Businesses, Traders, Retailers, Manufacturers',
      geographicArea: {
        '@type': 'Country',
        name: 'India',
      },
    },
  }

  const breadcrumbSchema = {
    '@context': 'https://schema.org',
    '@type': 'BreadcrumbList',
    itemListElement: [
      {
        '@type': 'ListItem',
        position: 1,
        name: 'Home',
  item: 'https://trulyinvoice.xyz',
      },
      {
        '@type': 'ListItem',
        position: 2,
        name: 'Features',
  item: 'https://trulyinvoice.xyz/features',
      },
      {
        '@type': 'ListItem',
        position: 3,
        name: 'Pricing',
  item: 'https://trulyinvoice.xyz/pricing',
      },
    ],
  }

  return (
    <html lang="en-IN" suppressHydrationWarning>
      <head>
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
        <script
          type="application/ld+json"
          dangerouslySetInnerHTML={{ __html: JSON.stringify(seoConfig.faqSchema) }}
        />
        
        {/* Alternate languages */}
  <link rel="alternate" hrefLang="en-IN" href="https://trulyinvoice.xyz" />
  <link rel="alternate" hrefLang="hi-IN" href="https://trulyinvoice.xyz/hi" />
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
        <GoogleAnalytics />
        <ThemeProvider>
          {children}
        </ThemeProvider>
        <Analytics />
        <SpeedInsights />
      </body>
    </html>
  )
}
