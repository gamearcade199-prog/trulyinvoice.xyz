import { Metadata } from 'next'
import Link from 'next/link'

export const metadata: Metadata = {
  title: 'Blog - Invoice Processing, GST Compliance & Automation Tips | TrulyInvoice',
  description: 'Read expert tips on invoice processing, GST compliance, accounting automation, and invoice management for Indian businesses. Learn how to save time and reduce errors.',
  keywords: ['invoice processing blog', 'GST compliance guide', 'accounting automation', 'invoice management tips', 'invoice extraction tutorial'],
  openGraph: {
    title: 'Blog - TrulyInvoice',
    description: 'Expert tips and guides on invoice processing and GST compliance',
    images: ['/og-image-india.jpg'],
  },
}

const blogPosts = [
  {
    slug: 'extract-gst-from-invoices-automatically',
    title: 'How to Extract GST from Invoices Automatically in 5 Seconds (2025)',
    excerpt: 'Stop wasting 5 minutes per invoice on manual GST extraction. Learn how Indian accountants automate GSTIN, tax amounts, and invoice data extraction with 99% accuracy.',
    date: '2025-10-28',
    category: 'GST Compliance',
    readTime: '8 min read',
  },
  {
    slug: 'invoice-to-excel-complete-guide',
    title: 'Invoice to Excel Conversion: Complete Guide for Indian Accountants & CAs',
    excerpt: 'Processing 200+ invoices manually every month? Learn how top Indian CAs convert invoices to Excel in seconds—not hours. Includes real success stories.',
    date: '2025-10-28',
    category: 'Accounting Automation',
    readTime: '12 min read',
  },
  {
    slug: 'save-50-hours-invoice-automation',
    title: 'Save 50 Hours Per Month: Invoice Data Entry Automation for Small Businesses',
    excerpt: 'Real case studies showing how restaurants, retailers & distributors save 8+ hours weekly on invoice processing. Includes ROI calculator.',
    date: '2025-10-28',
    category: 'Business Automation',
    readTime: '10 min read',
  },
  {
    slug: 'how-to-extract-data-from-gst-invoices',
    title: 'How to Extract Data from GST Invoices Automatically in 2025',
    excerpt: 'Learn the best methods to automatically extract GSTIN, invoice numbers, and tax details from GST invoices.',
    date: '2025-10-24',
    category: 'GST Compliance',
    readTime: '6 min read',
  },
]

export default function BlogPage() {
  return (
    <main>
      <div className="container mx-auto px-4 py-12">
        <h1 className="text-4xl font-bold mb-4">
          Invoice Processing & GST Compliance Blog
        </h1>
        <p className="text-xl text-gray-600 mb-12">
          Expert tips, guides, and tutorials on invoice management, GST compliance, and accounting automation for Indian businesses.
        </p>

        <section className="grid md:grid-cols-2 gap-8">
          {blogPosts.map((post) => (
            <article key={post.slug} className="border rounded-lg p-6 hover:shadow-lg transition">
              <div className="flex justify-between items-start mb-3">
                <span className="text-sm bg-blue-100 dark:bg-blue-900 text-blue-800 dark:text-blue-200 px-3 py-1 rounded">
                  {post.category}
                </span>
                <time className="text-sm text-gray-500 dark:text-gray-400">{post.date}</time>
              </div>
              <h2 className="text-2xl font-bold mb-2">
                <Link href={`/blog/${post.slug}`} className="hover:text-blue-600 dark:text-white dark:hover:text-blue-400">
                  {post.title}
                </Link>
              </h2>
              <p className="text-gray-600 dark:text-gray-300 mb-4">{post.excerpt}</p>
              <div className="flex justify-between items-center">
                <Link href={`/blog/${post.slug}`} className="text-blue-600 font-semibold hover:underline">
                  Read More →
                </Link>
                <span className="text-sm text-gray-500 dark:text-gray-400">{post.readTime}</span>
              </div>
            </article>
          ))}
        </section>
      </div>
    </main>
  )
}
