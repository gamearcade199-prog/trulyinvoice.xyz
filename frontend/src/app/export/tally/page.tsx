import { Metadata } from 'next'
import Link from 'next/link'
import { ArrowRight, CheckCircle2, Database, Zap, Shield, TrendingUp, FileCode, Settings, MapPin, Sparkles, Clock } from 'lucide-react'
import { FAQSchema, SoftwareAppSchema } from '@/components/SeoSchemaMarkup'
import TrulyInvoiceLogo from '@/components/TrulyInvoiceLogo'

export const metadata: Metadata = {
  title: 'Invoice to Tally XML Converter | Auto-Ledger Creation for ERP 9 & Prime | TrulyInvoice',
  description: 'Convert invoices to Tally XML instantly. Auto-creates ledgers, detects place of supply from GSTIN (37 states), generates purchase vouchers. Compatible with Tally ERP 9 & Tally Prime. Free trial.',
  keywords: ['invoice to tally xml', 'convert invoice to tally', 'tally erp invoice import', 'tally prime xml', 'invoice to tally voucher', 'tally auto ledger creation', 'invoice to tally erp9', 'tally xml converter india'],
  openGraph: {
    title: 'Invoice to Tally XML Converter - Auto-Ledger Creation',
    description: 'Convert invoices to Tally XML with automatic ledger creation, GSTIN-based place of supply detection, and purchase voucher generation.',
    images: ['/og-tally-export.jpg'],
    type: 'website',
    locale: 'en_IN',
    url: 'https://trulyinvoice.xyz/export/tally',
  },
  twitter: {
    card: 'summary_large_image',
    title: 'Invoice to Tally XML Converter | TrulyInvoice',
    description: 'Auto-creates ledgers, detects place of supply, generates purchase vouchers for Tally ERP 9 & Prime.',
    images: ['/twitter-tally.jpg'],
  },
  alternates: {
    canonical: 'https://trulyinvoice.xyz/export/tally',
  },
}

