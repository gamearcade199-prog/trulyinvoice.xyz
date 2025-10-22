import { Metadata } from 'next'
import HomePageComponent from '@/components/HomePage'

export const metadata: Metadata = {
  title: 'TrulyInvoice - Convert Invoice to Excel Instantly | AI-Powered Converter',
  description: 'AI-powered invoice to Excel converter with 99% accuracy. Convert PDFs & images instantly. GST compliant. Free plan available.',
  keywords: ['convert invoice to excel', 'invoice to excel converter', 'AI invoice extraction', 'pdf to excel converter', 'GST invoice to excel', 'indian invoice processing'],
  openGraph: {
    title: 'Convert Invoice to Excel Instantly | TrulyInvoice',
    description: 'AI-powered invoice to Excel converter with 99% accuracy. GST compliant, automatic processing.',
    images: ['/og-image-india.jpg'],
  },
  twitter: {
    card: 'summary_large_image',
    title: 'Convert Invoice to Excel | TrulyInvoice',
    description: 'AI-powered invoice to Excel converter with 99% accuracy.',
    images: ['/twitter-image.jpg'],
  },
  alternates: {
    canonical: 'https://trulyinvoice.xyz',
  },
}

export default function Home() {
  return <HomePageComponent />
}
