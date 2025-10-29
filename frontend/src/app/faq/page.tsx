import { Metadata } from 'next'

export const metadata: Metadata = {
  title: 'FAQ - Invoice to Excel Converter | TrulyInvoice Questions Answered',
  description: 'Frequently asked questions about TrulyInvoice invoice to Excel converter. Learn about accuracy, pricing, security, integrations, and GST compliance.',
  keywords: ['invoice to excel FAQ', 'TrulyInvoice questions', 'invoice converter FAQ', 'GST software FAQ'],
  openGraph: {
    title: 'FAQ - TrulyInvoice Invoice to Excel Converter',
    description: 'Common questions about invoice extraction, GST compliance, and pricing',
    images: ['/og-image-india.jpg'],
  },
}

const faqs = [
  {
    category: 'Accuracy & Processing',
    questions: [
      {
        q: 'How accurate is TrulyInvoice for Indian GST invoices?',
        a: 'TrulyInvoice achieves 98% accuracy for Indian GST invoices, automatically extracting GSTIN, PAN, invoice numbers, line items, tax details, and amounts. Our AI is specifically trained on 10,000+ Indian invoice samples.',
      },
      {
        q: 'What invoice formats does TrulyInvoice support?',
        a: 'We support PDF invoices, scanned images (JPG, PNG), and handwritten invoices. Our AI can process invoices in any Indian format, including GST invoices, proforma invoices, and purchase orders.',
      },
      {
        q: 'Can TrulyInvoice handle blurry or poor-quality images?',
        a: 'Yes! Our AI includes image enhancement features. For best results, use images with 300+ DPI resolution and good lighting. We can process images up to 50MB.',
      },
    ],
  },
  {
    category: 'Security & Data Protection',
    questions: [
      {
        q: 'Is my invoice data secure with TrulyInvoice?',
        a: 'Yes, your data is completely secure. We use bank-level encryption (256-bit AES), comply with Indian data protection laws, and have a zero-retention policy—invoices are deleted immediately after processing. All data is hosted on secure Supabase servers.',
      },
      {
        q: 'Do you store my uploaded invoices?',
        a: 'No. We follow a strict zero-retention policy. Your invoices are processed in real-time and permanently deleted after extraction. We never store your documents on our servers.',
      },
      {
        q: 'What about GDPR and data privacy compliance?',
        a: 'TrulyInvoice complies with GDPR, Indian Privacy Policy, and various other data protection regulations. We have regular security audits and maintain ISO-grade security standards.',
      },
    ],
  },
  {
    category: 'Pricing & Plans',
    questions: [
      {
        q: 'How much does TrulyInvoice cost?',
        a: 'We offer a free plan with 10 conversions per month. Paid plans start from ₹299/month for 100 conversions, ₹799/month for unlimited conversions. No setup fees or hidden charges.',
      },
      {
        q: 'Do I need a credit card for the free trial?',
        a: 'No credit card required! Sign up for free and get 10 invoice conversions per month to test our service. Upgrade anytime to a paid plan.',
      },
      {
        q: 'Can I cancel my subscription anytime?',
        a: 'Yes, absolutely. You can cancel your subscription anytime without penalty. Your remaining credits are available until the end of your billing period.',
      },
      {
        q: 'Do you offer annual discounts?',
        a: 'Yes, we offer 20% discount on annual plans. Contact our sales team for enterprise pricing and bulk discounts.',
      },
    ],
  },
  {
    category: 'Integrations',
    questions: [
      {
        q: 'Can I integrate TrulyInvoice with Tally?',
        a: 'Yes! We provide direct integration with Tally. Converted invoices can be exported directly to Tally with automatic field mapping. Perfect for Tally users.',
      },
      {
        q: 'Does TrulyInvoice work with QuickBooks?',
        a: 'Yes, we support QuickBooks integration. Export converted invoices directly to QuickBooks for seamless accounting workflow.',
      },
      {
        q: 'What about Excel export?',
        a: 'Excel export is our standard format. You can export in .xlsx format with all invoice details properly organized in columns.',
      },
      {
        q: 'Can I use the API for custom integrations?',
        a: 'Yes! We provide a robust REST API for developers. Contact our sales team for API access and documentation.',
      },
    ],
  },
  {
    category: 'GST & Compliance',
    questions: [
      {
        q: 'Can TrulyInvoice extract GSTIN from invoices?',
        a: 'Yes! Our AI automatically identifies and extracts GSTIN with 99% accuracy. We can also extract GST numbers, PAN, invoice dates, amounts, line items, and all other relevant fields.',
      },
      {
        q: 'Does TrulyInvoice handle different GST types (CGST/SGST/IGST)?',
        a: 'Absolutely. We handle all GST invoice types: B2B invoices (CGST/SGST), interstate invoices (IGST), and B2C invoices. Automatic tax calculation and validation.',
      },
      {
        q: 'Is TrulyInvoice GST compliant?',
        a: 'Yes, TrulyInvoice is fully compliant with Indian GST regulations. We support proper invoice format validation and maintain audit trails for 6 years as per GST rules.',
      },
      {
        q: 'Can I export data directly to GSTN portal?',
        a: 'Currently, we support export to Excel and accounting software. Direct GSTN portal integration is coming in Q1 2026.',
      },
    ],
  },
  {
    category: 'Bulk Processing',
    questions: [
      {
        q: 'Can I process multiple invoices at once?',
        a: 'Yes! You can upload and process up to 100 invoices in a single batch. Get all your invoices converted to Excel in minutes.',
      },
      {
        q: 'How fast is bulk processing?',
        a: 'Our system processes 10-20 invoices per minute. A batch of 100 invoices typically completes in 5-10 minutes.',
      },
      {
        q: 'What if bulk processing fails?',
        a: 'If any invoice fails in bulk processing, we provide detailed error logs. You can retry or contact support for assistance.',
      },
    ],
  },
  {
    category: 'Technical Support',
    questions: [
      {
        q: 'What customer support options are available?',
        a: 'We offer email support, live chat, and a comprehensive FAQ section. Premium plans include priority support.',
      },
      {
        q: 'Do you have a mobile app?',
        a: 'Currently, TrulyInvoice is web-based and works great on mobile browsers. Native iOS and Android apps are planned for 2026.',
      },
      {
        q: 'What file formats do you accept?',
        a: 'We accept PDF, JPG, PNG, JPEG, BMP, TIFF, and WebP formats. Maximum file size is 50MB per invoice.',
      },
      {
        q: 'Is TrulyInvoice available offline?',
        a: 'TrulyInvoice requires an internet connection as it uses cloud-based AI processing. We don\'t currently offer offline processing.',
      },
    ],
  },
  {
    category: 'Account & Billing',
    questions: [
      {
        q: 'How do I upgrade my plan?',
        a: 'Login to your dashboard, go to Plans section, and click Upgrade. Changes take effect immediately.',
      },
      {
        q: 'What payment methods do you accept?',
        a: 'We accept credit/debit cards (Visa, MasterCard, Rupay), net banking, UPI, and other Indian payment methods.',
      },
      {
        q: 'Do you offer invoices for billing?',
        a: 'Yes, detailed invoices are sent to your email at the start of each billing cycle. GST invoices are available for businesses registered under GST.',
      },
      {
        q: 'Can multiple users access one account?',
        a: 'Yes! You can add team members to your account. Each member gets individual login credentials and usage tracking.',
      },
    ],
  },
  {
    category: 'Getting Started',
    questions: [
      {
        q: 'How do I create a TrulyInvoice account?',
        a: 'Visit TrulyInvoice.xyz, click Sign Up, provide your email and password, verify your email, and you\'re ready to go!',
      },
      {
        q: 'What information do I need to sign up?',
        a: 'Just your email and a password. Optionally, provide company name and phone number to unlock additional features.',
      },
      {
        q: 'How do I upload my first invoice?',
        a: 'After login, click "Upload Invoice", select your file (PDF or image), and click "Convert". Our AI will extract the data in seconds.',
      },
      {
        q: 'Can I try TrulyInvoice for free first?',
        a: 'Yes! Our free plan includes 10 invoice conversions per month. No credit card required.',
      },
    ],
  },
];

