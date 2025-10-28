import { Metadata } from 'next'
import Link from 'next/link'
import { ArrowRight, CheckCircle2, DollarSign, Zap, Shield, FileText, Download, Briefcase, Wallet, Clock } from 'lucide-react'
import { FAQSchema, SoftwareAppSchema } from '@/components/SeoSchemaMarkup'
import TrulyInvoiceLogo from '@/components/TrulyInvoiceLogo'

export const metadata: Metadata = {
  title: 'Invoice to QuickBooks Converter | IIF (Desktop) & CSV (Online) | TrulyInvoice',
  description: 'Export invoices to QuickBooks Desktop (IIF) or QuickBooks Online (CSV). Dual format support, auto-balancing entries, vendor management, tax calculations. Free 10 invoices/month.',
  keywords: ['invoice to quickbooks', 'quickbooks iif converter', 'quickbooks csv import', 'invoice to qbo', 'quickbooks desktop import', 'quickbooks online upload', 'invoice to quickbooks india'],
  openGraph: {
    title: 'Invoice to QuickBooks Converter - IIF & CSV Export',
    description: 'Convert invoices to QuickBooks Desktop (IIF) or QuickBooks Online (CSV) with dual format support.',
    images: ['/og-quickbooks-export.jpg'],
    type: 'website',
    locale: 'en_IN',
    url: 'https://trulyinvoice.xyz/export/quickbooks',
  },
  twitter: {
    card: 'summary_large_image',
    title: 'Invoice to QuickBooks Converter | TrulyInvoice',
    description: 'Dual format support: IIF for Desktop, CSV for Online. Automatic vendor management and tax calculations.',
    images: ['/twitter-quickbooks.jpg'],
  },
  alternates: {
    canonical: 'https://trulyinvoice.xyz/export/quickbooks',
  },
}

