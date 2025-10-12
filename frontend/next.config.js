/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  // Remove Babel - use default Next.js compiler
  images: {
    domains: [],
  },
  async rewrites() {
    return [
      {
        source: '/api/:path*',
        destination: 'http://localhost:8000/:path*',
      },
    ]
  },
}

module.exports = nextConfig
