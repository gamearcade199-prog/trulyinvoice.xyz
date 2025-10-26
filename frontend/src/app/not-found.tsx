import Link from 'next/link'
import { ArrowLeft, Home } from 'lucide-react'

export const metadata = {
  title: '404 - Page Not Found | TrulyInvoice',
  description: 'The page you\'re looking for doesn\'t exist. Go back to TrulyInvoice home to convert invoices to Excel.',
}

export default function NotFound() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-purple-50 dark:from-gray-900 dark:to-gray-800 flex items-center justify-center px-4 py-20">
      <div className="max-w-md w-full text-center">
        {/* 404 Icon */}
        <div className="mb-8">
          <div className="text-7xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent mb-4">
            404
          </div>
        </div>

        {/* Heading */}
        <h1 className="text-3xl md:text-4xl font-bold text-gray-900 dark:text-white mb-4">
          Page Not Found
        </h1>

        {/* Description */}
        <p className="text-lg text-gray-600 dark:text-gray-400 mb-8">
          Sorry! The page you're looking for doesn't exist. It might have been moved or deleted. Let's get you back on track.
        </p>

        {/* CTA Buttons */}
        <div className="flex flex-col sm:flex-row gap-4 justify-center">
          <Link
            href="/"
            className="inline-flex items-center justify-center gap-2 px-6 py-3 bg-gradient-to-r from-blue-600 to-purple-600 text-white font-semibold rounded-lg hover:from-blue-700 hover:to-purple-700 transition-all"
          >
            <Home className="w-5 h-5" />
            Back to Home
          </Link>

          <Link
            href="/pricing"
            className="inline-flex items-center justify-center gap-2 px-6 py-3 bg-white dark:bg-gray-700 text-gray-900 dark:text-white font-semibold rounded-lg border-2 border-gray-300 dark:border-gray-600 hover:bg-gray-50 dark:hover:bg-gray-600 transition-all"
          >
            View Pricing
          </Link>
        </div>

        {/* Additional Links */}
        <div className="mt-12 pt-8 border-t border-gray-200 dark:border-gray-700">
          <p className="text-sm text-gray-600 dark:text-gray-400 mb-4">Popular pages:</p>
          <ul className="space-y-2">
            <li>
              <Link href="/features" className="text-blue-600 dark:text-blue-400 hover:underline">
                ✓ Features
              </Link>
            </li>
            <li>
              <Link href="/about" className="text-blue-600 dark:text-blue-400 hover:underline">
                ✓ About Us
              </Link>
            </li>
            <li>
              <Link href="/contact" className="text-blue-600 dark:text-blue-400 hover:underline">
                ✓ Contact Support
              </Link>
            </li>
          </ul>
        </div>
      </div>
    </div>
  )
}
