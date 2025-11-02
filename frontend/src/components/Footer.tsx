'use client'

import Link from 'next/link'
import { Mail, FileText, Shield, Users, CreditCard } from 'lucide-react'

export default function Footer() {
  return (
    <footer className="bg-gray-900 dark:bg-gray-950 text-gray-300 py-12 mt-auto">
      <div className="container mx-auto px-4 sm:px-6 lg:px-8">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8 mb-8">
          
          {/* Company */}
          <div>
            <h3 className="text-white font-bold text-lg mb-4">Company</h3>
            <ul className="space-y-2">
              <li><Link href="/about" className="hover:text-blue-400 transition-colors flex items-center gap-2"><Users className="h-4 w-4" />About Us</Link></li>
              <li><Link href="/contact" className="hover:text-blue-400 transition-colors flex items-center gap-2"><Mail className="h-4 w-4" />Contact</Link></li>
              <li><Link href="/pricing" className="hover:text-blue-400 transition-colors">Pricing</Link></li>
              <li><Link href="/features" className="hover:text-blue-400 transition-colors">Features</Link></li>
            </ul>
          </div>

          {/* Legal */}
          <div>
            <h3 className="text-white font-bold text-lg mb-4">Legal</h3>
            <ul className="space-y-2">
              <li><Link href="/privacy" className="hover:text-blue-400 transition-colors flex items-center gap-2"><Shield className="h-4 w-4" />Privacy Policy</Link></li>
              <li><Link href="/terms" className="hover:text-blue-400 transition-colors flex items-center gap-2"><FileText className="h-4 w-4" />Terms of Service</Link></li>
              <li><Link href="/billing" className="hover:text-blue-400 transition-colors flex items-center gap-2"><CreditCard className="h-4 w-4" />Billing Policy</Link></li>
              <li><Link href="/security" className="hover:text-blue-400 transition-colors">Security</Link></li>
            </ul>
          </div>

          {/* Resources */}
          <div>
            <h3 className="text-white font-bold text-lg mb-4">Resources</h3>
            <ul className="space-y-2">
              <li><Link href="/features" className="hover:text-blue-400 transition-colors">How It Works</Link></li>
              <li><Link href="/pricing" className="hover:text-blue-400 transition-colors">Compare Plans</Link></li>
              <li><Link href="/about" className="hover:text-blue-400 transition-colors">Customer Stories</Link></li>
              <li><Link href="/dashboard" className="hover:text-blue-400 transition-colors">Dashboard</Link></li>
              <li><Link href="/billing" className="hover:text-blue-400 transition-colors">Billing & Subscriptions</Link></li>
            </ul>
          </div>
        </div>

        {/* Bottom Section */}
        <div className="border-t border-gray-800 pt-8">
          <div className="flex flex-col md:flex-row justify-between items-center gap-4">
            <div className="text-sm">
              © {new Date().getFullYear()} TrulyInvoice. All rights reserved.
            </div>
            <div className="text-sm text-gray-400">
              🇮🇳 Made in India for Indian Businesses | GST Compliant | 99% Accurate
            </div>
          </div>
        </div>
      </div>
    </footer>
  )
}
