import { Metadata } from 'next'
import Link from 'next/link'
import { CheckCircle2, Clock, TrendingUp, Calculator, Zap, Users, DollarSign } from 'lucide-react'

export const metadata: Metadata = {
  title: 'Save 50 Hours Per Month: Invoice Data Entry Automation for Small Business Owners (2025)',
  description: 'Automate invoice processing & save 8+ hours weekly. Free tool to convert invoices to Excel. See ROI calculator & real results from restaurant & retail owners.',
  keywords: [
    'invoice data entry automation',
    'automate invoice processing',
    'invoice management tool India',
    'free invoice to Excel converter',
    'save time invoice processing',
    'invoice automation for small business',
    'reduce invoice processing time',
    'invoice digitization India',
    'invoice automation ROI',
    'invoice processing software India',
  ],
  openGraph: {
    title: 'Save 50 Hours Per Month with Invoice Automation - Small Business Guide',
    description: 'Real case studies showing how restaurants, retailers & distributors save 8+ hours weekly on invoice processing.',
    images: ['/og-image-india.jpg'],
    type: 'article',
  },
  twitter: {
    card: 'summary_large_image',
    title: 'Save 50+ Hours Monthly on Invoice Processing',
    description: 'See how small businesses automate invoices and free up time for growth.',
  },
  alternates: {
    canonical: 'https://trulyinvoice.com/blog/save-50-hours-invoice-automation',
  },
  authors: [{ name: 'TrulyInvoice Team' }],
}

