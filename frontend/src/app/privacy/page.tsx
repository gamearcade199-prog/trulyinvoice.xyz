'use client'

import Link from 'next/link'
import { ArrowLeft, FileText, Shield, Lock, Eye, Database, UserCheck, AlertTriangle } from 'lucide-react'

export default function PrivacyPage() {
  return (
    <main className="min-h-screen bg-gray-50 dark:bg-gray-900 transition-colors">
      {/* Navigation */}
      <nav className="bg-gray-50 dark:bg-gray-900 border-b border-gray-200 dark:border-gray-800 sticky top-0 z-50">
        <div className="container mx-auto px-4">
          <div className="flex items-center justify-between h-16">
            <Link href="/" className="flex items-center gap-2">
              <div className="w-8 h-8 bg-gradient-to-br from-blue-500 to-blue-600 rounded-lg flex items-center justify-center">
                <FileText className="w-5 h-5 text-white" />
              </div>
              <span className="text-xl font-bold text-gray-900 dark:text-white">TrulyInvoice</span>
            </Link>
            <Link 
              href="/" 
              className="flex items-center gap-2 text-gray-700 dark:text-gray-300 hover:text-blue-600 dark:hover:text-blue-400 transition-colors"
            >
              <ArrowLeft className="w-4 h-4" />
              Back to Home
            </Link>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="bg-gradient-to-br from-blue-50 to-purple-50 dark:from-gray-800 dark:to-gray-900 py-16">
        <div className="container mx-auto px-4">
          <div className="max-w-4xl mx-auto text-center">
            <div className="w-16 h-16 bg-blue-100 dark:bg-blue-900/50 rounded-full flex items-center justify-center mx-auto mb-6">
              <Shield className="w-8 h-8 text-blue-600 dark:text-blue-400" />
            </div>
            <h1 className="text-4xl md:text-5xl font-bold text-gray-900 dark:text-white mb-4">
              Privacy Policy
            </h1>
            <p className="text-lg text-gray-600 dark:text-gray-400">
              Last updated: October 12, 2025
            </p>
          </div>
        </div>
      </section>

      {/* Content */}
      <section className="py-16">
        <div className="container mx-auto px-4">
          <div className="max-w-4xl mx-auto">
            {/* Introduction */}
            <div className="bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800 rounded-xl p-6 mb-12">
              <p className="text-gray-900 dark:text-white font-semibold mb-2">Your Privacy Matters</p>
              <p className="text-gray-700 dark:text-gray-300">
                At TrulyInvoice, we take your privacy seriously. This Privacy Policy explains how we collect, use, 
                and protect your personal information when you use our AI-powered invoice management platform.
              </p>
            </div>

            {/* Sections */}
            <div className="space-y-12">
              {/* Information We Collect */}
              <div>
                <div className="flex items-center gap-3 mb-4">
                  <div className="w-10 h-10 bg-purple-100 dark:bg-purple-900/50 rounded-lg flex items-center justify-center">
                    <Database className="w-5 h-5 text-purple-600 dark:text-purple-400" />
                  </div>
                  <h2 className="text-2xl font-bold text-gray-900 dark:text-white">1. Information We Collect</h2>
                </div>
                <div className="bg-gray-50 dark:bg-gray-900 rounded-xl p-6 border border-gray-200 dark:border-gray-800">
                  <h3 className="font-semibold text-gray-900 dark:text-white mb-3">Personal Information:</h3>
                  <ul className="list-disc list-inside space-y-2 text-gray-600 dark:text-gray-400 mb-4">
                    <li>Name, email address, and phone number</li>
                    <li>Company name and address</li>
                    <li>Payment information (processed securely through third-party providers)</li>
                  </ul>
                  
                  <h3 className="font-semibold text-gray-900 dark:text-white mb-3">Invoice Data:</h3>
                  <ul className="list-disc list-inside space-y-2 text-gray-600 dark:text-gray-400 mb-4">
                    <li>Uploaded invoice documents (PDF, JPG, PNG)</li>
                    <li>Extracted data (vendor names, amounts, dates, GST information)</li>
                    <li>Processing history and analytics</li>
                  </ul>

                  <h3 className="font-semibold text-gray-900 dark:text-white mb-3">Usage Data:</h3>
                  <ul className="list-disc list-inside space-y-2 text-gray-600 dark:text-gray-400">
                    <li>Device information and IP address</li>
                    <li>Browser type and version</li>
                    <li>Pages visited and features used</li>
                    <li>Time spent on platform</li>
                  </ul>
                </div>
              </div>

              {/* How We Use Your Information */}
              <div>
                <div className="flex items-center gap-3 mb-4">
                  <div className="w-10 h-10 bg-green-100 dark:bg-green-900/50 rounded-lg flex items-center justify-center">
                    <Eye className="w-5 h-5 text-green-600 dark:text-green-400" />
                  </div>
                  <h2 className="text-2xl font-bold text-gray-900 dark:text-white">2. How We Use Your Information</h2>
                </div>
                <div className="bg-gray-50 dark:bg-gray-900 rounded-xl p-6 border border-gray-200 dark:border-gray-800">
                  <ul className="list-disc list-inside space-y-2 text-gray-600 dark:text-gray-400">
                    <li>Process and extract data from your invoices using AI</li>
                    <li>Provide, maintain, and improve our services</li>
                    <li>Send service-related notifications and updates</li>
                    <li>Respond to your support requests</li>
                    <li>Analyze usage patterns to enhance user experience</li>
                    <li>Prevent fraud and ensure platform security</li>
                    <li>Comply with legal obligations</li>
                  </ul>
                </div>
              </div>

              {/* Data Security */}
              <div>
                <div className="flex items-center gap-3 mb-4">
                  <div className="w-10 h-10 bg-blue-100 dark:bg-blue-900/50 rounded-lg flex items-center justify-center">
                    <Lock className="w-5 h-5 text-blue-600 dark:text-blue-400" />
                  </div>
                  <h2 className="text-2xl font-bold text-gray-900 dark:text-white">3. Data Security</h2>
                </div>
                <div className="bg-gray-50 dark:bg-gray-900 rounded-xl p-6 border border-gray-200 dark:border-gray-800">
                  <p className="text-gray-600 dark:text-gray-400 mb-4">
                    We implement industry-standard security measures to protect your data:
                  </p>
                  <div className="grid md:grid-cols-2 gap-4">
                    <div className="flex items-start gap-3">
                      <div className="w-6 h-6 bg-green-100 dark:bg-green-900/50 rounded flex items-center justify-center flex-shrink-0 mt-0.5">
                        <span className="text-green-600 dark:text-green-400 text-xs">✓</span>
                      </div>
                      <div>
                        <p className="font-semibold text-gray-900 dark:text-white">Encryption</p>
                        <p className="text-sm text-gray-600 dark:text-gray-400">All data encrypted in transit and at rest</p>
                      </div>
                    </div>
                    <div className="flex items-start gap-3">
                      <div className="w-6 h-6 bg-green-100 dark:bg-green-900/50 rounded flex items-center justify-center flex-shrink-0 mt-0.5">
                        <span className="text-green-600 dark:text-green-400 text-xs">✓</span>
                      </div>
                      <div>
                        <p className="font-semibold text-gray-900 dark:text-white">Secure Storage</p>
                        <p className="text-sm text-gray-600 dark:text-gray-400">Enterprise-grade cloud infrastructure</p>
                      </div>
                    </div>
                    <div className="flex items-start gap-3">
                      <div className="w-6 h-6 bg-green-100 dark:bg-green-900/50 rounded flex items-center justify-center flex-shrink-0 mt-0.5">
                        <span className="text-green-600 dark:text-green-400 text-xs">✓</span>
                      </div>
                      <div>
                        <p className="font-semibold text-gray-900 dark:text-white">Access Control</p>
                        <p className="text-sm text-gray-600 dark:text-gray-400">Role-based access restrictions</p>
                      </div>
                    </div>
                    <div className="flex items-start gap-3">
                      <div className="w-6 h-6 bg-green-100 dark:bg-green-900/50 rounded flex items-center justify-center flex-shrink-0 mt-0.5">
                        <span className="text-green-600 dark:text-green-400 text-xs">✓</span>
                      </div>
                      <div>
                        <p className="font-semibold text-gray-900 dark:text-white">Regular Audits</p>
                        <p className="text-sm text-gray-600 dark:text-gray-400">Continuous security monitoring</p>
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              {/* Your Rights */}
              <div>
                <div className="flex items-center gap-3 mb-4">
                  <div className="w-10 h-10 bg-yellow-100 dark:bg-yellow-900/50 rounded-lg flex items-center justify-center">
                    <UserCheck className="w-5 h-5 text-yellow-600 dark:text-yellow-400" />
                  </div>
                  <h2 className="text-2xl font-bold text-gray-900 dark:text-white">4. Your Rights</h2>
                </div>
                <div className="bg-gray-50 dark:bg-gray-900 rounded-xl p-6 border border-gray-200 dark:border-gray-800">
                  <p className="text-gray-600 dark:text-gray-400 mb-4">You have the right to:</p>
                  <ul className="list-disc list-inside space-y-2 text-gray-600 dark:text-gray-400">
                    <li>Access your personal data and invoice information</li>
                    <li>Correct inaccurate or incomplete data</li>
                    <li>Request deletion of your data</li>
                    <li>Export your data in a portable format</li>
                    <li>Opt-out of marketing communications</li>
                    <li>Withdraw consent for data processing</li>
                  </ul>
                </div>
              </div>

              {/* Data Retention */}
              <div>
                <div className="flex items-center gap-3 mb-4">
                  <div className="w-10 h-10 bg-red-100 dark:bg-red-900/50 rounded-lg flex items-center justify-center">
                    <AlertTriangle className="w-5 h-5 text-red-600 dark:text-red-400" />
                  </div>
                  <h2 className="text-2xl font-bold text-gray-900 dark:text-white">5. Data Retention</h2>
                </div>
                <div className="bg-gray-50 dark:bg-gray-900 rounded-xl p-6 border border-gray-200 dark:border-gray-800">
                  <p className="text-gray-600 dark:text-gray-400 mb-4">
                    We retain your data only as long as necessary:
                  </p>
                  <ul className="list-disc list-inside space-y-2 text-gray-600 dark:text-gray-400">
                    <li>Active account data: Retained while your account is active</li>
                    <li>Invoice data: Retained for 7 years for tax compliance</li>
                    <li>Usage logs: Retained for 90 days</li>
                    <li>Deleted data: Permanently removed within 30 days of deletion request</li>
                  </ul>
                </div>
              </div>

              {/* Third-Party Services */}
              <div>
                <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-4">6. Third-Party Services</h2>
                <div className="bg-gray-50 dark:bg-gray-900 rounded-xl p-6 border border-gray-200 dark:border-gray-800">
                  <p className="text-gray-600 dark:text-gray-400 mb-4">
                    We use trusted third-party services for:
                  </p>
                  <ul className="list-disc list-inside space-y-2 text-gray-600 dark:text-gray-400">
                    <li><strong>Supabase:</strong> Database and authentication</li>
                    <li><strong>Google Gemini:</strong> AI-powered invoice extraction</li>
                    <li><strong>Payment Processors:</strong> Secure payment handling</li>
                  </ul>
                  <p className="text-gray-600 dark:text-gray-400 mt-4">
                    These services have their own privacy policies and security measures.
                  </p>
                </div>
              </div>

              {/* Contact */}
              <div>
                <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-4">7. Contact Us</h2>
                <div className="bg-gray-50 dark:bg-gray-900 rounded-xl p-6 border border-gray-200 dark:border-gray-800">
                  <p className="text-gray-600 dark:text-gray-400 mb-4">
                    If you have any questions about this Privacy Policy or your data:
                  </p>
                  <div className="space-y-2 text-gray-600 dark:text-gray-400">
                    <p><strong className="text-gray-900 dark:text-white">Email:</strong> infotrulybot@gmail.com</p>
                    <p><strong className="text-gray-900 dark:text-white">WhatsApp:</strong> +91 9101361482</p>
                    <p><strong className="text-gray-900 dark:text-white">Address:</strong> GS Road, Ganeshguri, Assam - 781005, India</p>
                  </div>
                </div>
              </div>
            </div>

            {/* Updates Notice */}
            <div className="mt-12 bg-yellow-50 dark:bg-yellow-900/20 border border-yellow-200 dark:border-yellow-800 rounded-xl p-6">
              <p className="text-yellow-900 dark:text-yellow-100 font-semibold mb-2">Policy Updates</p>
              <p className="text-yellow-800 dark:text-yellow-200">
                We may update this Privacy Policy from time to time. We will notify you of any significant changes 
                via email or through our platform. Your continued use of TrulyInvoice after changes constitutes 
                acceptance of the updated policy.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-gray-900 dark:bg-gray-950 text-gray-300 py-8 border-t border-gray-800">
        <div className="container mx-auto px-4">
          <div className="text-center">
            <p>&copy; 2024 TrulyInvoice. All rights reserved.</p>
            <div className="mt-4 flex justify-center gap-6">
              <Link href="/about" className="hover:text-white transition-colors">About</Link>
              <Link href="/terms" className="hover:text-white transition-colors">Terms</Link>
              <Link href="/contact" className="hover:text-white transition-colors">Contact</Link>
            </div>
          </div>
        </div>
      </footer>
    </main>
  )
}

