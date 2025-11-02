/**
 * SEO Schema Markup Component
 * Generates all necessary JSON-LD structured data for better search ranking
 * Covers: Excel, Tally, QuickBooks, Zoho Books, CSV export formats
 */

export const FAQSchema = () => {
  const faqData = {
    "@context": "https://schema.org",
    "@type": "FAQPage",
    "mainEntity": [
      {
        "@type": "Question",
        "name": "How do I convert an invoice to Excel, Tally, QuickBooks, or Zoho Books?",
        "acceptedAnswer": {
          "@type": "Answer",
          "text": "Simply upload your invoice (PDF, JPG, or PNG) to TrulyInvoice. Our AI will automatically extract all data and you can export to: Excel (formatted sheets), Tally XML (with auto-ledgers), QuickBooks IIF/CSV, Zoho Books CSV (37 columns), or bulk CSV for accountants."
        }
      },
      {
        "@type": "Question",
        "name": "Can I export invoices directly to Tally ERP 9 or Tally Prime?",
        "acceptedAnswer": {
          "@type": "Answer",
          "text": "Yes! TrulyInvoice generates Tally XML files compatible with both Tally ERP 9 and Tally Prime. The XML includes auto-ledger creation, GSTIN-based place of supply detection for all 37 Indian states, and proper voucher entries. Just import the XML file in Tally using Gateway > Import > Vouchers."
        }
      },
      {
        "@type": "Question",
        "name": "Does it support QuickBooks Desktop (IIF) and QuickBooks Online (CSV)?",
        "acceptedAnswer": {
          "@type": "Answer",
          "text": "Absolutely! We provide dual format support. For QuickBooks Desktop, download the IIF file with proper debit/credit entries. For QuickBooks Online, download the CSV file. Both formats include vendor details, invoice amounts, dates, and tax calculations ready for import."
        }
      },
      {
        "@type": "Question",
        "name": "How many columns does the Zoho Books CSV export have?",
        "acceptedAnswer": {
          "@type": "Answer",
          "text": "Our Zoho Books export includes 37 comprehensive columns: Customer Name, Invoice Number, Invoice Date, Due Date, Payment Terms, Item Name, Item Description, Quantity, Unit, Rate, Discount %, Tax %, Amount, Billing Address, Shipping Address, Notes, Terms & Conditions, and more. Fully compatible with Zoho Books import requirements."
        }
      },
      {
        "@type": "Question",
        "name": "Can I bulk export multiple invoices at once?",
        "acceptedAnswer": {
          "@type": "Answer",
          "text": "Yes! Our Pro and Ultra plans support bulk processing. Upload multiple invoices and export them all as: (1) Individual Excel files, (2) Single Tally XML with multiple vouchers, (3) Consolidated QuickBooks IIF/CSV, (4) Merged Zoho Books CSV, or (5) Accountant-friendly bulk CSV with all invoices in one sheet."
        }
      },
      {
        "@type": "Question",
        "name": "Does it extract GSTIN, HSN codes, and calculate CGST/SGST/IGST?",
        "acceptedAnswer": {
          "@type": "Answer",
          "text": "Yes! Our AI automatically extracts GSTIN numbers, validates them, detects place of supply from GSTIN state codes, extracts HSN/SAC codes, and calculates CGST/SGST (intra-state) or IGST (inter-state) based on buyer-seller locations. All exports include proper GST breakdowns."
        }
      },
      {
        "@type": "Question",
        "name": "What invoice formats are supported for conversion?",
        "acceptedAnswer": {
          "@type": "Answer",
          "text": "TrulyInvoice supports PDF invoices, scanned images (JPG, PNG), photographed invoices, and handwritten bills. We handle Indian invoice formats including GST invoices, tax invoices, proforma invoices, purchase orders, supplier bills, vendor invoices, and expense receipts."
        }
      },
      {
        "@type": "Question",
        "name": "How accurate is the invoice data extraction?",
        "acceptedAnswer": {
          "@type": "Answer",
          "text": "Our AI achieves 99% accuracy for Indian invoices. We extract vendor names, GSTIN, invoice numbers, dates, line items, quantities, rates, HSN codes, tax rates, CGST/SGST/IGST amounts, totals, and payment terms. Smart validation catches errors before export."
        }
      },
      {
        "@type": "Question",
        "name": "Can I export invoices to Tally with auto-ledger creation?",
        "acceptedAnswer": {
          "@type": "Answer",
          "text": "Yes! Our Tally XML export automatically creates party ledgers, GST ledgers (CGST, SGST, IGST), and expense ledgers. The system detects place of supply from GSTIN state codes (covering all 37 states), normalizes vendor names to Title Case, and handles zero-GST invoices correctly."
        }
      },
      {
        "@type": "Question",
        "name": "Is there a free plan for invoice conversion?",
        "acceptedAnswer": {
          "@type": "Answer",
          "text": "Yes! Our free plan allows 10 invoice conversions per month with full access to Excel, Tally, QuickBooks, Zoho Books, and CSV exports. No credit card required. Perfect for small businesses and freelancers. Upgrade anytime for unlimited conversions."
        }
      },
      {
        "@type": "Question",
        "name": "Can accountants and CA firms use this for client invoices?",
        "acceptedAnswer": {
          "@type": "Answer",
          "text": "Absolutely! TrulyInvoice is designed for chartered accountants, accounting firms, and professional bookkeepers. Bulk process client invoices, export to their preferred accounting software (Tally/QuickBooks/Zoho Books), and save 90% of manual data entry time. Our accountant Excel export includes separate sheets for summary, details, GST analysis, and reconciliation."
        }
      },
      {
        "@type": "Question",
        "name": "How long does it take to convert an invoice?",
        "acceptedAnswer": {
          "@type": "Answer",
          "text": "Most invoices are processed in under 5 seconds. Even complex invoices with multiple line items and GST calculations are converted instantly. Bulk processing of 50+ invoices typically completes in under 2 minutes."
        }
      },
      {
        "@type": "Question",
        "name": "Does TrulyInvoice work with scanned or photographed invoices?",
        "acceptedAnswer": {
          "@type": "Answer",
          "text": "Yes! Our AI uses advanced OCR technology to extract data from scanned documents and mobile phone photos. Even low-quality images or handwritten invoices can be processed with high accuracy."
        }
      },
      {
        "@type": "Question",
        "name": "Can I customize the export format for my accounting software?",
        "acceptedAnswer": {
          "@type": "Answer",
          "text": "Yes! We support multiple export formats: Excel (with custom templates), Tally XML (ERP 9/Prime compatible), QuickBooks IIF (Desktop) and CSV (Online), Zoho Books CSV (37 columns), and generic CSV. Each format is optimized for direct import into the respective software."
        }
      },
      {
        "@type": "Question",
        "name": "Is my invoice data secure with TrulyInvoice?",
        "acceptedAnswer": {
          "@type": "Answer",
          "text": "Yes! We use bank-level encryption, comply with Indian data protection laws, and have a zero-retention policy. Invoices are processed in real-time and immediately deleted after export. All data is hosted on secure Supabase servers with RLS policies."
        }
      }
    ]
  };

  return (
    <script
      type="application/ld+json"
      dangerouslySetInnerHTML={{ __html: JSON.stringify(faqData) }}
      suppressHydrationWarning
    />
  );
};

