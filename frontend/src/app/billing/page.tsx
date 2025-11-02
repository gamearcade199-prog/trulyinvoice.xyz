'use client'

import Link from 'next/link'
import { ArrowLeft, FileText, CreditCard, RefreshCw, XCircle, DollarSign, Calendar, Shield, CheckCircle, AlertCircle } from 'lucide-react'

export default function BillingPage() {
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
              <CreditCard className="w-8 h-8 text-blue-600 dark:text-blue-400" />
            </div>
            <h1 className="text-4xl md:text-5xl font-bold text-gray-900 dark:text-white mb-4">
              Billing & Subscription Policy
            </h1>
            <p className="text-lg text-gray-600 dark:text-gray-400">
              Last updated: November 2, 2025
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
              <div className="flex items-start gap-3">
                <AlertCircle className="w-6 h-6 text-blue-600 dark:text-blue-400 flex-shrink-0 mt-0.5" />
                <div>
                  <p className="text-gray-900 dark:text-white font-semibold mb-2">Auto-Renewal Subscription Service</p>
                  <p className="text-gray-700 dark:text-gray-300">
                    TrulyInvoice operates on an auto-renewing subscription model. By subscribing to any paid plan, 
                    you authorize us to charge your payment method automatically at the start of each billing cycle 
                    until you cancel your subscription.
                  </p>
                </div>
              </div>
            </div>

            {/* Sections */}
            <div className="space-y-12">
              {/* How Subscriptions Work */}
              <div>
                <div className="flex items-center gap-3 mb-4">
                  <div className="w-10 h-10 bg-purple-100 dark:bg-purple-900/50 rounded-lg flex items-center justify-center">
                    <RefreshCw className="w-5 h-5 text-purple-600 dark:text-purple-400" />
                  </div>
                  <h2 className="text-2xl font-bold text-gray-900 dark:text-white">1. How Subscriptions Work</h2>
                </div>
                <div className="bg-gray-50 dark:bg-gray-900 rounded-xl p-6 border border-gray-200 dark:border-gray-800">
                  <div className="space-y-4">
                    <div className="flex items-start gap-3">
                      <CheckCircle className="w-5 h-5 text-green-600 dark:text-green-400 flex-shrink-0 mt-0.5" />
                      <div>
                        <p className="font-semibold text-gray-900 dark:text-white">Automatic Renewal</p>
                        <p className="text-gray-600 dark:text-gray-400 text-sm">
                          Your subscription automatically renews on the same date each month (or year for annual plans) 
                          unless you cancel before the renewal date.
                        </p>
                      </div>
                    </div>
                    <div className="flex items-start gap-3">
                      <CheckCircle className="w-5 h-5 text-green-600 dark:text-green-400 flex-shrink-0 mt-0.5" />
                      <div>
                        <p className="font-semibold text-gray-900 dark:text-white">Billing Date</p>
                        <p className="text-gray-600 dark:text-gray-400 text-sm">
                          You will be charged on the same day each billing cycle. For example, if you subscribe on 
                          January 15th, you'll be charged on the 15th of every month.
                        </p>
                      </div>
                    </div>
                    <div className="flex items-start gap-3">
                      <CheckCircle className="w-5 h-5 text-green-600 dark:text-green-400 flex-shrink-0 mt-0.5" />
                      <div>
                        <p className="font-semibold text-gray-900 dark:text-white">Continuous Service</p>
                        <p className="text-gray-600 dark:text-gray-400 text-sm">
                          Your service continues uninterrupted as long as payments are successful. You never have to 
                          manually renew your subscription.
                        </p>
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              {/* Billing Cycles */}
              <div>
                <div className="flex items-center gap-3 mb-4">
                  <div className="w-10 h-10 bg-blue-100 dark:bg-blue-900/50 rounded-lg flex items-center justify-center">
                    <Calendar className="w-5 h-5 text-blue-600 dark:text-blue-400" />
                  </div>
                  <h2 className="text-2xl font-bold text-gray-900 dark:text-white">2. Billing Cycles</h2>
                </div>
                <div className="bg-gray-50 dark:bg-gray-900 rounded-xl p-6 border border-gray-200 dark:border-gray-800">
                  <div className="grid md:grid-cols-2 gap-6">
                    <div className="border border-blue-200 dark:border-blue-800 rounded-lg p-4 bg-blue-50 dark:bg-blue-900/20">
                      <h3 className="font-semibold text-gray-900 dark:text-white mb-2 flex items-center gap-2">
                        <Calendar className="w-4 h-4 text-blue-600 dark:text-blue-400" />
                        Monthly Billing
                      </h3>
                      <ul className="space-y-2 text-sm text-gray-600 dark:text-gray-400">
                        <li className="flex items-start gap-2">
                          <span className="text-blue-600 dark:text-blue-400 mt-0.5">•</span>
                          <span>Charged every 30 days</span>
                        </li>
                        <li className="flex items-start gap-2">
                          <span className="text-blue-600 dark:text-blue-400 mt-0.5">•</span>
                          <span>Flexible plan changes</span>
                        </li>
                        <li className="flex items-start gap-2">
                          <span className="text-blue-600 dark:text-blue-400 mt-0.5">•</span>
                          <span>Cancel anytime</span>
                        </li>
                      </ul>
                    </div>
                    <div className="border border-green-200 dark:border-green-800 rounded-lg p-4 bg-green-50 dark:bg-green-900/20">
                      <h3 className="font-semibold text-gray-900 dark:text-white mb-2 flex items-center gap-2">
                        <Calendar className="w-4 h-4 text-green-600 dark:text-green-400" />
                        Yearly Billing
                      </h3>
                      <ul className="space-y-2 text-sm text-gray-600 dark:text-gray-400">
                        <li className="flex items-start gap-2">
                          <span className="text-green-600 dark:text-green-400 mt-0.5">•</span>
                          <span>Charged once per year</span>
                        </li>
                        <li className="flex items-start gap-2">
                          <span className="text-green-600 dark:text-green-400 mt-0.5">•</span>
                          <span>Save 20% compared to monthly</span>
                        </li>
                        <li className="flex items-start gap-2">
                          <span className="text-green-600 dark:text-green-400 mt-0.5">•</span>
                          <span>Best value for committed users</span>
                        </li>
                      </ul>
                    </div>
                  </div>
                </div>
              </div>

              {/* Payment Methods */}
              <div>
                <div className="flex items-center gap-3 mb-4">
                  <div className="w-10 h-10 bg-green-100 dark:bg-green-900/50 rounded-lg flex items-center justify-center">
                    <CreditCard className="w-5 h-5 text-green-600 dark:text-green-400" />
                  </div>
                  <h2 className="text-2xl font-bold text-gray-900 dark:text-white">3. Payment Methods</h2>
                </div>
                <div className="bg-gray-50 dark:bg-gray-900 rounded-xl p-6 border border-gray-200 dark:border-gray-800">
                  <p className="text-gray-600 dark:text-gray-400 mb-4">
                    We accept all major payment methods through our secure payment gateway, Razorpay:
                  </p>
                  <div className="grid md:grid-cols-2 gap-4">
                    <div className="flex items-center gap-3 p-3 bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700">
                      <Shield className="w-5 h-5 text-blue-600 dark:text-blue-400" />
                      <span className="text-gray-700 dark:text-gray-300">Credit & Debit Cards</span>
                    </div>
                    <div className="flex items-center gap-3 p-3 bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700">
                      <Shield className="w-5 h-5 text-blue-600 dark:text-blue-400" />
                      <span className="text-gray-700 dark:text-gray-300">UPI (Google Pay, PhonePe)</span>
                    </div>
                    <div className="flex items-center gap-3 p-3 bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700">
                      <Shield className="w-5 h-5 text-blue-600 dark:text-blue-400" />
                      <span className="text-gray-700 dark:text-gray-300">Net Banking</span>
                    </div>
                    <div className="flex items-center gap-3 p-3 bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700">
                      <Shield className="w-5 h-5 text-blue-600 dark:text-blue-400" />
                      <span className="text-gray-700 dark:text-gray-300">Wallets (Paytm, etc.)</span>
                    </div>
                  </div>
                  <div className="mt-4 p-4 bg-blue-50 dark:bg-blue-900/20 rounded-lg border border-blue-200 dark:border-blue-800">
                    <p className="text-sm text-blue-800 dark:text-blue-200 flex items-start gap-2">
                      <Shield className="w-4 h-4 flex-shrink-0 mt-0.5" />
                      <span>
                        All payments are processed securely through Razorpay, which is PCI-DSS Level 1 certified. 
                        We never store your complete card details on our servers.
                      </span>
                    </p>
                  </div>
                </div>
              </div>

              {/* Cancellation Policy */}
              <div>
                <div className="flex items-center gap-3 mb-4">
                  <div className="w-10 h-10 bg-orange-100 dark:bg-orange-900/50 rounded-lg flex items-center justify-center">
                    <XCircle className="w-5 h-5 text-orange-600 dark:text-orange-400" />
                  </div>
                  <h2 className="text-2xl font-bold text-gray-900 dark:text-white">4. Cancellation Policy</h2>
                </div>
                <div className="bg-gray-50 dark:bg-gray-900 rounded-xl p-6 border border-gray-200 dark:border-gray-800">
                  <div className="space-y-4">
                    <div>
                      <h3 className="font-semibold text-gray-900 dark:text-white mb-2">How to Cancel</h3>
                      <p className="text-gray-600 dark:text-gray-400 mb-3">
                        You can cancel your subscription at any time by:
                      </p>
                      <ol className="list-decimal list-inside space-y-2 text-gray-600 dark:text-gray-400 ml-4">
                        <li>Logging into your account dashboard</li>
                        <li>Going to Settings or Subscription page</li>
                        <li>Clicking "Cancel Subscription"</li>
                        <li>Confirming your cancellation</li>
                      </ol>
                    </div>
                    <div className="border-t border-gray-200 dark:border-gray-700 pt-4">
                      <h3 className="font-semibold text-gray-900 dark:text-white mb-2">What Happens After Cancellation</h3>
                      <ul className="space-y-2 text-gray-600 dark:text-gray-400">
                        <li className="flex items-start gap-2">
                          <CheckCircle className="w-4 h-4 text-green-600 dark:text-green-400 flex-shrink-0 mt-0.5" />
                          <span>Your subscription remains active until the end of the current billing period</span>
                        </li>
                        <li className="flex items-start gap-2">
                          <CheckCircle className="w-4 h-4 text-green-600 dark:text-green-400 flex-shrink-0 mt-0.5" />
                          <span>You can continue using all features until the paid period ends</span>
                        </li>
                        <li className="flex items-start gap-2">
                          <CheckCircle className="w-4 h-4 text-green-600 dark:text-green-400 flex-shrink-0 mt-0.5" />
                          <span>You will not be charged for the next billing cycle</span>
                        </li>
                        <li className="flex items-start gap-2">
                          <CheckCircle className="w-4 h-4 text-green-600 dark:text-green-400 flex-shrink-0 mt-0.5" />
                          <span>Your account automatically downgrades to the Free plan</span>
                        </li>
                      </ul>
                    </div>
                  </div>
                </div>
              </div>

              {/* Refund Policy */}
              <div>
                <div className="flex items-center gap-3 mb-4">
                  <div className="w-10 h-10 bg-yellow-100 dark:bg-yellow-900/50 rounded-lg flex items-center justify-center">
                    <DollarSign className="w-5 h-5 text-yellow-600 dark:text-yellow-400" />
                  </div>
                  <h2 className="text-2xl font-bold text-gray-900 dark:text-white">5. Refund Policy</h2>
                </div>
                <div className="bg-gray-50 dark:bg-gray-900 rounded-xl p-6 border border-gray-200 dark:border-gray-800">
                  <div className="space-y-4">
                    <div className="bg-green-50 dark:bg-green-900/20 border border-green-200 dark:border-green-800 rounded-lg p-4">
                      <h3 className="font-semibold text-green-900 dark:text-green-100 mb-2 flex items-center gap-2">
                        <CheckCircle className="w-5 h-5" />
                        14-Day Money-Back Guarantee
                      </h3>
                      <p className="text-green-800 dark:text-green-200 text-sm">
                        We offer a full refund within 14 days of your first subscription purchase if you are not 
                        satisfied with the service and have not extensively used it.
                      </p>
                    </div>
                    <div>
                      <h3 className="font-semibold text-gray-900 dark:text-white mb-2">Eligibility</h3>
                      <ul className="space-y-2 text-gray-600 dark:text-gray-400">
                        <li className="flex items-start gap-2">
                          <span className="text-green-600 dark:text-green-400 mt-0.5">✓</span>
                          <span>First-time purchases only</span>
                        </li>
                        <li className="flex items-start gap-2">
                          <span className="text-green-600 dark:text-green-400 mt-0.5">✓</span>
                          <span>Request made within 14 days of payment</span>
                        </li>
                        <li className="flex items-start gap-2">
                          <span className="text-green-600 dark:text-green-400 mt-0.5">✓</span>
                          <span>Minimal usage of the service (less than 10 scans)</span>
                        </li>
                      </ul>
                    </div>
                    <div className="border-t border-gray-200 dark:border-gray-700 pt-4">
                      <h3 className="font-semibold text-gray-900 dark:text-white mb-2">Not Eligible for Refund</h3>
                      <ul className="space-y-2 text-gray-600 dark:text-gray-400">
                        <li className="flex items-start gap-2">
                          <XCircle className="w-4 h-4 text-red-600 dark:text-red-400 flex-shrink-0 mt-0.5" />
                          <span>Subscription renewals (only first purchase qualifies)</span>
                        </li>
                        <li className="flex items-start gap-2">
                          <XCircle className="w-4 h-4 text-red-600 dark:text-red-400 flex-shrink-0 mt-0.5" />
                          <span>Requests made after 14 days</span>
                        </li>
                        <li className="flex items-start gap-2">
                          <XCircle className="w-4 h-4 text-red-600 dark:text-red-400 flex-shrink-0 mt-0.5" />
                          <span>Partial refunds for mid-cycle cancellations</span>
                        </li>
                        <li className="flex items-start gap-2">
                          <XCircle className="w-4 h-4 text-red-600 dark:text-red-400 flex-shrink-0 mt-0.5" />
                          <span>Accounts with extensive usage or abuse</span>
                        </li>
                      </ul>
                    </div>
                  </div>
                </div>
              </div>

              {/* Failed Payments */}
              <div>
                <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-4">6. Failed Payments</h2>
                <div className="bg-gray-50 dark:bg-gray-900 rounded-xl p-6 border border-gray-200 dark:border-gray-800">
                  <p className="text-gray-600 dark:text-gray-400 mb-4">
                    If a payment fails during renewal:
                  </p>
                  <ol className="list-decimal list-inside space-y-3 text-gray-600 dark:text-gray-400">
                    <li>We will automatically retry the payment up to 3 times over 7 days</li>
                    <li>You will receive email notifications about failed payment attempts</li>
                    <li>You have a 3-day grace period to update your payment method</li>
                    <li>If all retries fail, your subscription will be downgraded to the Free plan</li>
                    <li>You can reactivate anytime by updating your payment information</li>
                  </ol>
                </div>
              </div>

              {/* Price Changes */}
              <div>
                <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-4">7. Price Changes</h2>
                <div className="bg-gray-50 dark:bg-gray-900 rounded-xl p-6 border border-gray-200 dark:border-gray-800">
                  <p className="text-gray-600 dark:text-gray-400 mb-4">
                    We reserve the right to change our pricing at any time. However:
                  </p>
                  <ul className="space-y-2 text-gray-600 dark:text-gray-400">
                    <li className="flex items-start gap-2">
                      <CheckCircle className="w-4 h-4 text-blue-600 dark:text-blue-400 flex-shrink-0 mt-0.5" />
                      <span>We will provide at least 30 days advance notice via email</span>
                    </li>
                    <li className="flex items-start gap-2">
                      <CheckCircle className="w-4 h-4 text-blue-600 dark:text-blue-400 flex-shrink-0 mt-0.5" />
                      <span>Existing subscribers maintain their current pricing for their active subscription period</span>
                    </li>
                    <li className="flex items-start gap-2">
                      <CheckCircle className="w-4 h-4 text-blue-600 dark:text-blue-400 flex-shrink-0 mt-0.5" />
                      <span>New prices apply only at your next renewal</span>
                    </li>
                    <li className="flex items-start gap-2">
                      <CheckCircle className="w-4 h-4 text-blue-600 dark:text-blue-400 flex-shrink-0 mt-0.5" />
                      <span>You can cancel before the price change takes effect</span>
                    </li>
                  </ul>
                </div>
              </div>

              {/* Contact */}
              <div>
                <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-4">8. Billing Support</h2>
                <div className="bg-gray-50 dark:bg-gray-900 rounded-xl p-6 border border-gray-200 dark:border-gray-800">
                  <p className="text-gray-600 dark:text-gray-400 mb-4">
                    Have questions about billing, subscriptions, or refunds?
                  </p>
                  <div className="space-y-2 text-gray-600 dark:text-gray-400">
                    <p><strong className="text-gray-900 dark:text-white">Email:</strong> infotrulybot@gmail.com</p>
                    <p><strong className="text-gray-900 dark:text-white">WhatsApp:</strong> +91 9101361482</p>
                    <p><strong className="text-gray-900 dark:text-white">Address:</strong> GS Road, Ganeshguri, Assam - 781005, India</p>
                  </div>
                  <div className="mt-4 p-4 bg-blue-50 dark:bg-blue-900/20 rounded-lg border border-blue-200 dark:border-blue-800">
                    <p className="text-sm text-blue-800 dark:text-blue-200">
                      Our support team typically responds within 24 hours for billing-related inquiries.
                    </p>
                  </div>
                </div>
              </div>
            </div>

            {/* Updates Notice */}
            <div className="mt-12 bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800 rounded-xl p-6">
              <p className="text-blue-900 dark:text-blue-100 font-semibold mb-2">Policy Updates</p>
              <p className="text-blue-800 dark:text-blue-200">
                We may update this Billing Policy from time to time. We will notify users of any material changes 
                via email. Your continued use of TrulyInvoice after changes constitutes acceptance of the updated policy.
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
              <Link href="/privacy" className="hover:text-white transition-colors">Privacy</Link>
              <Link href="/contact" className="hover:text-white transition-colors">Contact</Link>
            </div>
          </div>
        </div>
      </footer>
    </main>
  )
}
