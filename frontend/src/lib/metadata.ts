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
  const baseUrl = 'https://trulyinvoice.com'
  
  return {
    title: page.title,
    description: page.description,
    keywords: page.keywords || seoConfig.keywords,
    alternates: {
      canonical: page.canonical || baseUrl,
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
    canonical: 'https://trulyinvoice.com',
  }),
  
  pricing: generatePageMetadata({
    title: 'Pricing Plans | Invoice to Excel Converter | Free 10/Month',
    description: 'Transparent pricing for invoice conversion. FREE (10/month), Basic (₹149/50), Pro (₹499/200), Ultra (₹1499/1000), Max (₹2999/10000). Excel, QuickBooks, Zoho Books, CSV exports included. No hidden fees.',
    keywords: [
      'invoice converter pricing india',
      'invoice to excel pricing',
      'quickbooks export cost',
      'zoho books pricing',
      'excel converter plans',
      'invoice automation pricing',
      'gst invoice software cost',
      'free invoice converter',
    ],
    canonical: 'https://trulyinvoice.com/pricing',
  }),
  
  features: generatePageMetadata({
    title: 'Features | 99% AI Accuracy | Excel, QuickBooks, Zoho Export',
    description: 'Export to Excel with formulas & multi-sheet structure, QuickBooks IIF/CSV dual format, Zoho Books 37-column CSV, Bulk CSV for accountants. 99% AI accuracy, GST validation, GSTIN extraction, HSN codes.',
    keywords: [
      'invoice export features',
      'ai invoice extraction 99%',
      'quickbooks iif export',
      'zoho books csv columns',
      'bulk invoice processing',
      'gst validation features',
      'gstin extraction',
      'hsn code extraction',
    ],
    canonical: 'https://trulyinvoice.com/features',
  }),
  
  // Removed tallyExport metadata - feature deprecated
  
  quickbooksExport: generatePageMetadata({
    title: 'Invoice to QuickBooks Converter | IIF & CSV Export | TrulyInvoice',
    description: 'Export invoices to QuickBooks Desktop (IIF) or QuickBooks Online (CSV). Dual format support, auto-balancing entries, vendor management, tax calculations.',
    keywords: [
      'invoice to quickbooks',
      'quickbooks iif converter',
      'quickbooks csv import',
      'invoice to qbo',
      'quickbooks desktop import',
      'quickbooks online upload',
    ],
    canonical: 'https://trulyinvoice.com/export/quickbooks',
  }),
  
  zohoBooksExport: generatePageMetadata({
    title: 'Invoice to Zoho Books CSV Converter | 37 Columns | TrulyInvoice',
    description: 'Export invoices to Zoho Books CSV with 37 comprehensive columns: payment terms, billing address, item descriptions, discount %, notes, terms & conditions.',
    keywords: [
      'invoice to zoho books',
      'zoho books csv converter',
      'zoho books invoice import',
      'zoho books csv upload',
      'invoice to zoho books online',
    ],
    canonical: 'https://trulyinvoice.com/export/zoho-books',
  }),
  
  excelExport: generatePageMetadata({
    title: 'Invoice to Excel Converter | Formatted Sheets with Formulas | TrulyInvoice',
    description: 'Convert invoices to Excel with professional formatting, formulas, GST calculations, multi-sheet structure. Accountant Excel with summary, details, GST analysis, reconciliation sheets.',
    keywords: [
      'invoice to excel converter',
      'convert invoice to excel',
      'invoice pdf to excel',
      'ai invoice to excel',
      'gst invoice to excel',
      'accountant excel export',
    ],
    canonical: 'https://trulyinvoice.com/export/excel',
  }),
  
  csvExport: generatePageMetadata({
    title: 'Bulk Invoice to CSV Converter | For Accountants & CA Firms | TrulyInvoice',
    description: 'Export multiple invoices to CSV in bulk. Perfect for accountants, CA firms, bookkeepers. Consolidated CSV with all invoice data, GST details, vendor info.',
    keywords: [
      'bulk invoice to csv',
      'invoice to csv converter',
      'invoice csv export',
      'accountant csv export',
      'ca invoice processing',
      'bulk csv download',
    ],
    canonical: 'https://trulyinvoice.com/export/csv',
  }),
  
  login: generatePageMetadata({
    title: 'Login | Access Invoice Dashboard | TrulyInvoice',
    description: 'Login to TrulyInvoice to manage your invoices and export to Excel, QuickBooks, Zoho Books, CSV. Secure access to your 99% accurate AI-powered invoice automation dashboard.',
    canonical: 'https://trulyinvoice.com/login',
  }),
  
  signup: generatePageMetadata({
    title: 'Sign Up Free | 10 Free Invoices/Month | TrulyInvoice',
    description: 'Create your free TrulyInvoice account. Get 10 free invoice conversions per month with 99% AI accuracy. Export to Excel, QuickBooks, Zoho Books, CSV. No credit card required.',
    canonical: 'https://trulyinvoice.com/signup',
  }),
  
  dashboard: generatePageMetadata({
    title: 'Dashboard | Invoice Management & Export | TrulyInvoice',
    description: 'View and manage all your invoices. Upload, process, and export to Excel, QuickBooks, Zoho Books, or CSV with 99% accurate AI-powered automation. Track your monthly usage.',
    canonical: 'https://trulyinvoice.com/dashboard',
  }),
  
  about: generatePageMetadata({
    title: 'About TrulyInvoice | 99% AI-Powered Invoice Converter',
    description: 'Learn how TrulyInvoice helps Indian businesses export invoices to Excel, QuickBooks, Zoho Books, and CSV with 99% AI accuracy. Our mission: automate invoice processing for SMBs and accountants.',
    canonical: 'https://trulyinvoice.com/about',
  }),
  
  contact: generatePageMetadata({
    title: 'Contact TrulyInvoice | Get Expert Help',
    description: 'Need help with Excel, QuickBooks, or Zoho Books export? Contact our Indian support team for expert guidance on invoice automation. Quick responses, helpful support.',
    canonical: 'https://trulyinvoice.com/contact',
  }),
  
  blog: generatePageMetadata({
    title: 'Invoice Automation Blog | Excel, QuickBooks, Zoho Export Guides',
    description: 'Expert guides on invoice to Excel conversion, QuickBooks IIF/CSV upload, Zoho Books integration, GST compliance, and AI-powered invoice processing. Learn best practices.',
    canonical: 'https://trulyinvoice.com/blog',
  }),
}
