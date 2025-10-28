'use client'

import Link from 'next/link'
import { ArrowRight, CheckCircle2, FileText, Users, TrendingUp, Shield, Download, Calculator, Zap, Clock } from 'lucide-react'
import { FAQSchema, SoftwareAppSchema } from '@/components/SeoSchemaMarkup'
import TrulyInvoiceLogo from '@/components/TrulyInvoiceLogo'

export default function CSVExportPage() {
  return (
    <>
      <FAQSchema />
      <SoftwareAppSchema />
      
      <div className="min-h-screen bg-gradient-to-b from-purple-50 via-white to-pink-50 dark:from-gray-900 dark:via-gray-800 dark:to-gray-900">
        <nav className="border-b border-gray-200 dark:border-gray-700 bg-white/80 dark:bg-gray-900/80 backdrop-blur-sm sticky top-0 z-50">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="flex justify-between items-center h-16">
              <Link href="/" className="flex items-center space-x-2">
                <TrulyInvoiceLogo size="sm" />
              </Link>
              <div className="flex items-center space-x-4">
                <Link href="/pricing" className="text-gray-600 dark:text-gray-300 hover:text-purple-600 font-medium">Pricing</Link>
                <Link href="/login" className="px-6 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700 font-medium transition-colors">Try Free</Link>
              </div>
            </div>
          </div>
        </nav>

        <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20">
          <div className="text-center mb-16">
            <div className="inline-flex items-center space-x-2 bg-purple-100 dark:bg-purple-900/30 text-purple-700 dark:text-purple-300 px-4 py-2 rounded-full text-sm font-medium mb-6">
              <FileText className="h-4 w-4" />
              <span>Bulk Invoice to CSV Converter</span>
            </div>
            
            <h1 className="text-5xl md:text-6xl font-bold text-gray-900 dark:text-white mb-6 leading-tight">
              Bulk Export Invoices to CSV<br />
              <span className="bg-gradient-to-r from-purple-600 to-pink-600 bg-clip-text text-transparent">
                For Accountants & CA Firms
              </span>
            </h1>
            
            <p className="text-xl text-gray-600 dark:text-gray-300 mb-8 max-w-3xl mx-auto leading-relaxed">
              Process <strong>50+ invoices in minutes</strong> to consolidated CSV. Perfect for chartered accountants, accounting firms, 
              and bookkeepers. Get all invoice data, GST details, vendor info in one professional CSV file with <strong>8 organized sections</strong>.
            </p>
            
            <div className="flex flex-col sm:flex-row items-center justify-center space-y-4 sm:space-y-0 sm:space-x-4 mb-12">
              <Link href="/" className="px-8 py-4 bg-blue-600 text-white rounded-lg hover:bg-blue-700 font-semibold text-lg transition-all transform hover:scale-105 shadow-xl flex items-center space-x-2">
                <span>Start Free</span>
                <ArrowRight className="h-5 w-5" />
              </Link>
              <Link href="/pricing" className="px-8 py-4 bg-white dark:bg-gray-800 text-purple-600 dark:text-purple-400 border-2 border-purple-600 rounded-lg hover:bg-purple-50 dark:hover:bg-gray-700 font-semibold text-lg transition-all">
                View Pricing
              </Link>
            </div>
            
            <div className="flex items-center justify-center space-x-8 text-sm text-gray-600 dark:text-gray-400">
              <div className="flex items-center space-x-2">
                <CheckCircle2 className="h-5 w-5 text-green-600" />
                <span>Bulk Processing (50+ invoices)</span>
              </div>
              <div className="flex items-center space-x-2">
                <CheckCircle2 className="h-5 w-5 text-green-600" />
                <span>8-Section Format</span>
              </div>
              <div className="flex items-center space-x-2">
                <CheckCircle2 className="h-5 w-5 text-green-600" />
                <span>UTF-8 with BOM</span>
              </div>
            </div>
          </div>

          <div className="grid md:grid-cols-3 gap-8">
            <div className="bg-white dark:bg-gray-800 p-8 rounded-2xl shadow-lg border border-gray-200 dark:border-gray-700">
              <div className="w-12 h-12 bg-purple-100 dark:bg-purple-900/30 rounded-lg flex items-center justify-center mb-4">
                <Users className="h-6 w-6 text-purple-600" />
              </div>
              <h3 className="text-xl font-bold text-gray-900 dark:text-white mb-3">Built for CA Firms</h3>
              <p className="text-gray-600 dark:text-gray-300">
                Process client invoices in bulk. Get one consolidated CSV with all invoices organized by vendor, date, and amount. Perfect for reconciliation.
              </p>
            </div>

            <div className="bg-white dark:bg-gray-800 p-8 rounded-2xl shadow-lg border border-gray-200 dark:border-gray-700">
              <div className="w-12 h-12 bg-pink-100 dark:bg-pink-900/30 rounded-lg flex items-center justify-center mb-4">
                <Calculator className="h-6 w-6 text-pink-600" />
              </div>
              <h3 className="text-xl font-bold text-gray-900 dark:text-white mb-3">8-Section Structure</h3>
              <p className="text-gray-600 dark:text-gray-300">
                Professional CSV with 8 sections: Invoice Summary, Vendor Details, Line Items, GST Breakdown, Payment Terms, Totals, Notes, and Audit Trail.
              </p>
            </div>

            <div className="bg-white dark:bg-gray-800 p-8 rounded-2xl shadow-lg border border-gray-200 dark:border-gray-700">
              <div className="w-12 h-12 bg-blue-100 dark:bg-blue-900/30 rounded-lg flex items-center justify-center mb-4">
                <TrendingUp className="h-6 w-6 text-blue-600" />
              </div>
              <h3 className="text-xl font-bold text-gray-900 dark:text-white mb-3">Excel Compatible</h3>
              <p className="text-gray-600 dark:text-gray-300">
                UTF-8 with BOM encoding ensures perfect Excel import. All special characters, GST symbols, currency symbols display correctly in Excel.
              </p>
            </div>
          </div>
        </section>

        <section className="bg-white dark:bg-gray-800 py-20">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="text-center mb-16">
              <h2 className="text-4xl font-bold text-gray-900 dark:text-white mb-4">8-Section Professional CSV Format</h2>
              <p className="text-xl text-gray-600 dark:text-gray-300">Everything accountants need in one organized file</p>
            </div>

            <div className="grid md:grid-cols-2 gap-8">
              <div className="bg-purple-50 dark:bg-purple-900/10 p-8 rounded-2xl border border-purple-200 dark:border-purple-700">
                <h3 className="text-2xl font-bold text-gray-900 dark:text-white mb-6 flex items-center space-x-2">
                  <span className="bg-purple-600 text-white w-8 h-8 rounded-full flex items-center justify-center text-sm">1</span>
                  <span>Invoice Summary</span>
                </h3>
                <ul className="space-y-2 text-gray-700 dark:text-gray-300">
                  <li>• Invoice Number</li>
                  <li>• Invoice Date</li>
                  <li>• Due Date</li>
                  <li>• Vendor Name</li>
                  <li>• Grand Total</li>
                  <li>• Payment Status</li>
                </ul>
              </div>

              <div className="bg-pink-50 dark:bg-pink-900/10 p-8 rounded-2xl border border-pink-200 dark:border-pink-700">
                <h3 className="text-2xl font-bold text-gray-900 dark:text-white mb-6 flex items-center space-x-2">
                  <span className="bg-pink-600 text-white w-8 h-8 rounded-full flex items-center justify-center text-sm">2</span>
                  <span>Vendor Details</span>
                </h3>
                <ul className="space-y-2 text-gray-700 dark:text-gray-300">
                  <li>• Vendor Name (Normalized)</li>
                  <li>• GSTIN</li>
                  <li>• PAN Number</li>
                  <li>• Address</li>
                  <li>• Contact Info</li>
                  <li>• State Code</li>
                </ul>
              </div>

              <div className="bg-blue-50 dark:bg-blue-900/10 p-8 rounded-2xl border border-blue-200 dark:border-blue-700">
                <h3 className="text-2xl font-bold text-gray-900 dark:text-white mb-6 flex items-center space-x-2">
                  <span className="bg-blue-600 text-white w-8 h-8 rounded-full flex items-center justify-center text-sm">3</span>
                  <span>Line Items</span>
                </h3>
                <ul className="space-y-2 text-gray-700 dark:text-gray-300">
                  <li>• Item Description</li>
                  <li>• Quantity</li>
                  <li>• Unit Price</li>
                  <li>• HSN/SAC Code</li>
                  <li>• Discount</li>
                  <li>• Line Total</li>
                </ul>
              </div>

              <div className="bg-green-50 dark:bg-green-900/10 p-8 rounded-2xl border border-green-200 dark:border-green-700">
                <h3 className="text-2xl font-bold text-gray-900 dark:text-white mb-6 flex items-center space-x-2">
                  <span className="bg-green-600 text-white w-8 h-8 rounded-full flex items-center justify-center text-sm">4</span>
                  <span>GST Breakdown</span>
                </h3>
                <ul className="space-y-2 text-gray-700 dark:text-gray-300">
                  <li>• CGST Amount & %</li>
                  <li>• SGST Amount & %</li>
                  <li>• IGST Amount & %</li>
                  <li>• Total GST</li>
                  <li>• Place of Supply</li>
                  <li>• Taxable Amount</li>
                </ul>
              </div>

              <div className="bg-orange-50 dark:bg-orange-900/10 p-8 rounded-2xl border border-orange-200 dark:border-orange-700">
                <h3 className="text-2xl font-bold text-gray-900 dark:text-white mb-6 flex items-center space-x-2">
                  <span className="bg-orange-600 text-white w-8 h-8 rounded-full flex items-center justify-center text-sm">5</span>
                  <span>Payment Terms</span>
                </h3>
                <ul className="space-y-2 text-gray-700 dark:text-gray-300">
                  <li>• Payment Terms (Net 30)</li>
                  <li>• Payment Method</li>
                  <li>• Bank Details</li>
                  <li>• Payment Notes</li>
                </ul>
              </div>

              <div className="bg-red-50 dark:bg-red-900/10 p-8 rounded-2xl border border-red-200 dark:border-red-700">
                <h3 className="text-2xl font-bold text-gray-900 dark:text-white mb-6 flex items-center space-x-2">
                  <span className="bg-red-600 text-white w-8 h-8 rounded-full flex items-center justify-center text-sm">6</span>
                  <span>Totals</span>
                </h3>
                <ul className="space-y-2 text-gray-700 dark:text-gray-300">
                  <li>• Subtotal</li>
                  <li>• Total Discount</li>
                  <li>• Total Tax</li>
                  <li>• Grand Total</li>
                  <li>• Rounding Off</li>
                </ul>
              </div>

              <div className="bg-yellow-50 dark:bg-yellow-900/10 p-8 rounded-2xl border border-yellow-200 dark:border-yellow-700">
                <h3 className="text-2xl font-bold text-gray-900 dark:text-white mb-6 flex items-center space-x-2">
                  <span className="bg-yellow-600 text-white w-8 h-8 rounded-full flex items-center justify-center text-sm">7</span>
                  <span>Notes & Terms</span>
                </h3>
                <ul className="space-y-2 text-gray-700 dark:text-gray-300">
                  <li>• Invoice Notes</li>
                  <li>• Terms & Conditions</li>
                  <li>• Special Instructions</li>
                </ul>
              </div>

              <div className="bg-indigo-50 dark:bg-indigo-900/10 p-8 rounded-2xl border border-indigo-200 dark:border-indigo-700">
                <h3 className="text-2xl font-bold text-gray-900 dark:text-white mb-6 flex items-center space-x-2">
                  <span className="bg-indigo-600 text-white w-8 h-8 rounded-full flex items-center justify-center text-sm">8</span>
                  <span>Audit Trail</span>
                </h3>
                <ul className="space-y-2 text-gray-700 dark:text-gray-300">
                  <li>• Upload Date</li>
                  <li>• Processing Date</li>
                  <li>• File Name</li>
                  <li>• Confidence Score</li>
                </ul>
              </div>
            </div>
          </div>
        </section>

        <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold text-gray-900 dark:text-white mb-4">Perfect for Accounting Professionals</h2>
          </div>

          <div className="grid md:grid-cols-2 gap-12">
            <div className="bg-gradient-to-br from-purple-50 to-pink-50 dark:from-purple-900/20 dark:to-pink-900/20 p-8 rounded-2xl border-2 border-purple-200 dark:border-purple-700">
              <h3 className="text-2xl font-bold text-gray-900 dark:text-white mb-6">For CA Firms</h3>
              <ul className="space-y-4 text-gray-700 dark:text-gray-300">
                <li className="flex items-start space-x-3">
                  <CheckCircle2 className="h-6 w-6 text-purple-600 flex-shrink-0 mt-1" />
                  <div>
                    <strong>Multi-Client Processing:</strong> Process invoices from multiple clients, each identified by vendor name and client code
                  </div>
                </li>
                <li className="flex items-start space-x-3">
                  <CheckCircle2 className="h-6 w-6 text-purple-600 flex-shrink-0 mt-1" />
                  <div>
                    <strong>GST Reconciliation:</strong> All GST details in separate columns for easy GSTR-2A/2B reconciliation
                  </div>
                </li>
                <li className="flex items-start space-x-3">
                  <CheckCircle2 className="h-6 w-6 text-purple-600 flex-shrink-0 mt-1" />
                  <div>
                    <strong>Audit Trail:</strong> Complete processing history with timestamps and confidence scores
                  </div>
                </li>
              </ul>
            </div>

            <div className="bg-gradient-to-br from-blue-50 to-green-50 dark:from-blue-900/20 dark:to-green-900/20 p-8 rounded-2xl border-2 border-blue-200 dark:border-blue-700">
              <h3 className="text-2xl font-bold text-gray-900 dark:text-white mb-6">For Businesses</h3>
              <ul className="space-y-4 text-gray-700 dark:text-gray-300">
                <li className="flex items-start space-x-3">
                  <CheckCircle2 className="h-6 w-6 text-blue-600 flex-shrink-0 mt-1" />
                  <div>
                    <strong>Month-End Closing:</strong> Process all month's invoices to one CSV for faster closing
                  </div>
                </li>
                <li className="flex items-start space-x-3">
                  <CheckCircle2 className="h-6 w-6 text-blue-600 flex-shrink-0 mt-1" />
                  <div>
                    <strong>Vendor Analysis:</strong> Sort by vendor to analyze spending patterns and negotiate better rates
                  </div>
                </li>
                <li className="flex items-start space-x-3">
                  <CheckCircle2 className="h-6 w-6 text-blue-600 flex-shrink-0 mt-1" />
                  <div>
                    <strong>Budget Tracking:</strong> Import to Excel pivot tables for category-wise expense analysis
                  </div>
                </li>
              </ul>
            </div>
          </div>
        </section>

        <section className="bg-gradient-to-r from-purple-600 to-pink-600 py-20">
          <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
            <h2 className="text-4xl font-bold text-white mb-6">Save 90% Time on Invoice Data Entry</h2>
            <p className="text-xl text-purple-100 mb-8">Process 50 invoices in 5 minutes instead of 8 hours</p>
            <Link href="/signup" className="px-8 py-4 bg-white text-purple-600 rounded-lg hover:bg-gray-100 font-semibold text-lg transition-all transform hover:scale-105 shadow-xl inline-flex items-center space-x-2">
              <span>Start Bulk Processing Free</span>
              <ArrowRight className="h-5 w-5" />
            </Link>
            <p className="text-purple-100 mt-6">✓ Bulk CSV export • ✓ 10 free invoices/month • ✓ No credit card required</p>
          </div>
        </section>

        <footer className="bg-gray-900 text-gray-300 py-12">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="text-center mb-6">
              <h3 className="text-white font-bold mb-2">Connect With Us</h3>
              <p className="text-sm">Email: infotrulybot@gmail.com</p>
              <p className="text-sm mt-1">WhatsApp: +91 9101361482</p>
            </div>
            <div className="border-t border-gray-800 pt-6 text-center">
              <p>&copy; 2025 TrulyInvoice. All rights reserved.</p>
            </div>
          </div>
        </footer>
      </div>
    </>
  )
}
