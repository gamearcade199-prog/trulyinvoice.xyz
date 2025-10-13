import { Metadata } from 'next'

export const metadata: Metadata = {
  title: 'Dashboard - Invoice Management',
  description: 'View and manage all your invoices in one place. Upload, process, and export GST invoices with AI-powered automation.',
  alternates: {
  canonical: 'https://trulyinvoice.xyz/dashboard',
  },
  robots: {
    index: false, // Don't index dashboard (user-specific content)
    follow: false,
  },
}

export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return children
}