export const SoftwareAppSchema = () => {
  const schema = {
    "@context": "https://schema.org",
    "@type": "SoftwareApplication",
    "name": "TrulyInvoice",
    "alternateName": "Invoice to Excel Tally QuickBooks Zoho Books CSV Converter India",
    "description": "AI-powered invoice converter for Indian businesses. Export to Excel, Tally XML (ERP 9/Prime), QuickBooks IIF/CSV, Zoho Books CSV (37 columns), Bulk CSV. 99% accuracy. GST compliant, GSTIN extraction, auto-ledger creation.",
    "applicationCategory": "BusinessApplication",
    "applicationSubCategory": "Invoice Data Extraction & Multi-Format Export",
    "operatingSystem": "Web",
    "url": "https://trulyinvoice.com",
    "image": "https://trulyinvoice.com/og-image-india.jpg",
    "screenshot": [
      "https://trulyinvoice.com/og-image-india.jpg",
      "https://trulyinvoice.com/screenshot-1.jpg"
    ],
    "offers": {
      "@type": "AggregateOffer",
      "priceCurrency": "INR",
      "lowPrice": "0",
      "highPrice": "599",
      "offerCount": "4",
      "offers": [
        {
          "@type": "Offer",
          "name": "Free Plan",
          "price": "0",
          "priceCurrency": "INR",
          "description": "10 invoices/month - Excel, Tally, QuickBooks, Zoho, CSV exports"
        },
        {
          "@type": "Offer",
          "name": "Basic Plan",
          "price": "149",
          "priceCurrency": "INR",
          "description": "80 invoices/month - All export formats included"
        },
        {
          "@type": "Offer",
          "name": "Pro Plan",
          "price": "299",
          "priceCurrency": "INR",
          "description": "300 invoices/month - Bulk processing enabled"
        },
        {
          "@type": "Offer",
          "name": "Ultra Plan",
          "price": "599",
          "priceCurrency": "INR",
          "description": "Unlimited invoices - Priority support"
        }
      ]
    },
    "author": {
      "@type": "Organization",
      "name": "TrulyInvoice",
      "url": "https://trulyinvoice.com"
    },
    "publisher": {
      "@type": "Organization",
      "name": "TrulyInvoice",
      "logo": {
        "@type": "ImageObject",
        "url": "https://trulyinvoice.com/favicon-32x32.png"
      }
    },
    "downloadUrl": "https://trulyinvoice.com",
    "fileFormat": ["PDF", "JPG", "PNG", "Excel (XLSX)", "CSV", "XML (Tally)", "IIF (QuickBooks)"],
    "featureList": [
      "AI-powered invoice scanning with 99% accuracy",
      "Excel export with formulas and multi-sheet structure",
      "Tally XML export with auto-ledger creation",
      "QuickBooks IIF export for Desktop",
      "QuickBooks CSV export for Online",
      "Zoho Books CSV export with 37 columns",
      "Bulk CSV export for accountants",
      "GST compliant processing",
      "GSTIN extraction and validation",
      "Place of supply detection (37 Indian states)",
      "HSN/SAC code extraction",
      "CGST/SGST/IGST calculation",
      "Bulk invoice processing",
      "Indian invoice format support",
      "Vendor name normalization",
      "Zero-GST invoice handling",
      "Bank-level security",
      "Zero data retention policy",
      "Free trial available"
    ],
    "inLanguage": ["en-IN", "hi-IN"],
    "areaServed": {
      "@type": "Country",
      "name": "India"
    },
    "audience": {
      "@type": "BusinessAudience",
      "audienceType": "Small Businesses, Medium Businesses, Traders, Retailers, Distributors, Manufacturers, Wholesalers, Exporters, Importers, Accountants, Chartered Accountants, CA Firms, Bookkeepers, MSME, SME",
      "geographicArea": {
        "@type": "Country",
        "name": "India"
      }
    },
    "softwareVersion": "2.0",
    "releaseNotes": "Enhanced AI for multi-format export: Excel, Tally XML with auto-ledgers, QuickBooks IIF/CSV, Zoho Books 37-column CSV, bulk CSV. Improved GST validation and place of supply detection for all 37 Indian states."
  };

  return (
    <script
      type="application/ld+json"
      dangerouslySetInnerHTML={{ __html: JSON.stringify(schema) }}
      suppressHydrationWarning
    />
  );
};

