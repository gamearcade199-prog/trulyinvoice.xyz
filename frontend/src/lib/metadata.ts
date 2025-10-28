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
    canonical: 'https://trulyinvoice.xyz',
  }),
  
  pricing: generatePageMetadata({
    title: 'Pricing - Excel, Tally, QuickBooks, Zoho Export Plans | TrulyInvoice',
    description: 'Transparent pricing for all export formats. Free (₹0/10 invoices), Basic (₹149/80), Pro (₹299/300), Ultra (₹599/unlimited). Excel, Tally XML, QuickBooks, Zoho Books, CSV exports included.',
    keywords: [
      'invoice converter pricing india',
      'tally export pricing',
      'quickbooks export cost',
      'zoho books pricing',
      'excel converter plans',
      'invoice automation pricing',
      'gst invoice software cost',
    ],
    canonical: 'https://trulyinvoice.xyz/pricing',
  }),
  
  features: generatePageMetadata({
    title: 'Features - Excel, Tally XML, QuickBooks IIF, Zoho CSV Export | TrulyInvoice',
    description: 'Export to Excel with formulas, Tally XML with auto-ledgers, QuickBooks IIF/CSV dual format, Zoho Books 37-column CSV, Bulk CSV for accountants. GST validation, 99% AI accuracy.',
    keywords: [
      'invoice export features',
      'tally xml auto ledger',
      'quickbooks iif export',
      'zoho books csv columns',
      'bulk invoice processing',
      'gst validation features',
    ],
    canonical: 'https://trulyinvoice.xyz/features',
  }),
  
  tallyExport: generatePageMetadata({
    title: 'Invoice to Tally XML Converter | Auto-Ledger Creation | TrulyInvoice',
    description: 'Convert invoices to Tally XML instantly. Auto-creates ledgers, detects place of supply from GSTIN (37 states), generates purchase vouchers. Compatible with Tally ERP 9 & Tally Prime.',
    keywords: [
      'invoice to tally xml',
      'convert invoice to tally',
      'tally erp invoice import',
      'tally prime xml',
      'invoice to tally voucher',
      'tally auto ledger creation',
    ],
    canonical: 'https://trulyinvoice.xyz/export/tally',
  }),
  
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
    canonical: 'https://trulyinvoice.xyz/export/quickbooks',
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
    canonical: 'https://trulyinvoice.xyz/export/zoho-books',
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
    canonical: 'https://trulyinvoice.xyz/export/excel',
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
    canonical: 'https://trulyinvoice.xyz/export/csv',
  }),
  
  login: generatePageMetadata({
    title: 'Login - Access Your Invoice Dashboard | TrulyInvoice',
    description: 'Login to TrulyInvoice to manage your invoices, export to Excel, Tally, QuickBooks, Zoho Books, CSV. Secure access to your invoice automation dashboard.',
    canonical: 'https://trulyinvoice.xyz/login',
  }),
  
  signup: generatePageMetadata({
    title: 'Sign Up Free - 10 Free Invoice Exports/Month | TrulyInvoice',
    description: 'Create your free TrulyInvoice account. Get 10 free invoice conversions per month. Export to Excel, Tally, QuickBooks, Zoho Books, CSV. No credit card required.',
    canonical: 'https://trulyinvoice.xyz/signup',
  }),
  
  dashboard: generatePageMetadata({
    title: 'Dashboard - Invoice Management & Export | TrulyInvoice',
    description: 'View and manage all your invoices. Upload, process, and export to Excel, Tally XML, QuickBooks, Zoho Books, or CSV with AI-powered automation.',
    canonical: 'https://trulyinvoice.xyz/dashboard',
  }),
  
  about: generatePageMetadata({
    title: 'About TrulyInvoice | Multi-Format Invoice Export Platform',
    description: 'Learn how TrulyInvoice helps Indian businesses export invoices to Excel, Tally, QuickBooks, Zoho Books, and CSV. Our mission: automate invoice processing.',
    canonical: 'https://trulyinvoice.xyz/about',
  }),
  
  contact: generatePageMetadata({
    title: 'Contact TrulyInvoice | Get Help with Invoice Export',
    description: 'Need help with Excel, Tally, QuickBooks, or Zoho Books export? Contact our Indian support team. Quick responses, expert guidance.',
    canonical: 'https://trulyinvoice.xyz/contact',
  }),
  
  blog: generatePageMetadata({
    title: 'Invoice Automation Blog | Excel, Tally, QuickBooks Export Guides',
    description: 'Expert guides on invoice to Excel conversion, Tally XML import, QuickBooks IIF/CSV upload, Zoho Books integration, GST compliance.',
    canonical: 'https://trulyinvoice.xyz/blog',
  }),
}
