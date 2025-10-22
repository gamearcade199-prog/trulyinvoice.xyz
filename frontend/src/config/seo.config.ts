// SEO Configuration for TrulyInvoice - Invoice to Excel Converter
// This file contains all SEO settings optimized for Indian market

export const seoConfig = {
  // Base configuration
  siteName: 'TrulyInvoice',
  siteUrl: 'https://trulyinvoice.xyz',
  defaultTitle: 'TrulyInvoice - Invoice to Excel Converter | 99% Accurate AI Extraction',
  defaultDescription: 'AI-powered invoice to Excel converter with 99% accuracy. Convert PDFs & images instantly. GST compliant. Free plan available.',
  
  // Keywords targeting Indian market - Invoice to Excel focus
  keywords: [
    // Primary keywords - Invoice to Excel
    'invoice to excel converter',
    'convert invoice to excel',
    'invoice pdf to excel',
    'invoice image to excel',
    'AI invoice to excel',
    
    // Secondary keywords
    'invoice data extraction',
    'excel invoice converter',
    'pdf invoice to spreadsheet',
    'invoice automation excel',
    'bulk invoice to excel',
    
    // Long-tail keywords
    'convert indian invoice to excel',
    'GST invoice to excel converter',
    'automatic invoice data to excel',
    'invoice scanner to excel online',
    'invoice OCR to excel',
    
    // Indian market specific
    'invoice to excel India',
    'GST bill to excel converter',
    'indian invoice processing to excel',
    'invoice management excel India',
    
    // Use case specific
    'convert supplier invoice to excel',
    'vendor invoice to excel sheet',
    'purchase invoice to excel',
    'sales invoice data extraction',
    'invoice reconciliation excel',
    
    // Technical keywords
    'AI invoice data extraction',
    'automated invoice processing',
    'invoice digitization excel',
    'invoice scanning to excel',
    'invoice text extraction excel',
    
    // Location-based
    'invoice to excel Mumbai',
    'invoice to excel Delhi',
    'invoice to excel Bangalore',
    'invoice to excel Hyderabad',
    'invoice to excel Chennai',
    'invoice to excel Pune',
    
    // Industry-specific
    'invoice to excel for traders',
    'invoice to excel for retailers',
    'invoice to excel for distributors',
    'invoice to excel for manufacturers',
    'invoice to excel for accountants',
    
    // Competitor alternatives
    'Zoho invoice to excel alternative',
    'QuickBooks invoice export to excel',
    'Tally invoice to excel converter',
    'SAP invoice to excel',
    'invoice processing software excel export',
    
    // Problem-solution keywords
    'extract data from invoice to excel',
    'convert scanned invoice to excel',
    'invoice pdf data to excel',
    'bulk invoice processing to excel',
    'multiple invoice to excel converter',
  ],
  
  // Open Graph settings
  openGraph: {
    type: 'website',
    locale: 'en_IN',
  url: 'https://trulyinvoice.xyz',
    siteName: 'TrulyInvoice',
    images: [
      {
  url: 'https://trulyinvoice.xyz/og-image.jpg',
        width: 1200,
        height: 630,
        alt: 'TrulyInvoice - AI Invoice Management for India',
      },
    ],
  },
  
  // Twitter Card settings
  twitter: {
    handle: '@TrulyInvoice',
    site: '@TrulyInvoice',
    cardType: 'summary_large_image',
  },
  
  // Schema.org structured data for Indian market - Invoice to Excel focus
  organization: {
    '@context': 'https://schema.org',
    '@type': 'SoftwareApplication',
    name: 'TrulyInvoice',
    applicationCategory: 'BusinessApplication',
    operatingSystem: 'Web Browser',
    offers: {
      '@type': 'Offer',
      price: '0',
      priceCurrency: 'INR',
      description: 'Free plan with 10 invoice conversions per month',
    },
    address: {
      '@type': 'PostalAddress',
      addressCountry: 'IN',
    },
    description: 'AI-powered invoice to Excel converter for Indian businesses. Convert PDFs and images to Excel sheets with 99% accuracy.',
    softwareVersion: '2.0',
    fileFormat: ['PDF', 'JPG', 'PNG'],
    applicationSubCategory: 'Data Extraction',
    featureList: [
      'AI-powered invoice scanning',
      '99% accurate data extraction',
      'Excel export functionality',
      'GST compliant processing',
      'Bulk invoice processing',
      'Indian invoice format support'
    ],
  },
  
  // Local business schema for India
  localBusiness: {
    '@context': 'https://schema.org',
    '@type': 'SoftwareCompany',
    name: 'TrulyInvoice',
  image: 'https://trulyinvoice.xyz/logo.png',
  '@id': 'https://trulyinvoice.xyz',
  url: 'https://trulyinvoice.xyz',
    priceRange: '₹0 - ₹999',
    address: {
      '@type': 'PostalAddress',
      addressLocality: 'India',
      addressCountry: 'IN',
    },
    areaServed: [
      {
        '@type': 'Country',
        name: 'India',
      },
    ],
    sameAs: [
      'https://www.facebook.com/trulyinvoice',
      'https://twitter.com/trulyinvoice',
      'https://www.linkedin.com/company/trulyinvoice',
  'https://www.instagram.com/trulyinvoice',
    ],
  },
  
  // FAQ Schema for rich snippets - Invoice to Excel focus
  faqSchema: {
    '@context': 'https://schema.org',
    '@type': 'FAQPage',
    mainEntity: [
      {
        '@type': 'Question',
        name: 'How do I convert an invoice to Excel?',
        acceptedAnswer: {
          '@type': 'Answer',
          text: 'Simply upload your invoice (PDF, JPG, or PNG) to TrulyInvoice. Our AI will automatically extract all data and convert it to a perfectly formatted Excel sheet in seconds.',
        },
      },
      {
        '@type': 'Question',
        name: 'What formats can I convert to Excel?',
        acceptedAnswer: {
          '@type': 'Answer',
          text: 'TrulyInvoice supports PDF invoices, scanned images (JPG, PNG), and photographed invoices. We handle Indian invoice formats including GST bills, tax invoices, and supplier bills.',
        },
      },
      {
        '@type': 'Question',
        name: 'How accurate is the invoice to Excel conversion?',
        acceptedAnswer: {
          '@type': 'Answer',
          text: 'Our AI achieves 99% accuracy in extracting invoice data to Excel. We automatically detect vendor names, amounts, GST numbers, line items, dates, and all other invoice details.',
        },
      },
      {
        '@type': 'Question',
        name: 'Can I convert multiple invoices to Excel at once?',
        acceptedAnswer: {
          '@type': 'Answer',
          text: 'Yes! Our Pro and Ultra plans support bulk processing. You can upload multiple invoices simultaneously and download them all as organized Excel sheets.',
        },
      },
      {
        '@type': 'Question',
        name: 'Does it work with Indian GST invoices?',
        acceptedAnswer: {
          '@type': 'Answer',
          text: 'Absolutely! TrulyInvoice is specifically designed for Indian invoices. It automatically extracts GSTIN numbers, HSN codes, tax rates, CGST/SGST/IGST amounts, and validates GST formats.',
        },
      },
      {
        '@type': 'Question',
        name: 'How long does it take to convert an invoice to Excel?',
        acceptedAnswer: {
          '@type': 'Answer',
          text: 'Most invoices are converted in under 5 seconds. Even complex invoices with multiple line items and GST calculations are processed instantly.',
        },
      },
      {
        '@type': 'Question',
        name: 'Can I edit the Excel file after conversion?',
        acceptedAnswer: {
          '@type': 'Answer',
          text: 'Yes, you get a standard Excel file that you can edit, format, and use in any accounting software like Tally, QuickBooks, or Excel itself.',
        },
      },
      {
        '@type': 'Question',
        name: 'Is there a free plan for invoice to Excel conversion?',
        acceptedAnswer: {
          '@type': 'Answer',
          text: 'Yes! Our free plan allows you to convert 10 invoices to Excel per month. Perfect for small businesses and freelancers who need occasional invoice processing.',
        },
      },
    ],
  },
  
  // Robots.txt rules
  robots: {
    rules: [
      {
        userAgent: '*',
        allow: '/',
        disallow: ['/api/', '/dashboard/', '/admin/'],
      },
      {
        userAgent: 'Googlebot',
        allow: '/',
      },
      {
        userAgent: 'Googlebot-Image',
        allow: '/',
      },
    ],
  sitemap: 'https://trulyinvoice.xyz/sitemap.xml',
  },
  
  // Canonical URLs
  canonicalBase: 'https://trulyinvoice.xyz',
  
  // Alternate language versions (for future)
  alternates: {
  canonical: 'https://trulyinvoice.xyz',
    languages: {
  'en-IN': 'https://trulyinvoice.xyz',
  'hi-IN': 'https://trulyinvoice.xyz/hi', // Future Hindi version
    },
  },
}

