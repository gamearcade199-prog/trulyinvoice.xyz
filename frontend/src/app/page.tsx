import { Metadata } from 'next'
import HomePageComponent from '@/components/HomePage'
import { advancedSEOSchemas } from '@/config/seo.advanced'

export const metadata: Metadata = {
  title: 'Convert Invoice to Excel Instantly with AI | TrulyInvoice - GST Compliant',
  description: 'Convert PDF & image invoices to Excel in 5 seconds. AI-powered invoice extraction for Indian businesses. High accuracy, GST/GSTIN compliant. Free trial - no signup required.',
  keywords: ['invoice to excel converter India', 'GST invoice extraction', 'invoice processing software', 'PDF to Excel converter', 'invoice OCR India', 'accounting automation', 'convert invoice to excel', 'AI invoice extraction', 'GSTIN extraction', 'Tally invoice import'],
  openGraph: {
    title: 'Convert Invoice to Excel Instantly | TrulyInvoice',
    description: 'AI-powered invoice extraction with high accuracy. Built for Indian businesses. GST/GSTIN compliant. Start free today.',
    images: ['/og-image-india.jpg'],
    type: 'website',
    locale: 'en_IN',
  },
  twitter: {
    card: 'summary_large_image',
    title: 'Convert Invoice to Excel | TrulyInvoice',
    description: 'AI-powered invoice extraction for Indian businesses. High accuracy. GST compliant.',
    images: ['/twitter-image.jpg'],
  },
  alternates: {
    canonical: 'https://trulyinvoice.com',
  },
}

export default function Home() {
  return (
    <>
      {/* Advanced SEO Schemas */}
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{
          __html: JSON.stringify(advancedSEOSchemas.howTo),
        }}
      />
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{
          __html: JSON.stringify(advancedSEOSchemas.createBreadcrumb([
            { name: 'Home', url: 'https://trulyinvoice.com' },
          ])),
        }}
      />
      
      <HomePageComponent />
    </>
  )
}