export const OrganizationSchema = () => {
  const schema = {
    "@context": "https://schema.org",
    "@type": "Organization",
    "name": "TrulyInvoice",
    "alternateName": "trulyinvoice.com",
    "url": "https://trulyinvoice.com",
    "logo": "https://trulyinvoice.com/logo.png",
    "description": "AI-powered invoice to Excel converter for Indian businesses",
    "email": "infotrulybot@gmail.com",
    "telephone": "+91-9101361482",
    "address": {
      "@type": "PostalAddress",
      "addressCountry": "IN",
      "addressLocality": "India"
    },
    "sameAs": [
      "https://twitter.com/trulyinvoice",
      "https://linkedin.com/company/trulyinvoice",
      "https://facebook.com/trulyinvoice"
    ],
    "foundingDate": "2024",
    "areaServed": {
      "@type": "Country",
      "name": "India"
    }
  };

  return (
    <script
      type="application/ld+json"
      dangerouslySetInnerHTML={{ __html: JSON.stringify(schema) }}
      suppressHydrationWarning
    />
  );
};

export const LocalBusinessSchema = () => {
  const cities = [
    { name: "Mumbai", lat: "19.0760", lon: "72.8777" },
    { name: "Delhi", lat: "28.6139", lon: "77.2090" },
    { name: "Bangalore", lat: "12.9716", lon: "77.5946" },
  ];

  return cities.map((city) => (
    <script
      key={city.name}
      type="application/ld+json"
      dangerouslySetInnerHTML={{
        __html: JSON.stringify({
          "@context": "https://schema.org",
          "@type": "LocalBusiness",
          "name": `TrulyInvoice - ${city.name}`,
          "url": `https://trulyinvoice.com/${city.name.toLowerCase()}`,
          "description": `Invoice to Excel converter for businesses in ${city.name}`,
          "geo": {
            "@type": "GeoCoordinates",
            "latitude": city.lat,
            "longitude": city.lon
          },
          "areaServed": city.name,
          "image": "https://trulyinvoice.com/og-image-india.jpg"
        })
      }}
      suppressHydrationWarning
    />
  ));
};
