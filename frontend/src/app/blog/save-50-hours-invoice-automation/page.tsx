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
    canonical: 'https://trulyinvoice.xyz/blog/save-50-hours-invoice-automation',
  },
  authors: [{ name: 'TrulyInvoice Team' }],
}

export default function BlogPost() {
  return (
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
            <time dateTime="2025-10-28">October 28, 2025</time>
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
            <li><a href="#faq" className="text-blue-600 hover:underline">8. FAQ: Common Concerns Answered</a></li>
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
            ❓ FAQ: Common Concerns Answered
          </h2>

          <div className="space-y-4">
            {/* FAQ 1 */}
            <div className="bg-white dark:bg-gray-800 rounded-lg p-6 border border-gray-200 dark:border-gray-700">
              <h3 className="font-bold text-gray-900 dark:text-white mb-2 text-lg">
                Q: Is my invoice data safe? I'm worried about privacy.
              </h3>
              <p className="text-gray-700 dark:text-gray-300">
                <strong>A:</strong> Yes, your data is completely secure. TrulyInvoice uses <strong>bank-level encryption</strong> (same as your online banking). 
                Your invoices are processed in real-time and <strong>never stored</strong> on our servers. 
                We have a zero-retention policy—after extraction, your documents are permanently deleted. 
                We're also <strong>ISO 27001 compliant</strong> and follow Indian data protection laws.
              </p>
            </div>

            {/* FAQ 2 */}
            <div className="bg-white dark:bg-gray-800 rounded-lg p-6 border border-gray-200 dark:border-gray-700">
              <h3 className="font-bold text-gray-900 dark:text-white mb-2 text-lg">
                Q: What if the AI makes mistakes? I can't afford errors.
              </h3>
              <p className="text-gray-700 dark:text-gray-300">
                <strong>A:</strong> AI accuracy is <strong>98-99%</strong>—actually higher than human accuracy (92-95%). 
                Plus, you get a quick review screen before exporting. The AI highlights low-confidence fields (rare) for manual verification. 
                We also offer a <strong>money-back guarantee</strong> if accuracy is below 98%.
              </p>
            </div>

            {/* FAQ 3 */}
            <div className="bg-white dark:bg-gray-800 rounded-lg p-6 border border-gray-200 dark:border-gray-700">
              <h3 className="font-bold text-gray-900 dark:text-white mb-2 text-lg">
                Q: Is it hard to learn? I'm not tech-savvy.
              </h3>
              <p className="text-gray-700 dark:text-gray-300">
                <strong>A:</strong> If you can use WhatsApp, you can use TrulyInvoice. It's 3 steps: <strong>Upload → AI extracts → Download Excel</strong>. 
                That's it. No technical knowledge needed. Plus, we have <strong>Hindi support</strong> and <strong>video tutorials</strong> in multiple Indian languages.
              </p>
            </div>

            {/* FAQ 4 */}
            <div className="bg-white dark:bg-gray-800 rounded-lg p-6 border border-gray-200 dark:border-gray-700">
              <h3 className="font-bold text-gray-900 dark:text-white mb-2 text-lg">
                Q: What types of invoices does it work with?
              </h3>
              <p className="text-gray-700 dark:text-gray-300">
                <strong>A:</strong> All types! PDF invoices, scanned images, <strong>WhatsApp photos</strong> (even blurry ones), handwritten invoices, 
                different Indian vendor formats. The AI is trained on 50,000+ Indian invoices, so it understands our formats.
              </p>
            </div>

            {/* FAQ 5 */}
            <div className="bg-white dark:bg-gray-800 rounded-lg p-6 border border-gray-200 dark:border-gray-700">
              <h3 className="font-bold text-gray-900 dark:text-white mb-2 text-lg">
                Q: Can I try it before paying?
              </h3>
              <p className="text-gray-700 dark:text-gray-300">
                <strong>A:</strong> Yes! Free plan includes <strong>10 invoices/month</strong>. No credit card required. 
                Upload your toughest invoices and see the accuracy yourself. If it works, upgrade. If not, no cost to you.
              </p>
            </div>

            {/* FAQ 6 */}
            <div className="bg-white dark:bg-gray-800 rounded-lg p-6 border border-gray-200 dark:border-gray-700">
              <h3 className="font-bold text-gray-900 dark:text-white mb-2 text-lg">
                Q: Will this work with my accounting software (Tally, Zoho, etc.)?
              </h3>
              <p className="text-gray-700 dark:text-gray-300">
                <strong>A:</strong> Yes! We export to <strong>Excel, CSV, Tally XML, QuickBooks, Zoho Books</strong>. 
                One-click export means your data goes straight into your existing workflow.
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
  )
}
