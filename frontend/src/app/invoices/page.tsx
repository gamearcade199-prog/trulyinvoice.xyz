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
  process.env.NEXT_PUBLIC_SUPABASE_URL!,
  process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!
)

export default function InvoicesPageClean() {
  const [searchQuery, setSearchQuery] = useState('')
  const [filterStatus, setFilterStatus] = useState('all')
  const [invoices, setInvoices] = useState<any[]>([])
  const [loading, setLoading] = useState(true)
  const [selectedInvoices, setSelectedInvoices] = useState<Set<number>>(new Set())

  useEffect(() => {
    fetchInvoices()
    // Auto-refresh removed - was annoying. User can manually refresh if needed.
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

      // Fetch ONLY user's invoices (removed .or(user_id.is.null) to exclude dummy data)
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
        .eq('user_id', user.id)
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

  // Checkbox handlers
  const toggleSelectInvoice = (invoiceId: number) => {
    const newSelected = new Set(selectedInvoices)
    if (newSelected.has(invoiceId)) {
      newSelected.delete(invoiceId)
    } else {
      newSelected.add(invoiceId)
    }
    setSelectedInvoices(newSelected)
  }

  const toggleSelectAll = () => {
    if (selectedInvoices.size === filteredInvoices.length) {
      setSelectedInvoices(new Set())
    } else {
      setSelectedInvoices(new Set(filteredInvoices.map(inv => inv.id)))
    }
  }

  const exportSelectedInvoices = () => {
    const selected = invoices.filter(inv => selectedInvoices.has(inv.id))
    if (selected.length === 0) {
      alert('Please select invoices to export')
      return
    }
    try {
      exportInvoicesToCSV(selected)
    } catch (error) {
      console.error('Export error:', error)
      alert('Failed to export selected invoices')
    }
  }

  const deleteSelectedInvoices = async () => {
    if (selectedInvoices.size === 0) {
      alert('Please select invoices to delete')
      return
    }

    if (!confirm(`Are you sure you want to delete ${selectedInvoices.size} selected invoice(s)?`)) {
      return
    }

    try {
      const { error } = await supabase
        .from('invoices')
        .delete()
        .in('id', Array.from(selectedInvoices))
      
      if (error) throw error
      
      setSelectedInvoices(new Set())
      await fetchInvoices()
      alert(`Successfully deleted ${selectedInvoices.size} invoice(s)`)
    } catch (error) {
      console.error('Delete error:', error)
      alert('Failed to delete selected invoices')
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
              <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 dark:border-blue-400 mx-auto"></div>
              <p className="mt-4 text-gray-600 dark:text-gray-400">Loading invoices...</p>
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
            <h1 className="text-3xl font-bold text-gray-900 dark:text-white">Invoices</h1>
            <p className="text-gray-600 dark:text-gray-400 mt-1">Manage and track all your invoices in one place</p>
          </div>
          <Link
            href="/upload"
            className="inline-flex items-center gap-2 px-4 py-2 bg-blue-600 dark:bg-blue-500 text-white rounded-lg hover:bg-blue-700 dark:hover:bg-blue-600 transition-colors font-semibold"
          >
            <Plus className="w-4 h-4" />
            Upload Invoice
          </Link>
        </div>

        {/* Search and Filter */}
        <div className="flex flex-col sm:flex-row gap-4 mb-6">
          <div className="relative flex-1">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 dark:text-gray-500 w-5 h-5" />
            <input
              type="text"
              placeholder="Search invoices by vendor, number..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="w-full pl-10 pr-4 py-2 border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-white rounded-lg focus:ring-2 focus:ring-blue-500 dark:focus:ring-blue-400 focus:border-transparent"
            />
          </div>
          <div className="flex gap-2">
            <select
              value={filterStatus}
              onChange={(e) => setFilterStatus(e.target.value)}
              className="px-4 py-2 border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-white rounded-lg focus:ring-2 focus:ring-blue-500 dark:focus:ring-blue-400 focus:border-transparent"
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
                className="px-4 py-2 bg-blue-600 dark:bg-blue-500 text-white rounded-lg hover:bg-blue-700 dark:hover:bg-blue-600 transition-colors flex items-center gap-2 font-semibold"
              >
                <Download className="w-4 h-4" />
                Export All
              </button>
            )}
          </div>
        </div>

        {/* Bulk Actions Bar */}
        {selectedInvoices.size > 0 && (
          <div className="mb-4 p-4 bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800 rounded-lg flex items-center justify-between">
            <span className="text-blue-900 dark:text-blue-100 font-semibold">
              {selectedInvoices.size} invoice(s) selected
            </span>
            <div className="flex gap-2">
              <button
                onClick={exportSelectedInvoices}
                className="px-4 py-2 bg-blue-600 dark:bg-blue-500 text-white rounded-lg hover:bg-blue-700 dark:hover:bg-blue-600 transition-colors flex items-center gap-2 text-sm font-semibold"
              >
                <Download className="w-4 h-4" />
                Export Selected
              </button>
              <button
                onClick={deleteSelectedInvoices}
                className="px-4 py-2 bg-red-600 dark:bg-red-500 text-white rounded-lg hover:bg-red-700 dark:hover:bg-red-600 transition-colors flex items-center gap-2 text-sm font-semibold"
              >
                <Trash2 className="w-4 h-4" />
                Delete Selected
              </button>
            </div>
          </div>
        )}

        {/* Empty State */}
        {filteredInvoices.length === 0 ? (
          <div className="text-center py-12 bg-gray-50 dark:bg-gray-800/50 rounded-xl">
            <div className="max-w-md mx-auto">
              <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">No invoices found</h3>
              <p className="text-gray-600 dark:text-gray-400 mb-6">Upload your first invoice to get started with AI-powered extraction</p>
              <Link href="/upload" className="inline-flex items-center gap-2 px-6 py-3 bg-blue-600 dark:bg-blue-500 text-white rounded-lg hover:bg-blue-700 dark:hover:bg-blue-600 transition-colors font-semibold">
                <Plus className="w-4 h-4" />
                Upload Invoice
              </Link>
            </div>
          </div>
        ) : (
          <>
            {/* Desktop Table */}
            <div className="hidden md:block bg-white dark:bg-gray-800 rounded-xl border border-gray-200 dark:border-gray-700 overflow-hidden">
              <table className="w-full">
                <thead className="bg-gray-50 dark:bg-gray-700/50">
                  <tr>
                    <th className="px-6 py-4">
                      <input
                        type="checkbox"
                        checked={selectedInvoices.size === filteredInvoices.length && filteredInvoices.length > 0}
                        onChange={toggleSelectAll}
                        className="w-4 h-4 text-blue-600 border-gray-300 dark:border-gray-600 rounded focus:ring-blue-500 cursor-pointer"
                      />
                    </th>
                    <th className="text-left px-6 py-4 font-semibold text-gray-900 dark:text-gray-300">VENDOR</th>
                    <th className="text-left px-6 py-4 font-semibold text-gray-900 dark:text-gray-300">INVOICE #</th>
                    <th className="text-left px-6 py-4 font-semibold text-gray-900 dark:text-gray-300">DATE</th>
                    <th className="text-left px-6 py-4 font-semibold text-gray-900 dark:text-gray-300">DUE DATE</th>
                    <th className="text-left px-6 py-4 font-semibold text-gray-900 dark:text-gray-300">AMOUNT</th>
                    <th className="text-left px-6 py-4 font-semibold text-gray-900 dark:text-gray-300">GST</th>
                    <th className="text-left px-6 py-4 font-semibold text-gray-900 dark:text-gray-300">STATUS</th>
                    <th className="text-left px-6 py-4 font-semibold text-gray-900 dark:text-gray-300">ACTIONS</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-gray-200 dark:divide-gray-700">
                  {filteredInvoices.map((invoice) => (
                    <tr key={invoice.id} className="hover:bg-gray-50 dark:hover:bg-gray-700/50">
                      <td className="px-6 py-4">
                        <input
                          type="checkbox"
                          checked={selectedInvoices.has(invoice.id)}
                          onChange={() => toggleSelectInvoice(invoice.id)}
                          className="w-4 h-4 text-blue-600 border-gray-300 dark:border-gray-600 rounded focus:ring-blue-500 cursor-pointer"
                        />
                      </td>
                      <td className="px-6 py-4">
                        <div className="font-medium text-gray-900 dark:text-white">{invoice.vendor_name || 'Unknown Vendor'}</div>
                      </td>
                      <td className="px-6 py-4 text-gray-600 dark:text-gray-400">{invoice.invoice_number || 'N/A'}</td>
                      <td className="px-6 py-4 text-gray-600 dark:text-gray-400">{invoice.invoice_date || 'N/A'}</td>
                      <td className="px-6 py-4 text-gray-600 dark:text-gray-400">{invoice.due_date || 'N/A'}</td>
                      <td className="px-6 py-4 font-semibold text-gray-900 dark:text-white">₹{invoice.total_amount?.toLocaleString() || '0'}</td>
                      <td className="px-6 py-4 text-gray-600 dark:text-gray-400">₹{(invoice.cgst + invoice.sgst + invoice.igst || 0).toLocaleString()}</td>
                      <td className="px-6 py-4">
                        <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                          invoice.payment_status === 'paid' 
                            ? 'bg-green-100 dark:bg-green-900/50 text-green-800 dark:text-green-300'
                            : invoice.payment_status === 'overdue'
                            ? 'bg-red-100 dark:bg-red-900/50 text-red-800 dark:text-red-300'
                            : 'bg-yellow-100 dark:bg-yellow-900/50 text-yellow-800 dark:text-yellow-300'
                        }`}>
                          {(invoice.payment_status || 'unpaid').charAt(0).toUpperCase() + (invoice.payment_status || 'unpaid').slice(1)}
                        </span>
                      </td>
                      <td className="px-6 py-4">
                        <div className="flex items-center gap-2">
                          {/* View Details button */}
                          <Link
                            href={`/invoices/${invoice.id}`}
                            className="p-2 hover:bg-blue-50 dark:hover:bg-blue-900/30 rounded-lg transition-colors group"
                            title="View Details"
                          >
                            <Eye className="w-5 h-5 text-gray-600 dark:text-gray-400 group-hover:text-blue-600 dark:group-hover:text-blue-400" />
                          </Link>
                          {/* Export button for each invoice */}
                          <button
                            onClick={() => exportSingleInvoice(invoice)}
                            className="p-2 hover:bg-green-50 dark:hover:bg-green-900/30 rounded-lg transition-colors group"
                            title="Export to Excel"
                          >
                            <Download className="w-5 h-5 text-gray-600 dark:text-gray-400 group-hover:text-green-600 dark:group-hover:text-green-400" />
                          </button>
                          <button
                            onClick={() => deleteDocument(invoice.id)}
                            className="p-2 hover:bg-red-50 dark:hover:bg-red-900/30 rounded-lg transition-colors group"
                            title="Delete Invoice"
                          >
                            <Trash2 className="w-5 h-5 text-gray-600 dark:text-gray-400 group-hover:text-red-600 dark:group-hover:text-red-400" />
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
                <div key={invoice.id} className="bg-white dark:bg-gray-800 rounded-xl border border-gray-200 dark:border-gray-700 p-4">
                  <div className="flex items-start gap-3 mb-3">
                    <input
                      type="checkbox"
                      checked={selectedInvoices.has(invoice.id)}
                      onChange={() => toggleSelectInvoice(invoice.id)}
                      className="mt-1 w-4 h-4 text-blue-600 border-gray-300 dark:border-gray-600 rounded focus:ring-blue-500 cursor-pointer"
                    />
                    <div className="flex-1">
                      <div className="flex items-start justify-between">
                        <div>
                          <h3 className="font-semibold text-gray-900 dark:text-white">{invoice.vendor_name || 'Unknown Vendor'}</h3>
                          <p className="text-sm text-gray-600 dark:text-gray-400">{invoice.invoice_number || 'N/A'}</p>
                        </div>
                        <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                          invoice.payment_status === 'paid' 
                            ? 'bg-green-100 dark:bg-green-900/50 text-green-800 dark:text-green-300'
                            : invoice.payment_status === 'overdue'
                            ? 'bg-red-100 dark:bg-red-900/50 text-red-800 dark:text-red-300'
                            : 'bg-yellow-100 dark:bg-yellow-900/50 text-yellow-800 dark:text-yellow-300'
                        }`}>
                          {(invoice.payment_status || 'unpaid').charAt(0).toUpperCase() + (invoice.payment_status || 'unpaid').slice(1)}
                        </span>
                      </div>
                    </div>
                  </div>
                  <div className="space-y-2 mb-4">
                    <div className="flex justify-between text-sm">
                      <span className="text-gray-600 dark:text-gray-400">Amount:</span>
                      <span className="font-semibold text-gray-900 dark:text-white">₹{invoice.total_amount?.toLocaleString() || '0'}</span>
                    </div>
                    <div className="flex justify-between text-sm">
                      <span className="text-gray-600 dark:text-gray-400">GST:</span>
                      <span className="text-gray-900 dark:text-white">₹{(invoice.cgst + invoice.sgst + invoice.igst || 0).toLocaleString()}</span>
                    </div>
                    <div className="flex justify-between text-sm">
                      <span className="text-gray-600 dark:text-gray-400">Due:</span>
                      <span className="text-gray-900 dark:text-white">{invoice.due_date || 'N/A'}</span>
                    </div>
                  </div>
                  <div className="flex items-center gap-2">
                    <Link
                      href={`/invoices/${invoice.id}`}
                      className="flex-1 py-2 px-3 bg-blue-50 dark:bg-blue-900/30 text-blue-600 dark:text-blue-400 rounded-lg hover:bg-blue-100 dark:hover:bg-blue-900/50 transition-colors text-sm font-medium text-center"
                    >
                      Details
                    </Link>
                    <button
                      onClick={() => exportSingleInvoice(invoice)}
                      className="flex-1 py-2 px-3 bg-green-50 dark:bg-green-900/30 text-green-600 dark:text-green-400 rounded-lg hover:bg-green-100 dark:hover:bg-green-900/50 transition-colors text-sm font-medium"
                    >
                      Export
                    </button>
                    <button
                      onClick={() => deleteDocument(invoice.id)}
                      className="py-2 px-3 bg-red-50 dark:bg-red-900/30 text-red-600 dark:text-red-400 rounded-lg hover:bg-red-100 dark:hover:bg-red-900/50 transition-colors text-sm"
                    >
                      <Trash2 className="w-4 h-4" />
                    </button>
                  </div>
                </div>
              ))}
            </div>

            {/* Pagination */}
            <div className="flex items-center justify-between mt-6">
              <p className="text-sm text-gray-600 dark:text-gray-400">
                Showing {filteredInvoices.length} invoice{filteredInvoices.length !== 1 ? 's' : ''}
              </p>
              <div className="flex gap-2">
                <button className="px-4 py-2 text-gray-600 dark:text-gray-400 border border-gray-300 dark:border-gray-600 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700">
                  Previous
                </button>
                <button className="px-4 py-2 bg-blue-600 dark:bg-blue-500 text-white rounded-lg hover:bg-blue-700 dark:hover:bg-blue-600">
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