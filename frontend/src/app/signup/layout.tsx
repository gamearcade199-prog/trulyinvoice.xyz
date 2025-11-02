import { Metadata } from 'next'

export const metadata: Metadata = {
  title: 'Sign Up Free - Start Managing Invoices Today',
  description: 'Create your free TrulyInvoice account. Get 10 free invoice scans per month. No credit card required. Start automating your GST invoices in 2 minutes.',
  keywords: [
    'invoice software signup',
    'create invoice account',
    'free invoice software India',
    'GST software free trial',
    'invoice management registration',
  ],
  alternates: {
  canonical: 'https://trulyinvoice.com/signup',
  },
  robots: {
    index: true,
    follow: true,
  },
  openGraph: {
    title: 'Sign Up Free - TrulyInvoice Invoice Management',
    description: 'Create your free account. Get 10 free invoice scans per month. No credit card required.',
  url: 'https://trulyinvoice.com/signup',
    siteName: 'TrulyInvoice',
    images: [
      {
        url: '/og-image-signup.jpg',
        width: 1200,
        height: 630,
        alt: 'Sign up for TrulyInvoice',
      },
    ],
    locale: 'en_IN',
    type: 'website',
  },
  twitter: {
    card: 'summary_large_image',
    title: 'Sign Up Free - TrulyInvoice Invoice Management',
    description: 'Create your free account. Get 10 free invoice scans per month.',
    images: ['/twitter-image-signup.jpg'],
  },
}

export default function SignupLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return children
}