export default function QuickBooksExportPage() {
  return (
    <>
      <FAQSchema />
      <SoftwareAppSchema />
      
      <div className="min-h-screen bg-gradient-to-b from-green-50 via-white to-blue-50 dark:from-gray-900 dark:via-gray-800 dark:to-gray-900">
        {/* Navigation */}
        <nav className="border-b border-gray-200 dark:border-gray-700 bg-white/80 dark:bg-gray-900/80 backdrop-blur-sm sticky top-0 z-50">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="flex justify-between items-center h-16">
              <Link href="/" className="flex items-center space-x-2">
                <TrulyInvoiceLogo size="sm" />
              </Link>
              <div className="flex items-center space-x-4">
                <Link href="/pricing" className="text-gray-600 dark:text-gray-300 hover:text-green-600 dark:hover:text-green-400 font-medium">
                  Pricing
                </Link>
                <Link href="/login" className="px-6 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 font-medium transition-colors">
                  Try Free
                </Link>
              </div>
            </div>
          </div>
        </nav>

        {/* Hero Section */}
        <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20">
          <div className="text-center mb-16">
            <div className="inline-flex items-center space-x-2 bg-green-100 dark:bg-green-900/30 text-green-700 dark:text-green-300 px-4 py-2 rounded-full text-sm font-medium mb-6">
              <DollarSign className="h-4 w-4" />
              <span>Invoice to QuickBooks Converter</span>
            </div>
            
            <h1 className="text-5xl md:text-6xl font-bold text-gray-900 dark:text-white mb-6 leading-tight">
              Convert Invoices to QuickBooks<br />
              <span className="bg-gradient-to-r from-green-600 to-blue-600 bg-clip-text text-transparent">
                IIF for Desktop, CSV for Online
              </span>
            </h1>
            
            <p className="text-xl text-gray-600 dark:text-gray-300 mb-8 max-w-3xl mx-auto leading-relaxed">
              AI-powered invoice to QuickBooks converter with <strong>dual format support</strong>. Get IIF files for QuickBooks Desktop 
              or CSV files for QuickBooks Online. Auto-balancing entries, vendor management, and tax calculations included.
            </p>
            
            <div className="flex flex-col sm:flex-row items-center justify-center space-y-4 sm:space-y-0 sm:space-x-4 mb-12">
              <Link href="/" className="px-8 py-4 bg-blue-600 text-white rounded-lg hover:bg-blue-700 font-semibold text-lg transition-all transform hover:scale-105 shadow-xl flex items-center space-x-2">
                <span>Start Free</span>
                <ArrowRight className="h-5 w-5" />
              </Link>
              <Link href="/pricing" className="px-8 py-4 bg-white dark:bg-gray-800 text-green-600 dark:text-green-400 border-2 border-green-600 dark:border-green-400 rounded-lg hover:bg-green-50 dark:hover:bg-gray-700 font-semibold text-lg transition-all">
                View Pricing
              </Link>
            </div>
            
            <div className="flex items-center justify-center space-x-8 text-sm text-gray-600 dark:text-gray-400">
              <div className="flex items-center space-x-2">
                <CheckCircle2 className="h-5 w-5 text-green-600" />
                <span>Desktop & Online Support</span>
              </div>
              <div className="flex items-center space-x-2">
                <CheckCircle2 className="h-5 w-5 text-green-600" />
                <span>Auto-Balancing Entries</span>
              </div>
              <div className="flex items-center space-x-2">
                <CheckCircle2 className="h-5 w-5 text-green-600" />
                <span>10 Free/Month</span>
              </div>
            </div>
          </div>

          {/* Dual Format Feature */}
          <div className="grid md:grid-cols-2 gap-8 mb-20">
            <div className="bg-gradient-to-br from-green-50 to-green-100 dark:from-green-900/20 dark:to-green-800/20 p-8 rounded-2xl shadow-lg border-2 border-green-200 dark:border-green-700">
              <div className="w-12 h-12 bg-green-600 text-white rounded-lg flex items-center justify-center mb-4">
                <FileText className="h-6 w-6" />
              </div>
              <h3 className="text-2xl font-bold text-gray-900 dark:text-white mb-3">QuickBooks Desktop (IIF)</h3>
              <p className="text-gray-700 dark:text-gray-300 leading-relaxed mb-4">
                Get IIF files compatible with QuickBooks Desktop (Pro, Premier, Enterprise). Includes proper debit/credit entries, 
                vendor details, and balanced journal entries.
              </p>
              <ul className="space-y-2 text-gray-700 dark:text-gray-300">
                <li className="flex items-center space-x-2">
                  <CheckCircle2 className="h-5 w-5 text-green-600 flex-shrink-0" />
                  <span>IIF format with proper Dr/Cr balancing</span>
                </li>
                <li className="flex items-center space-x-2">
                  <CheckCircle2 className="h-5 w-5 text-green-600 flex-shrink-0" />
                  <span>Vendor name and invoice details</span>
                </li>
                <li className="flex items-center space-x-2">
                  <CheckCircle2 className="h-5 w-5 text-green-600 flex-shrink-0" />
                  <span>Tax calculations and accounts</span>
                </li>
              </ul>
            </div>

            <div className="bg-gradient-to-br from-blue-50 to-blue-100 dark:from-blue-900/20 dark:to-blue-800/20 p-8 rounded-2xl shadow-lg border-2 border-blue-200 dark:border-blue-700">
              <div className="w-12 h-12 bg-blue-600 text-white rounded-lg flex items-center justify-center mb-4">
                <Briefcase className="h-6 w-6" />
              </div>
              <h3 className="text-2xl font-bold text-gray-900 dark:text-white mb-3">QuickBooks Online (CSV)</h3>
              <p className="text-gray-700 dark:text-gray-300 leading-relaxed mb-4">
                Get CSV files ready to import into QuickBooks Online. Perfect for cloud-based accounting with automatic 
                field mapping and vendor creation.
              </p>
              <ul className="space-y-2 text-gray-700 dark:text-gray-300">
                <li className="flex items-center space-x-2">
                  <CheckCircle2 className="h-5 w-5 text-blue-600 flex-shrink-0" />
                  <span>CSV format for QBO import</span>
                </li>
                <li className="flex items-center space-x-2">
                  <CheckCircle2 className="h-5 w-5 text-blue-600 flex-shrink-0" />
                  <span>Auto field mapping to QBO columns</span>
                </li>
                <li className="flex items-center space-x-2">
                  <CheckCircle2 className="h-5 w-5 text-blue-600 flex-shrink-0" />
                  <span>Vendor auto-creation support</span>
                </li>
              </ul>
            </div>
          </div>
        </section>

        {/* How It Works */}
        <section className="bg-white dark:bg-gray-800 py-20">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="text-center mb-16">
              <h2 className="text-4xl font-bold text-gray-900 dark:text-white mb-4">
                Import Invoice to QuickBooks in 3 Steps
              </h2>
              <p className="text-xl text-gray-600 dark:text-gray-300">
                Choose your QuickBooks version and import in seconds
              </p>
            </div>

            <div className="grid md:grid-cols-3 gap-12">
              <div className="text-center">
                <div className="w-16 h-16 bg-green-600 text-white rounded-full flex items-center justify-center text-2xl font-bold mx-auto mb-6">
                  1
                </div>
                <h3 className="text-2xl font-bold text-gray-900 dark:text-white mb-4">Upload & Process</h3>
                <p className="text-gray-600 dark:text-gray-300 leading-relaxed">
                  Upload your invoice (PDF/JPG/PNG). AI extracts vendor, amount, date, tax details with 99% accuracy.
                </p>
              </div>

              <div className="text-center">
                <div className="w-16 h-16 bg-blue-600 text-white rounded-full flex items-center justify-center text-2xl font-bold mx-auto mb-6">
                  2
                </div>
                <h3 className="text-2xl font-bold text-gray-900 dark:text-white mb-4">Choose Format</h3>
                <p className="text-gray-600 dark:text-gray-300 leading-relaxed">
                  Select IIF (Desktop) or CSV (Online). We'll ask which QuickBooks version you use and generate the right format.
                </p>
              </div>

              <div className="text-center">
                <div className="w-16 h-16 bg-purple-600 text-white rounded-full flex items-center justify-center text-2xl font-bold mx-auto mb-6">
                  3
                </div>
                <h3 className="text-2xl font-bold text-gray-900 dark:text-white mb-4">Import to QuickBooks</h3>
                <p className="text-gray-600 dark:text-gray-300 leading-relaxed">
                  Desktop: File → Utilities → Import → IIF. Online: Settings → Import → Bills. Done!
                </p>
              </div>
            </div>
          </div>
        </section>

        {/* Comparison Table */}
        <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold text-gray-900 dark:text-white mb-4">
              Why Choose TrulyInvoice for QuickBooks?
            </h2>
          </div>

          <div className="overflow-x-auto">
            <table className="w-full bg-white dark:bg-gray-800 rounded-2xl shadow-xl overflow-hidden">
              <thead className="bg-gradient-to-r from-green-600 to-blue-600 text-white">
                <tr>
                  <th className="px-6 py-4 text-left text-lg font-semibold">Feature</th>
                  <th className="px-6 py-4 text-center text-lg font-semibold">Manual QuickBooks Entry</th>
                  <th className="px-6 py-4 text-center text-lg font-semibold">TrulyInvoice</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-200 dark:divide-gray-700">
                <tr>
                  <td className="px-6 py-4 font-medium text-gray-900 dark:text-white">Time per Invoice</td>
                  <td className="px-6 py-4 text-center text-red-600 font-semibold">8-12 minutes</td>
                  <td className="px-6 py-4 text-center text-green-600 font-semibold">Under 10 seconds</td>
                </tr>
                <tr>
                  <td className="px-6 py-4 font-medium text-gray-900 dark:text-white">Desktop + Online Support</td>
                  <td className="px-6 py-4 text-center text-gray-600">Manual for each</td>
                  <td className="px-6 py-4 text-center text-green-600 font-semibold">✓ Dual format (IIF + CSV)</td>
                </tr>
                <tr>
                  <td className="px-6 py-4 font-medium text-gray-900 dark:text-white">Vendor Auto-Creation</td>
                  <td className="px-6 py-4 text-center text-gray-600">Manual setup</td>
                  <td className="px-6 py-4 text-center text-green-600 font-semibold">✓ Automatic</td>
                </tr>
                <tr>
                  <td className="px-6 py-4 font-medium text-gray-900 dark:text-white">Tax Calculations</td>
                  <td className="px-6 py-4 text-center text-gray-600">Manual entry</td>
                  <td className="px-6 py-4 text-center text-green-600 font-semibold">✓ Auto-calculated</td>
                </tr>
                <tr>
                  <td className="px-6 py-4 font-medium text-gray-900 dark:text-white">Balanced Entries (IIF)</td>
                  <td className="px-6 py-4 text-center text-gray-600">Manual balancing</td>
                  <td className="px-6 py-4 text-center text-green-600 font-semibold">✓ Auto-balanced Dr/Cr</td>
                </tr>
              </tbody>
            </table>
          </div>

          <div className="mt-12 text-center">
            <Link href="/signup" className="inline-flex items-center px-8 py-4 bg-gradient-to-r from-green-600 to-blue-600 text-white rounded-lg hover:from-green-700 hover:to-blue-700 font-semibold text-lg transition-all transform hover:scale-105 shadow-xl space-x-2">
              <span>Start Converting for Free</span>
              <ArrowRight className="h-5 w-5" />
            </Link>
          </div>
        </section>

        {/* CTA */}
        <section className="bg-gradient-to-r from-green-600 to-blue-600 py-20">
          <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
            <h2 className="text-4xl font-bold text-white mb-6">
              Automate QuickBooks Invoice Import Today
            </h2>
            <p className="text-xl text-green-100 mb-8">
              Works with QuickBooks Desktop (Pro, Premier, Enterprise) and QuickBooks Online
            </p>
            <Link href="/signup" className="px-8 py-4 bg-white text-green-600 rounded-lg hover:bg-gray-100 font-semibold text-lg transition-all transform hover:scale-105 shadow-xl inline-flex items-center space-x-2">
              <span>Get Started Free</span>
              <ArrowRight className="h-5 w-5" />
            </Link>
            <p className="text-green-100 mt-6">
              ✓ IIF & CSV formats • ✓ 10 free conversions/month • ✓ No credit card required
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
                </ul>
              </div>
              <div>
                <h3 className="text-white font-bold mb-4">Legal</h3>
                <ul className="space-y-2">
                  <li><Link href="/privacy" className="hover:text-white transition-colors">Privacy Policy</Link></li>
                  <li><Link href="/terms" className="hover:text-white transition-colors">Terms</Link></li>
                </ul>
              </div>
              <div>
                <h3 className="text-white font-bold mb-4">Connect</h3>
                <p className="text-sm">Email: infotrulybot@gmail.com</p>
                <p className="text-sm mt-2">WhatsApp: +91 9101361482</p>
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
