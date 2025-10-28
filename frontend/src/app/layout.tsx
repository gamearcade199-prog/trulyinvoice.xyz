import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import './globals.css'
import { ThemeProvider } from '@/components/ThemeProvider'
import GoogleAnalytics from '@/components/GoogleAnalytics'
import { TrackingWrapper } from '@/components/TrackingWrapper'
import seoConfig from '@/config/seo.config'
import { Analytics } from '@vercel/analytics/react'
import { SpeedInsights } from '@vercel/speed-insights/next'
import { FAQSchema, SoftwareAppSchema, OrganizationSchema, LocalBusinessSchema } from '@/components/SeoSchemaMarkup'

const inter = Inter({ 
  subsets: ['latin'],
  display: 'swap',
  preload: true,
})

// Comprehensive SEO Metadata for Invoice to Excel Converter
export const metadata: Metadata = {
  metadataBase: new URL('https://trulyinvoice.xyz'),
  
  // Basic metadata - Multi-Export Invoice Converter
  title: {
    default: 'TrulyInvoice - Convert Invoice to Excel, Tally, QuickBooks, Zoho Books | AI-Powered Converter',
    template: '%s | TrulyInvoice - Multi-Export Invoice Converter',
  },
  description: 'AI-powered invoice converter with 99% accuracy. Export to Excel, CSV, Tally ERP 9, QuickBooks India, Zoho Books. GST compliant, instant processing. Free plan available.',
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
    canonical: 'https://trulyinvoice.xyz',
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
    url: 'https://trulyinvoice.xyz',
    siteName: 'TrulyInvoice',
    title: 'Convert Invoice to Excel, Tally, QuickBooks, Zoho Books | AI-Powered Converter',
    description: 'Transform any invoice into Excel, Tally, QuickBooks, or Zoho Books with 99% accuracy. GST compliant, automatic processing. Free plan available.',
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
    description: 'AI-powered invoice converter with 99% accuracy. Export to Excel, Tally, QuickBooks, Zoho Books. GST compliant, instant processing.',
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
  // JSON-LD Structured Data for Invoice to Excel Converter
  const organizationSchema = {
    '@context': 'https://schema.org',
    '@type': 'SoftwareApplication',
    '@id': 'https://trulyinvoice.xyz',
    name: 'TrulyInvoice',
    alternateName: 'Multi-Export Invoice Converter',
    description: 'AI-powered invoice converter with 99% accuracy. Export to Excel, CSV, Tally ERP 9, QuickBooks India, Zoho Books. GST compliant, perfect for Indian businesses.',
    applicationCategory: 'BusinessApplication',
    operatingSystem: 'Web Browser, iOS, Android',
    url: 'https://trulyinvoice.xyz',
    image: 'https://trulyinvoice.xyz/og-image-india.jpg',
    screenshot: 'https://trulyinvoice.xyz/og-image-india.jpg',
    offers: {
      '@type': 'AggregateOffer',
      priceCurrency: 'INR',
      lowPrice: '0',
      highPrice: '999',
      offerCount: '5',
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
        url: 'https://trulyinvoice.xyz/favicon-32x32.png',
      },
    },
    softwareVersion: '2.0',
    fileFormat: ['PDF', 'JPG', 'PNG'],
    applicationSubCategory: 'Data Extraction',
    featureList: [
      'AI-powered invoice scanning',
      '99% accurate data extraction',
      'Excel export functionality',
      'CSV export for bulk processing',
      'Tally ERP 9 integration',
      'QuickBooks India compatibility',
      'Zoho Books CSV export',
      'GST compliant processing',
      'Bulk invoice processing',
      'Indian invoice format support'
    ],
    inLanguage: 'en-IN',
    areaServed: {
      '@type': 'Country',
      name: 'India',
    },
    audience: {
      '@type': 'BusinessAudience',
      audienceType: 'Small and Medium Businesses, Traders, Retailers, Manufacturers, Accountants',
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
        <script
          type="application/ld+json"
          dangerouslySetInnerHTML={{ __html: JSON.stringify(seoConfig.faqSchema) }}
        />
        <FAQSchema />
        <SoftwareAppSchema />
        <OrganizationSchema />
        
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
        <TrackingWrapper />
        <ThemeProvider>
          {children}
        </ThemeProvider>
        <Analytics />
        <SpeedInsights />
      </body>
    </html>
  )
}
