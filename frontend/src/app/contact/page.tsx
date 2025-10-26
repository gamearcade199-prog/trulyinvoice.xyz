'use client'

import Link from 'next/link'
import { ArrowLeft, FileText, Mail, Phone, MapPin, MessageCircle, Clock } from 'lucide-react'

export default function ContactPage() {
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
            <h1 className="text-4xl md:text-5xl font-bold text-gray-900 dark:text-white mb-4">
              Contact Us
            </h1>
            <p className="text-xl text-gray-600 dark:text-gray-400">
              We're here to help! Reach out to us through any of the channels below.
            </p>
          </div>
        </div>
      </section>

      {/* Contact Information */}
      <section className="py-16">
        <div className="container mx-auto px-4">
          <div className="max-w-6xl mx-auto">
            <div className="grid md:grid-cols-3 gap-8 mb-12">
              {/* WhatsApp */}
              <a 
                href="https://wa.me/919101361482"
                target="_blank"
                rel="noopener noreferrer"
                className="bg-gray-50 dark:bg-gray-900 rounded-xl p-8 border border-gray-200 dark:border-gray-800 hover:border-green-500 dark:hover:border-green-500 transition-all hover:shadow-lg group"
              >
                <div className="w-16 h-16 bg-green-100 dark:bg-green-900/30 rounded-full flex items-center justify-center mb-4 group-hover:scale-110 transition-transform">
                  <MessageCircle className="w-8 h-8 text-green-600 dark:text-green-400" />
                </div>
                <h3 className="text-xl font-bold text-gray-900 dark:text-white mb-2">WhatsApp Support</h3>
                <p className="text-gray-600 dark:text-gray-400 mb-2">Available 24/7</p>
                <p className="text-lg font-semibold text-green-600 dark:text-green-400">+91 9101361482</p>
              </a>

              {/* Email */}
              <a 
                href="mailto:infotrulybot@gmail.com"
                className="bg-gray-50 dark:bg-gray-900 rounded-xl p-8 border border-gray-200 dark:border-gray-800 hover:border-blue-500 dark:hover:border-blue-500 transition-all hover:shadow-lg group"
              >
                <div className="w-16 h-16 bg-blue-100 dark:bg-blue-900/30 rounded-full flex items-center justify-center mb-4 group-hover:scale-110 transition-transform">
                  <Mail className="w-8 h-8 text-blue-600 dark:text-blue-400" />
                </div>
                <h3 className="text-xl font-bold text-gray-900 dark:text-white mb-2">Email Us</h3>
                <p className="text-gray-600 dark:text-gray-400 mb-2">Response within 24 hours</p>
                <p className="text-lg font-semibold text-blue-600 dark:text-blue-400 break-all">infotrulybot@gmail.com</p>
              </a>

              {/* Office */}
              <div className="bg-gray-50 dark:bg-gray-900 rounded-xl p-8 border border-gray-200 dark:border-gray-800">
                <div className="w-16 h-16 bg-purple-100 dark:bg-purple-900/30 rounded-full flex items-center justify-center mb-4">
                  <MapPin className="w-8 h-8 text-purple-600 dark:text-purple-400" />
                </div>
                <h3 className="text-xl font-bold text-gray-900 dark:text-white mb-2">Visit Us</h3>
                <p className="text-gray-600 dark:text-gray-400 mb-2">Our Office</p>
                <p className="text-lg font-semibold text-purple-600 dark:text-purple-400">
                  GS Road, Ganeshguri<br />
                  Assam - 781005<br />
                  India
                </p>
              </div>
            </div>

            {/* Business Hours */}
            <div className="bg-gradient-to-br from-blue-50 to-purple-50 dark:from-gray-800 dark:to-gray-900 rounded-xl p-8 mb-12">
              <div className="flex items-start gap-4">
                <div className="w-12 h-12 bg-blue-100 dark:bg-blue-900/50 rounded-lg flex items-center justify-center flex-shrink-0">
                  <Clock className="w-6 h-6 text-blue-600 dark:text-blue-400" />
                </div>
                <div className="flex-1">
                  <h3 className="text-2xl font-bold text-gray-900 dark:text-white mb-4">Business Hours</h3>
                  <div className="grid md:grid-cols-2 gap-4">
                    <div>
                      <p className="text-gray-600 dark:text-gray-400 mb-2">
                        <strong className="text-gray-900 dark:text-white">Monday - Friday:</strong> 9:00 AM - 6:00 PM
                      </p>
                      <p className="text-gray-600 dark:text-gray-400 mb-2">
                        <strong className="text-gray-900 dark:text-white">Saturday:</strong> 10:00 AM - 4:00 PM
                      </p>
                      <p className="text-gray-600 dark:text-gray-400">
                        <strong className="text-gray-900 dark:text-white">Sunday:</strong> Closed
                      </p>
                    </div>
                    <div className="bg-green-100 dark:bg-green-900/30 rounded-lg p-4 border border-green-200 dark:border-green-800">
                      <p className="text-green-900 dark:text-green-100 font-semibold mb-1">
                        🟢 WhatsApp Support
                      </p>
                      <p className="text-green-700 dark:text-green-300 text-sm">
                        Available 24/7 for urgent queries
                      </p>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            {/* Support Center Link */}
            <div className="bg-gradient-to-r from-blue-600 to-purple-600 rounded-xl p-8 md:p-12 text-center">
              <h2 className="text-3xl font-bold text-white mb-4">Need Immediate Assistance?</h2>
              <p className="text-blue-100 mb-6 max-w-2xl mx-auto">
                Visit our comprehensive Support Center for FAQs, guides, and instant help.
              </p>
              <Link 
                href="/dashboard/support"
                className="inline-block px-8 py-3 bg-white text-blue-600 rounded-lg font-semibold hover:bg-gray-100 transition-colors"
              >
                Visit Support Center
              </Link>
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
              <Link href="/terms" className="hover:text-white transition-colors">Terms</Link>
            </div>
          </div>
        </div>
      </footer>
    </main>
  )
}

