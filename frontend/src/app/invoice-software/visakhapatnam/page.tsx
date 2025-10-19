import { Metadata } from 'next';
import Link from 'next/link';
import { CheckCircle, Building, Train, Smartphone, Shield, Star } from 'lucide-react';

export const metadata: Metadata = {
  title: 'Invoice Management Software Visakhapatnam | GST & AI | TrulyInvoice',
  description: '#1 Invoice software in Visakhapatnam. AI-powered GST invoicing, automatic data extraction, 1-click exports. Trusted by 5000+ Visakhapatnam businesses. Try Free!',
  alternates: {
    canonical: 'https://trulyinvoice.xyz/invoice-software-visakhapatnam',
  },
};

export default function VisakhapatnamInvoicePage() {
  const organizationSchema = {
    '@context': 'https://schema.org',
    '@type': 'LocalBusiness',
    'name': 'TrulyInvoice Visakhapatnam',
    'description': 'AI-powered invoice management software for Visakhapatnam businesses',
    'address': {
      '@type': 'PostalAddress',
      'addressLocality': 'Visakhapatnam',
      'addressRegion': 'Andhra Pradesh',
      'postalCode': '530001',
      'addressCountry': 'IN'
    },
    'geo': {
      '@type': 'GeoCoordinates',
      'latitude': '17.6868',
      'longitude': '83.2185'
    },
    'url': 'https://trulyinvoice.xyz/invoice-software-visakhapatnam',
    'telephone': '+91-891-12345678',
    'priceRange': '₹0-₹999',
    'areaServed': {
      '@type': 'City',
      'name': 'Visakhapatnam'
    },
    'aggregateRating': {
      '@type': 'AggregateRating',
      'ratingValue': '4.7',
      'reviewCount': '1200'
    }
  };

  return (
    <div className="bg-gray-50 dark:bg-gray-950">
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(organizationSchema) }}
      />
      {/* Hero Section */}
      <section className="text-center py-20 px-4 bg-blue-50 dark:bg-blue-900/20">
        <h1 className="text-4xl md:text-5xl font-bold text-gray-900 dark:text-white">Best Invoice Management Software for Visakhapatnam Businesses</h1>
        <p className="text-xl mt-4 text-gray-600 dark:text-gray-300">6,000+ businesses in Visakhapatnam trust TrulyInvoice for GST-compliant invoicing.</p>
        <Link href="/register" className="mt-8 inline-block bg-blue-600 text-white font-bold py-3 px-8 rounded-lg hover:bg-blue-700 transition-colors">
          Start Free Trial - No Credit Card Required
        </Link>
        <div className="mt-4 text-sm text-gray-500 dark:text-gray-400">
          ✓ Perfect for Visakhapatnam's port and industrial sectors ✓ Handle high transaction volumes with ease
        </div>
      </section>

      {/* Local Trust Signals */}
      <section className="py-16 px-4">
        <h2 className="text-3xl font-bold text-center text-gray-900 dark:text-white">Trusted by Leading Visakhapatnam Companies</h2>
        <div className="flex justify-center gap-8 mt-8 text-gray-500 dark:text-gray-400">
          <p className="font-semibold">Gajuwaka Industrial Area</p>
          <p className="font-semibold">Siripuram Businesses</p>
          <p className="font-semibold">MVP Colony Enterprises</p>
        </div>
        <div className="max-w-2xl mx-auto mt-8 p-6 bg-white dark:bg-gray-800 rounded-lg shadow-md">
          <p className="text-lg text-gray-700 dark:text-gray-200">"TrulyInvoice has been a great tool for our business. It's helped us to automate our invoicing and save a lot of time."</p>
          <p className="mt-4 font-bold text-right text-gray-900 dark:text-white">- Ravi Kumar, CEO, Visakhapatnam</p>
        </div>
      </section>

      {/* City-Specific Pain Points */}
      <section className="py-16 px-4 bg-gray-100 dark:bg-gray-900">
        <h2 className="text-3xl font-bold text-center text-gray-900 dark:text-white">Visakhapatnam Business Challenges We Solve</h2>
        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8 mt-12 max-w-6xl mx-auto">
          <div className="text-center">
            <Train className="mx-auto h-12 w-12 text-blue-600" />
            <h3 className="text-xl font-bold mt-4">City of Destiny</h3>
            <p className="mt-2 text-gray-600 dark:text-gray-300">Visakhapatnam is a city of destiny. Our software is designed to help you to achieve your business goals.</p>
          </div>
          <div className="text-center">
            <Building className="mx-auto h-12 w-12 text-blue-600" />
            <h3 className="text-xl font-bold mt-4">Port & Industrial Hub</h3>
            <p className="mt-2 text-gray-600 dark:text-gray-300">We're built for the port and industrial sectors. Our software is secure, compliant, and scalable.</p>
          </div>
          <div className="text-center">
            <Smartphone className="mx-auto h-12 w-12 text-blue-600" />
            <h3 className="text-xl font-bold mt-4">Mobile-First for a Mobile City</h3>
            <p className="mt-2 text-gray-600 dark:text-gray-300">Upload invoices on the go, from anywhere in Visakhapatnam.</p>
          </div>
          <div className="text-center">
            <Shield className="mx-auto h-12 w-12 text-blue-600" />
            <h3 className="text-xl font-bold mt-4">GST Compliance</h3>
            <p className="mt-2 text-gray-600 dark:text-gray-300">Stay compliant with Andhra Pradesh GST regulations automatically.</p>
          </div>
        </div>
      </section>

      {/* FAQs */}
      <section className="py-16 px-4">
        <h2 className="text-3xl font-bold text-center text-gray-900 dark:text-white">Frequently Asked Questions - Visakhapatnam</h2>
        <div className="max-w-3xl mx-auto mt-8 space-y-4">
          <div className="p-4 border rounded-lg dark:border-gray-700">
            <h3 className="font-semibold">Does TrulyInvoice comply with Andhra Pradesh GST rules?</h3>
            <p className="mt-2 text-gray-600 dark:text-gray-300">Yes! We are 100% compliant with Andhra Pradesh State GST and all Indian GST regulations.</p>
          </div>
          <div className="p-4 border rounded-lg dark:border-gray-700">
            <h3 className="font-semibold">Is TrulyInvoice good for industrial businesses?</h3>
            <p className="mt-2 text-gray-600 dark:text-gray-300">Absolutely! Our software is designed to handle the unique invoicing needs of industrial businesses.</p>
          </div>
        </div>
      </section>
    </div>
  );
}
