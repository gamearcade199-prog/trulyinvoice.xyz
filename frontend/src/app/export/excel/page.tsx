'use client'

import Link from 'next/link'
import { ArrowRight, CheckCircle2, FileSpreadsheet, Zap, Shield, TrendingUp, Download, BarChart3, Calculator, Clock } from 'lucide-react'
import { FAQSchema, SoftwareAppSchema } from '@/components/SeoSchemaMarkup'
import TrulyInvoiceLogo from '@/components/TrulyInvoiceLogo'

export default function ExcelExportPage() {
  return (
    <>
      <FAQSchema />
      <SoftwareAppSchema />
      
      <div className="min-h-screen bg-gradient-to-b from-blue-50 via-white to-green-50 dark:from-gray-900 dark:via-gray-800 dark:to-gray-900">
        {/* Navigation */}
        <nav className="border-b border-gray-200 dark:border-gray-700 bg-white/80 dark:bg-gray-900/80 backdrop-blur-sm sticky top-0 z-50">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="flex justify-between items-center h-16">
              <Link href="/" className="flex items-center space-x-2">
                <TrulyInvoiceLogo size="sm" />
              </Link>
              <div className="flex items-center space-x-4">
                <Link href="/pricing" className="text-gray-600 dark:text-gray-300 hover:text-blue-600 dark:hover:text-blue-400 font-medium">
                  Pricing
                </Link>
                <Link href="/login" className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 font-medium transition-colors">
                  Try Free
                </Link>
              </div>
            </div>
          </div>
        </nav>

        {/* Hero Section */}
        <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20">
          <div className="text-center mb-16">
            <div className="inline-flex items-center space-x-2 bg-blue-100 dark:bg-blue-900/30 text-blue-700 dark:text-blue-300 px-4 py-2 rounded-full text-sm font-medium mb-6">
              <FileSpreadsheet className="h-4 w-4" />
              <span>Invoice to Excel Converter</span>
            </div>
            
            <h1 className="text-5xl md:text-6xl font-bold text-gray-900 dark:text-white mb-6 leading-tight">
              Convert Invoices to Excel<br />
              <span className="bg-gradient-to-r from-blue-600 to-green-600 bg-clip-text text-transparent">
                with Professional Formatting
              </span>
            </h1>
            
            <p className="text-xl text-gray-600 dark:text-gray-300 mb-8 max-w-3xl mx-auto leading-relaxed">
              AI-powered invoice to Excel converter with <strong>multi-sheet structure</strong>, automatic formulas, 
              GST calculations, and accountant-ready formatting. Perfect for Indian businesses and CA firms.
            </p>
            
            <div className="flex flex-col sm:flex-row items-center justify-center space-y-4 sm:space-y-0 sm:space-x-4 mb-12">
              <Link href="/" className="px-8 py-4 bg-blue-600 text-white rounded-lg hover:bg-blue-700 font-semibold text-lg transition-all transform hover:scale-105 shadow-xl flex items-center space-x-2">
                <span>Start Free</span>
                <ArrowRight className="h-5 w-5" />
              </Link>
              <Link href="/pricing" className="px-8 py-4 bg-white dark:bg-gray-800 text-blue-600 dark:text-blue-400 border-2 border-blue-600 dark:border-blue-400 rounded-lg hover:bg-blue-50 dark:hover:bg-gray-700 font-semibold text-lg transition-all">
                View Pricing
              </Link>
            </div>
            
            <div className="flex items-center justify-center space-x-8 text-sm text-gray-600 dark:text-gray-400">
              <div className="flex items-center space-x-2">
                <CheckCircle2 className="h-5 w-5 text-green-600" />
                <span>10 Free Invoices/Month</span>
              </div>
              <div className="flex items-center space-x-2">
                <CheckCircle2 className="h-5 w-5 text-green-600" />
                <span>99% AI Accuracy</span>
              </div>
              <div className="flex items-center space-x-2">
                <CheckCircle2 className="h-5 w-5 text-green-600" />
                <span>No Credit Card</span>
              </div>
            </div>
          </div>

          {/* Feature Cards */}
          <div className="grid md:grid-cols-3 gap-8 mb-20">
            <div className="bg-white dark:bg-gray-800 p-8 rounded-2xl shadow-lg border border-gray-200 dark:border-gray-700 hover:shadow-xl transition-shadow">
              <div className="w-12 h-12 bg-blue-100 dark:bg-blue-900/30 rounded-lg flex items-center justify-center mb-4">
                <FileSpreadsheet className="h-6 w-6 text-blue-600" />
              </div>
              <h3 className="text-xl font-bold text-gray-900 dark:text-white mb-3">Multi-Sheet Structure</h3>
              <p className="text-gray-600 dark:text-gray-300 leading-relaxed">
                Get separate sheets for Summary, Invoice Details, Line Items, GST Analysis, and Reconciliation. Professional Excel format for accountants.
              </p>
            </div>

            <div className="bg-white dark:bg-gray-800 p-8 rounded-2xl shadow-lg border border-gray-200 dark:border-gray-700 hover:shadow-xl transition-shadow">
              <div className="w-12 h-12 bg-green-100 dark:bg-green-900/30 rounded-lg flex items-center justify-center mb-4">
                <Calculator className="h-6 w-6 text-green-600" />
              </div>
              <h3 className="text-xl font-bold text-gray-900 dark:text-white mb-3">Automatic Formulas</h3>
              <p className="text-gray-600 dark:text-gray-300 leading-relaxed">
                Excel formulas for totals, GST calculations, subtotals, and grand totals. Fully editable and compatible with all Excel versions.
              </p>
            </div>

            <div className="bg-white dark:bg-gray-800 p-8 rounded-2xl shadow-lg border border-gray-200 dark:border-gray-700 hover:shadow-xl transition-shadow">
              <div className="w-12 h-12 bg-purple-100 dark:bg-purple-900/30 rounded-lg flex items-center justify-center mb-4">
                <Shield className="h-6 w-6 text-purple-600" />
              </div>
              <h3 className="text-xl font-bold text-gray-900 dark:text-white mb-3">GST Compliant</h3>
              <p className="text-gray-600 dark:text-gray-300 leading-relaxed">
                Automatic GSTIN extraction, validation, CGST/SGST/IGST calculations, HSN codes, and place of supply detection for all 37 Indian states.
              </p>
            </div>
          </div>
        </section>

        {/* How It Works */}
        <section className="bg-white dark:bg-gray-800 py-20">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="text-center mb-16">
              <h2 className="text-4xl font-bold text-gray-900 dark:text-white mb-4">
                Convert Invoice to Excel in 3 Steps
              </h2>
              <p className="text-xl text-gray-600 dark:text-gray-300">
                Simple, fast, and accurate. Get your Excel file in under 5 seconds.
              </p>
            </div>

            <div className="grid md:grid-cols-3 gap-12">
              <div className="text-center">
                <div className="w-16 h-16 bg-blue-600 text-white rounded-full flex items-center justify-center text-2xl font-bold mx-auto mb-6">
                  1
                </div>
                <h3 className="text-2xl font-bold text-gray-900 dark:text-white mb-4">Upload Invoice</h3>
                <p className="text-gray-600 dark:text-gray-300 leading-relaxed">
                  Upload your PDF or image invoice (JPG, PNG). Supports scanned documents and mobile photos.
                </p>
              </div>

              <div className="text-center">
                <div className="w-16 h-16 bg-green-600 text-white rounded-full flex items-center justify-center text-2xl font-bold mx-auto mb-6">
                  2
                </div>
                <h3 className="text-2xl font-bold text-gray-900 dark:text-white mb-4">AI Extracts Data</h3>
                <p className="text-gray-600 dark:text-gray-300 leading-relaxed">
                  Our AI extracts vendor name, GSTIN, invoice number, line items, amounts, GST details with 99% accuracy.
                </p>
              </div>

              <div className="text-center">
                <div className="w-16 h-16 bg-purple-600 text-white rounded-full flex items-center justify-center text-2xl font-bold mx-auto mb-6">
                  3
                </div>
                <h3 className="text-2xl font-bold text-gray-900 dark:text-white mb-4">Download Excel</h3>
                <p className="text-gray-600 dark:text-gray-300 leading-relaxed">
                  Get a professionally formatted Excel file with multiple sheets, formulas, and GST calculations ready for accounting software.
                </p>
              </div>
            </div>
          </div>
        </section>

        {/* Excel Features Comparison */}
        <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold text-gray-900 dark:text-white mb-4">
              TrulyInvoice vs Manual Excel Entry
            </h2>
            <p className="text-xl text-gray-600 dark:text-gray-300">
              See how much time and effort you save with AI automation
            </p>
          </div>

          <div className="overflow-x-auto">
            <table className="w-full bg-white dark:bg-gray-800 rounded-2xl shadow-xl overflow-hidden">
              <thead className="bg-gradient-to-r from-blue-600 to-green-600 text-white">
                <tr>
                  <th className="px-6 py-4 text-left text-lg font-semibold">Feature</th>
                  <th className="px-6 py-4 text-center text-lg font-semibold">Manual Excel Entry</th>
                  <th className="px-6 py-4 text-center text-lg font-semibold">TrulyInvoice AI</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-200 dark:divide-gray-700">
                <tr className="hover:bg-gray-50 dark:hover:bg-gray-700/50 transition-colors">
                  <td className="px-6 py-4 font-medium text-gray-900 dark:text-white">Time per Invoice</td>
                  <td className="px-6 py-4 text-center text-red-600 dark:text-red-400 font-semibold">10-15 minutes</td>
                  <td className="px-6 py-4 text-center text-green-600 dark:text-green-400 font-semibold">Under 5 seconds</td>
                </tr>
                <tr className="hover:bg-gray-50 dark:hover:bg-gray-700/50 transition-colors">
                  <td className="px-6 py-4 font-medium text-gray-900 dark:text-white">Accuracy Rate</td>
                  <td className="px-6 py-4 text-center text-gray-600 dark:text-gray-400">85-90% (human error)</td>
                  <td className="px-6 py-4 text-center text-green-600 dark:text-green-400 font-semibold">99% AI accuracy</td>
                </tr>
                <tr className="hover:bg-gray-50 dark:hover:bg-gray-700/50 transition-colors">
                  <td className="px-6 py-4 font-medium text-gray-900 dark:text-white">Multi-Sheet Structure</td>
                  <td className="px-6 py-4 text-center text-gray-600 dark:text-gray-400">Manual setup required</td>
                  <td className="px-6 py-4 text-center text-green-600 dark:text-green-400 font-semibold">✓ Automatic</td>
                </tr>
                <tr className="hover:bg-gray-50 dark:hover:bg-gray-700/50 transition-colors">
                  <td className="px-6 py-4 font-medium text-gray-900 dark:text-white">Excel Formulas</td>
                  <td className="px-6 py-4 text-center text-gray-600 dark:text-gray-400">Manual creation</td>
                  <td className="px-6 py-4 text-center text-green-600 dark:text-green-400 font-semibold">✓ Pre-built formulas</td>
                </tr>
                <tr className="hover:bg-gray-50 dark:hover:bg-gray-700/50 transition-colors">
                  <td className="px-6 py-4 font-medium text-gray-900 dark:text-white">GST Calculations</td>
                  <td className="px-6 py-4 text-center text-gray-600 dark:text-gray-400">Manual calculation</td>
                  <td className="px-6 py-4 text-center text-green-600 dark:text-green-400 font-semibold">✓ Auto CGST/SGST/IGST</td>
                </tr>
                <tr className="hover:bg-gray-50 dark:hover:bg-gray-700/50 transition-colors">
                  <td className="px-6 py-4 font-medium text-gray-900 dark:text-white">GSTIN Validation</td>
                  <td className="px-6 py-4 text-center text-gray-600 dark:text-gray-400">Manual check</td>
                  <td className="px-6 py-4 text-center text-green-600 dark:text-green-400 font-semibold">✓ Automatic validation</td>
                </tr>
                <tr className="hover:bg-gray-50 dark:hover:bg-gray-700/50 transition-colors">
                  <td className="px-6 py-4 font-medium text-gray-900 dark:text-white">Professional Formatting</td>
                  <td className="px-6 py-4 text-center text-gray-600 dark:text-gray-400">Time-consuming</td>
                  <td className="px-6 py-4 text-center text-green-600 dark:text-green-400 font-semibold">✓ Pre-formatted</td>
                </tr>
                <tr className="hover:bg-gray-50 dark:hover:bg-gray-700/50 transition-colors">
                  <td className="px-6 py-4 font-medium text-gray-900 dark:text-white">Cost per Invoice</td>
                  <td className="px-6 py-4 text-center text-red-600 dark:text-red-400 font-semibold">₹25-50 (labor cost)</td>
                  <td className="px-6 py-4 text-center text-green-600 dark:text-green-400 font-semibold">₹0-2 per invoice</td>
                </tr>
              </tbody>
            </table>
          </div>

          <div className="mt-12 text-center">
            <p className="text-xl text-gray-600 dark:text-gray-300 mb-6">
              <strong className="text-green-600 dark:text-green-400">Save 98% of your time</strong> and eliminate manual data entry errors
            </p>
            <Link href="/signup" className="inline-flex items-center px-8 py-4 bg-gradient-to-r from-blue-600 to-green-600 text-white rounded-lg hover:from-blue-700 hover:to-green-700 font-semibold text-lg transition-all transform hover:scale-105 shadow-xl space-x-2">
              <span>Start Converting for Free</span>
              <ArrowRight className="h-5 w-5" />
            </Link>
          </div>
        </section>

        {/* CTA Section */}
        <section className="bg-gradient-to-r from-blue-600 to-green-600 py-20">
          <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
            <h2 className="text-4xl font-bold text-white mb-6">
              Ready to Automate Your Invoice Processing?
            </h2>
            <p className="text-xl text-blue-100 mb-8">
              Join thousands of Indian businesses and CA firms using TrulyInvoice to save 90% of manual data entry time
            </p>
            <div className="flex flex-col sm:flex-row items-center justify-center space-y-4 sm:space-y-0 sm:space-x-4">
              <Link href="/signup" className="px-8 py-4 bg-white text-blue-600 rounded-lg hover:bg-gray-100 font-semibold text-lg transition-all transform hover:scale-105 shadow-xl flex items-center space-x-2">
                <span>Get Started Free</span>
                <ArrowRight className="h-5 w-5" />
              </Link>
              <Link href="/pricing" className="px-8 py-4 bg-blue-700 text-white border-2 border-white rounded-lg hover:bg-blue-800 font-semibold text-lg transition-all">
                View All Plans
              </Link>
            </div>
            <p className="text-blue-100 mt-6">
              ✓ 10 free conversions per month • ✓ No credit card required • ✓ Cancel anytime
            </p>
          </div>
        </section>

        {/* Footer */}
        <footer className="bg-gray-900 text-gray-300 py-12">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="grid md:grid-cols-4 gap-8 mb-8">
              <div>
                <h3 className="text-white font-bold mb-4">Product</h3>
                <ul className="space-y-2">
                  <li><Link href="/export/excel" className="hover:text-white transition-colors">Excel Export</Link></li>
                  <li><Link href="/export/tally" className="hover:text-white transition-colors">Tally XML</Link></li>
                  <li><Link href="/export/quickbooks" className="hover:text-white transition-colors">QuickBooks</Link></li>
                  <li><Link href="/export/zoho-books" className="hover:text-white transition-colors">Zoho Books</Link></li>
                  <li><Link href="/export/csv" className="hover:text-white transition-colors">Bulk CSV</Link></li>
                </ul>
              </div>
              <div>
                <h3 className="text-white font-bold mb-4">Company</h3>
                <ul className="space-y-2">
                  <li><Link href="/about" className="hover:text-white transition-colors">About Us</Link></li>
                  <li><Link href="/pricing" className="hover:text-white transition-colors">Pricing</Link></li>
                  <li><Link href="/contact" className="hover:text-white transition-colors">Contact</Link></li>
                </ul>
              </div>
              <div>
                <h3 className="text-white font-bold mb-4">Legal</h3>
                <ul className="space-y-2">
                  <li><Link href="/privacy" className="hover:text-white transition-colors">Privacy Policy</Link></li>
                  <li><Link href="/terms" className="hover:text-white transition-colors">Terms of Service</Link></li>
                </ul>
              </div>
              <div>
                <h3 className="text-white font-bold mb-4">Connect</h3>
                <p className="text-sm">Email: infotrulybot@gmail.com</p>
                <p className="text-sm mt-2">WhatsApp: +91 9101361482</p>
                <p className="text-sm mt-2">Making invoice processing simple for Indian businesses</p>
              </div>
            </div>
            <div className="border-t border-gray-800 pt-8 text-center text-sm">
              <p>&copy; 2025 TrulyInvoice. All rights reserved.</p>
            </div>
          </div>
        </footer>
      </div>
    </>
  )
}
