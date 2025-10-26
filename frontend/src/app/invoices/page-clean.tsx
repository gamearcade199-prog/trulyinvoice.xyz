'use client'

import { useState, useEffect } from 'react'
import DashboardLayout from '@/components/DashboardLayout'
import Link from 'next/link'
import { 
  Search, 
  Filter, 
  Download,
  Eye,
  Trash2,
  Plus
} from 'lucide-react'
import { createClient } from '@supabase/supabase-js'
import { exportInvoicesToCSV } from '@/lib/invoiceUtils'

const supabase = createClient(
  process.env.NEXT_PUBLIC_SUPABASE_URL || 'https://placeholder.supabase.co',
  process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY || 'placeholder-anon-key'
)

export default function InvoicesPageClean() {
  const [searchQuery, setSearchQuery] = useState('')
  const [filterStatus, setFilterStatus] = useState('all')
  const [invoices, setInvoices] = useState<any[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchInvoices()
    
    // Auto-refresh every 10 seconds to pick up newly processed invoices
    const interval = setInterval(fetchInvoices, 10000)
    return () => clearInterval(interval)
  }, [])

  const fetchInvoices = async () => {
    try {
      setLoading(true)
      
      const { data: { user } } = await supabase.auth.getUser()
      if (!user) {
        console.log('No user logged in')
        setLoading(false)
        return
      }

      console.log('Fetching completed invoices for user:', user.id)

      // Fetch ONLY completed invoices with real data
      const { data: invoicesData, error: invoicesError } = await supabase
        .from('invoices')
        .select(`
          *,
          documents:document_id (
            storage_path,
            file_url,
            file_name
          )
        `)
        .neq('vendor_name', 'Processing...')  // No processing states
        .gt('total_amount', 0)  // Only real amounts
        .or(`user_id.eq.${user.id},user_id.is.null`)
        .order('created_at', { ascending: false })

      if (invoicesError) {
        console.error('Error fetching invoices:', invoicesError)
        setInvoices([])
        return
      }

      console.log('Fetched invoices:', invoicesData?.length || 0)
      setInvoices(invoicesData || [])
      
    } catch (error) {
      console.error('Fetch error:', error)
      setInvoices([])
    } finally {
      setLoading(false)
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
      exportInvoicesToCSV([invoice])
    } catch (error) {
      console.error('Export error:', error)
      alert('Failed to export invoice')
    }
  }

  const viewDocument = async (invoice: any) => {
    try {
      if (invoice.documents?.file_url) {
        window.open(invoice.documents.file_url, '_blank')
      } else if (invoice.documents?.storage_path) {
        const { data } = supabase.storage
          .from('invoice-documents')
          .getPublicUrl(invoice.documents.storage_path)
        
        if (data?.publicUrl) {
          window.open(data.publicUrl, '_blank')
        } else {
          alert('Unable to generate view URL')
        }
      } else {
        alert('No document file available')
      }
    } catch (error) {
      console.error('View error:', error)
      alert('Failed to open document. Please try again.')
    }
  }

  const deleteDocument = async (invoiceId: number) => {
    if (!confirm('Are you sure you want to delete this invoice?')) return
    
    try {
      const { error } = await supabase
        .from('invoices')
        .delete()
        .eq('id', invoiceId)
      
      if (error) throw error
      
      // Refresh the list
      await fetchInvoices()
    } catch (error) {
      console.error('Delete error:', error)
      alert('Failed to delete invoice')
    }
  }

  // Filter invoices based on search and status
  const filteredInvoices = invoices.filter(invoice => {
    const matchesSearch = searchQuery === '' || 
      invoice.vendor_name?.toLowerCase().includes(searchQuery.toLowerCase()) ||
      invoice.invoice_number?.toLowerCase().includes(searchQuery.toLowerCase())
    
    const matchesStatus = filterStatus === 'all' || 
      invoice.payment_status === filterStatus
    
    return matchesSearch && matchesStatus
  })

  if (loading) {
    return (
      <DashboardLayout>
        <div className="max-w-6xl mx-auto">
          <div className="flex items-center justify-center h-64">
            <div className="text-center">
              <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
              <p className="mt-4 text-gray-600">Loading invoices...</p>
            </div>
          </div>
        </div>
      </DashboardLayout>
    )
  }

  return (
    <DashboardLayout>
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 mb-8">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">Invoices</h1>
            <p className="text-gray-600 mt-1">Manage and track all your invoices in one place</p>
          </div>
          <Link
            href="/upload"
            className="inline-flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors font-semibold"
          >
            <Plus className="w-4 h-4" />
            Upload Invoice
          </Link>
        </div>

        {/* Search and Filter */}
        <div className="flex flex-col sm:flex-row gap-4 mb-6">
          <div className="relative flex-1">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
            <input
              type="text"
              placeholder="Search invoices by vendor, number..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
          </div>
          <div className="flex gap-2">
            <select
              value={filterStatus}
              onChange={(e) => setFilterStatus(e.target.value)}
              className="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            >
              <option value="all">All Status</option>
              <option value="paid">Paid</option>
              <option value="unpaid">Unpaid</option>
              <option value="overdue">Overdue</option>
            </select>
            
            {/* Export Button */}
            {invoices.length > 0 && (
              <button
                onClick={handleExport}
                className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors flex items-center gap-2 font-semibold"
              >
                <Download className="w-4 h-4" />
                Export
              </button>
            )}
          </div>
        </div>

        {/* Empty State */}
        {filteredInvoices.length === 0 ? (
          <div className="text-center py-12 bg-gray-50 rounded-xl">
            <div className="max-w-md mx-auto">
              <h3 className="text-lg font-semibold text-gray-900 mb-2">No invoices found</h3>
              <p className="text-gray-600 mb-6">Upload your first invoice to get started with AI-powered extraction</p>
              <Link href="/upload" className="inline-flex items-center gap-2 px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors font-semibold">
                <Plus className="w-4 h-4" />
                Upload Invoice
              </Link>
            </div>
          </div>
        ) : (
          <>
            {/* Desktop Table */}
            <div className="hidden md:block bg-white rounded-xl border border-gray-200 overflow-hidden">
              <table className="w-full">
                <thead className="bg-gray-50">
                  <tr>
                    <th className="text-left px-6 py-4 font-semibold text-gray-900">VENDOR</th>
                    <th className="text-left px-6 py-4 font-semibold text-gray-900">INVOICE #</th>
                    <th className="text-left px-6 py-4 font-semibold text-gray-900">DATE</th>
                    <th className="text-left px-6 py-4 font-semibold text-gray-900">DUE DATE</th>
                    <th className="text-left px-6 py-4 font-semibold text-gray-900">AMOUNT</th>
                    <th className="text-left px-6 py-4 font-semibold text-gray-900">GST</th>
                    <th className="text-left px-6 py-4 font-semibold text-gray-900">STATUS</th>
                    <th className="text-left px-6 py-4 font-semibold text-gray-900">ACTIONS</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-gray-200">
                  {filteredInvoices.map((invoice) => (
                    <tr key={invoice.id} className="hover:bg-gray-50">
                      <td className="px-6 py-4">
                        <div className="font-medium text-gray-900">{invoice.vendor_name || 'Unknown Vendor'}</div>
                      </td>
                      <td className="px-6 py-4 text-gray-600">{invoice.invoice_number || 'N/A'}</td>
                      <td className="px-6 py-4 text-gray-600">{invoice.invoice_date || 'N/A'}</td>
                      <td className="px-6 py-4 text-gray-600">{invoice.due_date || 'N/A'}</td>
                      <td className="px-6 py-4 font-semibold text-gray-900">₹{invoice.total_amount?.toLocaleString() || '0'}</td>
                      <td className="px-6 py-4 text-gray-600">₹{(invoice.cgst + invoice.sgst + invoice.igst || 0).toLocaleString()}</td>
                      <td className="px-6 py-4">
                        <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                          invoice.payment_status === 'paid' 
                            ? 'bg-green-100 text-green-800'
                            : invoice.payment_status === 'overdue'
                            ? 'bg-red-100 text-red-800'
                            : 'bg-yellow-100 text-yellow-800'
                        }`}>
                          {(invoice.payment_status || 'unpaid').charAt(0).toUpperCase() + (invoice.payment_status || 'unpaid').slice(1)}
                        </span>
                      </td>
                      <td className="px-6 py-4">
                        <div className="flex items-center gap-2">
                          {/* Export button for each invoice */}
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
                            title="Delete Invoice"
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

            {/* Mobile Cards */}
            <div className="md:hidden space-y-4">
              {filteredInvoices.map((invoice) => (
                <div key={invoice.id} className="bg-white rounded-xl border border-gray-200 p-4">
                  <div className="flex items-start justify-between mb-3">
                    <div>
                      <h3 className="font-semibold text-gray-900">{invoice.vendor_name || 'Unknown Vendor'}</h3>
                      <p className="text-sm text-gray-600">{invoice.invoice_number || 'N/A'}</p>
                    </div>
                    <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                      invoice.payment_status === 'paid' 
                        ? 'bg-green-100 text-green-800'
                        : invoice.payment_status === 'overdue'
                        ? 'bg-red-100 text-red-800'
                        : 'bg-yellow-100 text-yellow-800'
                    }`}>
                      {(invoice.payment_status || 'unpaid').charAt(0).toUpperCase() + (invoice.payment_status || 'unpaid').slice(1)}
                    </span>
                  </div>
                  <div className="space-y-2 mb-4">
                    <div className="flex justify-between text-sm">
                      <span className="text-gray-600">Amount:</span>
                      <span className="font-semibold">₹{invoice.total_amount?.toLocaleString() || '0'}</span>
                    </div>
                    <div className="flex justify-between text-sm">
                      <span className="text-gray-600">GST:</span>
                      <span>₹{(invoice.cgst + invoice.sgst + invoice.igst || 0).toLocaleString()}</span>
                    </div>
                    <div className="flex justify-between text-sm">
                      <span className="text-gray-600">Due:</span>
                      <span>{invoice.due_date || 'N/A'}</span>
                    </div>
                  </div>
                  <div className="flex items-center gap-2">
                    <button
                      onClick={() => exportSingleInvoice(invoice)}
                      className="flex-1 py-2 px-3 bg-green-50 text-green-600 rounded-lg hover:bg-green-100 transition-colors text-sm font-medium"
                    >
                      Export
                    </button>
                    <button
                      onClick={() => viewDocument(invoice)}
                      className="flex-1 py-2 px-3 bg-blue-50 text-blue-600 rounded-lg hover:bg-blue-100 transition-colors text-sm font-medium"
                    >
                      View
                    </button>
                    <button
                      onClick={() => deleteDocument(invoice.id)}
                      className="py-2 px-3 bg-red-50 text-red-600 rounded-lg hover:bg-red-100 transition-colors text-sm"
                    >
                      <Trash2 className="w-4 h-4" />
                    </button>
                  </div>
                </div>
              ))}
            </div>

            {/* Pagination */}
            <div className="flex items-center justify-between mt-6">
              <p className="text-sm text-gray-600">
                Showing {filteredInvoices.length} invoice{filteredInvoices.length !== 1 ? 's' : ''}
              </p>
              <div className="flex gap-2">
                <button className="px-4 py-2 text-gray-600 border border-gray-300 rounded-lg hover:bg-gray-50">
                  Previous
                </button>
                <button className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700">
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