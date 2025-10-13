// SEO Configuration for TrulyInvoice - India Market
// This file contains all SEO settings optimized for Indian search engines

export const seoConfig = {
  // Base configuration
  siteName: 'TrulyInvoice',
  siteUrl: 'https://trulyinvoice.xyz',
  defaultTitle: 'TrulyInvoice - AI-Powered Invoice Management for Indian Businesses | GST Compliant',
  defaultDescription: 'India\'s #1 AI-powered invoice management software. Extract GST invoice data in seconds. 99% accuracy, automatic GST validation, Excel export. Free plan available. Trusted by 1000+ Indian businesses.',
  
  // Keywords targeting Indian market
  keywords: [
    // Primary keywords
    'invoice management software India',
    'GST invoice software',
    'AI invoice extraction',
    'invoice OCR India',
    'GST compliant invoice software',
    
    // Secondary keywords
    'invoice automation India',
    'invoice data extraction',
    'GST invoice validation',
    'invoice processing software',
    'Indian invoice management',
    
    // Long-tail keywords
    'automatic invoice data extraction India',
    'GST invoice scanner online',
    'invoice management for small business India',
    'GST compliant invoice extractor',
    'AI invoice reader India',
    
    // Hindi keywords (transliterated)
    'invoice software Hindi',
    'GST bill management',
    'invoice automation for Indian SMEs',
    
    // Location-based
    'invoice software Mumbai',
    'invoice software Delhi',
    'invoice software Bangalore',
    'invoice software Hyderabad',
    'invoice software Chennai',
    'invoice software Pune',
    
    // Industry-specific
    'invoice software for retailers India',
    'invoice management for traders',
    'invoice software for distributors',
    'invoice OCR for Indian businesses',
    
    // Competitor alternatives
    'Zoho invoice alternative India',
    'QuickBooks alternative for GST',
    'invoice management software like Tally',
    
    // Use case specific
    'bulk invoice processing India',
    'GST return preparation software',
    'invoice export to Excel',
    'invoice data for accounting',
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
  
  // Schema.org structured data for Indian market
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
    },
    aggregateRating: {
      '@type': 'AggregateRating',
      ratingValue: '4.8',
      ratingCount: '1247',
    },
    address: {
      '@type': 'PostalAddress',
      addressCountry: 'IN',
    },
  },
  
  // Local business schema for India
  localBusiness: {
    '@context': 'https://schema.org',
    '@type': 'SoftwareCompany',
    name: 'TrulyInvoice',
  image: 'https://trulyinvoice.xyz/logo.png',
  '@id': 'https://trulyinvoice.xyz',
  url: 'https://trulyinvoice.xyz',
    telephone: '+91-XXXXXXXXXX',
    priceRange: '₹0 - ₹999',
    address: {
      '@type': 'PostalAddress',
      streetAddress: 'Your Street Address',
      addressLocality: 'Mumbai',
      addressRegion: 'Maharashtra',
      postalCode: '400001',
      addressCountry: 'IN',
    },
    geo: {
      '@type': 'GeoCoordinates',
      latitude: 19.0760,
      longitude: 72.8777,
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
  
  // FAQ Schema for rich snippets
  faqSchema: {
    '@context': 'https://schema.org',
    '@type': 'FAQPage',
    mainEntity: [
      {
        '@type': 'Question',
        name: 'Is TrulyInvoice GST compliant?',
        acceptedAnswer: {
          '@type': 'Answer',
          text: 'Yes, TrulyInvoice is fully GST compliant. Our AI automatically extracts GSTIN, HSN codes, tax rates, and validates GST invoice formats as per Indian government standards.',
        },
      },
      {
        '@type': 'Question',
        name: 'How accurate is the AI invoice extraction?',
        acceptedAnswer: {
          '@type': 'Answer',
          text: 'Our AI achieves 99% accuracy in extracting invoice data from Indian invoices, including vendor details, line items, GST amounts, and total values.',
        },
      },
      {
        '@type': 'Question',
        name: 'Can I export data to Tally or Excel?',
        acceptedAnswer: {
          '@type': 'Answer',
          text: 'Yes, you can export extracted invoice data to Excel, CSV, and other formats compatible with Tally, QuickBooks, and other Indian accounting software.',
        },
      },
      {
        '@type': 'Question',
        name: 'Is there a free plan available?',
        acceptedAnswer: {
          '@type': 'Answer',
          text: 'Yes, we offer a forever-free plan with 10 invoice scans per month. Perfect for small businesses and freelancers in India.',
        },
      },
      {
        '@type': 'Question',
        name: 'Which payment methods do you accept?',
        acceptedAnswer: {
          '@type': 'Answer',
          text: 'We accept all major Indian payment methods including UPI, credit/debit cards, net banking, and wallets through our secure Razorpay integration.',
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
    title: 'TrulyInvoice - AI Invoice Management | GST Compliant Invoice Software India',
    description: 'Process Indian invoices 10x faster with AI. Automatic GST validation, 99% accuracy, Excel export. Free plan with 10 scans/month. Used by 1000+ businesses across India.',
    keywords: 'invoice management software India, GST invoice software, AI invoice extraction, invoice OCR India, GST compliant software',
  canonical: 'https://trulyinvoice.xyz',
  },
  
  pricing: {
    title: 'Pricing Plans - Affordable Invoice Management for Indian Businesses | TrulyInvoice',
    description: 'Transparent pricing for Indian businesses. Free plan (₹0), Basic (₹99), Pro (₹399), Ultra (₹999). All plans include GST validation, Excel export, and email support. No hidden charges.',
    keywords: 'invoice software pricing India, GST software cost, affordable invoice management, invoice software plans India',
  canonical: 'https://trulyinvoice.xyz/pricing',
  },
  
  features: {
    title: 'Features - AI-Powered Invoice Processing for India | TrulyInvoice',
    description: 'Powerful features for Indian businesses: AI invoice extraction, GST validation, bulk processing, Excel export, 30-day storage, 24/7 support. Try free today.',
    keywords: 'invoice software features, GST invoice validation, bulk invoice processing, invoice data extraction India',
  canonical: 'https://trulyinvoice.xyz/features',
  },
  
  about: {
    title: 'About Us - Making Invoice Management Simple for India | TrulyInvoice',
    description: 'Learn how TrulyInvoice is helping thousands of Indian businesses automate invoice processing with AI. Our mission is to simplify GST compliance and save time.',
    keywords: 'about TrulyInvoice, invoice software company India, GST compliance solution',
  canonical: 'https://trulyinvoice.xyz/about',
  },
  
  contact: {
    title: 'Contact Us - Get Help with Invoice Management | TrulyInvoice',
    description: 'Need help with invoice processing? Contact our Indian support team via email or phone. Quick responses, expert guidance, GST compliance assistance.',
    keywords: 'TrulyInvoice contact, invoice software support India, GST software help',
  canonical: 'https://trulyinvoice.xyz/contact',
  },
  
  blog: {
    title: 'Blog - Invoice Management Tips & GST Updates for India | TrulyInvoice',
    description: 'Expert insights on invoice management, GST compliance, accounting automation, and business efficiency for Indian SMEs and enterprises.',
    keywords: 'invoice management blog India, GST compliance tips, accounting automation guide',
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
