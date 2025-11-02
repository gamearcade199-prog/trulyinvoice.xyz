'use client'

import Link from 'next/link'
import { ArrowLeft, FileText, Scale, CheckCircle, XCircle, AlertCircle } from 'lucide-react'

export default function TermsPage() {
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
            <div className="w-16 h-16 bg-purple-100 dark:bg-purple-900/50 rounded-full flex items-center justify-center mx-auto mb-6">
              <Scale className="w-8 h-8 text-purple-600 dark:text-purple-400" />
            </div>
            <h1 className="text-4xl md:text-5xl font-bold text-gray-900 dark:text-white mb-4">
              Terms of Service
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
              <p className="text-gray-900 dark:text-white font-semibold mb-2">Agreement to Terms</p>
              <p className="text-gray-700 dark:text-gray-300">
                By accessing and using TrulyInvoice ("the Service"), you agree to be bound by these Terms of Service. 
                If you do not agree to these terms, please do not use our service.
              </p>
            </div>

            {/* Sections */}
            <div className="space-y-12">
              {/* Service Description */}
              <div>
                <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-4">1. Service Description</h2>
                <div className="bg-gray-50 dark:bg-gray-900 rounded-xl p-6 border border-gray-200 dark:border-gray-800">
                  <p className="text-gray-600 dark:text-gray-400 mb-4">
                    TrulyInvoice provides an AI-powered invoice management platform that:
                  </p>
                  <ul className="list-disc list-inside space-y-2 text-gray-600 dark:text-gray-400">
                    <li>Extracts data from invoice documents using artificial intelligence</li>
                    <li>Organizes and stores invoice information securely</li>
                    <li>Provides analytics and reporting features</li>
                    <li>Offers GST-compliant invoice management for Indian businesses</li>
                  </ul>
                </div>
              </div>

              {/* User Accounts */}
              <div>
                <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-4">2. User Accounts</h2>
                <div className="bg-gray-50 dark:bg-gray-900 rounded-xl p-6 border border-gray-200 dark:border-gray-800 space-y-4">
                  <div className="flex items-start gap-3">
                    <CheckCircle className="w-5 h-5 text-green-600 dark:text-green-400 flex-shrink-0 mt-0.5" />
                    <div>
                      <p className="font-semibold text-gray-900 dark:text-white">Account Creation</p>
                      <p className="text-gray-600 dark:text-gray-400 text-sm">
                        You must provide accurate and complete information when creating an account
                      </p>
                    </div>
                  </div>
                  <div className="flex items-start gap-3">
                    <CheckCircle className="w-5 h-5 text-green-600 dark:text-green-400 flex-shrink-0 mt-0.5" />
                    <div>
                      <p className="font-semibold text-gray-900 dark:text-white">Security</p>
                      <p className="text-gray-600 dark:text-gray-400 text-sm">
                        You are responsible for maintaining the confidentiality of your account credentials
                      </p>
                    </div>
                  </div>
                  <div className="flex items-start gap-3">
                    <CheckCircle className="w-5 h-5 text-green-600 dark:text-green-400 flex-shrink-0 mt-0.5" />
                    <div>
                      <p className="font-semibold text-gray-900 dark:text-white">Age Requirement</p>
                      <p className="text-gray-600 dark:text-gray-400 text-sm">
                        You must be at least 18 years old or the age of majority in your jurisdiction
                      </p>
                    </div>
                  </div>
                </div>
              </div>

              {/* Acceptable Use */}
              <div>
                <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-4">3. Acceptable Use</h2>
                <div className="bg-gray-50 dark:bg-gray-900 rounded-xl p-6 border border-gray-200 dark:border-gray-800">
                  <p className="text-gray-600 dark:text-gray-400 mb-4">You agree NOT to:</p>
                  <div className="space-y-3">
                    <div className="flex items-start gap-3">
                      <XCircle className="w-5 h-5 text-red-600 dark:text-red-400 flex-shrink-0 mt-0.5" />
                      <p className="text-gray-600 dark:text-gray-400 text-sm">
                        Upload malicious files or attempt to compromise the platform's security
                      </p>
                    </div>
                    <div className="flex items-start gap-3">
                      <XCircle className="w-5 h-5 text-red-600 dark:text-red-400 flex-shrink-0 mt-0.5" />
                      <p className="text-gray-600 dark:text-gray-400 text-sm">
                        Use the service for any illegal or unauthorized purpose
                      </p>
                    </div>
                    <div className="flex items-start gap-3">
                      <XCircle className="w-5 h-5 text-red-600 dark:text-red-400 flex-shrink-0 mt-0.5" />
                      <p className="text-gray-600 dark:text-gray-400 text-sm">
                        Violate any laws or regulations in your jurisdiction
                      </p>
                    </div>
                    <div className="flex items-start gap-3">
                      <XCircle className="w-5 h-5 text-red-600 dark:text-red-400 flex-shrink-0 mt-0.5" />
                      <p className="text-gray-600 dark:text-gray-400 text-sm">
                        Attempt to reverse engineer or copy any part of the platform
                      </p>
                    </div>
                    <div className="flex items-start gap-3">
                      <XCircle className="w-5 h-5 text-red-600 dark:text-red-400 flex-shrink-0 mt-0.5" />
                      <p className="text-gray-600 dark:text-gray-400 text-sm">
                        Share your account credentials with unauthorized parties
                      </p>
                    </div>
                  </div>
                </div>
              </div>

              {/* Subscription & Payment */}
              <div>
                <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-4">4. Subscription & Payment</h2>
                <div className="bg-gray-50 dark:bg-gray-900 rounded-xl p-6 border border-gray-200 dark:border-gray-800">
                  <div className="bg-blue-50 dark:bg-blue-900/30 border border-blue-200 dark:border-blue-800 rounded-lg p-4 mb-4 flex items-start gap-3">
                    <AlertCircle className="w-5 h-5 text-blue-600 dark:text-blue-400 flex-shrink-0 mt-0.5" />
                    <div>
                      <p className="font-semibold text-blue-900 dark:text-blue-100 mb-2">Auto-Renewal Subscription Service</p>
                      <p className="text-blue-800 dark:text-blue-200 text-sm">
                        By subscribing to any paid plan, you agree to automatic monthly or yearly recurring billing. 
                        Your subscription will automatically renew at the end of each billing period unless you cancel before the renewal date.
                      </p>
                    </div>
                  </div>
                  <ul className="list-disc list-inside space-y-3 text-gray-600 dark:text-gray-400">
                    <li><strong className="text-gray-900 dark:text-white">Free Plan:</strong> Includes 10 invoice scans per month with no payment required</li>
                    <li><strong className="text-gray-900 dark:text-white">Paid Plans:</strong> Billed automatically on a monthly or yearly basis as selected at signup</li>
                    <li><strong className="text-gray-900 dark:text-white">Auto-Renewal:</strong> Your subscription automatically renews each billing cycle. You will be charged on the same date each month/year</li>
                    <li><strong className="text-gray-900 dark:text-white">Payment Processing:</strong> All payments are processed securely through Razorpay payment gateway</li>
                    <li><strong className="text-gray-900 dark:text-white">Cancellation:</strong> You can cancel your subscription at any time from your account settings. Cancellation takes effect at the end of the current billing period</li>
                    <li><strong className="text-gray-900 dark:text-white">Refund Policy:</strong> Full refunds are provided within 14 days of initial purchase if the service has not been used. No refunds for subsequent renewal charges</li>
                    <li><strong className="text-gray-900 dark:text-white">Price Changes:</strong> We will provide 30 days advance notice of any price changes via email</li>
                    <li><strong className="text-gray-900 dark:text-white">Failed Payments:</strong> If payment fails, we will retry up to 3 times. Access may be restricted after failed payment attempts</li>
                  </ul>
                </div>
              </div>

              {/* Data & Privacy */}
              <div>
                <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-4">5. Data & Privacy</h2>
                <div className="bg-gray-50 dark:bg-gray-900 rounded-xl p-6 border border-gray-200 dark:border-gray-800">
                  <p className="text-gray-600 dark:text-gray-400 mb-4">
                    Your invoice data and personal information are handled according to our{' '}
                    <Link href="/privacy" className="text-blue-600 dark:text-blue-400 hover:underline">
                      Privacy Policy
                    </Link>. Key points:
                  </p>
                  <ul className="list-disc list-inside space-y-2 text-gray-600 dark:text-gray-400">
                    <li>You retain ownership of all uploaded invoice data</li>
                    <li>We use your data only to provide and improve our services</li>
                    <li>Data is encrypted in transit and at rest</li>
                    <li>You can export or delete your data at any time</li>
                  </ul>
                </div>
              </div>

              {/* AI Processing */}
              <div>
                <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-4">6. AI Processing & Accuracy</h2>
                <div className="bg-gray-50 dark:bg-gray-900 rounded-xl p-6 border border-gray-200 dark:border-gray-800">
                  <div className="flex items-start gap-3 mb-4">
                    <AlertCircle className="w-5 h-5 text-yellow-600 dark:text-yellow-400 flex-shrink-0 mt-0.5" />
                    <p className="text-gray-600 dark:text-gray-400">
                      Our AI achieves 95%+ accuracy, but you should always review extracted data before using it 
                      for critical business decisions.
                    </p>
                  </div>
                  <ul className="list-disc list-inside space-y-2 text-gray-600 dark:text-gray-400">
                    <li>We continuously improve our AI models for better accuracy</li>
                    <li>We are not liable for errors in extracted data</li>
                    <li>You are responsible for verifying all extracted information</li>
                    <li>We may use anonymized data to train and improve our AI</li>
                  </ul>
                </div>
              </div>

              {/* Intellectual Property */}
              <div>
                <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-4">7. Intellectual Property</h2>
                <div className="bg-gray-50 dark:bg-gray-900 rounded-xl p-6 border border-gray-200 dark:border-gray-800">
                  <p className="text-gray-600 dark:text-gray-400 mb-4">
                    TrulyInvoice and all related trademarks, logos, and content are owned by us. You receive 
                    a limited license to use the service, which does not grant you ownership of:
                  </p>
                  <ul className="list-disc list-inside space-y-2 text-gray-600 dark:text-gray-400">
                    <li>The platform's code, design, and functionality</li>
                    <li>Our AI models and algorithms</li>
                    <li>TrulyInvoice branding and marketing materials</li>
                    <li>Documentation and support materials</li>
                  </ul>
                </div>
              </div>

              {/* Limitation of Liability */}
              <div>
                <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-4">8. Limitation of Liability</h2>
                <div className="bg-gray-50 dark:bg-gray-900 rounded-xl p-6 border border-gray-200 dark:border-gray-800">
                  <p className="text-gray-600 dark:text-gray-400 mb-4">
                    To the maximum extent permitted by law:
                  </p>
                  <ul className="list-disc list-inside space-y-2 text-gray-600 dark:text-gray-400">
                    <li>The service is provided "as is" without warranties of any kind</li>
                    <li>We are not liable for any indirect, incidental, or consequential damages</li>
                    <li>Our total liability is limited to the amount you paid in the last 12 months</li>
                    <li>We are not responsible for third-party services or integrations</li>
                  </ul>
                </div>
              </div>

              {/* Termination */}
              <div>
                <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-4">9. Termination</h2>
                <div className="bg-gray-50 dark:bg-gray-900 rounded-xl p-6 border border-gray-200 dark:border-gray-800">
                  <p className="text-gray-600 dark:text-gray-400 mb-4">
                    We may suspend or terminate your account if:
                  </p>
                  <ul className="list-disc list-inside space-y-2 text-gray-600 dark:text-gray-400 mb-4">
                    <li>You violate these Terms of Service</li>
                    <li>Your payment fails or account is past due</li>
                    <li>We suspect fraudulent or illegal activity</li>
                    <li>We discontinue the service (with 30 days notice)</li>
                  </ul>
                  <p className="text-gray-600 dark:text-gray-400">
                    You may cancel your account at any time through your account settings.
                  </p>
                </div>
              </div>

              {/* Governing Law */}
              <div>
                <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-4">10. Governing Law</h2>
                <div className="bg-gray-50 dark:bg-gray-900 rounded-xl p-6 border border-gray-200 dark:border-gray-800">
                  <p className="text-gray-600 dark:text-gray-400">
                    These terms are governed by the laws of India. Any disputes will be resolved in the courts 
                    of Assam, India. The parties agree to submit to the exclusive jurisdiction of these courts.
                  </p>
                </div>
              </div>

              {/* Contact */}
              <div>
                <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-4">11. Contact Information</h2>
                <div className="bg-gray-50 dark:bg-gray-900 rounded-xl p-6 border border-gray-200 dark:border-gray-800">
                  <p className="text-gray-600 dark:text-gray-400 mb-4">
                    Questions about these terms? Contact us:
                  </p>
                  <div className="space-y-2 text-gray-600 dark:text-gray-400">
                    <p><strong className="text-gray-900 dark:text-white">Email:</strong> infotrulybot@gmail.com</p>
                    <p><strong className="text-gray-900 dark:text-white">WhatsApp:</strong> +91 9101361482</p>
                    <p><strong className="text-gray-900 dark:text-white">Address:</strong> GS Road, Ganeshguri, Assam - 781005, India</p>
                  </div>
                </div>
              </div>
            </div>

            {/* Changes Notice */}
            <div className="mt-12 bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800 rounded-xl p-6">
              <p className="text-blue-900 dark:text-blue-100 font-semibold mb-2">Changes to Terms</p>
              <p className="text-blue-800 dark:text-blue-200">
                We reserve the right to modify these terms at any time. We will notify users of material changes 
                via email or platform notification. Continued use of the service after changes constitutes acceptance 
                of the updated terms.
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
              <Link href="/privacy" className="hover:text-white transition-colors">Privacy</Link>
              <Link href="/contact" className="hover:text-white transition-colors">Contact</Link>
            </div>
          </div>
        </div>
      </footer>
    </main>
  )
}

