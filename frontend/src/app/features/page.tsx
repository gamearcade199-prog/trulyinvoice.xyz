import { Metadata } from 'next'
import FeaturesPage from '@/components/FeaturesPage'

export const metadata: Metadata = {
  title: 'Features - Invoice to Excel Converter | AI-Powered OCR & GST Compliance',
  description: 'AI invoice extraction with 99% accuracy. GST compliant, bulk processing, multi-currency support. Auto-convert PDF/image invoices to Excel. Learn more!',
  keywords: [
    'invoice to excel features',
    'AI OCR invoice processing',
    'GST compliance software',
    'bulk invoice processing',
    'invoice automation features',
    'invoice digitization tools',
    'multi-currency invoice processing',
    'invoice analytics dashboard',
    'invoice extraction features',
    'invoice parsing capabilities',
    'Indian invoice processing features',
    'GST invoice automation',
    'invoice data extraction AI',
    'invoice to spreadsheet features',
    'automated invoice processing'
  ],
  openGraph: {
    title: 'Features - Invoice to Excel Converter | AI-Powered OCR & GST Compliance',
    description: 'AI invoice extraction with 99% accuracy. GST compliant, bulk processing, multi-currency support. Auto-convert PDF/image invoices to Excel. Learn more!',
    url: 'https://trulyinvoice.xyz/features',
    siteName: 'TrulyInvoice',
    images: [
      {
        url: 'https://trulyinvoice.xyz/og-image-square.jpg',
        width: 1200,
        height: 630,
        alt: 'TrulyInvoice Features - Invoice to Excel Converter',
      },
    ],
    locale: 'en_US',
    type: 'website',
  },
  twitter: {
    card: 'summary_large_image',
    title: 'Features - Invoice to Excel Converter | AI-Powered OCR & GST Compliance',
    description: 'AI invoice extraction with 99% accuracy. GST compliant, bulk processing, multi-currency support. Auto-convert PDF/image invoices to Excel. Learn more!',
    images: ['https://trulyinvoice.xyz/twitter-image.jpg'],
  },
  alternates: {
    canonical: 'https://trulyinvoice.xyz/features',
  },
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
  authors: [{ name: 'TrulyInvoice Team' }],
  creator: 'TrulyInvoice',
  publisher: 'TrulyInvoice',
  formatDetection: {
    email: false,
    address: false,
    telephone: false,
  },
}

export default function Page() {
  return <FeaturesPage />
}