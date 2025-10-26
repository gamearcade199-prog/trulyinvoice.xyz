/**
 * SEO Schema Markup Component
 * Generates all necessary JSON-LD structured data for better search ranking
 */

export const FAQSchema = () => {
  const faqData = {
    "@context": "https://schema.org",
    "@type": "FAQPage",
    "mainEntity": [
      {
        "@type": "Question",
        "name": "How accurate is TrulyInvoice for Indian GST invoices?",
        "acceptedAnswer": {
          "@type": "Answer",
          "text": "TrulyInvoice achieves 98% accuracy for Indian GST invoices, automatically extracting GSTIN, PAN, invoice numbers, line items, tax details, and amounts. Our AI is specifically trained on Indian invoice formats."
        }
      },
      {
        "@type": "Question",
        "name": "What invoice formats does TrulyInvoice support?",
        "acceptedAnswer": {
          "@type": "Answer",
          "text": "We support PDF invoices, scanned images (JPG, PNG), and handwritten invoices. Our AI can process invoices in any Indian format, including GST invoices, proforma invoices, and purchase orders."
        }
      },
      {
        "@type": "Question",
        "name": "Is my invoice data secure with TrulyInvoice?",
        "acceptedAnswer": {
          "@type": "Answer",
          "text": "Yes, your data is completely secure. We use bank-level encryption, comply with Indian data protection laws, and never store your invoices after processing. All data is hosted on secure Supabase servers."
        }
      },
      {
        "@type": "Question",
        "name": "Can I integrate TrulyInvoice with Tally or QuickBooks?",
        "acceptedAnswer": {
          "@type": "Answer",
          "text": "Yes! We provide direct integration with Tally, QuickBooks, and Excel. You can export converted invoices directly to your accounting software with a single click."
        }
      },
      {
        "@type": "Question",
        "name": "How much does TrulyInvoice cost?",
        "acceptedAnswer": {
          "@type": "Answer",
          "text": "TrulyInvoice offers a free plan with 10 conversions per month. Paid plans start from ₹299/month for 100 conversions, ₹799/month for unlimited conversions. No credit card required for free trial."
        }
      },
      {
        "@type": "Question",
        "name": "Can I extract GSTIN from invoices automatically?",
        "acceptedAnswer": {
          "@type": "Answer",
          "text": "Yes! Our AI automatically identifies and extracts GSTIN from invoices. We can extract GST numbers, PAN, invoice dates, amounts, line items, and all other relevant fields automatically."
        }
      },
      {
        "@type": "Question",
        "name": "Do you support bulk invoice processing?",
        "acceptedAnswer": {
          "@type": "Answer",
          "text": "Absolutely! You can upload and process up to 100 invoices at once with our bulk processing feature. Get all your invoices converted to Excel in minutes, not hours."
        }
      },
      {
        "@type": "Question",
        "name": "What happens to my uploaded invoices?",
        "acceptedAnswer": {
          "@type": "Answer",
          "text": "Your invoices are never stored on our servers. They are processed in real-time and permanently deleted after extraction. We have a zero-retention policy for your documents."
        }
      },
      {
        "@type": "Question",
        "name": "Is TrulyInvoice suitable for accountants and CA firms?",
        "acceptedAnswer": {
          "@type": "Answer",
          "text": "Yes, TrulyInvoice is designed for chartered accountants, accounting firms, and professional bookkeepers. It significantly reduces data entry time and improves accuracy in invoice processing."
        }
      },
      {
        "@type": "Question",
        "name": "Can I try TrulyInvoice for free before paying?",
        "acceptedAnswer": {
          "@type": "Answer",
          "text": "Yes! We offer a completely free trial with 10 invoices per month. No credit card required to start. Upgrade to a paid plan anytime to process unlimited invoices."
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
    "alternateName": "Invoice to Excel Converter India",
    "description": "AI-powered invoice to Excel converter for Indian businesses. Convert PDF and image invoices to Excel in seconds with 98% accuracy. GST compliant, GSTIN extraction, Tally integration.",
    "applicationCategory": "BusinessApplication",
    "applicationSubCategory": "Data Extraction Software",
    "operatingSystem": "Web",
    "url": "https://trulyinvoice.xyz",
    "image": "https://trulyinvoice.xyz/og-image-india.jpg",
    "screenshot": [
      "https://trulyinvoice.xyz/og-image-india.jpg",
      "https://trulyinvoice.xyz/screenshot-1.jpg"
    ],
    "offers": {
      "@type": "AggregateOffer",
      "priceCurrency": "INR",
      "lowPrice": "0",
      "highPrice": "799",
      "offerCount": "4",
      "offers": [
        {
          "@type": "Offer",
          "name": "Free Plan",
          "price": "0",
          "priceCurrency": "INR",
          "description": "10 invoices per month"
        },
        {
          "@type": "Offer",
          "name": "Starter Plan",
          "price": "299",
          "priceCurrency": "INR",
          "description": "100 invoices per month"
        },
        {
          "@type": "Offer",
          "name": "Professional Plan",
          "price": "799",
          "priceCurrency": "INR",
          "description": "Unlimited invoices"
        }
      ]
    },
    "aggregateRating": {
      "@type": "AggregateRating",
      "ratingValue": "4.8",
      "ratingCount": "127",
      "bestRating": "5",
      "worstRating": "1"
    },
    "author": {
      "@type": "Organization",
      "name": "TrulyInvoice",
      "url": "https://trulyinvoice.xyz"
    },
    "publisher": {
      "@type": "Organization",
      "name": "TrulyInvoice",
      "logo": {
        "@type": "ImageObject",
        "url": "https://trulyinvoice.xyz/favicon-32x32.png"
      }
    },
    "downloadUrl": "https://trulyinvoice.xyz",
    "fileFormat": ["PDF", "JPG", "PNG"],
    "featureList": [
      "AI-powered invoice scanning",
      "98% accurate data extraction",
      "Excel export functionality",
      "GST compliant processing",
      "GSTIN extraction",
      "Bulk invoice processing",
      "Indian invoice format support",
      "Tally integration",
      "QuickBooks integration",
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
      "audienceType": "Small and Medium Businesses, Traders, Retailers, Manufacturers, Accountants, Chartered Accountants, CA Firms",
      "geographicArea": {
        "@type": "Country",
        "name": "India"
      }
    },
    "softwareVersion": "2.0",
    "releaseNotes": "Enhanced AI for GST invoice processing, bulk processing, and better accuracy"
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
    "alternateName": "TrulyInvoice.xyz",
    "url": "https://trulyinvoice.xyz",
    "logo": "https://trulyinvoice.xyz/logo.png",
    "description": "AI-powered invoice to Excel converter for Indian businesses",
    "email": "support@trulyinvoice.xyz",
    "telephone": "+91-XXXXXXXXXX",
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
          "url": `https://trulyinvoice.xyz/${city.name.toLowerCase()}`,
          "description": `Invoice to Excel converter for businesses in ${city.name}`,
          "geo": {
            "@type": "GeoCoordinates",
            "latitude": city.lat,
            "longitude": city.lon
          },
          "areaServed": city.name,
          "image": "https://trulyinvoice.xyz/og-image-india.jpg"
        })
      }}
      suppressHydrationWarning
    />
  ));
};
