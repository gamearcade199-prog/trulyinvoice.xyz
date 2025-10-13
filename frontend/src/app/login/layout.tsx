import { Metadata } from 'next'

export const metadata: Metadata = {
  title: 'Login - Access Your Invoice Dashboard',
  description: 'Login to TrulyInvoice to manage your invoices, track payments, and automate GST billing. Secure access to your invoice management dashboard.',
  alternates: {
  canonical: 'https://trulyinvoice.xyz/login',
  },
  robots: {
    index: false, // Don't index login page
    follow: true,
  },
  openGraph: {
    title: 'Login - TrulyInvoice Invoice Management',
    description: 'Login to access your invoice dashboard.',
  url: 'https://trulyinvoice.xyz/login',
    siteName: 'TrulyInvoice',
    locale: 'en_IN',
    type: 'website',
  },
}

export default function LoginLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return children
}
