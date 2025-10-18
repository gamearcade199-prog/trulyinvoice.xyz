import { Suspense } from 'react'

// This is a server component - no 'use client'
export const dynamic = 'force-dynamic'
export const revalidate = 0

export default async function TestInvoicePage({
  params,
}: {
  params: { id: string }
}) {
  return (
    <div style={{ padding: '20px', fontFamily: 'Arial' }}>
      <h1>Test Invoice Page</h1>
      <p>Invoice ID: <strong>{params.id}</strong></p>
      <p>✅ Dynamic route is working!</p>
      <p>If you see this, the routing issue is fixed.</p>
      
      <hr />
      
      <h2>Test Results:</h2>
      <ul>
        <li>✅ Page loaded successfully (no 404)</li>
        <li>✅ Dynamic route [id] is rendering</li>
        <li>✅ Server component (no 'use client')</li>
        <li>✅ Force-dynamic is enabled</li>
      </ul>
      
      <p><a href="/invoices">← Back to invoices list</a></p>
    </div>
  )
}
