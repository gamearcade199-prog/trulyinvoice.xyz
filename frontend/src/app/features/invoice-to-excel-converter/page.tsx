import { Metadata } from 'next';
import Link from 'next/link';
import { CheckCircle, Download, Zap } from 'lucide-react';

export const metadata: Metadata = {
  title: 'Invoice to Excel Converter | AI-Powered | TrulyInvoice',
  description: 'Convert PDF invoices to Excel in seconds. Our AI-powered tool extracts invoice data with 99% accuracy, saving you hours of manual data entry. GST compliant.',
  alternates: {
    canonical: 'https://trulyinvoice.xyz/features/invoice-to-excel-converter',
  },
};

export default function InvoiceToExcelPage() {
  return (
    <div className="bg-gray-50 dark:bg-gray-950">
      {/* Hero Section */}
      <section className="text-center py-20 px-4 bg-green-50 dark:bg-green-900/20">
        <h1 className="text-4xl md:text-5xl font-bold text-gray-900 dark:text-white">The Best Invoice to Excel Converter for Indian Businesses</h1>
        <p className="text-xl mt-4 text-gray-600 dark:text-gray-300">Stop manual data entry. Convert PDF invoices to Excel in seconds with 99% accuracy.</p>
        <Link href="/register" className="mt-8 inline-block bg-green-600 text-white font-bold py-3 px-8 rounded-lg hover:bg-green-700 transition-colors">
          Convert Your First Invoice for Free
        </Link>
      </section>

      {/* How It Works */}
      <section className="py-16 px-4">
        <h2 className="text-3xl font-bold text-center text-gray-900 dark:text-white">How It Works in 3 Simple Steps</h2>
        <div className="grid md:grid-cols-3 gap-8 mt-12 max-w-4xl mx-auto">
          <div className="text-center">
            <Zap className="mx-auto h-12 w-12 text-green-600" />
            <h3 className="text-xl font-bold mt-4">1. Upload Your Invoice</h3>
            <p className="mt-2 text-gray-600 dark:text-gray-300">Drag and drop any PDF or image file.</p>
          </div>
          <div className="text-center">
            <CheckCircle className="mx-auto h-12 w-12 text-green-600" />
            <h3 className="text-xl font-bold mt-4">2. AI Extracts the Data</h3>
            <p className="mt-2 text-gray-600 dark:text-gray-300">Our AI reads and structures the data in seconds.</p>
          </div>
          <div className="text-center">
            <Download className="mx-auto h-12 w-12 text-green-600" />
            <h3 className="text-xl font-bold mt-4">3. Download as Excel</h3>
            <p className="mt-2 text-gray-600 dark:text-gray-300">Get a perfectly formatted Excel file in one click.</p>
          </div>
        </div>
      </section>

      {/* Testimonial */}
      <section className="py-16 px-4 bg-gray-100 dark:bg-gray-900">
        <div className="max-w-2xl mx-auto p-6 bg-white dark:bg-gray-800 rounded-lg shadow-md">
          <p className="text-lg text-gray-700 dark:text-gray-200">"The invoice to Excel feature is a lifesaver. I used to spend hours manually entering data into spreadsheets. Now, it's done in seconds with zero errors."</p>
          <p className="mt-4 font-bold text-right text-gray-900 dark:text-white">- Priya Sharma, Accountant, Bangalore</p>
        </div>
      </section>
    </div>
  );
}