export default function FAQPage() {
  // Generate FAQ Schema for Google Rich Results
  const faqSchema = {
    "@context": "https://schema.org",
    "@type": "FAQPage",
    "mainEntity": faqs.flatMap(section => 
      section.questions.map(item => ({
        "@type": "Question",
        "name": item.q,
        "acceptedAnswer": {
          "@type": "Answer",
          "text": item.a
        }
      }))
    )
  };

  return (
    <main>
      {/* FAQ Schema for Google Rich Results */}
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(faqSchema) }}
        suppressHydrationWarning
      />
      
      <div className="container mx-auto px-4 py-12">
        <h1 className="text-4xl font-bold mb-4">
          Frequently Asked Questions - TrulyInvoice Invoice Converter
        </h1>
        <p className="text-xl text-gray-600 mb-12">
          Find answers to common questions about invoice extraction, GST compliance, pricing, and more.
        </p>

        <div className="grid md:grid-cols-3 gap-6 mb-12">
          <div className="bg-blue-50 p-4 rounded">
            <h3 className="font-bold mb-2">📞 Can't find your answer?</h3>
            <p className="text-sm">Contact our support team at support@trulyinvoice.xyz or use live chat.</p>
          </div>
          <div className="bg-green-50 p-4 rounded">
            <h3 className="font-bold mb-2">🚀 Want to get started?</h3>
            <p className="text-sm">Sign up for free and get 10 invoice conversions. No credit card required!</p>
          </div>
          <div className="bg-purple-50 p-4 rounded">
            <h3 className="font-bold mb-2">💼 Enterprise needs?</h3>
            <p className="text-sm">Contact sales for custom pricing and dedicated support options.</p>
          </div>
        </div>

        <div className="space-y-12">
          {faqs.map((section) => (
            <section key={section.category}>
              <h2 className="text-2xl font-bold mb-6">{section.category}</h2>
              <div className="space-y-6">
                {section.questions.map((item, idx) => (
                  <div key={idx} className="border rounded-lg p-6 hover:shadow-md transition">
                    <h3 className="text-lg font-semibold mb-3 text-blue-600">
                      Q: {item.q}
                    </h3>
                    <p className="text-gray-700">
                      A: {item.a}
                    </p>
                  </div>
                ))}
              </div>
            </section>
          ))}
        </div>

        <section className="bg-gradient-to-r from-blue-600 to-blue-800 text-white p-12 rounded-lg mt-16 text-center">
          <h2 className="text-3xl font-bold mb-4">Still have questions?</h2>
          <p className="mb-6 text-lg">Our support team is here to help you succeed with TrulyInvoice.</p>
          <div className="flex justify-center gap-4 flex-wrap">
            <a href="/contact" className="bg-white text-blue-600 px-6 py-3 rounded font-semibold hover:bg-gray-100">
              Contact Us
            </a>
            <a href="/signup" className="border-2 border-white text-white px-6 py-3 rounded font-semibold hover:bg-blue-700">
              Start Free Trial
            </a>
          </div>
        </section>
      </div>
    </main>
  )
}
