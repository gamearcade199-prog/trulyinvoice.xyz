'use client'

import Link from 'next/link'
import Breadcrumb from '@/components/Breadcrumb'
import { ArrowLeft, FileText, Target, Users, Award, Heart } from 'lucide-react'

export default function AboutPage() {
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
          <div className="mb-6">
            <Breadcrumb items={[{ label: 'Home', href: '/' }, { label: 'About' }]} />
          </div>
          <div className="max-w-4xl mx-auto text-center">
            <h1 className="text-4xl md:text-5xl font-bold text-gray-900 dark:text-white mb-4">
              About TrulyInvoice - AI Invoice to Excel Conversion Platform
            </h1>
            <p className="text-xl text-gray-600 dark:text-gray-400">
              Transforming invoice management with AI-powered automation
            </p>
            <p className="text-sm text-gray-500 dark:text-gray-500 mt-2">
              Last updated: October 17, 2025 - Production deployment active
            </p>
          </div>
        </div>
      </section>

      {/* Main Content */}
      <section className="py-16">
        <div className="container mx-auto px-4">
          <div className="max-w-4xl mx-auto">
            {/* Our Story */}
            <div className="mb-16">
              <h2 className="text-3xl font-bold text-gray-900 dark:text-white mb-6">Our Story</h2>
              <div className="prose dark:prose-invert max-w-none">
                <p className="text-lg text-gray-600 dark:text-gray-400 leading-relaxed mb-4">
                  TrulyInvoice was born from a simple observation: businesses waste countless hours manually entering invoice data. 
                  We believed there had to be a better way.
                </p>
                <p className="text-lg text-gray-600 dark:text-gray-400 leading-relaxed mb-4">
                  Founded in 2024, we set out to build an AI-powered platform that could extract, organize, and analyze invoice 
                  data in seconds—not hours. What started as a small project has grown into a comprehensive invoice management 
                  solution trusted by businesses across India.
                </p>
                <p className="text-lg text-gray-600 dark:text-gray-400 leading-relaxed">
                  Based in Assam, we're proud to serve businesses of all sizes, from startups to enterprises, helping them 
                  streamline their financial workflows and focus on what matters most: growing their business.
                </p>
                <p className="text-lg text-gray-600 dark:text-gray-400 leading-relaxed mt-4">
                  Our AI-powered platform processes thousands of invoices daily with 99.9% accuracy, helping businesses 
                  save up to 40 hours per month on manual data entry. Join the growing community of businesses that 
                  have transformed their invoice management with TrulyInvoice.
                </p>
              </div>
            </div>

            {/* Our Mission */}
            <div className="grid md:grid-cols-2 gap-8 mb-16">
              <div className="bg-gray-50 dark:bg-gray-900 rounded-xl p-8 border border-gray-200 dark:border-gray-800">
                <div className="w-12 h-12 bg-blue-100 dark:bg-blue-900/50 rounded-lg flex items-center justify-center mb-4">
                  <Target className="w-6 h-6 text-blue-600 dark:text-blue-400" />
                </div>
                <h3 className="text-2xl font-bold text-gray-900 dark:text-white mb-4">Our Mission</h3>
                <p className="text-gray-600 dark:text-gray-400">
                  To empower businesses with intelligent automation that saves time, reduces errors, and provides 
                  actionable insights from their financial documents.
                </p>
              </div>

              <div className="bg-gray-50 dark:bg-gray-900 rounded-xl p-8 border border-gray-200 dark:border-gray-800">
                <div className="w-12 h-12 bg-purple-100 dark:bg-purple-900/50 rounded-lg flex items-center justify-center mb-4">
                  <Heart className="w-6 h-6 text-purple-600 dark:text-purple-400" />
                </div>
                <h3 className="text-2xl font-bold text-gray-900 dark:text-white mb-4">Our Values</h3>
                <p className="text-gray-600 dark:text-gray-400">
                  Innovation, accuracy, and customer success drive everything we do. We're committed to continuous 
                  improvement and delivering exceptional value to our users.
                </p>
              </div>
            </div>

            {/* Key Features */}
            <div className="mb-16">
              <h2 className="text-3xl font-bold text-gray-900 dark:text-white mb-8">Why Choose TrulyInvoice?</h2>
              <div className="grid md:grid-cols-3 gap-6">
                <div className="text-center">
                  <div className="w-16 h-16 bg-blue-100 dark:bg-blue-900/50 rounded-full flex items-center justify-center mx-auto mb-4">
                    <FileText className="w-8 h-8 text-blue-600 dark:text-blue-400" />
                  </div>
                  <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-2">AI-Powered</h3>
                  <p className="text-gray-600 dark:text-gray-400">
                    95%+ accuracy with advanced machine learning
                  </p>
                </div>

                <div className="text-center">
                  <div className="w-16 h-16 bg-green-100 dark:bg-green-900/50 rounded-full flex items-center justify-center mx-auto mb-4">
                    <Award className="w-8 h-8 text-green-600 dark:text-green-400" />
                  </div>
                  <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-2">GST Compliant</h3>
                  <p className="text-gray-600 dark:text-gray-400">
                    Fully compliant with Indian GST regulations
                  </p>
                </div>

                <div className="text-center">
                  <div className="w-16 h-16 bg-purple-100 dark:bg-purple-900/50 rounded-full flex items-center justify-center mx-auto mb-4">
                    <Users className="w-8 h-8 text-purple-600 dark:text-purple-400" />
                  </div>
                  <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-2">24/7 Support</h3>
                  <p className="text-gray-600 dark:text-gray-400">
                    Always here to help via WhatsApp and email
                  </p>
                </div>
              </div>
            </div>

            {/* Contact CTA */}
            <div className="bg-gradient-to-r from-blue-600 to-purple-600 rounded-xl p-8 md:p-12 text-center">
              <h2 className="text-3xl font-bold text-white mb-4">Get in Touch</h2>
              <p className="text-blue-100 mb-6 max-w-2xl mx-auto">
                Have questions or want to learn more? Our team is here to help you succeed.
              </p>
              <div className="flex flex-col sm:flex-row gap-4 justify-center">
                <Link 
                  href="/contact"
                  className="px-8 py-3 bg-white text-blue-600 rounded-lg font-semibold hover:bg-gray-100 transition-colors"
                >
                  Contact Us
                </Link>
                <Link 
                  href="/dashboard/support"
                  className="px-8 py-3 bg-blue-700 text-white rounded-lg font-semibold hover:bg-blue-800 transition-colors border-2 border-blue-400"
                >
                  Support Center
                </Link>
              </div>
            </div>

            {/* Technology Section */}
            <div className="mb-16 bg-gradient-to-r from-blue-50 to-purple-50 dark:from-gray-800 dark:to-gray-900 rounded-2xl p-8">
              <h2 className="text-3xl font-bold text-gray-900 dark:text-white mb-6 text-center">Powered by Advanced AI</h2>
              <div className="grid md:grid-cols-2 gap-8">
                <div>
                  <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-3">Google Gemini AI</h3>
                  <p className="text-gray-600 dark:text-gray-400 mb-4">
                    Our platform leverages Google's cutting-edge Gemini AI for unparalleled accuracy in invoice data extraction, 
                    ensuring 99.9% precision across all document types.
                  </p>
                </div>
                <div>
                  <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-3">Smart Processing</h3>
                  <p className="text-gray-600 dark:text-gray-400 mb-4">
                    Advanced OCR and machine learning algorithms work together to understand complex invoice layouts, 
                    handwritten text, and multi-language documents with ease.
                  </p>
                </div>
              </div>
              <div className="text-center mt-6">
                <p className="text-sm text-gray-500 dark:text-gray-400 italic">
                  Updated October 2025 - Enhanced with latest AI capabilities
                </p>
              </div>
            </div>

            {/* Related Links Section */}
            <div className="mb-16">
              <h2 className="text-3xl font-bold text-gray-900 dark:text-white mb-8 text-center">Learn More About TrulyInvoice</h2>
              <div className="grid md:grid-cols-3 gap-6">
                <Link 
                  href="/pricing"
                  className="group p-6 bg-gray-50 dark:bg-gray-800 rounded-xl border border-gray-200 dark:border-gray-700 hover:border-blue-500 dark:hover:border-blue-500 transition-all hover:shadow-lg"
                >
                  <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-2 group-hover:text-blue-600 dark:group-hover:text-blue-400 transition-colors">
                    Pricing Plans
                  </h3>
                  <p className="text-gray-600 dark:text-gray-400">
                    Choose the perfect plan for your invoice processing needs. From free to enterprise.
                  </p>
                </Link>

                <Link 
                  href="/features"
                  className="group p-6 bg-gray-50 dark:bg-gray-800 rounded-xl border border-gray-200 dark:border-gray-700 hover:border-blue-500 dark:hover:border-blue-500 transition-all hover:shadow-lg"
                >
                  <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-2 group-hover:text-blue-600 dark:group-hover:text-blue-400 transition-colors">
                    Features
                  </h3>
                  <p className="text-gray-600 dark:text-gray-400">
                    Explore powerful AI-powered invoice processing capabilities.
                  </p>
                </Link>

                <Link 
                  href="/"
                  className="group p-6 bg-gray-50 dark:bg-gray-800 rounded-xl border border-gray-200 dark:border-gray-700 hover:border-blue-500 dark:hover:border-blue-500 transition-all hover:shadow-lg"
                >
                  <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-2 group-hover:text-blue-600 dark:group-hover:text-blue-400 transition-colors">
                    Start Converting
                  </h3>
                  <p className="text-gray-600 dark:text-gray-400">
                    Ready to automate your invoice processing? Get started today.
                  </p>
                </Link>
              </div>
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
              <Link href="/privacy" className="hover:text-white transition-colors">Privacy</Link>
              <Link href="/terms" className="hover:text-white transition-colors">Terms</Link>
              <Link href="/contact" className="hover:text-white transition-colors">Contact</Link>
            </div>
          </div>
        </div>
      </footer>
    </main>
  )
}

