import { Metadata } from 'next'
import HomePageComponent from '@/components/HomePage'

export const metadata: Metadata = {
  title: 'Convert Invoice to Excel Instantly with AI | TrulyInvoice - GST Compliant',
  description: 'Convert PDF & image invoices to Excel in 5 seconds. AI-powered invoice extraction for Indian businesses. 99% accuracy, GST/GSTIN compliant. Free trial - no signup required.',
  keywords: ['invoice to excel converter India', 'GST invoice extraction', 'invoice processing software', 'PDF to Excel converter', 'invoice OCR India', 'accounting automation', 'convert invoice to excel', 'AI invoice extraction', 'GSTIN extraction', 'Tally invoice import'],
  openGraph: {
    title: 'Convert Invoice to Excel Instantly | TrulyInvoice',
    description: 'AI-powered invoice extraction with 99% accuracy. Built for Indian businesses. GST/GSTIN compliant. Start free today.',
    images: ['/og-image-india.jpg'],
    type: 'website',
    locale: 'en_IN',
  },
  twitter: {
    card: 'summary_large_image',
    title: 'Convert Invoice to Excel | TrulyInvoice',
    description: 'AI-powered invoice extraction for Indian businesses. 99% accuracy. GST compliant.',
    images: ['/twitter-image.jpg'],
  },
  alternates: {
    canonical: 'https://trulyinvoice.xyz',
  },
}

export default function Home() {
  return <HomePageComponent />
}
