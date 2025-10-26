import { Metadata } from 'next'

export const metadata: Metadata = {
  title: 'Upgrade Plan - Dashboard Pricing | TrulyInvoice',
  description: 'Upgrade your TrulyInvoice subscription plan. Choose from free to enterprise with unlimited invoice processing.',
  robots: {
    index: false,
    follow: false,
  },
}

export default function PricingLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return children
}
