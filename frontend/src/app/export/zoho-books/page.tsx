'use client'

import Link from 'next/link'
import { ArrowRight, CheckCircle2, Table2, Zap, Shield, FileSpreadsheet, List, Clock } from 'lucide-react'
import { FAQSchema, SoftwareAppSchema } from '@/components/SeoSchemaMarkup'
import TrulyInvoiceLogo from '@/components/TrulyInvoiceLogo'

export default function ZohoBooksExportPage() {
  return (
    <>
      <FAQSchema />
      <SoftwareAppSchema />
      
      <div className="min-h-screen bg-gradient-to-b from-red-50 via-white to-orange-50 dark:from-gray-900 dark:via-gray-800 dark:to-gray-900">
        <nav className="border-b border-gray-200 dark:border-gray-700 bg-white/80 dark:bg-gray-900/80 backdrop-blur-sm sticky top-0 z-50">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="flex justify-between items-center h-16">
              <Link href="/" className="flex items-center space-x-2">
                <TrulyInvoiceLogo size="sm" />
              </Link>
              <div className="flex items-center space-x-4">
                <Link href="/pricing" className="text-gray-600 dark:text-gray-300 hover:text-red-600 font-medium">Pricing</Link>
                <Link href="/login" className="px-6 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 font-medium transition-colors">Try Free</Link>
              </div>
            </div>
          </div>
        </nav>

        <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20">
          <div className="text-center mb-16">
            <div className="inline-flex items-center space-x-2 bg-red-100 dark:bg-red-900/30 text-red-700 dark:text-red-300 px-4 py-2 rounded-full text-sm font-medium mb-6">
              <Table2 className="h-4 w-4" />
              <span>Invoice to Zoho Books CSV Converter</span>
            </div>
            
            <h1 className="text-5xl md:text-6xl font-bold text-gray-900 dark:text-white mb-6 leading-tight">
              Convert Invoices to Zoho Books<br />
              <span className="bg-gradient-to-r from-red-600 to-orange-600 bg-clip-text text-transparent">
                37-Column CSV Export
              </span>
            </h1>
            
            <p className="text-xl text-gray-600 dark:text-gray-300 mb-8 max-w-3xl mx-auto leading-relaxed">
              AI-powered invoice to Zoho Books CSV converter with <strong>37 comprehensive columns</strong>: payment terms, 
              billing address, item descriptions, discount %, notes, terms & conditions. <strong>Fully compatible</strong> with Zoho Books import.
            </p>
            
            <div className="flex flex-col sm:flex-row items-center justify-center space-y-4 sm:space-y-0 sm:space-x-4 mb-12">
              <Link href="/" className="px-8 py-4 bg-blue-600 text-white rounded-lg hover:bg-blue-700 font-semibold text-lg transition-all transform hover:scale-105 shadow-xl flex items-center space-x-2">
                <span>Start Free</span>
                <ArrowRight className="h-5 w-5" />
              </Link>
              <Link href="/pricing" className="px-8 py-4 bg-white dark:bg-gray-800 text-red-600 dark:text-red-400 border-2 border-red-600 rounded-lg hover:bg-red-50 dark:hover:bg-gray-700 font-semibold text-lg transition-all">
                View Pricing
              </Link>
            </div>
            
            <div className="flex items-center justify-center space-x-8 text-sm text-gray-600 dark:text-gray-400">
              <div className="flex items-center space-x-2">
                <CheckCircle2 className="h-5 w-5 text-green-600" />
                <span>37 Columns Included</span>
              </div>
              <div className="flex items-center space-x-2">
                <CheckCircle2 className="h-5 w-5 text-green-600" />
                <span>Zoho Books Compatible</span>
              </div>
              <div className="flex items-center space-x-2">
                <CheckCircle2 className="h-5 w-5 text-green-600" />
                <span>10 Free/Month</span>
              </div>
            </div>
          </div>

          <div className="grid md:grid-cols-3 gap-8">
            <div className="bg-white dark:bg-gray-800 p-8 rounded-2xl shadow-lg border border-gray-200 dark:border-gray-700">
              <div className="w-12 h-12 bg-red-100 dark:bg-red-900/30 rounded-lg flex items-center justify-center mb-4">
                <FileSpreadsheet className="h-6 w-6 text-red-600" />
              </div>
              <h3 className="text-xl font-bold text-gray-900 dark:text-white mb-3">37 Comprehensive Columns</h3>
              <p className="text-gray-600 dark:text-gray-300">
                Customer Name, Invoice Number, Date, Due Date, Payment Terms, Item Name, Description, Quantity, Unit, Rate, Discount %, Tax %, Amount, Addresses, Notes, Terms & Conditions, and more.
              </p>
            </div>

            <div className="bg-white dark:bg-gray-800 p-8 rounded-2xl shadow-lg border border-gray-200 dark:border-gray-700">
              <div className="w-12 h-12 bg-orange-100 dark:bg-orange-900/30 rounded-lg flex items-center justify-center mb-4">
                <Zap className="h-6 w-6 text-orange-600" />
              </div>
              <h3 className="text-xl font-bold text-gray-900 dark:text-white mb-3">Smart Default Values</h3>
              <p className="text-gray-600 dark:text-gray-300">
                Automatically fills payment terms, currency, tax types, and other fields with intelligent defaults based on Indian GST invoices.
              </p>
            </div>

            <div className="bg-white dark:bg-gray-800 p-8 rounded-2xl shadow-lg border border-gray-200 dark:border-gray-700">
              <div className="w-12 h-12 bg-green-100 dark:bg-green-900/30 rounded-lg flex items-center justify-center mb-4">
                <Shield className="h-6 w-6 text-green-600" />
              </div>
              <h3 className="text-xl font-bold text-gray-900 dark:text-white mb-3">Import-Ready Format</h3>
              <p className="text-gray-600 dark:text-gray-300">
                CSV format matches Zoho Books import requirements exactly. No manual field mapping needed. Import directly via Zoho Books → Import → Bills.
              </p>
            </div>
          </div>
        </section>

        <section className="bg-white dark:bg-gray-800 py-20">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="text-center mb-16">
              <h2 className="text-4xl font-bold text-gray-900 dark:text-white mb-4">37 Columns Explained</h2>
              <p className="text-xl text-gray-600 dark:text-gray-300">Every field Zoho Books needs, automatically filled</p>
            </div>

            <div className="grid md:grid-cols-2 gap-8">
              <div className="bg-red-50 dark:bg-red-900/10 p-8 rounded-2xl border border-red-200 dark:border-red-700">
                <h3 className="text-2xl font-bold text-gray-900 dark:text-white mb-6">Invoice Header Fields (12)</h3>
                <ul className="space-y-3 text-gray-700 dark:text-gray-300">
                  <li className="flex items-start space-x-2"><CheckCircle2 className="h-5 w-5 text-red-600 flex-shrink-0 mt-0.5" /><span>Customer/Vendor Name</span></li>
                  <li className="flex items-start space-x-2"><CheckCircle2 className="h-5 w-5 text-red-600 flex-shrink-0 mt-0.5" /><span>Invoice Number</span></li>
                  <li className="flex items-start space-x-2"><CheckCircle2 className="h-5 w-5 text-red-600 flex-shrink-0 mt-0.5" /><span>Invoice Date</span></li>
                  <li className="flex items-start space-x-2"><CheckCircle2 className="h-5 w-5 text-red-600 flex-shrink-0 mt-0.5" /><span>Due Date</span></li>
                  <li className="flex items-start space-x-2"><CheckCircle2 className="h-5 w-5 text-red-600 flex-shrink-0 mt-0.5" /><span>Payment Terms (Net 30/Net 15)</span></li>
                  <li className="flex items-start space-x-2"><CheckCircle2 className="h-5 w-5 text-red-600 flex-shrink-0 mt-0.5" /><span>Currency (INR)</span></li>
                  <li className="flex items-start space-x-2"><CheckCircle2 className="h-5 w-5 text-red-600 flex-shrink-0 mt-0.5" /><span>Exchange Rate</span></li>
                  <li className="flex items-start space-x-2"><CheckCircle2 className="h-5 w-5 text-red-600 flex-shrink-0 mt-0.5" /><span>Reference Number</span></li>
                  <li className="flex items-start space-x-2"><CheckCircle2 className="h-5 w-5 text-red-600 flex-shrink-0 mt-0.5" /><span>Notes</span></li>
                  <li className="flex items-start space-x-2"><CheckCircle2 className="h-5 w-5 text-red-600 flex-shrink-0 mt-0.5" /><span>Terms & Conditions</span></li>
                  <li className="flex items-start space-x-2"><CheckCircle2 className="h-5 w-5 text-red-600 flex-shrink-0 mt-0.5" /><span>Customer Email</span></li>
                  <li className="flex items-start space-x-2"><CheckCircle2 className="h-5 w-5 text-red-600 flex-shrink-0 mt-0.5" /><span>Customer Phone</span></li>
                </ul>
              </div>

              <div className="bg-orange-50 dark:bg-orange-900/10 p-8 rounded-2xl border border-orange-200 dark:border-orange-700">
                <h3 className="text-2xl font-bold text-gray-900 dark:text-white mb-6">Line Item Fields (15)</h3>
                <ul className="space-y-3 text-gray-700 dark:text-gray-300">
                  <li className="flex items-start space-x-2"><CheckCircle2 className="h-5 w-5 text-orange-600 flex-shrink-0 mt-0.5" /><span>Item Name/Product</span></li>
                  <li className="flex items-start space-x-2"><CheckCircle2 className="h-5 w-5 text-orange-600 flex-shrink-0 mt-0.5" /><span>Item Description</span></li>
                  <li className="flex items-start space-x-2"><CheckCircle2 className="h-5 w-5 text-orange-600 flex-shrink-0 mt-0.5" /><span>Quantity</span></li>
                  <li className="flex items-start space-x-2"><CheckCircle2 className="h-5 w-5 text-orange-600 flex-shrink-0 mt-0.5" /><span>Unit (Pcs, Kgs, Ltrs)</span></li>
                  <li className="flex items-start space-x-2"><CheckCircle2 className="h-5 w-5 text-orange-600 flex-shrink-0 mt-0.5" /><span>Rate/Unit Price</span></li>
                  <li className="flex items-start space-x-2"><CheckCircle2 className="h-5 w-5 text-orange-600 flex-shrink-0 mt-0.5" /><span>Discount %</span></li>
                  <li className="flex items-start space-x-2"><CheckCircle2 className="h-5 w-5 text-orange-600 flex-shrink-0 mt-0.5" /><span>Discount Amount</span></li>
                  <li className="flex items-start space-x-2"><CheckCircle2 className="h-5 w-5 text-orange-600 flex-shrink-0 mt-0.5" /><span>Tax Name (GST/IGST)</span></li>
                  <li className="flex items-start space-x-2"><CheckCircle2 className="h-5 w-5 text-orange-600 flex-shrink-0 mt-0.5" /><span>Tax %</span></li>
                  <li className="flex items-start space-x-2"><CheckCircle2 className="h-5 w-5 text-orange-600 flex-shrink-0 mt-0.5" /><span>Tax Amount</span></li>
                  <li className="flex items-start space-x-2"><CheckCircle2 className="h-5 w-5 text-orange-600 flex-shrink-0 mt-0.5" /><span>HSN/SAC Code</span></li>
                  <li className="flex items-start space-x-2"><CheckCircle2 className="h-5 w-5 text-orange-600 flex-shrink-0 mt-0.5" /><span>Item Total</span></li>
                  <li className="flex items-start space-x-2"><CheckCircle2 className="h-5 w-5 text-orange-600 flex-shrink-0 mt-0.5" /><span>Account Name</span></li>
                  <li className="flex items-start space-x-2"><CheckCircle2 className="h-5 w-5 text-orange-600 flex-shrink-0 mt-0.5" /><span>Item Type (Goods/Service)</span></li>
                  <li className="flex items-start space-x-2"><CheckCircle2 className="h-5 w-5 text-orange-600 flex-shrink-0 mt-0.5" /><span>SKU/Product Code</span></li>
                </ul>
              </div>

              <div className="bg-green-50 dark:bg-green-900/10 p-8 rounded-2xl border border-green-200 dark:border-green-700">
                <h3 className="text-2xl font-bold text-gray-900 dark:text-white mb-6">Address Fields (6)</h3>
                <ul className="space-y-3 text-gray-700 dark:text-gray-300">
                  <li className="flex items-start space-x-2"><CheckCircle2 className="h-5 w-5 text-green-600 flex-shrink-0 mt-0.5" /><span>Billing Address Line 1</span></li>
                  <li className="flex items-start space-x-2"><CheckCircle2 className="h-5 w-5 text-green-600 flex-shrink-0 mt-0.5" /><span>Billing City</span></li>
                  <li className="flex items-start space-x-2"><CheckCircle2 className="h-5 w-5 text-green-600 flex-shrink-0 mt-0.5" /><span>Billing State</span></li>
                  <li className="flex items-start space-x-2"><CheckCircle2 className="h-5 w-5 text-green-600 flex-shrink-0 mt-0.5" /><span>Billing ZIP/Pincode</span></li>
                  <li className="flex items-start space-x-2"><CheckCircle2 className="h-5 w-5 text-green-600 flex-shrink-0 mt-0.5" /><span>Shipping Address</span></li>
                  <li className="flex items-start space-x-2"><CheckCircle2 className="h-5 w-5 text-green-600 flex-shrink-0 mt-0.5" /><span>Shipping State (Place of Supply)</span></li>
                </ul>
              </div>

              <div className="bg-blue-50 dark:bg-blue-900/10 p-8 rounded-2xl border border-blue-200 dark:border-blue-700">
                <h3 className="text-2xl font-bold text-gray-900 dark:text-white mb-6">Total Fields (4)</h3>
                <ul className="space-y-3 text-gray-700 dark:text-gray-300">
                  <li className="flex items-start space-x-2"><CheckCircle2 className="h-5 w-5 text-blue-600 flex-shrink-0 mt-0.5" /><span>Sub Total</span></li>
                  <li className="flex items-start space-x-2"><CheckCircle2 className="h-5 w-5 text-blue-600 flex-shrink-0 mt-0.5" /><span>Total Tax</span></li>
                  <li className="flex items-start space-x-2"><CheckCircle2 className="h-5 w-5 text-blue-600 flex-shrink-0 mt-0.5" /><span>Discount Total</span></li>
                  <li className="flex items-start space-x-2"><CheckCircle2 className="h-5 w-5 text-blue-600 flex-shrink-0 mt-0.5" /><span>Grand Total</span></li>
                </ul>
              </div>
            </div>
          </div>
        </section>

        <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20">
          <div className="text-center mb-12">
            <h2 className="text-4xl font-bold text-gray-900 dark:text-white mb-4">Import to Zoho Books in 3 Steps</h2>
          </div>

          <div className="grid md:grid-cols-3 gap-12">
            <div className="text-center">
              <div className="w-16 h-16 bg-red-600 text-white rounded-full flex items-center justify-center text-2xl font-bold mx-auto mb-6">1</div>
              <h3 className="text-2xl font-bold text-gray-900 dark:text-white mb-4">Upload Invoice</h3>
              <p className="text-gray-600 dark:text-gray-300">Upload PDF or image invoice. AI extracts all 37 fields automatically.</p>
            </div>
            <div className="text-center">
              <div className="w-16 h-16 bg-orange-600 text-white rounded-full flex items-center justify-center text-2xl font-bold mx-auto mb-6">2</div>
              <h3 className="text-2xl font-bold text-gray-900 dark:text-white mb-4">Download CSV</h3>
              <p className="text-gray-600 dark:text-gray-300">Get Zoho Books compatible CSV with all 37 columns filled with smart defaults.</p>
            </div>
            <div className="text-center">
              <div className="w-16 h-16 bg-green-600 text-white rounded-full flex items-center justify-center text-2xl font-bold mx-auto mb-6">3</div>
              <h3 className="text-2xl font-bold text-gray-900 dark:text-white mb-4">Import to Zoho</h3>
              <p className="text-gray-600 dark:text-gray-300">Settings → Import → Bills → Upload CSV. Done!</p>
            </div>
          </div>
        </section>

        <section className="bg-gradient-to-r from-red-600 to-orange-600 py-20">
          <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
            <h2 className="text-4xl font-bold text-white mb-6">Automate Zoho Books Invoice Import</h2>
            <p className="text-xl text-red-100 mb-8">37 columns. Zero manual field mapping. Perfect for Indian GST invoices.</p>
            <Link href="/signup" className="px-8 py-4 bg-white text-red-600 rounded-lg hover:bg-gray-100 font-semibold text-lg transition-all transform hover:scale-105 shadow-xl inline-flex items-center space-x-2">
              <span>Get Started Free</span>
              <ArrowRight className="h-5 w-5" />
            </Link>
            <p className="text-red-100 mt-6">✓ 37-column CSV • ✓ 10 free conversions/month • ✓ No credit card required</p>
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
