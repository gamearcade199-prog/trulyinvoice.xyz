// Comprehensive robots.txt configuration for TrulyInvoice - Multi-Format Invoice Converter
import { MetadataRoute } from 'next'

export default function robots(): MetadataRoute.Robots {
  return {
    rules: [
      {
        userAgent: '*',
        allow: '/',
        disallow: [
          '/api/',
          '/dashboard/',
          '/admin/',
          '/_next/',
          '/private/',
          '/checkout/',
          '/payment/',
          '/subscription/',
          '/debug-*',
          '/test*',
          '/temp*',
          '/internal*',
          '/staging*',
          '/dev*',
          '/beta*',
          '/preview*',
        ],
      },
      {
        userAgent: 'Googlebot',
        allow: '/',
        crawlDelay: 0,
      },
      {
        userAgent: 'Googlebot-Image',
        allow: '/',
        crawlDelay: 0,
      },
      {
        userAgent: 'Googlebot-News',
        allow: '/',
        crawlDelay: 0,
      },
      {
        userAgent: 'Googlebot-Video',
        allow: '/',
        crawlDelay: 0,
      },
      {
        userAgent: 'Bingbot',
        allow: '/',
        crawlDelay: 1,
      },
      {
        userAgent: 'Slurp',
        allow: '/',
        crawlDelay: 1,
      },
      {
        userAgent: 'DuckDuckBot',
        allow: '/',
        crawlDelay: 1,
      },
      {
        userAgent: 'Baiduspider',
        allow: '/',
        crawlDelay: 2,
      },
      {
        userAgent: 'YandexBot',
        allow: '/',
        crawlDelay: 2,
      },
      {
        userAgent: 'facebookexternalhit',
        allow: '/',
        crawlDelay: 0,
      },
      {
        userAgent: 'Twitterbot',
        allow: '/',
        crawlDelay: 0,
      },
      {
        userAgent: 'LinkedInBot',
        allow: '/',
        crawlDelay: 0,
      },
      {
        userAgent: 'WhatsApp',
        allow: '/',
        crawlDelay: 0,
      },
      // Block aggressive scrapers and bots
      {
        userAgent: 'AhrefsBot',
        disallow: '/',
      },
      {
        userAgent: 'SemrushBot',
        disallow: '/',
      },
      {
        userAgent: 'MJ12bot',
        disallow: '/',
      },
      {
        userAgent: 'DotBot',
        disallow: '/',
      },
      {
        userAgent: 'ZoomBot',
        disallow: '/',
      },
    ],
    sitemap: 'https://trulyinvoice.xyz/sitemap.xml',
    host: 'https://trulyinvoice.xyz',
  }
}
