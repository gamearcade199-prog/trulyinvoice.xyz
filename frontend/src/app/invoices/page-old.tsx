'use client'

import { useState, useEffect } from 'react'
import DashboardLayout from '@/components/DashboardLayout'
import Link from 'next/link'
import { 
  Search, 
  Filter, 
  Download,
  Eye,
  Edit,
  Trash2,
  MoreVertical,
  ArrowUpDown
} from 'lucide-react'
import { supabase } from '@/lib/supabase'
import { exportInvoicesToCSV } from '@/lib/invoiceUtils'

export default function InvoicesPage() {
  const [searchQuery, setSearchQuery] = useState('')
  const [filterStatus, setFilterStatus] = useState('all')
  const [invoices, setInvoices] = useState<any[]>([])
  const [loading, setLoading] = useState(true)
  const [processing, setProcessing] = useState<string | null>(null)
  const [autoRefreshEnabled, setAutoRefreshEnabled] = useState(true)

  useEffect(() => {
    fetchInvoices()
    
    // Set up auto-refresh polling every 5 seconds for real-time updates
    const interval = setInterval(() => {
      if (autoRefreshEnabled) {
        fetchInvoices()
      }
    }, 5000)
    
    return () => clearInterval(interval)
  }, [autoRefreshEnabled])

  const processDocument = async (documentId: string) => {
    setProcessing(documentId)
    try {
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/documents/${documentId}/process`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${(await supabase.auth.getSession()).data.session?.access_token}`
        }
      })

      if (!response.ok) {
        throw new Error('Failed to process document')
      }

      // Refresh the list
      await fetchInvoices()
      alert('Invoice processed successfully! Refresh the page to see extracted data.')
    } catch (error) {
      console.error('Error processing document:', error)
      alert('Failed to process document. Make sure the backend is running.')
    } finally {
      setProcessing(null)
    }
  }

  const deleteDocument = async (documentId: string) => {
    if (!confirm('Are you sure you want to delete this invoice?')) return

    try {
      const { error } = await supabase
        .from('documents')
        .delete()
        .eq('id', documentId)

      if (error) throw error

      // Also delete from invoices table
      await supabase
        .from('invoices')
        .delete()
        .eq('document_id', documentId)

      // Refresh the list
      await fetchInvoices()
      alert('Invoice deleted successfully!')
    } catch (error) {
      console.error('Error deleting document:', error)
      alert('Failed to delete invoice')
    }
  }

  const viewDocument = async (invoice: any) => {
    try {
      if (!invoice.storage_path) {
        alert('File path not found')
        return
      }

      // Generate a signed URL for private bucket
      const { data, error } = await supabase.storage
        .from('invoice-documents')
        .createSignedUrl(invoice.storage_path, 3600) // Valid for 1 hour

      if (error) throw error

      if (data?.signedUrl) {
        window.open(data.signedUrl, '_blank')
      } else {
        alert('Could not generate file URL')
      }
    } catch (error) {
      console.error('Error viewing document:', error)
      alert('Failed to open document. Please try again.')
    }
  }

  const handleExport = () => {
    try {
      exportInvoicesToCSV(invoices)
    } catch (error) {
      console.error('Export error:', error)
      alert('Failed to export invoices')
    }
  }

  const exportSingleInvoice = (invoice: any) => {
    try {
      exportInvoicesToCSV([invoice])  // Export single invoice as array
    } catch (error) {
      console.error('Export error:', error)
      alert('Failed to export invoice')
    }
  }

  const retryProcessing = async (invoice: any) => {
    try {
      if (!invoice.document_id) {
        alert('Document ID not found')
        return
      }

      const confirmRetry = confirm(`Retry AI extraction for invoice ${invoice.invoice_number}?`)
      if (!confirmRetry) return

      console.log('🚀 Starting AI processing for document:', invoice.document_id)
      
      // Update UI to show processing state
      const updateProcessingState = (message: string) => {
        setInvoices(prevInvoices => 
          prevInvoices.map(inv => 
            inv.id === invoice.id 
              ? { ...inv, vendor_name: message, processing: true }
              : inv
          )
        )
      }
      
      updateProcessingState('🧠 AI Extracting...')
      
      // Get the current session token
      const { data: { session } } = await supabase.auth.getSession()
      
      const response = await fetch(`http://localhost:8000/api/documents/${invoice.document_id}/process`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${session?.access_token || ''}`
        }
      })

      if (!response.ok) {
        const errorText = await response.text()
        console.error('❌ Processing failed:', errorText)
        updateProcessingState('❌ Processing Failed')
        throw new Error(`Failed to process: ${errorText}`)
      }

      const result = await response.json()
      console.log('✅ Processing result:', result)
      
      // Show success state briefly
      updateProcessingState('✅ Processing Complete!')
      
      // Auto-refresh data after 2 seconds
      setTimeout(async () => {
        console.log('📊 Refreshing invoice data...')
        await fetchInvoices()
        console.log('🎉 Data refreshed! Invoice should show real values now.')
      }, 2000)
      
    } catch (error) {
      console.error('Error triggering processing:', error)
      alert('Failed to trigger AI extraction. Check console for details.')
    }
  }

  const fetchInvoices = async () => {
    try {
      const { data: { user } } = await supabase.auth.getUser()
      if (!user) {
        console.log('No user logged in')
        setLoading(false)
        return
      }

      console.log('Fetching data for user:', user.id)

      // Fetch only successfully processed invoices (no processing states)
      const { data: invoicesData, error: invoicesError } = await supabase
        .from('invoices')
        .select(`
          *,
          documents:document_id (
            storage_path,
            file_url
          )
        `)
        .neq('vendor_name', 'Processing...')  // Only real invoices
        .gt('total_amount', 0)  // Only invoices with real amounts
        .or(`user_id.eq.${user.id},user_id.is.null`)
        .order('invoice_date', { ascending: false })

      const { data: documentsData, error: documentsError } = await supabase
        .from('documents')
        .select('*')
        .or(`user_id.eq.${user.id},user_id.is.null`)
        .order('created_at', { ascending: false })

      console.log('Invoices data:', invoicesData)
      console.log('Documents data:', documentsData)

      if (invoicesError) console.error('Invoices error:', invoicesError)
      if (documentsError) console.error('Documents error:', documentsError)

      // Flatten the invoices data to include storage_path from documents
      const flattenedInvoices = (invoicesData || []).map(inv => ({
        ...inv,
        storage_path: inv.documents?.storage_path,
        file_url: inv.documents?.file_url
      }))

      // Combine invoices and documents (show documents that don't have invoices yet)
      const invoiceDocIds = flattenedInvoices.map(inv => inv.document_id)
      const unprocessedDocs = (documentsData || []).filter(doc => !invoiceDocIds.includes(doc.id))
      
      console.log('Unprocessed documents:', unprocessedDocs)
      
      // Convert unprocessed documents to invoice format for display
      const docsAsInvoices = unprocessedDocs.map(doc => ({
        id: doc.id,
        vendor_name: 'Processing...',
        invoice_number: doc.file_name || doc.storage_path?.split('/').pop() || 'Uploaded File',
        invoice_date: doc.created_at,
        due_date: null,
        total_amount: 0,
        tax_amount: 0,
        payment_status: 'processing',
        document_id: doc.id,
        storage_path: doc.storage_path, // Add this for viewDocument to work
        file_url: doc.file_url || doc.storage_path
      }))

      console.log('Final invoices:', [...flattenedInvoices, ...docsAsInvoices])
      setInvoices([...flattenedInvoices, ...docsAsInvoices])
      setLoading(false)
    } catch (error) {
      console.error('Error fetching invoices:', error)
      setLoading(false)
    }
  }

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'paid':
        return 'bg-green-100 text-green-700 border-green-200'
      case 'unpaid':
        return 'bg-yellow-100 text-yellow-700 border-yellow-200'
      case 'overdue':
        return 'bg-red-100 text-red-700 border-red-200'
      case 'processing':
        return 'bg-blue-100 text-blue-700 border-blue-200'
      case 'completed':
        return 'bg-emerald-100 text-emerald-700 border-emerald-200'
      default:
        return 'bg-gray-100 text-gray-700 border-gray-200'
    }
  }

  return (
    <DashboardLayout>
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="mb-6">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">Invoices</h1>
          <p className="text-gray-600">Manage and track all your invoices in one place</p>
        </div>

        {/* Filters & Search */}
        <div className="bg-white rounded-xl border border-gray-200 p-6 mb-6">
          <div className="flex flex-col md:flex-row gap-4">
            {/* Search */}
            <div className="flex-1 relative">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" />
              <input
                type="text"
                placeholder="Search invoices by vendor, number..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="w-full pl-10 pr-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>

            {/* Status Filter */}
            <select
              value={filterStatus}
              onChange={(e) => setFilterStatus(e.target.value)}
              className="px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            >
              <option value="all">All Status</option>
              <option value="paid">Paid</option>
              <option value="unpaid">Unpaid</option>
              <option value="overdue">Overdue</option>
            </select>

            {/* Export Button */}
            <button 
              onClick={handleExport}
              className="flex items-center gap-2 px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors font-semibold"
            >
              <Download className="w-5 h-5" />
              Export
            </button>
          </div>
        </div>

        {/* Invoice Cards (Mobile) */}
        {loading ? (
          <div className="text-center py-12">
            <div className="inline-block h-8 w-8 animate-spin rounded-full border-4 border-solid border-blue-600 border-r-transparent"></div>
            <p className="mt-4 text-gray-600">Loading invoices...</p>
          </div>
        ) : invoices.length === 0 ? (
          <div className="bg-white rounded-xl border border-gray-200 p-12 text-center">
            <h3 className="text-xl font-semibold text-gray-900 mb-2">No Invoices Yet</h3>
            <p className="text-gray-600 mb-6">Upload your first invoice to get started with AI-powered extraction</p>
            <Link href="/upload" className="inline-flex items-center gap-2 px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors font-semibold">
              Upload Invoice
            </Link>
          </div>
        ) : (
          <>
        <div className="md:hidden space-y-4 mb-6">
          {invoices.map((invoice) => (
            <div key={invoice.id} className="bg-white rounded-xl border border-gray-200 p-4">
              <div className="flex items-start justify-between mb-3">
                <div>
                  <h3 className="font-semibold text-gray-900">{invoice.vendor_name || 'Unknown Vendor'}</h3>
                  <p className="text-sm text-gray-600">{invoice.invoice_number || 'N/A'}</p>
                </div>
                <span className={`px-3 py-1 rounded-full text-xs font-semibold border ${getStatusColor(invoice.payment_status || 'unpaid')}`}>
                  {(invoice.payment_status || 'unpaid').charAt(0).toUpperCase() + (invoice.payment_status || 'unpaid').slice(1)}
                </span>
              </div>
              <div className="grid grid-cols-2 gap-3 mb-3 text-sm">
                <div>
                  <p className="text-gray-600">Amount</p>
                  <p className="font-semibold text-gray-900">₹{invoice.total_amount ? invoice.total_amount.toLocaleString('en-IN') : '0'}</p>
                </div>
                <div>
                  <p className="text-gray-600">Date</p>
                  <p className="font-semibold text-gray-900">{invoice.invoice_date ? new Date(invoice.invoice_date).toLocaleDateString() : 'N/A'}</p>
                </div>
              </div>
              <div className="flex gap-2">
                <button
                  onClick={() => viewDocument(invoice)}
                  className="flex-1 flex items-center justify-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors font-semibold"
                >
                  <Eye className="w-4 h-4" />
                  View Invoice
                </button>
                <button
                  onClick={() => deleteDocument(invoice.id)}
                  className="px-4 py-2 border border-red-300 text-red-600 rounded-lg hover:bg-red-50 transition-colors"
                >
                  <Trash2 className="w-5 h-5" />
                </button>
              </div>
            </div>
          ))}
        </div>

        {/* Invoice Table (Desktop) */}
        <div className="hidden md:block bg-white rounded-xl border border-gray-200 overflow-hidden">
          <table className="w-full">
            <thead className="bg-gray-50 border-b border-gray-200">
              <tr>
                <th className="px-6 py-4 text-left">
                  <button className="flex items-center gap-2 text-xs font-semibold text-gray-600 uppercase tracking-wider hover:text-gray-900">
                    Vendor <ArrowUpDown className="w-4 h-4" />
                  </button>
                </th>
                <th className="px-6 py-4 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">
                  Invoice #
                </th>
                <th className="px-6 py-4 text-left">
                  <button className="flex items-center gap-2 text-xs font-semibold text-gray-600 uppercase tracking-wider hover:text-gray-900">
                    Date <ArrowUpDown className="w-4 h-4" />
                  </button>
                </th>
                <th className="px-6 py-4 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">
                  Due Date
                </th>
                <th className="px-6 py-4 text-left">
                  <button className="flex items-center gap-2 text-xs font-semibold text-gray-600 uppercase tracking-wider hover:text-gray-900">
                    Amount <ArrowUpDown className="w-4 h-4" />
                  </button>
                </th>
                <th className="px-6 py-4 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">
                  GST
                </th>
                <th className="px-6 py-4 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">
                  Status
                </th>
                <th className="px-6 py-4 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">
                  Actions
                </th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-200">
              {invoices.map((invoice) => (
                <tr key={invoice.id} data-invoice-id={invoice.id} className={`hover:bg-gray-50 transition-colors ${invoice.processing ? 'bg-blue-50' : ''}`}>
                  <td className="px-6 py-4">
                    <div className={`font-semibold ${invoice.processing ? 'text-blue-600 animate-pulse' : 'text-gray-900'}`}>
                      {invoice.vendor_name || 'Processing...'}
                    </div>
                  </td>
                  <td className="px-6 py-4 text-gray-600">{invoice.invoice_number || 'N/A'}</td>
                  <td className="px-6 py-4 text-gray-600">{invoice.invoice_date ? new Date(invoice.invoice_date).toLocaleDateString() : 'N/A'}</td>
                  <td className="px-6 py-4 text-gray-600">{invoice.due_date ? new Date(invoice.due_date).toLocaleDateString() : 'N/A'}</td>
                  <td className="px-6 py-4">
                    <span className="font-semibold text-gray-900">
                      ₹{invoice.total_amount ? invoice.total_amount.toLocaleString('en-IN') : '0'}
                    </span>
                  </td>
                  <td className="px-6 py-4 text-gray-600">
                    ₹{invoice.tax_amount ? invoice.tax_amount.toLocaleString('en-IN') : '0'}
                  </td>
                  <td className="px-6 py-4">
                    <span className={`px-3 py-1 rounded-full text-xs font-semibold border ${getStatusColor(invoice.payment_status || 'unpaid')}`}>
                      {(invoice.payment_status || 'unpaid').charAt(0).toUpperCase() + (invoice.payment_status || 'unpaid').slice(1)}
                    </span>
                  </td>
                  <td className="px-6 py-4">
                    <div className="flex items-center gap-2">
                      {/* Export button for all invoices (since they're all completed) */}
                      <button
                        onClick={() => exportSingleInvoice(invoice)}
                        className="p-2 hover:bg-green-50 rounded-lg transition-colors group"
                        title="Export to Excel"
                      >
                        <Download className="w-5 h-5 text-gray-600 group-hover:text-green-600" />
                      </button>
                      <button
                        onClick={() => viewDocument(invoice)}
                        className="p-2 hover:bg-blue-50 rounded-lg transition-colors group"
                        title="View Invoice"
                      >
                        <Eye className="w-5 h-5 text-gray-600 group-hover:text-blue-600" />
                      </button>
                      <button
                        onClick={() => deleteDocument(invoice.id)}
                        className="p-2 hover:bg-red-50 rounded-lg transition-colors group"
                        title="Delete"
                      >
                        <Trash2 className="w-5 h-5 text-gray-600 group-hover:text-red-600" />
                      </button>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        {/* Pagination */}
        <div className="mt-6 flex items-center justify-between">
          <p className="text-sm text-gray-600">
            Showing <span className="font-semibold">{invoices.length}</span> invoice{invoices.length !== 1 ? 's' : ''}
          </p>
          <div className="flex gap-2">
            <button className="px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors text-sm font-semibold text-gray-700">
              Previous
            </button>
            <button className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors text-sm font-semibold">
              Next
            </button>
          </div>
        </div>
        </>
        )}
      </div>
    </DashboardLayout>
  )
}