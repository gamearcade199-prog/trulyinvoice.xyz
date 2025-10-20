import { Metadata } from 'next'
import PricingPage from '@/components/PricingPage'

export const metadata: Metadata = {
  title: 'Pricing Plans - Invoice to Excel Converter | TrulyInvoice',
  description: 'Choose the perfect pricing plan for your invoice processing needs. From free tier to enterprise solutions, get accurate invoice data extraction with 95-99.5% AI accuracy. Start converting invoices to Excel today.',
  keywords: [
    'invoice to excel pricing',
    'invoice processing plans',
    'invoice converter pricing',
    'invoice extraction pricing',
    'GST invoice pricing',
    'bulk invoice processing pricing',
    'invoice OCR pricing',
    'invoice automation pricing',
    'invoice digitization pricing',
    'invoice data extraction pricing',
    'Indian invoice processing pricing',
    'invoice software pricing India',
    'invoice to spreadsheet pricing',
    'invoice conversion pricing',
    'invoice parsing pricing'
  ],
  openGraph: {
    title: 'Pricing Plans - Invoice to Excel Converter | TrulyInvoice',
    description: 'Choose the perfect pricing plan for your invoice processing needs. From free tier to enterprise solutions, get accurate invoice data extraction with 95-99.5% AI accuracy.',
    url: 'https://trulyinvoice.xyz/pricing',
    siteName: 'TrulyInvoice',
    images: [
      {
        url: 'https://trulyinvoice.xyz/og-image-pricing.jpg',
        width: 1200,
        height: 630,
        alt: 'TrulyInvoice Pricing Plans - Invoice to Excel Converter',
      },
    ],
    locale: 'en_US',
    type: 'website',
  },
  twitter: {
    card: 'summary_large_image',
    title: 'Pricing Plans - Invoice to Excel Converter | TrulyInvoice',
    description: 'Choose the perfect pricing plan for your invoice processing needs. From free tier to enterprise solutions, get accurate invoice data extraction with 95-99.5% AI accuracy.',
    images: ['https://trulyinvoice.xyz/twitter-image-pricing.jpg'],
  },
  alternates: {
    canonical: 'https://trulyinvoice.xyz/pricing',
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
  return <PricingPage />
}
