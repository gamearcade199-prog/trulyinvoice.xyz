import { Metadata } from 'next'

export const metadata: Metadata = {
  title: 'Dashboard - Your Invoice History & Statistics | TrulyInvoice',
  description: 'Access your invoice history, processing statistics, and account overview. Track uploads, conversions, and usage on your TrulyInvoice dashboard.',
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
