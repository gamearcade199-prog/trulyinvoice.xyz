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
    slug: 'how-to-extract-data-from-gst-invoices',
    title: 'How to Extract Data from GST Invoices Automatically in 2025',
    excerpt: 'Learn the best methods to automatically extract GSTIN, invoice numbers, and tax details from GST invoices.',
    date: '2025-10-24',
    category: 'GST Compliance',
  },
  {
    slug: 'complete-guide-invoice-management-indian-small-businesses',
    title: 'Complete Guide to Invoice Management for Indian Small Businesses',
    excerpt: 'Everything small business owners in India need to know about managing invoices efficiently.',
    date: '2025-10-23',
    category: 'Business Tips',
  },
  {
    slug: 'gst-invoice-format-everything-you-need-to-know',
    title: 'GST Invoice Format: Everything You Need to Know',
    excerpt: 'Detailed breakdown of Indian GST invoice format, required fields, and compliance requirements.',
    date: '2025-10-22',
    category: 'GST Compliance',
  },
  {
    slug: 'how-to-convert-pdf-invoices-to-excel',
    title: 'How to Convert PDF Invoices to Excel (3 Methods Compared)',
    excerpt: 'Compare manual entry, Excel formulas, and AI-powered conversion methods. Find out which is best for your business.',
    date: '2025-10-21',
    category: 'Tutorials',
  },
  {
    slug: 'invoice-processing-automation-save-10-hours-weekly',
    title: 'Invoice Processing Automation: Save 10+ Hours Weekly',
    excerpt: 'Discover how invoice automation can save your accounting team time and reduce errors dramatically.',
    date: '2025-10-20',
    category: 'Automation',
  },
  {
    slug: 'tally-integration-import-invoices-automatically',
    title: 'Tally Integration: How to Import Invoices Automatically',
    excerpt: 'Step-by-step guide to integrating TrulyInvoice with Tally for seamless invoice imports.',
    date: '2025-10-19',
    category: 'Integrations',
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
                <span className="text-sm bg-blue-100 text-blue-800 px-3 py-1 rounded">
                  {post.category}
                </span>
                <time className="text-sm text-gray-500">{post.date}</time>
              </div>
              <h2 className="text-2xl font-bold mb-2">
                <Link href={`/blog/${post.slug}`} className="hover:text-blue-600">
                  {post.title}
                </Link>
              </h2>
              <p className="text-gray-600 mb-4">{post.excerpt}</p>
              <Link href={`/blog/${post.slug}`} className="text-blue-600 font-semibold hover:underline">
                Read More →
              </Link>
            </article>
          ))}
        </section>
      </div>
    </main>
  )
}
