'use client'

export default function InvoiceDetailsPage() {
  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50">
      <div className="text-center p-8 bg-white rounded-lg shadow-lg">
        <h1 className="text-3xl font-bold text-green-600 mb-4">🎉 ROUTE WORKING!</h1>
        <p className="text-xl text-gray-700 mb-2">Invoice Details Page Loaded Successfully</p>
        <p className="text-sm text-gray-500">Dynamic [id] route is working correctly</p>
        <div className="mt-4">
          <a 
            href="/invoices" 
            className="text-blue-600 hover:text-blue-800 underline"
          >
            ← Back to Invoices
          </a>
        </div>
      </div>
    </div>
  )
}