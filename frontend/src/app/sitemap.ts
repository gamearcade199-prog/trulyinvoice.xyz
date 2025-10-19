// Sitemap generation for TrulyInvoice
// Only includes pages that actually exist to avoid 404s

import { MetadataRoute } from 'next'

export default function sitemap(): MetadataRoute.Sitemap {
  const baseUrl = 'https://trulyinvoice.xyz'
  
  // Static pages that currently exist
  const staticPages = [
    {
      url: baseUrl,
      lastModified: new Date(),
      changeFrequency: 'daily' as const,
      priority: 1.0,
    },
    {
      url: `${baseUrl}/pricing`,
      lastModified: new Date(),
      changeFrequency: 'weekly' as const,
      priority: 0.9,
    },
    {
      url: `${baseUrl}/login`,
      lastModified: new Date(),
      changeFrequency: 'monthly' as const,
      priority: 0.6,
    },
    {
      url: `${baseUrl}/signup`,
      lastModified: new Date(),
      changeFrequency: 'monthly' as const,
      priority: 0.6,
    },
    {
      url: `${baseUrl}/features/invoice-to-excel-converter`,
      lastModified: new Date(),
      changeFrequency: 'weekly' as const,
      priority: 0.8,
    },
    {
      url: `${baseUrl}/invoice-software/mumbai`,
      lastModified: new Date(),
      changeFrequency: 'monthly' as const,
      priority: 0.7,
    },
  ]
  
  // TODO: Add these pages to sitemap when they are created:
  // - /features (when features page is built)
  // - /about (when about page is built)
  // - /contact (when contact page is built)
  // - /privacy (when privacy page is built)
  // - /terms (when terms page is built)
  // - /blog (when blog is built)
  // - City pages: /invoice-software-{city} (when landing pages are built)
  // - Industry pages: /invoice-software-{industry} (when industry pages are built)
  
  return staticPages
}
