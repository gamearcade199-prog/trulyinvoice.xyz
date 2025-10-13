import { Metadata } from 'next'

export const metadata: Metadata = {
  title: 'Pricing Plans - Affordable GST Invoice Software',
  description: 'Simple, transparent pricing for Indian businesses. Start free with 10 invoices/month. Premium plans from ₹99/month. No hidden charges. 30-day money-back guarantee.',
  keywords: [
    'invoice software pricing India',
    'GST software pricing',
    'invoice management cost',
    'affordable invoice software',
    'invoice software plans India',
    'cheap invoice software',
    'invoice software subscription',
  ],
  alternates: {
  canonical: 'https://trulyinvoice.xyz/pricing',
  },
  openGraph: {
    title: 'Pricing Plans - Affordable GST Invoice Software | TrulyInvoice',
    description: 'Simple, transparent pricing for Indian businesses. Start free with 10 invoices/month. Premium plans from ₹99/month.',
  url: 'https://trulyinvoice.xyz/pricing',
    siteName: 'TrulyInvoice',
    images: [
      {
        url: '/og-image-pricing.jpg',
        width: 1200,
        height: 630,
        alt: 'TrulyInvoice Pricing Plans',
      },
    ],
    locale: 'en_IN',
    type: 'website',
  },
  twitter: {
    card: 'summary_large_image',
    title: 'Pricing Plans - Affordable GST Invoice Software | TrulyInvoice',
    description: 'Simple, transparent pricing for Indian businesses. Start free with 10 invoices/month. Premium plans from ₹99/month.',
    images: ['/twitter-image-pricing.jpg'],
  },
}

export default function PricingLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return children
}