export default function BlogPost() {
  // Article Schema
  const articleSchema = {
    "@context": "https://schema.org",
    "@type": "Article",
    "headline": "Save 50 Hours Per Month: Invoice Data Entry Automation for Small Business Owners (2025)",
    "image": [
      "https://trulyinvoice.com/og-image-india.jpg"
    ],
    "datePublished": "2025-10-28T08:00:00+05:30",
    "dateModified": "2025-11-01T10:00:00+05:30",
    "author": {
      "@type": "Person",
      "name": "Amit Verma",
      "jobTitle": "Business Automation Expert",
      "description": "Business automation consultant with 12+ years of experience helping Indian small businesses implement time-saving technologies."
    },
    "publisher": {
      "@type": "Organization",
      "name": "TrulyInvoice",
      "logo": {
        "@type": "ImageObject",
        "url": "https://trulyinvoice.com/logo.png"
      }
    },
    "description": "Automate invoice processing & save 8+ hours weekly. Free tool to convert invoices to Excel. See ROI calculator & real results from restaurant & retail owners."
  }

  // FAQ Schema
  const faqSchema = {
    "@context": "https://schema.org",
    "@type": "FAQPage",
    "mainEntity": [
      {
        "@type": "Question",
        "name": "Is my invoice data safe? I'm worried about privacy.",
        "acceptedAnswer": {
          "@type": "Answer",
          "text": "Yes, your data is completely secure. TrulyInvoice uses bank-level encryption (same as your online banking). Your invoices are processed in real-time and never stored on our servers. We have a zero-retention policy—after extraction, your documents are permanently deleted. We're also ISO 27001 compliant and follow Indian data protection laws."
        }
      },
      {
        "@type": "Question",
        "name": "What if the AI makes mistakes? I can't afford errors.",
        "acceptedAnswer": {
          "@type": "Answer",
          "text": "AI accuracy is 98-99%—actually higher than human accuracy (92-95%). Plus, you get a quick review screen before exporting. The AI highlights low-confidence fields (rare) for manual verification. We also offer a money-back guarantee if accuracy is below 99%."
        }
      },
      {
        "@type": "Question",
        "name": "Is it hard to learn? I'm not tech-savvy.",
        "acceptedAnswer": {
          "@type": "Answer",
          "text": "If you can use WhatsApp, you can use TrulyInvoice. It's 3 steps: Upload → AI extracts → Download Excel. That's it. No technical knowledge needed. Plus, we have Hindi support and video tutorials in multiple Indian languages."
        }
      },
      {
        "@type": "Question",
        "name": "Can I try it before paying?",
        "acceptedAnswer": {
          "@type": "Answer",
          "text": "Yes! Free plan includes 10 invoices/month. No credit card required. Upload your toughest invoices and see the accuracy yourself. If it works, upgrade. If not, no cost to you."
        }
      },
      {
        "@type": "Question",
        "name": "Will this work with my accounting software (Tally, Zoho, etc.)?",
        "acceptedAnswer": {
          "@type": "Answer",
          "text": "Yes! We export to Excel, CSV, Tally XML, QuickBooks, Zoho Books. One-click export means your data goes straight into your existing workflow."
        }
      },
      {
        "@type": "Question",
        "name": "How much does invoice automation cost for small businesses?",
        "acceptedAnswer": {
          "@type": "Answer",
          "text": "Plans start at ₹299/month (50 invoices) or ₹599/month (100 invoices). For most small businesses processing 80-120 invoices monthly, the ROI is 10-15x: you save ₹6,000-8,000 in labor costs while spending ₹599. Plus, you get 10 free invoices/month to test without risk."
        }
      },
      {
        "@type": "Question",
        "name": "How long does it take to set up invoice automation?",
        "acceptedAnswer": {
          "@type": "Answer",
          "text": "Setup takes 5 minutes: 1) Sign up (30 seconds), 2) Upload a sample invoice (30 seconds), 3) Verify extracted data (1 minute), 4) Configure export format (2 minutes), 5) Start processing (instant). No technical setup, IT support, or training required."
        }
      },
      {
        "@type": "Question",
        "name": "What ROI can I expect from invoice automation?",
        "acceptedAnswer": {
          "@type": "Answer",
          "text": "Typical ROI is 10-15x investment within the first month. Example: If you process 100 invoices/month manually (25 hours at ₹300/hour labor cost = ₹7,500), automation costs ₹599/month and saves 24 hours, resulting in ₹7,200 monthly savings (12x ROI). Most businesses recoup costs in the first week."
        }
      },
      {
        "@type": "Question",
        "name": "Can invoice automation handle handwritten invoices?",
        "acceptedAnswer": {
          "@type": "Answer",
          "text": "Yes, with 85-90% accuracy for clear handwriting. The AI is trained on handwritten Indian invoices and can extract data from legible handwritten documents, including WhatsApp photos. For best results, ensure handwriting is clear and images are well-lit. Typed/printed invoices achieve 98-99% accuracy."
        }
      },
      {
        "@type": "Question",
        "name": "Will I need to hire someone to manage the automation?",
        "acceptedAnswer": {
          "@type": "Answer",
          "text": "No. Invoice automation actually reduces your staffing needs—most small businesses go from 2 people doing data entry to 1 person doing quick reviews (10-15 minutes daily). The AI handles 95% of the work automatically. Your existing staff can manage it without additional training or technical expertise."
        }
      }
    ]
  }

  return (
    <>
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(articleSchema) }}
      />
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(faqSchema) }}
      />
      <main className="min-h-screen bg-gradient-to-br from-blue-50 to-purple-50 dark:from-gray-900 dark:to-gray-800">
        {/* Breadcrumb */}
        <div className="bg-white dark:bg-gray-800 border-b border-gray-200 dark:border-gray-700">
          <div className="container mx-auto px-4 py-3">
            <nav className="text-sm">
              <Link href="/" className="text-blue-600 hover:underline">Home</Link>
              {' > '}
              <Link href="/blog" className="text-blue-600 hover:underline">Blog</Link>
              {' > '}
              <span className="text-gray-600 dark:text-gray-400">Save 50 Hours Per Month</span>
            </nav>
          </div>
        </div>

      <article className="container mx-auto px-4 py-12 max-w-4xl">
        {/* Hero Section */}
        <header className="mb-12">
          <div className="flex items-center gap-2 text-sm text-gray-600 dark:text-gray-400 mb-4">
            <time dateTime="2025-10-28">📅 Published: October 28, 2025</time>
            <span>•</span>
            <time dateTime="2025-11-01">🔄 Updated: November 1, 2025</time>
            <span>•</span>
            <span>10 min read</span>
            <span>•</span>
            <span className="text-blue-600 font-semibold">Small Business Automation</span>
          </div>

          <h1 className="text-4xl md:text-5xl font-bold text-gray-900 dark:text-white mb-6 leading-tight">
            Save 50 Hours Per Month: Invoice Data Entry Automation for Small Business Owners
          </h1>

          <p className="text-xl text-gray-600 dark:text-gray-300 mb-8 leading-relaxed">
            Are you or your staff spending 8-12 hours every week manually typing vendor invoices into Excel? 
            Discover how restaurants, retailers, and distributors are using invoice automation to save 50+ hours monthly—time you could spend growing your business instead.
          </p>

          <div className="bg-gradient-to-r from-green-600 to-blue-600 text-white rounded-lg p-6">
            <div className="flex items-start gap-4">
              <Clock className="flex-shrink-0 mt-1" size={40} />
              <div>
                <p className="text-lg font-bold mb-2">💡 Real Success Story:</p>
                <p className="text-white/90">
                  <strong>Sneha Kulkarni</strong> (restaurant owner, Pune) was spending <strong>12 hours/week</strong> processing vendor invoices for her 3 restaurants. 
                  After automating with TrulyInvoice, she now spends <strong>30 minutes/week</strong>. 
                  That's <strong>46 hours saved every month</strong>—time she now uses to open a 4th location.
                </p>
              </div>
            </div>
          </div>
        </header>

        {/* Table of Contents */}
        <nav className="bg-white dark:bg-gray-800 rounded-lg shadow-sm p-6 mb-12 border border-gray-200 dark:border-gray-700">
          <h2 className="text-xl font-bold text-gray-900 dark:text-white mb-4">📋 Table of Contents</h2>
          <ul className="space-y-2">
            <li><a href="#nightmare" className="text-blue-600 hover:underline">1. The Invoice Processing Nightmare</a></li>
            <li><a href="#true-cost" className="text-blue-600 hover:underline">2. The True Cost of Manual Invoice Processing</a></li>
            <li><a href="#automation-methods" className="text-blue-600 hover:underline">3. Invoice Automation Methods Compared</a></li>
            <li><a href="#how-to-choose" className="text-blue-600 hover:underline">4. How to Choose the Right Solution</a></li>
            <li><a href="#setup-guide" className="text-blue-600 hover:underline">5. Step-by-Step Setup Guide (5 Minutes)</a></li>
            <li><a href="#time-savings" className="text-blue-600 hover:underline">6. Time Savings Calculator by Invoice Volume</a></li>
            <li><a href="#case-study" className="text-blue-600 hover:underline">7. Case Study: Restaurant Owner's Journey</a></li>
            <li><a href="#faq" className="text-blue-600 hover:underline">8. Frequently Asked Questions (12 FAQs)</a></li>
          </ul>
        </nav>

        {/* Section 1: The Nightmare */}
        <section id="nightmare" className="mb-12 scroll-mt-20">
          <h2 className="text-3xl font-bold text-gray-900 dark:text-white mb-6 flex items-center gap-3">
            <TrendingUp className="text-red-500" size={32} />
            The Small Business Owner's Invoice Processing Nightmare
          </h2>

          <div className="prose prose-lg dark:prose-invert max-w-none">
            <p className="text-gray-700 dark:text-gray-300 mb-6">
              You didn't start your business to spend evenings typing invoice data into spreadsheets. 
              But here you are, every week:
            </p>

            <div className="bg-red-50 dark:bg-red-900/20 border-l-4 border-red-500 p-6 rounded-r-lg mb-6">
              <h3 className="font-bold text-red-800 dark:text-red-200 mb-3 text-lg">
                📉 The Weekly Invoice Hell Cycle:
              </h3>
              <ul className="space-y-3 text-gray-800 dark:text-gray-200">
                <li className="flex items-start gap-3">
                  <span className="font-bold text-red-600">Monday PM:</span>
                  <span>50+ vendor invoices arrive (email, WhatsApp, delivery person hands them over)</span>
                </li>
                <li className="flex items-start gap-3">
                  <span className="font-bold text-red-600">Tuesday-Thursday:</span>
                  <span>Staff member (or you) spends 2-3 hours/day entering data into Excel/accounting software</span>
                </li>
                <li className="flex items-start gap-3">
                  <span className="font-bold text-red-600">Friday:</span>
                  <span>Discover 5-10 errors—wrong amounts, missed invoices, duplicate entries</span>
                </li>
                <li className="flex items-start gap-3">
                  <span className="font-bold text-red-600">Weekend:</span>
                  <span>You personally spend Saturday morning fixing the mess</span>
                </li>
                <li className="flex items-start gap-3">
                  <span className="font-bold text-red-600">Repeat:</span>
                  <span>Every. Single. Week. For years.</span>
                </li>
              </ul>
            </div>

            <div className="grid md:grid-cols-3 gap-6 mb-8">
              <div className="bg-white dark:bg-gray-800 rounded-lg p-6 border-l-4 border-red-500">
                <div className="text-3xl font-bold text-red-600 mb-2">12hrs</div>
                <p className="text-gray-700 dark:text-gray-300 text-sm">
                  <strong>Average time</strong> small businesses spend on invoice data entry per week
                </p>
              </div>
              <div className="bg-white dark:bg-gray-800 rounded-lg p-6 border-l-4 border-orange-500">
                <div className="text-3xl font-bold text-orange-600 mb-2">₹15k</div>
                <p className="text-gray-700 dark:text-gray-300 text-sm">
                  <strong>Monthly cost</strong> of hiring someone part-time just for invoice entry
                </p>
              </div>
              <div className="bg-white dark:bg-gray-800 rounded-lg p-6 border-l-4 border-yellow-500">
                <div className="text-3xl font-bold text-yellow-600 mb-2">5-8%</div>
                <p className="text-gray-700 dark:text-gray-300 text-sm">
                  <strong>Error rate</strong> with manual entry leading to payment disputes & reconciliation headaches
                </p>
              </div>
            </div>

            <div className="bg-gray-100 dark:bg-gray-800 rounded-lg p-6 mb-6">
              <h3 className="font-bold text-gray-900 dark:text-white mb-3">📊 Common Scenarios by Industry:</h3>
              <div className="space-y-4">
                <div>
                  <p className="font-semibold text-gray-900 dark:text-white mb-1">🍽️ Restaurant Owners:</p>
                  <p className="text-sm text-gray-700 dark:text-gray-300">
                    50-100 vendor invoices/week (vegetables, meat, dairy, packaging). Thin margins mean every pricing error hurts. 
                    Staff turnover = constant retraining on invoice processing.
                  </p>
                </div>
                <div>
                  <p className="font-semibold text-gray-900 dark:text-white mb-1">🏪 Retail Shop Owners:</p>
                  <p className="text-sm text-gray-700 dark:text-gray-300">
                    30-80 supplier invoices/week (inventory replenishment). Need accurate records for GST filing. 
                    Can't afford full-time accountant but need professional bookkeeping.
                  </p>
                </div>
                <div>
                  <p className="font-semibold text-gray-900 dark:text-white mb-1">📦 Distributors/Wholesalers:</p>
                  <p className="text-sm text-gray-700 dark:text-gray-300">
                    100-200 invoices/week (high volume, low margin). Speed matters. Manual processing causes payment delays and vendor relationship issues.
                  </p>
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* Section 2: True Cost */}
        <section id="true-cost" className="mb-12 scroll-mt-20">
          <h2 className="text-3xl font-bold text-gray-900 dark:text-white mb-6 flex items-center gap-3">
            <DollarSign className="text-green-600" size={32} />
            The True Cost of Manual Invoice Processing (Hidden Numbers)
          </h2>

          <div className="prose prose-lg dark:prose-invert max-w-none">
            <p className="text-gray-700 dark:text-gray-300 mb-6">
              Most small business owners don't realize how much manual invoice processing actually costs. 
              Let's break down the <strong>hidden expenses</strong>:
            </p>

            <div className="bg-white dark:bg-gray-800 rounded-lg overflow-hidden border border-gray-200 dark:border-gray-700 mb-8">
              <table className="w-full">
                <thead className="bg-gray-100 dark:bg-gray-700">
                  <tr>
                    <th className="px-6 py-4 text-left font-bold text-gray-900 dark:text-white">Cost Category</th>
                    <th className="px-6 py-4 text-left font-bold text-gray-900 dark:text-white">Monthly Impact</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-gray-200 dark:divide-gray-700">
                  <tr>
                    <td className="px-6 py-4">
                      <p className="font-semibold text-gray-900 dark:text-white">Direct Labor Cost</p>
                      <p className="text-sm text-gray-600 dark:text-gray-400">Staff time @ ₹200/hour × 48 hours/month</p>
                    </td>
                    <td className="px-6 py-4 text-gray-700 dark:text-gray-300">₹9,600</td>
                  </tr>
                  <tr className="bg-gray-50 dark:bg-gray-750">
                    <td className="px-6 py-4">
                      <p className="font-semibold text-gray-900 dark:text-white">Error Correction Time</p>
                      <p className="text-sm text-gray-600 dark:text-gray-400">Rework for 5-10 invoices/month @ 30 min each</p>
                    </td>
                    <td className="px-6 py-4 text-gray-700 dark:text-gray-300">₹1,500</td>
                  </tr>
                  <tr>
                    <td className="px-6 py-4">
                      <p className="font-semibold text-gray-900 dark:text-white">Late Payment Penalties</p>
                      <p className="text-sm text-gray-600 dark:text-gray-400">1-2 invoices paid late due to processing delays</p>
                    </td>
                    <td className="px-6 py-4 text-gray-700 dark:text-gray-300">₹2,000</td>
                  </tr>
                  <tr className="bg-gray-50 dark:bg-gray-750">
                    <td className="px-6 py-4">
                      <p className="font-semibold text-gray-900 dark:text-white">Lost Vendor Discounts</p>
                      <p className="text-sm text-gray-600 dark:text-gray-400">2% early payment discount missed on 20% of invoices</p>
                    </td>
                    <td className="px-6 py-4 text-gray-700 dark:text-gray-300">₹3,000</td>
                  </tr>
                  <tr>
                    <td className="px-6 py-4">
                      <p className="font-semibold text-gray-900 dark:text-white">Owner's Time Opportunity Cost</p>
                      <p className="text-sm text-gray-600 dark:text-gray-400">6 hours/month you spend fixing errors @ ₹1,000/hr value</p>
                    </td>
                    <td className="px-6 py-4 text-gray-700 dark:text-gray-300">₹6,000</td>
                  </tr>
                  <tr className="bg-gray-50 dark:bg-gray-750">
                    <td className="px-6 py-4">
                      <p className="font-semibold text-gray-900 dark:text-white">GST Filing Delays/Errors</p>
                      <p className="text-sm text-gray-600 dark:text-gray-400">Occasional late fees or incorrect ITC claims</p>
                    </td>
                    <td className="px-6 py-4 text-gray-700 dark:text-gray-300">₹1,500</td>
                  </tr>
                  <tr className="bg-red-50 dark:bg-red-900/20">
                    <td className="px-6 py-4 font-bold text-gray-900 dark:text-white text-lg">
                      TOTAL MONTHLY COST
                    </td>
                    <td className="px-6 py-4 font-bold text-red-600 text-xl">
                      ₹23,600
                    </td>
                  </tr>
                  <tr className="bg-red-100 dark:bg-red-900/30">
                    <td className="px-6 py-4 font-bold text-gray-900 dark:text-white">
                      ANNUAL COST
                    </td>
                    <td className="px-6 py-4 font-bold text-red-600 text-2xl">
                      ₹2,83,200
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>

            <div className="bg-yellow-50 dark:bg-yellow-900/20 border-l-4 border-yellow-500 p-6 rounded-r-lg mb-6">
              <p className="text-gray-800 dark:text-gray-200 font-semibold mb-2">
                💰 The Shocking Reality:
              </p>
              <p className="text-gray-800 dark:text-gray-200">
                Most small businesses spend <strong>₹2.5-3 lakh per year</strong> on manual invoice processing without realizing it. 
                That's equivalent to hiring <strong>2 part-time employees</strong> or <strong>a month's rent</strong> for many businesses.
              </p>
            </div>

            <div className="bg-green-50 dark:bg-green-900/20 border-l-4 border-green-500 p-6 rounded-r-lg">
              <h3 className="font-bold text-green-800 dark:text-green-200 mb-3 text-lg">
                ✅ With Automation (₹299-799/month):
              </h3>
              <ul className="space-y-2 text-gray-800 dark:text-gray-200">
                <li>• <strong>Time reduced:</strong> 48 hours → 2-3 hours/month (94% reduction)</li>
                <li>• <strong>Cost reduced:</strong> ₹23,600 → ₹1,500/month (94% savings)</li>
                <li>• <strong>Annual savings:</strong> ₹2.7 lakh</li>
                <li>• <strong>ROI:</strong> 2,800% (you save ₹28 for every ₹1 spent)</li>
              </ul>
            </div>
          </div>
        </section>

        {/* ROI Calculator Section */}
        <section id="time-savings" className="mb-12 scroll-mt-20">
          <h2 className="text-3xl font-bold text-gray-900 dark:text-white mb-6 flex items-center gap-3">
            <Calculator className="text-purple-600" size={32} />
            Time Savings Calculator by Invoice Volume
          </h2>

          <div className="prose prose-lg dark:prose-invert max-w-none">
            <p className="text-gray-700 dark:text-gray-300 mb-6">
              Use this table to calculate <strong>your specific time savings</strong> based on how many invoices you process:
            </p>

            <div className="overflow-x-auto mb-8">
              <table className="w-full bg-white dark:bg-gray-800 rounded-lg overflow-hidden border border-gray-200 dark:border-gray-700">
                <thead className="bg-gradient-to-r from-blue-600 to-purple-600 text-white">
                  <tr>
                    <th className="px-6 py-4 text-left">Invoices/Month</th>
                    <th className="px-6 py-4 text-left">Manual Time</th>
                    <th className="px-6 py-4 text-left">Automated Time</th>
                    <th className="px-6 py-4 text-left">Hours Saved</th>
                    <th className="px-6 py-4 text-left">Money Saved*</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-gray-200 dark:divide-gray-700">
                  <tr>
                    <td className="px-6 py-4 font-semibold text-gray-900 dark:text-white">50</td>
                    <td className="px-6 py-4 text-gray-700 dark:text-gray-300">5 hours</td>
                    <td className="px-6 py-4 text-gray-700 dark:text-gray-300">30 min</td>
                    <td className="px-6 py-4 font-bold text-green-600">4.5 hours</td>
                    <td className="px-6 py-4 font-bold text-green-600">₹900</td>
                  </tr>
                  <tr className="bg-gray-50 dark:bg-gray-750">
                    <td className="px-6 py-4 font-semibold text-gray-900 dark:text-white">100</td>
                    <td className="px-6 py-4 text-gray-700 dark:text-gray-300">10 hours</td>
                    <td className="px-6 py-4 text-gray-700 dark:text-gray-300">1 hour</td>
                    <td className="px-6 py-4 font-bold text-green-600">9 hours</td>
                    <td className="px-6 py-4 font-bold text-green-600">₹1,800</td>
                  </tr>
                  <tr>
                    <td className="px-6 py-4 font-semibold text-gray-900 dark:text-white">200</td>
                    <td className="px-6 py-4 text-gray-700 dark:text-gray-300">20 hours</td>
                    <td className="px-6 py-4 text-gray-700 dark:text-gray-300">2 hours</td>
                    <td className="px-6 py-4 font-bold text-green-600">18 hours</td>
                    <td className="px-6 py-4 font-bold text-green-600">₹3,600</td>
                  </tr>
                  <tr className="bg-gray-50 dark:bg-gray-750">
                    <td className="px-6 py-4 font-semibold text-gray-900 dark:text-white">300</td>
                    <td className="px-6 py-4 text-gray-700 dark:text-gray-300">30 hours</td>
                    <td className="px-6 py-4 text-gray-700 dark:text-gray-300">3 hours</td>
                    <td className="px-6 py-4 font-bold text-green-600">27 hours</td>
                    <td className="px-6 py-4 font-bold text-green-600">₹5,400</td>
                  </tr>
                  <tr>
                    <td className="px-6 py-4 font-semibold text-gray-900 dark:text-white">500</td>
                    <td className="px-6 py-4 text-gray-700 dark:text-gray-300">50 hours</td>
                    <td className="px-6 py-4 text-gray-700 dark:text-gray-300">5 hours</td>
                    <td className="px-6 py-4 font-bold text-green-600">45 hours</td>
                    <td className="px-6 py-4 font-bold text-green-600">₹9,000</td>
                  </tr>
                </tbody>
              </table>
              <p className="text-xs text-gray-600 dark:text-gray-400 mt-2">
                *Based on ₹200/hour labor cost. Your actual savings may be higher if you value your time at owner/manager rates.
              </p>
            </div>

            <div className="bg-purple-50 dark:bg-purple-900/20 border-l-4 border-purple-600 p-6 rounded-r-lg">
              <p className="text-gray-800 dark:text-gray-200 text-lg font-semibold mb-2">
                🎯 Quick ROI Calculation:
              </p>
              <p className="text-gray-800 dark:text-gray-200 mb-3">
                If you process <strong>200 invoices/month</strong> (typical for mid-sized restaurants/retailers):
              </p>
              <ul className="space-y-1 text-gray-800 dark:text-gray-200">
                <li>• Software cost: <strong>₹799/month</strong> (unlimited plan)</li>
                <li>• Time saved: <strong>18 hours/month</strong></li>
                <li>• Value of time saved: <strong>₹3,600/month</strong> (at ₹200/hr)</li>
                <li>• <strong>Net savings: ₹2,800/month = ₹33,600/year</strong></li>
              </ul>
              <p className="text-purple-800 dark:text-purple-200 font-bold mt-3">
                Payback period: Less than 1 week!
              </p>
            </div>
          </div>
        </section>

        {/* Case Study Section */}
        <section id="case-study" className="mb-12 scroll-mt-20">
          <div className="bg-gradient-to-r from-blue-100 to-purple-100 dark:from-blue-900/30 dark:to-purple-900/30 rounded-lg p-8 border-2 border-blue-300 dark:border-blue-700">
            <h2 className="text-3xl font-bold text-gray-900 dark:text-white mb-6 flex items-center gap-3">
              <Users className="text-blue-600" size={32} />
              Case Study: How Sneha Freed Up 12 Hours/Week
            </h2>

            <div className="space-y-6">
              <div className="bg-white dark:bg-gray-800 rounded-lg p-6">
                <h3 className="font-bold text-gray-900 dark:text-white mb-3 text-xl">
                  📋 Business Profile:
                </h3>
                <ul className="space-y-2 text-gray-700 dark:text-gray-300">
                  <li>• <strong>Name:</strong> Sneha Kulkarni</li>
                  <li>• <strong>Business:</strong> 3 quick-service restaurants in Pune</li>
                  <li>• <strong>Volume:</strong> 180-220 vendor invoices/month (vegetables, meat, dairy, packaging, utilities)</li>
                  <li>• <strong>Team:</strong> 1 owner, 15 staff (no dedicated accountant)</li>
                </ul>
              </div>

              <div className="grid md:grid-cols-2 gap-6">
                <div className="bg-red-50 dark:bg-red-900/20 rounded-lg p-6 border-l-4 border-red-500">
                  <h3 className="font-bold text-red-800 dark:text-red-200 mb-3">❌ Before Automation:</h3>
                  <ul className="space-y-2 text-sm text-gray-700 dark:text-gray-300">
                    <li>• <strong>12 hours/week</strong> entering invoice data</li>
                    <li>• Saturday mornings spent reconciling</li>
                    <li>• 5-8 errors per month causing vendor disputes</li>
                    <li>• Missed 2 GST filing deadlines (₹1,200 late fees)</li>
                    <li>• Stress, burnout, no work-life balance</li>
                  </ul>
                </div>

                <div className="bg-green-50 dark:bg-green-900/20 rounded-lg p-6 border-l-4 border-green-500">
                  <h3 className="font-bold text-green-800 dark:text-green-200 mb-3">✅ After Automation:</h3>
                  <ul className="space-y-2 text-sm text-gray-700 dark:text-gray-300">
                    <li>• <strong>30 minutes/week</strong> reviewing extracted data</li>
                    <li>• Saturdays free for family time</li>
                    <li>• Error rate dropped to &lt;1%</li>
                    <li>• Never missed a filing deadline again</li>
                    <li>• Used saved time to open 4th restaurant!</li>
                  </ul>
                </div>
              </div>

              <div className="bg-blue-50 dark:bg-blue-900/20 rounded-lg p-6">
                <h3 className="font-bold text-blue-900 dark:text-blue-200 mb-3 text-xl">
                  💬 In Her Own Words:
                </h3>
                <p className="text-gray-800 dark:text-gray-200 italic mb-3">
                  "I started using TrulyInvoice in March 2024. Within the first week, I was shocked. 
                  What took me 3 hours on Monday was done in 10 minutes. I thought it was a fluke. 
                  But month after month, it kept working perfectly."
                </p>
                <p className="text-gray-800 dark:text-gray-200 italic mb-3">
                  "The ROI is insane. I pay ₹799/month and save at least ₹5,000 in my own time + ₹3,000 in staff time. 
                  More importantly, I got my weekends back. I can actually spend time with my kids now."
                </p>
                <p className="text-gray-800 dark:text-gray-200 italic font-semibold">
                  "In September 2024, I opened my 4th restaurant. That wouldn't have been possible without automation. 
                  I simply didn't have the time before. Now I do."
                </p>
                <p className="text-gray-600 dark:text-gray-400 text-sm mt-4">
                  — Sneha Kulkarni, Restaurant Owner, Pune
                </p>
              </div>

              <div className="bg-gradient-to-r from-green-600 to-blue-600 text-white rounded-lg p-6">
                <h3 className="font-bold mb-3 text-xl">🎯 Key Takeaways:</h3>
                <ul className="space-y-2">
                  <li className="flex items-start gap-2">
                    <CheckCircle2 className="flex-shrink-0 mt-1" size={20} />
                    <span><strong>Time savings:</strong> 46 hours/month = 552 hours/year (equivalent of 3.5 months of full-time work!)</span>
                  </li>
                  <li className="flex items-start gap-2">
                    <CheckCircle2 className="flex-shrink-0 mt-1" size={20} />
                    <span><strong>Money savings:</strong> ₹8,000+/month = ₹96,000/year</span>
                  </li>
                  <li className="flex items-start gap-2">
                    <CheckCircle2 className="flex-shrink-0 mt-1" size={20} />
                    <span><strong>Business growth:</strong> Freed up time to open 4th location (20% revenue increase)</span>
                  </li>
                  <li className="flex items-start gap-2">
                    <CheckCircle2 className="flex-shrink-0 mt-1" size={20} />
                    <span><strong>Quality of life:</strong> Weekends with family, reduced stress</span>
                  </li>
                </ul>
              </div>
            </div>
          </div>
        </section>

        {/* FAQ Section */}
        <section id="faq" className="mb-12 scroll-mt-20">
          <h2 className="text-3xl font-bold text-gray-900 dark:text-white mb-6">
            ❓ Frequently Asked Questions (12 FAQs)
          </h2>

          <div className="space-y-6">
            {/* FAQ 1 */}
            <div className="bg-white dark:bg-gray-800 rounded-lg p-6 border border-gray-200 dark:border-gray-700">
              <h3 className="text-xl font-bold text-gray-900 dark:text-white mb-3">
                1. Is my invoice data safe? I'm worried about privacy.
              </h3>
              <p className="text-gray-700 dark:text-gray-300 leading-relaxed mb-4">
                <strong>Yes, your data is completely secure.</strong> TrulyInvoice uses <strong>bank-level encryption</strong> (same as your online banking). 
                Your invoices are processed in real-time and <strong>never stored</strong> on our servers.
              </p>
              <p className="text-gray-700 dark:text-gray-300 leading-relaxed">
                We have a <strong>zero-retention policy</strong>—after extraction, your documents are permanently deleted. 
                We're also <strong>ISO 27001 compliant</strong> and follow Indian data protection laws. Your vendor information stays completely private.
              </p>
            </div>

            {/* FAQ 2 */}
            <div className="bg-white dark:bg-gray-800 rounded-lg p-6 border border-gray-200 dark:border-gray-700">
              <h3 className="text-xl font-bold text-gray-900 dark:text-white mb-3">
                2. What if the AI makes mistakes? I can't afford errors.
              </h3>
              <p className="text-gray-700 dark:text-gray-300 leading-relaxed mb-4">
                AI accuracy is <strong>98-99%</strong>—actually higher than human accuracy (92-95%). 
                Plus, you get a <strong>quick review screen before exporting</strong> where you can verify all data.
              </p>
              <p className="text-gray-700 dark:text-gray-300 leading-relaxed">
                The AI highlights low-confidence fields (rare) in yellow for manual verification. We also offer a <strong>money-back guarantee</strong> if accuracy is below 99%. 
                Most small businesses find fewer errors with automation than with manual data entry.
              </p>
            </div>

            {/* FAQ 3 */}
            <div className="bg-white dark:bg-gray-800 rounded-lg p-6 border border-gray-200 dark:border-gray-700">
              <h3 className="text-xl font-bold text-gray-900 dark:text-white mb-3">
                3. Is it hard to learn? I'm not tech-savvy.
              </h3>
              <p className="text-gray-700 dark:text-gray-300 leading-relaxed mb-4">
                <strong>If you can use WhatsApp, you can use TrulyInvoice.</strong> It's 3 simple steps:
              </p>
              <ol className="list-decimal list-inside text-gray-700 dark:text-gray-300 mb-4 space-y-2">
                <li><strong>Upload</strong> your invoice (drag & drop or email forward)</li>
                <li><strong>AI extracts</strong> data automatically (5 seconds)</li>
                <li><strong>Download Excel</strong> with one click</li>
              </ol>
              <p className="text-gray-700 dark:text-gray-300 leading-relaxed">
                That's it. No technical knowledge needed. Plus, we have <strong>Hindi support</strong> and <strong>video tutorials</strong> in multiple Indian languages (Hindi, Tamil, Telugu, Marathi).
              </p>
            </div>

            {/* FAQ 4 */}
            <div className="bg-white dark:bg-gray-800 rounded-lg p-6 border border-gray-200 dark:border-gray-700">
              <h3 className="text-xl font-bold text-gray-900 dark:text-white mb-3">
                4. What types of invoices does it work with?
              </h3>
              <p className="text-gray-700 dark:text-gray-300 leading-relaxed mb-4">
                <strong>All types!</strong> The AI is trained on 50,000+ Indian invoices:
              </p>
              <ul className="list-disc list-inside text-gray-700 dark:text-gray-300 mb-4 space-y-2">
                <li>PDF invoices (most common)</li>
                <li>Scanned images (JPG, PNG)</li>
                <li><strong>WhatsApp photos</strong> (even blurry ones)</li>
                <li>Handwritten invoices (85-90% accuracy)</li>
                <li>Different vendor formats (all supported)</li>
                <li>Multi-page invoices (automatically detected)</li>
              </ul>
              <p className="text-gray-700 dark:text-gray-300 leading-relaxed">
                Whether your vendors send PDFs by email or photos on WhatsApp, TrulyInvoice handles them all.
              </p>
            </div>

            {/* FAQ 5 */}
            <div className="bg-white dark:bg-gray-800 rounded-lg p-6 border border-gray-200 dark:border-gray-700">
              <h3 className="text-xl font-bold text-gray-900 dark:text-white mb-3">
                5. Can I try it before paying?
              </h3>
              <p className="text-gray-700 dark:text-gray-300 leading-relaxed mb-4">
                <strong>Yes!</strong> Free plan includes <strong>10 invoices/month</strong>—no credit card required.
              </p>
              <p className="text-gray-700 dark:text-gray-300 leading-relaxed">
                <Link href="/signup" className="text-blue-600 hover:underline">Upload your toughest invoices</Link> and see the accuracy yourself. Test with your actual vendor formats, not generic demos. 
                If it works (it will), upgrade to a paid plan. If not, no cost to you. <Link href="/pricing" className="text-blue-600 hover:underline">See pricing plans here</Link>.
              </p>
            </div>

            {/* FAQ 6 */}
            <div className="bg-white dark:bg-gray-800 rounded-lg p-6 border border-gray-200 dark:border-gray-700">
              <h3 className="text-xl font-bold text-gray-900 dark:text-white mb-3">
                6. Will this work with my accounting software (Tally, Zoho, etc.)?
              </h3>
              <p className="text-gray-700 dark:text-gray-300 leading-relaxed mb-4">
                <strong>Yes!</strong> We export to all major Indian accounting software:
              </p>
              <ul className="list-disc list-inside text-gray-700 dark:text-gray-300 mb-4 space-y-2">
                <li><Link href="/blog/export-invoices-to-tally-erp9" className="text-blue-600 hover:underline">Tally ERP 9 & Tally Prime</Link> (XML format)</li>
                <li><Link href="/blog/quickbooks-india-integration-guide" className="text-blue-600 hover:underline">QuickBooks India</Link> (CSV import)</li>
                <li><Link href="/blog/zoho-books-csv-export-tutorial" className="text-blue-600 hover:underline">Zoho Books</Link> (CSV import)</li>
                <li>Busy Accounting Software</li>
                <li>Excel & CSV (universal)</li>
              </ul>
              <p className="text-gray-700 dark:text-gray-300 leading-relaxed">
                One-click export means your data goes straight into your existing workflow without manual reformatting.
              </p>
            </div>

            {/* FAQ 7 */}
            <div className="bg-white dark:bg-gray-800 rounded-lg p-6 border border-gray-200 dark:border-gray-700">
              <h3 className="text-xl font-bold text-gray-900 dark:text-white mb-3">
                7. How much does invoice automation cost for small businesses?
              </h3>
              <p className="text-gray-700 dark:text-gray-300 leading-relaxed mb-4">
                Plans start at <strong>₹299/month</strong> (50 invoices) or <strong>₹599/month</strong> (100 invoices).
              </p>
              <p className="text-gray-700 dark:text-gray-300 leading-relaxed mb-4">
                <strong>ROI calculation:</strong> For most small businesses processing 80-120 invoices monthly:
              </p>
              <ul className="list-disc list-inside text-gray-700 dark:text-gray-300 mb-4 space-y-2">
                <li><strong>Manual cost:</strong> 25 hours × ₹300/hour = ₹7,500/month</li>
                <li><strong>Automation cost:</strong> ₹599/month (saves 24 hours)</li>
                <li><strong>Monthly savings:</strong> ₹6,900 (12x ROI)</li>
              </ul>
              <p className="text-gray-700 dark:text-gray-300 leading-relaxed">
                Plus, you get 10 free invoices/month to test without risk. Most businesses recoup costs in the first week.
              </p>
            </div>

            {/* FAQ 8 */}
            <div className="bg-white dark:bg-gray-800 rounded-lg p-6 border border-gray-200 dark:border-gray-700">
              <h3 className="text-xl font-bold text-gray-900 dark:text-white mb-3">
                8. How long does it take to set up invoice automation?
              </h3>
              <p className="text-gray-700 dark:text-gray-300 leading-relaxed mb-4">
                <strong>Setup takes 5 minutes:</strong>
              </p>
              <ol className="list-decimal list-inside text-gray-700 dark:text-gray-300 mb-4 space-y-2">
                <li>Sign up (30 seconds)</li>
                <li>Upload a sample invoice (30 seconds)</li>
                <li>Verify extracted data (1 minute)</li>
                <li>Configure export format for your accounting software (2 minutes)</li>
                <li>Start processing (instant)</li>
              </ol>
              <p className="text-gray-700 dark:text-gray-300 leading-relaxed">
                No technical setup, no IT support needed, no training sessions. If you can attach a file to an email, you can set up TrulyInvoice.
              </p>
            </div>

            {/* FAQ 9 */}
            <div className="bg-white dark:bg-gray-800 rounded-lg p-6 border border-gray-200 dark:border-gray-700">
              <h3 className="text-xl font-bold text-gray-900 dark:text-white mb-3">
                9. What ROI can I expect from invoice automation?
              </h3>
              <p className="text-gray-700 dark:text-gray-300 leading-relaxed mb-4">
                Typical ROI is <strong>10-15x your investment</strong> within the first month.
              </p>
              <p className="text-gray-700 dark:text-gray-300 leading-relaxed mb-4">
                <strong>Real example:</strong> If you process <strong>100 invoices/month manually</strong>:
              </p>
              <ul className="list-disc list-inside text-gray-700 dark:text-gray-300 mb-4 space-y-2">
                <li>Manual time: 25 hours at ₹300/hour labor cost = <strong>₹7,500</strong></li>
                <li>Automation cost: <strong>₹599/month</strong></li>
                <li>Time saved: 24 hours (96% reduction)</li>
                <li>Monthly savings: <strong>₹6,900</strong> (12x ROI)</li>
                <li>Annual savings: <strong>₹82,800</strong></li>
              </ul>
              <p className="text-gray-700 dark:text-gray-300 leading-relaxed">
                Most businesses recoup their investment <strong>in the first week</strong>. Plus, staff can focus on higher-value tasks like vendor negotiations or customer service.
              </p>
            </div>

            {/* FAQ 10 */}
            <div className="bg-white dark:bg-gray-800 rounded-lg p-6 border border-gray-200 dark:border-gray-700">
              <h3 className="text-xl font-bold text-gray-900 dark:text-white mb-3">
                10. Can invoice automation handle handwritten invoices?
              </h3>
              <p className="text-gray-700 dark:text-gray-300 leading-relaxed mb-4">
                <strong>Yes, with 85-90% accuracy</strong> for clear handwriting.
              </p>
              <p className="text-gray-700 dark:text-gray-300 leading-relaxed mb-4">
                The AI is trained on handwritten Indian invoices and can extract data from legible handwritten documents, including WhatsApp photos. 
                For best results, ensure:
              </p>
              <ul className="list-disc list-inside text-gray-700 dark:text-gray-300 mb-4 space-y-2">
                <li>Handwriting is clear and legible</li>
                <li>Images are well-lit (not shadowed)</li>
                <li>Text is not smudged or faded</li>
              </ul>
              <p className="text-gray-700 dark:text-gray-300 leading-relaxed">
                <strong>Note:</strong> Typed/printed invoices achieve 98-99% accuracy. For heavily handwritten invoices, expect to review 15-20% of fields manually (still faster than typing everything).
              </p>
            </div>

            {/* FAQ 11 */}
            <div className="bg-white dark:bg-gray-800 rounded-lg p-6 border border-gray-200 dark:border-gray-700">
              <h3 className="text-xl font-bold text-gray-900 dark:text-white mb-3">
                11. Will I need to hire someone to manage the automation?
              </h3>
              <p className="text-gray-700 dark:text-gray-300 leading-relaxed mb-4">
                <strong>No.</strong> Invoice automation actually <strong>reduces your staffing needs</strong>—not increases them.
              </p>
              <p className="text-gray-700 dark:text-gray-300 leading-relaxed mb-4">
                Most small businesses go from:
              </p>
              <ul className="list-disc list-inside text-gray-700 dark:text-gray-300 mb-4 space-y-2">
                <li><strong>Before:</strong> 2 people doing full-time data entry (8 hours/day)</li>
                <li><strong>After:</strong> 1 person doing quick reviews (10-15 minutes/day)</li>
              </ul>
              <p className="text-gray-700 dark:text-gray-300 leading-relaxed">
                The AI handles 95% of the work automatically. Your existing staff can manage it without additional training or technical expertise. 
                <strong>Sneha Kulkarni</strong> (from our case study) reduced her team from 2 staff to 1, saving ₹18,000/month in wages plus the time savings.
              </p>
            </div>

            {/* FAQ 12 */}
            <div className="bg-white dark:bg-gray-800 rounded-lg p-6 border border-gray-200 dark:border-gray-700">
              <h3 className="text-xl font-bold text-gray-900 dark:text-white mb-3">
                12. What happens if I have unique invoice formats or special requirements?
              </h3>
              <p className="text-gray-700 dark:text-gray-300 leading-relaxed mb-4">
                TrulyInvoice can be <strong>customized for your specific needs</strong>:
              </p>
              <ul className="list-disc list-inside text-gray-700 dark:text-gray-300 mb-4 space-y-2">
                <li><strong>Custom fields:</strong> Extract additional fields not in standard templates (e.g., lot numbers, expiry dates, warehouse codes)</li>
                <li><strong>Vendor-specific training:</strong> AI learns your unique vendor formats over time</li>
                <li><strong>Industry templates:</strong> Pre-built templates for restaurants, retail, manufacturing, distributors</li>
                <li><strong>Multi-language support:</strong> Invoices in Hindi, Tamil, Telugu, Marathi, Gujarati</li>
                <li><strong>Custom exports:</strong> Create export formats for any software (not just Tally/QuickBooks/Zoho)</li>
              </ul>
              <p className="text-gray-700 dark:text-gray-300 leading-relaxed">
                For enterprise needs (500+ invoices/month), <Link href="/pricing" className="text-blue-600 hover:underline">contact us for custom pricing</Link> with dedicated account manager and priority support. We've handled everything from simple grocery receipts to complex multi-page purchase orders with 100+ line items.
              </p>
            </div>
          </div>
        </section>

        {/* CTA Section */}
        <section id="get-started" className="mb-12 scroll-mt-20">
          <div className="bg-gradient-to-r from-blue-600 to-purple-600 rounded-lg p-8 md:p-12 text-white text-center">
            <h2 className="text-3xl md:text-4xl font-bold mb-4">
              Ready to Get Your Weekends Back?
            </h2>
            <p className="text-xl mb-8 opacity-90">
              Start automating your invoices today. First 10 invoices are free!
            </p>
            
            <div className="flex flex-col sm:flex-row gap-4 justify-center mb-8">
              <Link
                href="/signup"
                className="inline-flex items-center justify-center px-8 py-4 bg-white text-blue-600 font-bold rounded-lg hover:bg-gray-100 transition-all shadow-lg"
              >
                Start Free Trial
              </Link>
              <Link
                href="/pricing"
                className="inline-flex items-center justify-center px-8 py-4 bg-transparent border-2 border-white text-white font-bold rounded-lg hover:bg-white/10 transition-all"
              >
                View Pricing
              </Link>
            </div>

            <div className="grid md:grid-cols-3 gap-6 text-left">
              <div className="flex items-start gap-3">
                <CheckCircle2 className="flex-shrink-0 mt-1" size={24} />
                <div>
                  <p className="font-semibold mb-1">No Credit Card</p>
                  <p className="text-sm opacity-90">10 free invoices to test</p>
                </div>
              </div>
              <div className="flex items-start gap-3">
                <CheckCircle2 className="flex-shrink-0 mt-1" size={24} />
                <div>
                  <p className="font-semibold mb-1">Save 50+ Hours/Month</p>
                  <p className="text-sm opacity-90">Proven with 500+ businesses</p>
                </div>
              </div>
              <div className="flex items-start gap-3">
                <CheckCircle2 className="flex-shrink-0 mt-1" size={24} />
                <div>
                  <p className="font-semibold mb-1">₹299/month</p>
                  <p className="text-sm opacity-90">Less than a meal out</p>
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* Author Bio */}
        <section className="mb-12">
          <div className="bg-gradient-to-r from-blue-50 to-indigo-50 dark:from-gray-800 dark:to-gray-700 rounded-lg p-8 border border-blue-200 dark:border-blue-800">
            <div className="flex items-start gap-6">
              <div className="flex-shrink-0">
                <div className="w-20 h-20 bg-gradient-to-br from-green-600 to-blue-600 rounded-full flex items-center justify-center text-white text-2xl font-bold">
                  AV
                </div>
              </div>
              <div className="flex-1">
                <h3 className="text-2xl font-bold text-gray-900 dark:text-white mb-2">
                  About the Author: Amit Verma, Business Automation Expert
                </h3>
                <p className="text-gray-700 dark:text-gray-300 leading-relaxed mb-4">
                  Amit Verma is a business automation consultant with 12+ years of experience helping Indian small businesses implement time-saving technologies. 
                  He has personally helped <strong>300+ restaurants, retailers, and distributors</strong> automate their invoice processing, resulting in an average time savings of 45 hours per month per business.
                </p>
                <p className="text-gray-700 dark:text-gray-300 leading-relaxed mb-4">
                  His expertise includes ROI analysis for automation investments, workflow optimization, and helping non-technical business owners adopt AI-powered tools without overwhelming their teams. 
                  Amit's mission is to give small business owners their time back so they can focus on growth instead of paperwork.
                </p>
                <div className="flex items-center gap-4 text-sm">
                  <a href="https://www.linkedin.com/in/amitverma-automation" className="text-blue-600 hover:underline font-medium flex items-center gap-1">
                    <span>LinkedIn Profile</span>
                  </a>
                  <span className="text-gray-400">•</span>
                  <a href="mailto:amit@trulyinvoice.com" className="text-blue-600 hover:underline font-medium flex items-center gap-1">
                    <span>Email Amit</span>
                  </a>
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* Related Articles */}
        <section className="mb-12">
          <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-6">📚 Related Articles</h2>
          <div className="grid md:grid-cols-3 gap-6">
            <Link href="/blog/extract-gst-from-invoices-automatically" className="bg-white dark:bg-gray-800 rounded-lg p-6 border border-gray-200 dark:border-gray-700 hover:border-blue-500 transition-all">
              <h3 className="font-bold text-gray-900 dark:text-white mb-2">Extract GST Automatically</h3>
              <p className="text-sm text-gray-600 dark:text-gray-400">5-second guide for accountants</p>
            </Link>
            <Link href="/blog/invoice-to-excel-complete-guide" className="bg-white dark:bg-gray-800 rounded-lg p-6 border border-gray-200 dark:border-gray-700 hover:border-blue-500 transition-all">
              <h3 className="font-bold text-gray-900 dark:text-white mb-2">Complete Invoice to Excel Guide</h3>
              <p className="text-sm text-gray-600 dark:text-gray-400">For Indian CAs & accountants</p>
            </Link>
            <Link href="/features" className="bg-white dark:bg-gray-800 rounded-lg p-6 border border-gray-200 dark:border-gray-700 hover:border-blue-500 transition-all">
              <h3 className="font-bold text-gray-900 dark:text-white mb-2">See All Features</h3>
              <p className="text-sm text-gray-600 dark:text-gray-400">Bulk processing, Tally export & more</p>
            </Link>
          </div>
        </section>
      </article>
    </main>
    </>
  )
}
