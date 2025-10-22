import { Metadata } from 'next'

export const metadata: Metadata = {
  title: 'Support Center - Help & Documentation | TrulyInvoice',
  description: 'Get help with TrulyInvoice. Access FAQ, documentation, and contact support for invoice processing assistance.',
  robots: {
    index: false,
    follow: false,
  },
}

export default function SupportLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return children
}