// Page-specific SEO configurations
export const pageSEO = {
  home: {
    title: 'TrulyInvoice - Convert Invoice to Excel Instantly | AI-Powered Converter',
    description: 'AI-powered invoice to Excel converter with 99% accuracy. Convert PDFs & images instantly. GST compliant. Free plan available.',
    keywords: 'convert invoice to excel, invoice to excel converter, AI invoice extraction, pdf to excel converter, GST invoice to excel, indian invoice processing',
    canonical: 'https://trulyinvoice.xyz',
    structuredData: {
      '@context': 'https://schema.org',
      '@type': 'WebApplication',
      name: 'TrulyInvoice - Invoice to Excel Converter',
      description: 'AI-powered tool to convert invoices to Excel sheets instantly',
      url: 'https://trulyinvoice.xyz',
      applicationCategory: 'BusinessApplication',
      operatingSystem: 'Web Browser',
      offers: {
        '@type': 'Offer',
        price: '0',
        priceCurrency: 'INR',
      },
    },
  },
  
  pricing: {
    title: 'Invoice to Excel Converter Pricing | Affordable Plans for Indian Businesses',
    description: 'Transparent pricing for invoice to Excel conversion. Free plan (₹0), Basic (₹149), Pro (₹299), Ultra (₹599). All plans include Excel export, GST validation. No hidden charges.',
    keywords: 'invoice to excel pricing, excel converter cost India, affordable invoice processing, invoice automation pricing',
    canonical: 'https://trulyinvoice.xyz/pricing',
    structuredData: {
      '@context': 'https://schema.org',
      '@type': 'Product',
      name: 'TrulyInvoice Pricing Plans',
      description: 'Subscription plans for invoice to Excel conversion',
      offers: [
        {
          '@type': 'Offer',
          name: 'Free Plan',
          price: '0',
          priceCurrency: 'INR',
          description: '10 invoice conversions per month',
        },
        {
          '@type': 'Offer',
          name: 'Basic Plan',
          price: '149',
          priceCurrency: 'INR',
          description: '80 invoice conversions per month',
        },
      ],
    },
  },
  
  features: {
    title: 'Invoice to Excel Features | AI-Powered Data Extraction & Conversion',
    description: 'Powerful features for converting invoices to Excel: AI extraction, GST validation, bulk processing, Excel export, 30-day storage, 24/7 support. Try free today.',
    keywords: 'invoice to excel features, excel conversion features, AI invoice processing, bulk invoice to excel, GST invoice validation',
    canonical: 'https://trulyinvoice.xyz/features',
  },
  
  about: {
    title: 'About TrulyInvoice | Making Invoice to Excel Conversion Simple',
    description: 'Learn how TrulyInvoice helps thousands of Indian businesses convert invoices to Excel sheets instantly with AI. Our mission is to automate invoice processing and save time.',
    keywords: 'about TrulyInvoice, invoice to excel company India, AI invoice processing company',
    canonical: 'https://trulyinvoice.xyz/about',
  },
  
  contact: {
    title: 'Contact TrulyInvoice | Get Help with Invoice to Excel Conversion',
    description: 'Need help converting invoices to Excel? Contact our Indian support team via email or phone. Quick responses, expert guidance, GST compliance assistance.',
    keywords: 'TrulyInvoice contact, invoice to excel support India, excel conversion help',
    canonical: 'https://trulyinvoice.xyz/contact',
  },
  
  blog: {
    title: 'Invoice Processing Blog | Excel Conversion Tips & GST Updates for India',
    description: 'Expert insights on invoice to Excel conversion, GST compliance, accounting automation, and business efficiency for Indian SMEs and enterprises.',
    keywords: 'invoice to excel blog India, GST compliance tips, accounting automation guide',
    canonical: 'https://trulyinvoice.xyz/blog',
  },
}

// Indian city-specific landing pages (for local SEO)
export const cityPages = [
  { city: 'Mumbai', state: 'Maharashtra', population: '20M+' },
  { city: 'Delhi', state: 'Delhi NCR', population: '18M+' },
  { city: 'Bangalore', state: 'Karnataka', population: '12M+' },
  { city: 'Hyderabad', state: 'Telangana', population: '10M+' },
  { city: 'Chennai', state: 'Tamil Nadu', population: '9M+' },
  { city: 'Pune', state: 'Maharashtra', population: '7M+' },
  { city: 'Ahmedabad', state: 'Gujarat', population: '7M+' },
  { city: 'Kolkata', state: 'West Bengal', population: '14M+' },
]

export default seoConfig