export default function TallyExportPage() {
  return (
    <>
      <FAQSchema />
      <SoftwareAppSchema />
      
      <div className="min-h-screen bg-gradient-to-b from-orange-50 via-white to-yellow-50 dark:from-gray-900 dark:via-gray-800 dark:to-gray-900">
        {/* Navigation */}
        <nav className="border-b border-gray-200 dark:border-gray-700 bg-white/80 dark:bg-gray-900/80 backdrop-blur-sm sticky top-0 z-50">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="flex justify-between items-center h-16">
              <Link href="/" className="flex items-center space-x-2">
                <TrulyInvoiceLogo size="sm" />
              </Link>
              <div className="flex items-center space-x-4">
                <Link href="/pricing" className="text-gray-600 dark:text-gray-300 hover:text-orange-600 dark:hover:text-orange-400 font-medium">
                  Pricing
                </Link>
                <Link href="/login" className="px-6 py-2 bg-orange-600 text-white rounded-lg hover:bg-orange-700 font-medium transition-colors">
                  Try Free
                </Link>
              </div>
            </div>
          </div>
        </nav>

        {/* Hero Section */}
        <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20">
          <div className="text-center mb-16">
            <div className="inline-flex items-center space-x-2 bg-orange-100 dark:bg-orange-900/30 text-orange-700 dark:text-orange-300 px-4 py-2 rounded-full text-sm font-medium mb-6">
              <Database className="h-4 w-4" />
              <span>Invoice to Tally XML Converter</span>
            </div>
            
            <h1 className="text-5xl md:text-6xl font-bold text-gray-900 dark:text-white mb-6 leading-tight">
              Convert Invoices to Tally XML<br />
              <span className="bg-gradient-to-r from-orange-600 to-yellow-600 bg-clip-text text-transparent">
                with Auto-Ledger Creation
              </span>
            </h1>
            
            <p className="text-xl text-gray-600 dark:text-gray-300 mb-8 max-w-3xl mx-auto leading-relaxed">
              AI-powered invoice to Tally XML converter. <strong>Automatically creates ledgers</strong>, detects place of supply from GSTIN 
              (all 37 states), and generates ready-to-import purchase vouchers for <strong>Tally ERP 9 & Tally Prime</strong>.
            </p>
            
            <div className="flex flex-col sm:flex-row items-center justify-center space-y-4 sm:space-y-0 sm:space-x-4 mb-12">
              <Link href="/" className="px-8 py-4 bg-blue-600 text-white rounded-lg hover:bg-blue-700 font-semibold text-lg transition-all transform hover:scale-105 shadow-xl flex items-center space-x-2">
                <span>Start Free</span>
                <ArrowRight className="h-5 w-5" />
              </Link>
              <Link href="/pricing" className="px-8 py-4 bg-white dark:bg-gray-800 text-orange-600 dark:text-orange-400 border-2 border-orange-600 dark:border-orange-400 rounded-lg hover:bg-orange-50 dark:hover:bg-gray-700 font-semibold text-lg transition-all">
                View Pricing
              </Link>
            </div>
            
            <div className="flex items-center justify-center space-x-8 text-sm text-gray-600 dark:text-gray-400">
              <div className="flex items-center space-x-2">
                <CheckCircle2 className="h-5 w-5 text-green-600" />
                <span>Tally ERP 9 & Prime</span>
              </div>
              <div className="flex items-center space-x-2">
                <CheckCircle2 className="h-5 w-5 text-green-600" />
                <span>Auto-Ledger Creation</span>
              </div>
              <div className="flex items-center space-x-2">
                <CheckCircle2 className="h-5 w-5 text-green-600" />
                <span>37 States Supported</span>
              </div>
            </div>
          </div>

          {/* Feature Cards */}
          <div className="grid md:grid-cols-3 gap-8 mb-20">
            <div className="bg-white dark:bg-gray-800 p-8 rounded-2xl shadow-lg border border-gray-200 dark:border-gray-700 hover:shadow-xl transition-shadow">
              <div className="w-12 h-12 bg-orange-100 dark:bg-orange-900/30 rounded-lg flex items-center justify-center mb-4">
                <Settings className="h-6 w-6 text-orange-600" />
              </div>
              <h3 className="text-xl font-bold text-gray-900 dark:text-white mb-3">Auto-Ledger Creation</h3>
              <p className="text-gray-600 dark:text-gray-300 leading-relaxed">
                Automatically creates party ledgers, GST ledgers (CGST, SGST, IGST), and expense ledgers. No manual setup in Tally required.
              </p>
            </div>

            <div className="bg-white dark:bg-gray-800 p-8 rounded-2xl shadow-lg border border-gray-200 dark:border-gray-700 hover:shadow-xl transition-shadow">
              <div className="w-12 h-12 bg-yellow-100 dark:bg-yellow-900/30 rounded-lg flex items-center justify-center mb-4">
                <MapPin className="h-6 w-6 text-yellow-600" />
              </div>
              <h3 className="text-xl font-bold text-gray-900 dark:text-white mb-3">Place of Supply Detection</h3>
              <p className="text-gray-600 dark:text-gray-300 leading-relaxed">
                Smart GSTIN-based detection for all 37 Indian states. Automatically determines whether to apply CGST+SGST or IGST.
              </p>
            </div>

            <div className="bg-white dark:bg-gray-800 p-8 rounded-2xl shadow-lg border border-gray-200 dark:border-gray-700 hover:shadow-xl transition-shadow">
              <div className="w-12 h-12 bg-green-100 dark:bg-green-900/30 rounded-lg flex items-center justify-center mb-4">
                <FileCode className="h-6 w-6 text-green-600" />
              </div>
              <h3 className="text-xl font-bold text-gray-900 dark:text-white mb-3">Ready-to-Import XML</h3>
              <p className="text-gray-600 dark:text-gray-300 leading-relaxed">
                Compatible with Tally ERP 9 and Tally Prime. Import via Gateway → Import → Vouchers. Perfect voucher structure with all fields.
              </p>
            </div>
          </div>
        </section>

        {/* How It Works */}
        <section className="bg-white dark:bg-gray-800 py-20">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="text-center mb-16">
              <h2 className="text-4xl font-bold text-gray-900 dark:text-white mb-4">
                Import Invoice to Tally in 4 Steps
              </h2>
              <p className="text-xl text-gray-600 dark:text-gray-300">
                From invoice upload to Tally import in under 30 seconds
              </p>
            </div>

            <div className="grid md:grid-cols-4 gap-8">
              <div className="text-center">
                <div className="w-16 h-16 bg-orange-600 text-white rounded-full flex items-center justify-center text-2xl font-bold mx-auto mb-6">
                  1
                </div>
                <h3 className="text-xl font-bold text-gray-900 dark:text-white mb-4">Upload Invoice</h3>
                <p className="text-gray-600 dark:text-gray-300 leading-relaxed">
                  Upload your supplier invoice (PDF, JPG, or PNG) to TrulyInvoice.
                </p>
              </div>

              <div className="text-center">
                <div className="w-16 h-16 bg-yellow-600 text-white rounded-full flex items-center justify-center text-2xl font-bold mx-auto mb-6">
                  2
                </div>
                <h3 className="text-xl font-bold text-gray-900 dark:text-white mb-4">AI Extracts Data</h3>
                <p className="text-gray-600 dark:text-gray-300 leading-relaxed">
                  AI extracts vendor name, GSTIN, invoice number, amounts, line items, and GST details.
                </p>
              </div>

              <div className="text-center">
                <div className="w-16 h-16 bg-green-600 text-white rounded-full flex items-center justify-center text-2xl font-bold mx-auto mb-6">
                  3
                </div>
                <h3 className="text-xl font-bold text-gray-900 dark:text-white mb-4">Download Tally XML</h3>
                <p className="text-gray-600 dark:text-gray-300 leading-relaxed">
                  Get Tally XML file with auto-created ledgers and purchase voucher ready to import.
                </p>
              </div>

              <div className="text-center">
                <div className="w-16 h-16 bg-blue-600 text-white rounded-full flex items-center justify-center text-2xl font-bold mx-auto mb-6">
                  4
                </div>
                <h3 className="text-xl font-bold text-gray-900 dark:text-white mb-4">Import to Tally</h3>
                <p className="text-gray-600 dark:text-gray-300 leading-relaxed">
                  Open Tally → Gateway → Import → Vouchers → Select XML file. Done in 10 seconds!
                </p>
              </div>
            </div>
          </div>
        </section>

        {/* Tally Features Comparison */}
        <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold text-gray-900 dark:text-white mb-4">
              TrulyInvoice vs Manual Tally Entry
            </h2>
            <p className="text-xl text-gray-600 dark:text-gray-300">
              Eliminate 90% of manual data entry in Tally
            </p>
          </div>

          <div className="overflow-x-auto">
            <table className="w-full bg-white dark:bg-gray-800 rounded-2xl shadow-xl overflow-hidden">
              <thead className="bg-gradient-to-r from-orange-600 to-yellow-600 text-white">
                <tr>
                  <th className="px-6 py-4 text-left text-lg font-semibold">Feature</th>
                  <th className="px-6 py-4 text-center text-lg font-semibold">Manual Tally Entry</th>
                  <th className="px-6 py-4 text-center text-lg font-semibold">TrulyInvoice XML</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-200 dark:divide-gray-700">
                <tr className="hover:bg-gray-50 dark:hover:bg-gray-700/50 transition-colors">
                  <td className="px-6 py-4 font-medium text-gray-900 dark:text-white">Time per Invoice</td>
                  <td className="px-6 py-4 text-center text-red-600 dark:text-red-400 font-semibold">15-20 minutes</td>
                  <td className="px-6 py-4 text-center text-green-600 dark:text-green-400 font-semibold">30 seconds</td>
                </tr>
                <tr className="hover:bg-gray-50 dark:hover:bg-gray-700/50 transition-colors">
                  <td className="px-6 py-4 font-medium text-gray-900 dark:text-white">Ledger Creation</td>
                  <td className="px-6 py-4 text-center text-gray-600 dark:text-gray-400">Create manually each time</td>
                  <td className="px-6 py-4 text-center text-green-600 dark:text-green-400 font-semibold">✓ Auto-created</td>
                </tr>
                <tr className="hover:bg-gray-50 dark:hover:bg-gray-700/50 transition-colors">
                  <td className="px-6 py-4 font-medium text-gray-900 dark:text-white">Place of Supply</td>
                  <td className="px-6 py-4 text-center text-gray-600 dark:text-gray-400">Manual detection</td>
                  <td className="px-6 py-4 text-center text-green-600 dark:text-green-400 font-semibold">✓ Auto from GSTIN (37 states)</td>
                </tr>
                <tr className="hover:bg-gray-50 dark:hover:bg-gray-700/50 transition-colors">
                  <td className="px-6 py-4 font-medium text-gray-900 dark:text-white">Vendor Name Formatting</td>
                  <td className="px-6 py-4 text-center text-gray-600 dark:text-gray-400">Inconsistent case</td>
                  <td className="px-6 py-4 text-center text-green-600 dark:text-green-400 font-semibold">✓ Normalized Title Case</td>
                </tr>
                <tr className="hover:bg-gray-50 dark:hover:bg-gray-700/50 transition-colors">
                  <td className="px-6 py-4 font-medium text-gray-900 dark:text-white">GST Ledgers (CGST/SGST/IGST)</td>
                  <td className="px-6 py-4 text-center text-gray-600 dark:text-gray-400">Manual selection</td>
                  <td className="px-6 py-4 text-center text-green-600 dark:text-green-400 font-semibold">✓ Auto-selected correctly</td>
                </tr>
                <tr className="hover:bg-gray-50 dark:hover:bg-gray-700/50 transition-colors">
                  <td className="px-6 py-4 font-medium text-gray-900 dark:text-white">Zero-GST Invoices</td>
                  <td className="px-6 py-4 text-center text-gray-600 dark:text-gray-400">Often errors in ledger name</td>
                  <td className="px-6 py-4 text-center text-green-600 dark:text-green-400 font-semibold">✓ "Purchase - Non-GST" ledger</td>
                </tr>
                <tr className="hover:bg-gray-50 dark:hover:bg-gray-700/50 transition-colors">
                  <td className="px-6 py-4 font-medium text-gray-900 dark:text-white">Bulk Upload (50 invoices)</td>
                  <td className="px-6 py-4 text-center text-red-600 dark:text-red-400 font-semibold">12-15 hours</td>
                  <td className="px-6 py-4 text-center text-green-600 dark:text-green-400 font-semibold">25 minutes</td>
                </tr>
                <tr className="hover:bg-gray-50 dark:hover:bg-gray-700/50 transition-colors">
                  <td className="px-6 py-4 font-medium text-gray-900 dark:text-white">Data Entry Errors</td>
                  <td className="px-6 py-4 text-center text-red-600 dark:text-red-400 font-semibold">10-15% error rate</td>
                  <td className="px-6 py-4 text-center text-green-600 dark:text-green-400 font-semibold">&lt; 1% with validation</td>
                </tr>
              </tbody>
            </table>
          </div>

          <div className="mt-12 text-center">
            <p className="text-xl text-gray-600 dark:text-gray-300 mb-6">
              <strong className="text-orange-600 dark:text-orange-400">Save 96% of your time</strong> on Tally data entry
            </p>
            <Link href="/signup" className="inline-flex items-center px-8 py-4 bg-gradient-to-r from-orange-600 to-yellow-600 text-white rounded-lg hover:from-orange-700 hover:to-yellow-700 font-semibold text-lg transition-all transform hover:scale-105 shadow-xl space-x-2">
              <span>Start Converting for Free</span>
              <ArrowRight className="h-5 w-5" />
            </Link>
          </div>
        </section>

        {/* Auto-Ledger Feature Highlight */}
        <section className="bg-gradient-to-br from-orange-50 to-yellow-50 dark:from-gray-800 dark:to-gray-900 py-20">
          <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="text-center mb-12">
              <h2 className="text-4xl font-bold text-gray-900 dark:text-white mb-4">
                🎯 Auto-Ledger Creation - Our Secret Sauce
              </h2>
              <p className="text-xl text-gray-600 dark:text-gray-300">
                No other tool offers automatic Tally ledger creation!
              </p>
            </div>

            <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-2xl p-8 border-2 border-orange-200 dark:border-orange-700">
              <h3 className="text-2xl font-bold text-gray-900 dark:text-white mb-6">What Gets Auto-Created:</h3>
              
              <div className="space-y-4">
                <div className="flex items-start space-x-3">
                  <CheckCircle2 className="h-6 w-6 text-green-600 flex-shrink-0 mt-1" />
                  <div>
                    <h4 className="font-bold text-gray-900 dark:text-white">Party Ledger</h4>
                    <p className="text-gray-600 dark:text-gray-300">Vendor name in Title Case (e.g., "ABC Suppliers Pvt Ltd")</p>
                  </div>
                </div>

                <div className="flex items-start space-x-3">
                  <CheckCircle2 className="h-6 w-6 text-green-600 flex-shrink-0 mt-1" />
                  <div>
                    <h4 className="font-bold text-gray-900 dark:text-white">GST Ledgers</h4>
                    <p className="text-gray-600 dark:text-gray-300">CGST, SGST, or IGST ledgers based on place of supply detection</p>
                  </div>
                </div>

                <div className="flex items-start space-x-3">
                  <CheckCircle2 className="h-6 w-6 text-green-600 flex-shrink-0 mt-1" />
                  <div>
                    <h4 className="font-bold text-gray-900 dark:text-white">Expense Ledger</h4>
                    <p className="text-gray-600 dark:text-gray-300">"Purchase @ 18%" or "Purchase - Non-GST" for exempt supplies</p>
                  </div>
                </div>

                <div className="flex items-start space-x-3">
                  <CheckCircle2 className="h-6 w-6 text-green-600 flex-shrink-0 mt-1" />
                  <div>
                    <h4 className="font-bold text-gray-900 dark:text-white">Place of Supply</h4>
                    <p className="text-gray-600 dark:text-gray-300">Auto-detected from GSTIN state codes (01-Maharashtra, 29-Karnataka, etc.)</p>
                  </div>
                </div>

                <div className="flex items-start space-x-3">
                  <CheckCircle2 className="h-6 w-6 text-green-600 flex-shrink-0 mt-1" />
                  <div>
                    <h4 className="font-bold text-gray-900 dark:text-white">Voucher Type</h4>
                    <p className="text-gray-600 dark:text-gray-300">Purchase voucher with proper debit/credit entries</p>
                  </div>
                </div>
              </div>

              <div className="mt-8 p-4 bg-orange-50 dark:bg-orange-900/20 rounded-lg border border-orange-200 dark:border-orange-700">
                <p className="text-orange-800 dark:text-orange-300 font-semibold">
                  💡 <strong>Pro Tip:</strong> All ledgers are created under proper groups. Party ledgers under "Sundry Creditors", 
                  GST ledgers under "Duties & Taxes", and expense ledgers under "Purchase Accounts".
                </p>
              </div>
            </div>
          </div>
        </section>

        {/* CTA Section */}
        <section className="bg-gradient-to-r from-orange-600 to-yellow-600 py-20">
          <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
            <h2 className="text-4xl font-bold text-white mb-6">
              Stop Manual Tally Entry. Start Smart XML Import.
            </h2>
            <p className="text-xl text-orange-100 mb-8">
              Join 5,000+ Indian businesses using TrulyInvoice to automate Tally data entry
            </p>
            <div className="flex flex-col sm:flex-row items-center justify-center space-y-4 sm:space-y-0 sm:space-x-4">
              <Link href="/signup" className="px-8 py-4 bg-white text-orange-600 rounded-lg hover:bg-gray-100 font-semibold text-lg transition-all transform hover:scale-105 shadow-xl flex items-center space-x-2">
                <span>Get Started Free</span>
                <ArrowRight className="h-5 w-5" />
              </Link>
              <Link href="/pricing" className="px-8 py-4 bg-orange-700 text-white border-2 border-white rounded-lg hover:bg-orange-800 font-semibold text-lg transition-all">
                View All Plans
              </Link>
            </div>
            <p className="text-orange-100 mt-6">
              ✓ Works with Tally ERP 9 & Prime • ✓ Auto-ledger creation • ✓ 10 free imports/month
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
                <p className="text-sm mt-2">Automating Tally for Indian businesses</p>
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
