import { Metadata } from 'next'

export const metadata: Metadata = {
  title: 'About TrulyInvoice - AI Invoice to Excel Conversion Platform',
  description: 'Learn about TrulyInvoice, the AI-powered invoice to Excel converter for Indian businesses. Mission, values, and story behind the platform.',
  keywords: [
    'about TrulyInvoice',
    'invoice to excel platform',
    'AI invoice processing company',
    'GST invoice software',
    'invoice automation India',
    'about invoice converter',
    'TrulyInvoice mission',
    'TrulyInvoice values',
    'invoice processing AI',
  ],
  openGraph: {
    title: 'About TrulyInvoice - AI Invoice to Excel Conversion Platform',
    description: 'Learn about TrulyInvoice, the AI-powered invoice to Excel converter. Mission, values, and technology behind the platform.',
    url: 'https://trulyinvoice.xyz/about',
    siteName: 'TrulyInvoice',
    images: [
      {
        url: 'https://trulyinvoice.xyz/og-image-square.jpg',
        width: 1200,
        height: 630,
        alt: 'About TrulyInvoice - AI Invoice Conversion Platform',
      },
    ],
    locale: 'en_IN',
    type: 'website',
  },
  twitter: {
    card: 'summary_large_image',
    title: 'About TrulyInvoice - AI Invoice to Excel Conversion Platform',
    description: 'Learn about TrulyInvoice, the AI-powered invoice to Excel converter. Mission, values, and technology.',
    images: ['https://trulyinvoice.xyz/twitter-image.jpg'],
  },
  alternates: {
    canonical: 'https://trulyinvoice.xyz/about',
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

export default function AboutLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return children
}
