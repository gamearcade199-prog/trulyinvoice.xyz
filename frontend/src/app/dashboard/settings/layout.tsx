import { Metadata } from 'next'

export const metadata: Metadata = {
  title: 'Settings - Account & Preferences | TrulyInvoice',
  description: 'Manage your TrulyInvoice account settings, preferences, password, and profile information.',
  robots: {
    index: false,
    follow: false,
  },
}

export default function SettingsLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return children
}
