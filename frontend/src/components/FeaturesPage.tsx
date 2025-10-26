'use client'

import Link from 'next/link'
import Breadcrumb from '@/components/Breadcrumb'
import {
  ArrowLeft,
  FileText,
  Zap,
  Bot,
  Shield,
  Download,
  CheckCircle2,
  Globe,
  Smartphone,
  Clock,
  BarChart3,
  Users
} from 'lucide-react'

export default function FeaturesPage() {
  const features = [
    {
      icon: Bot,
      title: 'AI-Powered OCR',
      description: 'Advanced machine learning algorithms extract data from invoices with 99%+ accuracy',
      benefits: ['Supports Hindi, English, and regional languages', 'Works with handwritten invoices', 'Continuous learning improves accuracy']
    },
    {
      icon: Zap,
      title: 'Lightning Fast Processing',
      description: 'Process hundreds of invoices in seconds, not hours',
      benefits: ['Bulk upload support', 'Real-time processing', 'Instant preview and verification']
    },
    {
      icon: Shield,
      title: 'GST Compliance',
      description: 'Built-in GST validation and compliance checking for Indian businesses',
      benefits: ['Automatic GST calculation', 'GSTIN validation', 'Export-ready GST reports']
    },
    {
      icon: Download,
      title: 'Smart Export Options',
      description: 'Export your data in multiple formats with customizable templates',
      benefits: ['Excel, CSV formats', 'Custom export templates', 'Automated report generation']
    },
    {
      icon: Globe,
      title: 'Multi-Currency Support',
      description: 'Handle invoices in multiple currencies with automatic conversion',
      benefits: ['Support for 50+ currencies', 'Real-time exchange rates', 'Currency-wise reporting']
    },
    {
      icon: Smartphone,
      title: 'Mobile Optimized',
      description: 'Fully responsive design works perfectly on all devices',
      benefits: ['Mobile-first design', 'Touch-optimized interface', 'Offline capability']
    },
    {
      icon: Clock,
      title: 'Real-time Collaboration',
      description: 'Work together with your team in real-time',
      benefits: ['Team workspaces', 'Real-time updates', 'Role-based permissions']
    },
    {
      icon: BarChart3,
      title: 'Advanced Analytics',
      description: 'Get insights into your business with powerful analytics',
      benefits: ['Spending trends analysis', 'Vendor performance metrics', 'Custom dashboards']
    },
    {
      icon: Users,
      title: 'Multi-user Support',
      description: 'Scale your invoice processing with team collaboration features',
      benefits: ['Unlimited team members', 'Role-based access control', 'Audit logs']
    }
  ]

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
          <div className="mb-8">
            <Breadcrumb items={[{ label: 'Home', href: '/' }, { label: 'Features' }]} />
          </div>
          <div className="max-w-4xl mx-auto text-center">
            <div className="w-16 h-16 bg-blue-100 dark:bg-blue-900/50 rounded-full flex items-center justify-center mx-auto mb-6">
              <Zap className="w-8 h-8 text-blue-600 dark:text-blue-400" />
            </div>
            <h1 className="text-4xl md:text-5xl font-bold text-gray-900 dark:text-white mb-4">
              AI Invoice Processing Features - Extract, Convert & Automate
            </h1>
            <p className="text-xl text-gray-600 dark:text-gray-400 max-w-2xl mx-auto">
              Everything you need to automate your invoice processing and streamline your business operations
            </p>
          </div>
        </div>
      </section>

      {/* Features Grid */}
      <section className="py-16">
        <div className="container mx-auto px-4">
          <div className="max-w-6xl mx-auto">
            <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
              {features.map((feature, index) => {
                const Icon = feature.icon
                return (
                  <div
                    key={index}
                    className="bg-gray-50 dark:bg-gray-900 rounded-xl p-8 border border-gray-200 dark:border-gray-800 hover:shadow-lg transition-all group"
                  >
                    <div className="w-12 h-12 bg-blue-100 dark:bg-blue-900/50 rounded-lg flex items-center justify-center mb-6 group-hover:scale-110 transition-transform">
                      <Icon className="w-6 h-6 text-blue-600 dark:text-blue-400" />
                    </div>

                    <h3 className="text-xl font-bold text-gray-900 dark:text-white mb-3">
                      {feature.title}
                    </h3>

                    <p className="text-gray-600 dark:text-gray-400 mb-4">
                      {feature.description}
                    </p>

                    <ul className="space-y-2">
                      {feature.benefits.map((benefit, benefitIndex) => (
                        <li key={benefitIndex} className="flex items-center gap-2 text-sm text-gray-600 dark:text-gray-400">
                          <CheckCircle2 className="w-4 h-4 text-green-500 flex-shrink-0" />
                          <span>{benefit}</span>
                        </li>
                      ))}
                    </ul>
                  </div>
                )
              })}
            </div>
          </div>
        </div>
      </section>

      {/* Related Links Section */}
      <section className="py-16 bg-gray-50 dark:bg-gray-900">
        <div className="container mx-auto px-4">
          <div className="max-w-4xl mx-auto">
            <h2 className="text-3xl font-bold text-gray-900 dark:text-white mb-8 text-center">Learn More About TrulyInvoice</h2>
            <div className="grid md:grid-cols-3 gap-6">
              <Link 
                href="/"
                className="group p-6 bg-white dark:bg-gray-800 rounded-xl border border-gray-200 dark:border-gray-700 hover:border-blue-500 dark:hover:border-blue-500 transition-all hover:shadow-lg"
              >
                <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-2 group-hover:text-blue-600 dark:group-hover:text-blue-400 transition-colors">
                  Home
                </h3>
                <p className="text-gray-600 dark:text-gray-400">
                  Convert your invoices to Excel with our AI-powered solution.
                </p>
              </Link>

              <Link 
                href="/pricing"
                className="group p-6 bg-white dark:bg-gray-800 rounded-xl border border-gray-200 dark:border-gray-700 hover:border-blue-500 dark:hover:border-blue-500 transition-all hover:shadow-lg"
              >
                <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-2 group-hover:text-blue-600 dark:group-hover:text-blue-400 transition-colors">
                  Pricing Plans
                </h3>
                <p className="text-gray-600 dark:text-gray-400">
                  Choose the perfect plan for your invoice processing needs.
                </p>
              </Link>

              <Link 
                href="/about"
                className="group p-6 bg-white dark:bg-gray-800 rounded-xl border border-gray-200 dark:border-gray-700 hover:border-blue-500 dark:hover:border-blue-500 transition-all hover:shadow-lg"
              >
                <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-2 group-hover:text-blue-600 dark:group-hover:text-blue-400 transition-colors">
                  About Us
                </h3>
                <p className="text-gray-600 dark:text-gray-400">
                  Discover our mission to revolutionize invoice processing.
                </p>
              </Link>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="bg-gradient-to-r from-blue-600 to-purple-600 dark:from-blue-500 dark:to-purple-500 py-16">
        <div className="container mx-auto px-4">
          <div className="max-w-4xl mx-auto text-center">
            <h2 className="text-3xl md:text-4xl font-bold text-white mb-4">
              Ready to Transform Your Invoice Processing?
            </h2>
            <p className="text-lg mb-8 text-blue-100 max-w-2xl mx-auto">
              Join hundreds of Indian businesses already using TrulyInvoice to save time and money
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Link
                href="/register"
                className="bg-white text-blue-600 hover:bg-gray-100 px-8 py-3 rounded-xl font-bold transition-all shadow-lg hover:shadow-xl hover:scale-105"
              >
                Start Free
              </Link>
              <Link
                href="/pricing"
                className="bg-transparent border-2 border-white text-white hover:bg-white hover:text-blue-600 px-8 py-3 rounded-xl font-bold transition-all"
              >
                View Pricing
              </Link>
            </div>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-gray-900 dark:bg-gray-950 text-gray-400 py-8">
        <div className="container mx-auto px-4">
          <div className="text-center">
            <div className="flex items-center justify-center gap-2 mb-4">
              <div className="w-8 h-8 bg-gradient-to-br from-blue-500 to-blue-600 rounded-lg flex items-center justify-center">
                <FileText className="w-5 h-5 text-white" />
              </div>
              <span className="text-xl font-bold text-white">TrulyInvoice</span>
            </div>
            <p className="text-sm">
              © 2025 TrulyInvoice. All rights reserved.
            </p>
          </div>
        </div>
      </footer>
    </main>
  )
}