// Per-page metadata generator for SEO
import { Metadata } from 'next'
import seoConfig from '@/config/seo.config'

interface PageMetadata {
  title: string
  description: string
  keywords?: string[]
  canonical?: string
  ogImage?: string
}

export function generatePageMetadata(page: PageMetadata): Metadata {
  const baseUrl = 'https://trulyinvoice.xyz'
  
  return {
    title: page.title,
    description: page.description,
    keywords: page.keywords || seoConfig.keywords,
    alternates: {
      canonical: page.canonical || `${baseUrl}${typeof window !== 'undefined' ? window.location.pathname : ''}`,
    },
    openGraph: {
      title: page.title,
      description: page.description,
      url: page.canonical || baseUrl,
      siteName: seoConfig.siteName,
      images: [
        {
          url: page.ogImage || '/og-image-india.jpg',
          width: 1200,
          height: 630,
          alt: page.title,
        },
      ],
      locale: 'en_IN',
      type: 'website',
    },
    twitter: {
      card: 'summary_large_image',
      title: page.title,
      description: page.description,
      images: [page.ogImage || '/twitter-image.jpg'],
    },
  }
}

// Pre-defined metadata for each page
export const pageMetadata = {
  home: generatePageMetadata({
    title: seoConfig.defaultTitle,
    description: seoConfig.defaultDescription,
  canonical: 'https://trulyinvoice.xyz',
  }),
  
  pricing: generatePageMetadata({
    title: 'Pricing Plans - Affordable GST Invoice Software | TrulyInvoice',
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
  canonical: 'https://trulyinvoice.xyz/pricing',
  }),
  
  login: generatePageMetadata({
    title: 'Login - Access Your Invoice Dashboard | TrulyInvoice',
    description: 'Login to TrulyInvoice to manage your invoices, track payments, and automate GST billing. Secure access to your invoice management dashboard.',
  canonical: 'https://trulyinvoice.xyz/login',
  }),
  
  signup: generatePageMetadata({
    title: 'Sign Up Free - Start Managing Invoices Today | TrulyInvoice',
    description: 'Create your free TrulyInvoice account. Get 10 free invoice scans per month. No credit card required. Start automating your GST invoices in 2 minutes.',
  canonical: 'https://trulyinvoice.xyz/signup',
  }),
  
  dashboard: generatePageMetadata({
    title: 'Dashboard - Invoice Management | TrulyInvoice',
    description: 'View and manage all your invoices in one place. Upload, process, and export GST invoices with AI-powered automation.',
  canonical: 'https://trulyinvoice.xyz/dashboard',
  }),
}
