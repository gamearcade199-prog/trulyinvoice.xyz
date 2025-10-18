'use client'

import { useState, useEffect } from 'react'
import { useSearchParams, useRouter } from 'next/navigation'
import DashboardLayout from '@/components/DashboardLayout'
import { ArrowLeft, Calendar, DollarSign, Building2, FileText } from 'lucide-react'

export default function InvoiceDetailsPage() {
  const searchParams = useSearchParams()
  const router = useRouter()
  const invoiceId = searchParams.get('id')

  const [invoice, setInvoice] = useState<any>(null)
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    if (invoiceId) {
      fetchInvoiceDetails()
    }
  }, [invoiceId])

  const fetchInvoiceDetails = async () => {
    try {
      setLoading(true)
      console.log('🔍 Fetching invoice:', invoiceId)
      
      // Simple backend API call - no dynamic routing needed
      const response = await fetch(`https://trulyinvoice-backend.onrender.com/api/invoices/${invoiceId}`)
      
      if (!response.ok) {
        throw new Error(`Invoice not found: ${response.status}`)
      }
      
      const data = await response.json()
      console.log('✅ Invoice loaded:', data.vendor_name)
      setInvoice(data)
      
    } catch (error) {
      console.error('❌ Error:', error)
      alert('Could not load invoice details')
    } finally {
      setLoading(false)
    }
  }

  if (!invoiceId) {
    return (
      <DashboardLayout>
        <div className="p-8 text-center">
          <h1 className="text-xl text-gray-600">No invoice selected</h1>
          <button 
            onClick={() => router.push('/invoices')}
            className="mt-4 px-4 py-2 bg-blue-600 text-white rounded-md"
          >
            Back to Invoices
          </button>
        </div>
      </DashboardLayout>
    )
  }

  return (
    <DashboardLayout>
      <div className="p-6">
        {/* Header */}
        <div className="flex items-center gap-4 mb-6">
          <button
            onClick={() => router.push('/invoices')}
            className="flex items-center gap-2 px-3 py-2 text-gray-600 hover:text-gray-900 hover:bg-gray-100 rounded-md transition-colors"
          >
            <ArrowLeft className="w-4 h-4" />
            Back to Invoices
          </button>
          <h1 className="text-2xl font-bold text-gray-900 dark:text-white">
            Invoice Details
          </h1>
        </div>

        {loading ? (
          <div className="flex items-center justify-center py-12">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
          </div>
        ) : invoice ? (
          <div className="max-w-4xl">
            {/* Basic Information */}
            <div className="bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 p-6 mb-6">
              <h2 className="text-lg font-semibold text-gray-900 dark:text-white mb-4 flex items-center gap-2">
                <Building2 className="w-5 h-5" />
                Basic Information
              </h2>
              
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-500 dark:text-gray-400 mb-1">
                    Vendor Name
                  </label>
                  <p className="text-gray-900 dark:text-white font-medium">
                    {invoice.vendor_name || 'N/A'}
                  </p>
                </div>
                
                <div>
                  <label className="block text-sm font-medium text-gray-500 dark:text-gray-400 mb-1">
                    Invoice Number
                  </label>
                  <p className="text-gray-900 dark:text-white">
                    {invoice.invoice_number || 'N/A'}
                  </p>
                </div>
                
                <div>
                  <label className="block text-sm font-medium text-gray-500 dark:text-gray-400 mb-1">
                    Invoice Date
                  </label>
                  <p className="text-gray-900 dark:text-white flex items-center gap-2">
                    <Calendar className="w-4 h-4 text-gray-400" />
                    {invoice.invoice_date || 'N/A'}
                  </p>
                </div>
                
                <div>
                  <label className="block text-sm font-medium text-gray-500 dark:text-gray-400 mb-1">
                    Total Amount
                  </label>
                  <p className="text-gray-900 dark:text-white font-bold text-lg flex items-center gap-2">
                    <DollarSign className="w-4 h-4 text-green-600" />
                    ₹{invoice.total_amount?.toLocaleString() || '0'}
                  </p>
                </div>
                
                <div>
                  <label className="block text-sm font-medium text-gray-500 dark:text-gray-400 mb-1">
                    Payment Status
                  </label>
                  <span className={`inline-flex px-2 py-1 text-xs rounded-full ${
                    invoice.payment_status === 'paid' 
                      ? 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200'
                      : 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-200'
                  }`}>
                    {(invoice.payment_status || 'pending').charAt(0).toUpperCase() + 
                     (invoice.payment_status || 'pending').slice(1)}
                  </span>
                </div>
              </div>
            </div>

            {/* Amount Details */}
            <div className="bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 p-6">
              <h2 className="text-lg font-semibold text-gray-900 dark:text-white mb-4 flex items-center gap-2">
                <FileText className="w-5 h-5" />
                Amount Breakdown
              </h2>
              
              <div className="space-y-3">
                {invoice.subtotal && (
                  <div className="flex justify-between">
                    <span className="text-gray-600 dark:text-gray-400">Subtotal:</span>
                    <span className="text-gray-900 dark:text-white">₹{invoice.subtotal.toLocaleString()}</span>
                  </div>
                )}
                {invoice.cgst && (
                  <div className="flex justify-between">
                    <span className="text-gray-600 dark:text-gray-400">CGST:</span>
                    <span className="text-gray-900 dark:text-white">₹{invoice.cgst.toLocaleString()}</span>
                  </div>
                )}
                {invoice.sgst && (
                  <div className="flex justify-between">
                    <span className="text-gray-600 dark:text-gray-400">SGST:</span>
                    <span className="text-gray-900 dark:text-white">₹{invoice.sgst.toLocaleString()}</span>
                  </div>
                )}
                {invoice.igst && (
                  <div className="flex justify-between">
                    <span className="text-gray-600 dark:text-gray-400">IGST:</span>
                    <span className="text-gray-900 dark:text-white">₹{invoice.igst.toLocaleString()}</span>
                  </div>
                )}
                <div className="border-t border-gray-200 dark:border-gray-700 pt-3">
                  <div className="flex justify-between text-lg font-semibold">
                    <span className="text-gray-900 dark:text-white">Total Amount:</span>
                    <span className="text-gray-900 dark:text-white">₹{invoice.total_amount?.toLocaleString() || '0'}</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        ) : (
          <div className="text-center py-12">
            <p className="text-gray-600 dark:text-gray-400">Invoice not found</p>
            <button 
              onClick={() => router.push('/invoices')}
              className="mt-4 px-4 py-2 bg-blue-600 text-white rounded-md"
            >
              Back to Invoices
            </button>
          </div>
        )}
      </div>
    </DashboardLayout>
  )
}