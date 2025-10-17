'use client'

import { useState, useEffect } from 'react'
import { useParams, useRouter } from 'next/navigation'
import DashboardLayout from '@/components/DashboardLayout'
import { createClient } from '@supabase/supabase-js'
import { 
  ArrowLeft, 
  Save, 
  X, 
  Edit2, 
  Download,
  Trash2,
  FileText,
  Calendar,
  DollarSign,
  Building2,
  Hash
} from 'lucide-react'

const supabase = createClient(
  process.env.NEXT_PUBLIC_SUPABASE_URL!,
  process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!
)

export default function InvoiceDetailsPage() {
  const params = useParams()
  const router = useRouter()
  const invoiceId = params.id as string

  const [invoice, setInvoice] = useState<any>(null)
  const [loading, setLoading] = useState(true)
  const [editing, setEditing] = useState(false)
  const [saving, setSaving] = useState(false)
  const [editedInvoice, setEditedInvoice] = useState<any>({})

  useEffect(() => {
    fetchInvoiceDetails()
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [invoiceId])

  const fetchInvoiceDetails = async () => {
    try {
      setLoading(true)
      
      // Use backend API instead of client-side Supabase query (avoids RLS issues)
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/invoices/${invoiceId}`)
      
      if (!response.ok) {
        if (response.status === 404) {
          throw new Error('Invoice not found')
        }
        throw new Error(`Failed to fetch invoice: ${response.statusText}`)
      }
      
      const data = await response.json()
      setInvoice(data)
      setEditedInvoice(data)
      
    } catch (error) {
      console.error('Error fetching invoice:', error)
      alert('Failed to load invoice details. Please check the console for details.')
      // Fallback: try to fetch from Supabase in case API is down
      try {
        const { data, error } = await supabase
          .from('invoices')
          .select('*')
          .eq('id', invoiceId)
          .single()

        if (error) throw error
        
        setInvoice(data)
        setEditedInvoice(data)
      } catch (fallbackError) {
        console.error('Fallback Supabase fetch also failed:', fallbackError)
      }
    } finally {
      setLoading(false)
    }
  }

  const handleSave = async () => {
    try {
      setSaving(true)

      const { error } = await supabase
        .from('invoices')
        .update({
          vendor_name: editedInvoice.vendor_name,
          invoice_number: editedInvoice.invoice_number,
          invoice_date: editedInvoice.invoice_date,
          due_date: editedInvoice.due_date,
          subtotal: parseFloat(editedInvoice.subtotal),
          cgst: parseFloat(editedInvoice.cgst),
          sgst: parseFloat(editedInvoice.sgst),
          igst: parseFloat(editedInvoice.igst),
          total_amount: parseFloat(editedInvoice.total_amount),
          payment_status: editedInvoice.payment_status
        })
        .eq('id', invoiceId)

      if (error) throw error

      setInvoice(editedInvoice)
      setEditing(false)
      alert('Invoice updated successfully!')
      
    } catch (error) {
      console.error('Error saving invoice:', error)
      alert('Failed to save changes')
    } finally {
      setSaving(false)
    }
  }

  const handleDelete = async () => {
    if (!confirm('Are you sure you want to delete this invoice?')) return

    try {
      const { error } = await supabase
        .from('invoices')
        .delete()
        .eq('id', invoiceId)

      if (error) throw error

      alert('Invoice deleted successfully')
      router.push('/invoices')
      
    } catch (error) {
      console.error('Error deleting invoice:', error)
      alert('Failed to delete invoice')
    }
  }

  const exportToExcel = () => {
    // ACCOUNTANT-FRIENDLY EXCEL (light styling, formulas, import-ready)
    // For accountants, SMEs, bookkeeping teams
    // Import to Tally/Zoho/QuickBooks
    const link = document.createElement('a')
    link.href = `http://localhost:8000/api/invoices/${invoiceId}/export-excel`
    link.download = `Invoice_${invoice?.invoice_number || invoiceId}.xlsx`
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
  }

  const exportToPDF = () => {
    // STYLIZED PDF (beautiful formatting, colors, branding)
    // For clients, business owners, professional presentation
    // Print-ready, perfect for emailing to customers
    const link = document.createElement('a')
    link.href = `http://localhost:8000/api/invoices/${invoiceId}/export-pdf`
    link.download = `Invoice_${invoice?.invoice_number || invoiceId}.pdf`
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
  }

  const exportToCSV = () => {
    // RAW CSV (plain text, no formatting, machine-readable)
    // For developers, ERP/CRM systems, automation scripts
    // Bulk processing and API integration
    const link = document.createElement('a')
    link.href = `http://localhost:8000/api/invoices/${invoiceId}/export-csv`
    link.download = `Invoice_${invoice?.invoice_number || invoiceId}.csv`
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
  }

  if (loading) {
    return (
      <DashboardLayout>
        <div className="flex items-center justify-center h-64">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
        </div>
      </DashboardLayout>
    )
  }

  if (!invoice) {
    return (
      <DashboardLayout>
        <div className="text-center py-12">
          <h2 className="text-2xl font-bold text-gray-900 mb-4">Invoice Not Found</h2>
          <button
            onClick={() => router.push('/invoices')}
            className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
          >
            Back to Invoices
          </button>
        </div>
      </DashboardLayout>
    )
  }

  return (
    <DashboardLayout>
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="mb-6 flex items-center justify-between">
          <div className="flex items-center gap-4">
            <button
              onClick={() => router.push('/invoices')}
              className="p-2 hover:bg-gray-100 rounded-lg transition-colors"
            >
              <ArrowLeft className="w-5 h-5" />
            </button>
            <div>
              <h1 className="text-2xl font-bold text-gray-900">Invoice Details</h1>
              <p className="text-gray-600 mt-1">View and edit invoice information</p>
            </div>
          </div>

          <div className="flex items-center gap-2">
            {editing ? (
              <>
                <button
                  onClick={() => {
                    setEditing(false)
                    setEditedInvoice(invoice)
                  }}
                  className="px-4 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition-colors flex items-center gap-2"
                >
                  <X className="w-4 h-4" />
                  Cancel
                </button>
                <button
                  onClick={handleSave}
                  disabled={saving}
                  className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors flex items-center gap-2 disabled:opacity-50"
                >
                  <Save className="w-4 h-4" />
                  {saving ? 'Saving...' : 'Save Changes'}
                </button>
              </>
            ) : (
              <>
                {/* PRIMARY BUTTON: Download PDF (for clients, stylized) */}
                <button
                  onClick={exportToPDF}
                  className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors flex items-center gap-2 shadow-sm"
                  title="Stylized PDF - For clients, business owners, professional presentation"
                >
                  <Download className="w-4 h-4" />
                  PDF
                </button>
                
                {/* SECONDARY BUTTON: Export Excel (for accountants, light styling) */}
                <button
                  onClick={exportToExcel}
                  className="px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors flex items-center gap-2 shadow-sm"
                  title="Accountant-friendly Excel - For Tally/Zoho/QuickBooks import, with formulas"
                >
                  <Download className="w-4 h-4" />
                  Excel
                </button>
                
                {/* TERTIARY BUTTON: Export CSV (for developers, raw data) */}
                <button
                  onClick={exportToCSV}
                  className="px-4 py-2 bg-gray-500 text-white rounded-lg hover:bg-gray-600 transition-colors flex items-center gap-2 shadow-sm"
                  title="Raw CSV - For developers, ERP systems, automation scripts"
                >
                  <Download className="w-4 h-4" />
                  CSV
                </button>
                
                <button
                  onClick={() => setEditing(true)}
                  className="px-4 py-2 bg-gray-600 text-white rounded-lg hover:bg-gray-700 transition-colors flex items-center gap-2"
                >
                  <Edit2 className="w-4 h-4" />
                  Edit
                </button>
                <button
                  onClick={handleDelete}
                  className="px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors flex items-center gap-2"
                >
                  <Trash2 className="w-4 h-4" />
                  Delete
                </button>
              </>
            )}
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Left Column - Invoice Details */}
          <div className="space-y-6">
            {/* Basic Info Card */}
            <div className="bg-gray-50 dark:bg-gray-900 rounded-xl border border-gray-200 dark:border-gray-800 p-6">
              <h2 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">Basic Information</h2>
              
              <div className="space-y-4">
                {/* Vendor Name */}
                <div>
                  <label className="flex items-center gap-2 text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                    <Building2 className="w-4 h-4" />
                    Vendor Name
                  </label>
                  {editing ? (
                    <input
                      type="text"
                      value={editedInvoice.vendor_name}
                      onChange={(e) => setEditedInvoice({ ...editedInvoice, vendor_name: e.target.value })}
                      className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    />
                  ) : (
                    <p className="text-gray-900 dark:text-white">{invoice.vendor_name}</p>
                  )}
                </div>

                {/* Invoice Number */}
                <div>
                  <label className="flex items-center gap-2 text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                    <Hash className="w-4 h-4" />
                    Invoice Number
                  </label>
                  {editing ? (
                    <input
                      type="text"
                      value={editedInvoice.invoice_number}
                      onChange={(e) => setEditedInvoice({ ...editedInvoice, invoice_number: e.target.value })}
                      className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    />
                  ) : (
                    <p className="text-gray-900 dark:text-white">{invoice.invoice_number}</p>
                  )}
                </div>

                {/* Dates */}
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="flex items-center gap-2 text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                      <Calendar className="w-4 h-4" />
                      Invoice Date
                    </label>
                    {editing ? (
                      <input
                        type="date"
                        value={editedInvoice.invoice_date}
                        onChange={(e) => setEditedInvoice({ ...editedInvoice, invoice_date: e.target.value })}
                        className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                      />
                    ) : (
                      <p className="text-gray-900 dark:text-white">{invoice.invoice_date}</p>
                    )}
                  </div>

                  <div>
                    <label className="flex items-center gap-2 text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                      <Calendar className="w-4 h-4" />
                      Due Date
                    </label>
                    {editing ? (
                      <input
                        type="date"
                        value={editedInvoice.due_date || ''}
                        onChange={(e) => setEditedInvoice({ ...editedInvoice, due_date: e.target.value })}
                        className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                      />
                    ) : (
                      <p className="text-gray-900 dark:text-white">{invoice.due_date || 'N/A'}</p>
                    )}
                  </div>
                </div>

                {/* Payment Status */}
                <div>
                  <label className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-2 block">
                    Payment Status
                  </label>
                  {editing ? (
                    <select
                      value={editedInvoice.payment_status}
                      onChange={(e) => setEditedInvoice({ ...editedInvoice, payment_status: e.target.value })}
                      className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    >
                      <option value="unpaid">Unpaid</option>
                      <option value="paid">Paid</option>
                      <option value="overdue">Overdue</option>
                    </select>
                  ) : (
                    <span className={`inline-flex items-center px-3 py-1 rounded-full text-sm font-medium ${
                      invoice.payment_status === 'paid' 
                        ? 'bg-green-100 text-green-800'
                        : invoice.payment_status === 'overdue'
                        ? 'bg-red-100 text-red-800'
                        : 'bg-yellow-100 text-yellow-800'
                    }`}>
                      {invoice.payment_status.charAt(0).toUpperCase() + invoice.payment_status.slice(1)}
                    </span>
                  )}
                </div>
              </div>
            </div>

            {/* Amount Details Card */}
            <div className="bg-gray-50 dark:bg-gray-900 rounded-xl border border-gray-200 dark:border-gray-800 p-6">
              <h2 className="text-lg font-semibold text-gray-900 dark:text-white mb-4 flex items-center gap-2">
                <DollarSign className="w-5 h-5" />
                Amount Details
              </h2>
              
              <div className="space-y-3">
                {/* Subtotal */}
                <div className="flex justify-between items-center">
                  <span className="text-gray-600 dark:text-gray-400">Subtotal</span>
                  {editing ? (
                    <input
                      type="number"
                      step="0.01"
                      value={editedInvoice.subtotal}
                      onChange={(e) => setEditedInvoice({ ...editedInvoice, subtotal: e.target.value })}
                      className="w-32 px-3 py-1 border border-gray-300 rounded-lg text-right"
                    />
                  ) : (
                    <span className="font-medium">₹{(invoice.subtotal || 0).toLocaleString()}</span>
                  )}
                </div>

                {/* CGST */}
                <div className="flex justify-between items-center">
                  <span className="text-gray-600 dark:text-gray-400">CGST</span>
                  {editing ? (
                    <input
                      type="number"
                      step="0.01"
                      value={editedInvoice.cgst}
                      onChange={(e) => setEditedInvoice({ ...editedInvoice, cgst: e.target.value })}
                      className="w-32 px-3 py-1 border border-gray-300 rounded-lg text-right"
                    />
                  ) : (
                    <span className="font-medium">₹{(invoice.cgst || 0).toLocaleString()}</span>
                  )}
                </div>

                {/* SGST */}
                <div className="flex justify-between items-center">
                  <span className="text-gray-600 dark:text-gray-400">SGST</span>
                  {editing ? (
                    <input
                      type="number"
                      step="0.01"
                      value={editedInvoice.sgst}
                      onChange={(e) => setEditedInvoice({ ...editedInvoice, sgst: e.target.value })}
                      className="w-32 px-3 py-1 border border-gray-300 rounded-lg text-right"
                    />
                  ) : (
                    <span className="font-medium">₹{(invoice.sgst || 0).toLocaleString()}</span>
                  )}
                </div>

                {/* IGST */}
                <div className="flex justify-between items-center">
                  <span className="text-gray-600 dark:text-gray-400">IGST</span>
                  {editing ? (
                    <input
                      type="number"
                      step="0.01"
                      value={editedInvoice.igst}
                      onChange={(e) => setEditedInvoice({ ...editedInvoice, igst: e.target.value })}
                      className="w-32 px-3 py-1 border border-gray-300 rounded-lg text-right"
                    />
                  ) : (
                    <span className="font-medium">₹{(invoice.igst || 0).toLocaleString()}</span>
                  )}
                </div>

                <div className="border-t border-gray-200 dark:border-gray-800 pt-3 mt-3">
                  <div className="flex justify-between items-center">
                    <span className="text-lg font-semibold text-gray-900 dark:text-white">Total Amount</span>
                    {editing ? (
                      <input
                        type="number"
                        step="0.01"
                        value={editedInvoice.total_amount}
                        onChange={(e) => setEditedInvoice({ ...editedInvoice, total_amount: e.target.value })}
                        className="w-32 px-3 py-1 border border-gray-300 rounded-lg text-right font-bold"
                      />
                    ) : (
                      <span className="text-2xl font-bold text-blue-600">₹{(invoice.total_amount || 0).toLocaleString()}</span>
                    )}
                  </div>
                </div>
              </div>
            </div>

            {/* Metadata Card */}
            <div className="bg-gray-50 dark:bg-gray-900 rounded-xl border border-gray-200 dark:border-gray-800 p-6">
              <h2 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">Metadata</h2>
              
              <div className="space-y-2 text-sm">
                <div className="flex justify-between">
                  <span className="text-gray-600 dark:text-gray-400">Created At</span>
                  <span className="text-gray-900 dark:text-white">{new Date(invoice.created_at).toLocaleString()}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600 dark:text-gray-400">Last Updated</span>
                  <span className="text-gray-900 dark:text-white">{new Date(invoice.updated_at || invoice.created_at).toLocaleString()}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600 dark:text-gray-400">File Name</span>
                  <span className="text-gray-900 dark:text-white">{invoice.documents?.file_name || 'N/A'}</span>
                </div>
              </div>
            </div>
          </div>

          {/* Right Column - PDF Preview */}
          <div className="lg:sticky lg:top-6 h-fit">
            <div className="bg-gray-50 dark:bg-gray-900 rounded-xl border border-gray-200 dark:border-gray-800 p-6">
              <h2 className="text-lg font-semibold text-gray-900 dark:text-white mb-4 flex items-center gap-2">
                <FileText className="w-5 h-5" />
                Document Preview
              </h2>
              
              {invoice.documents?.file_url ? (
                <div className="border border-gray-200 dark:border-gray-800 rounded-lg overflow-hidden">
                  {invoice.documents.file_name.toLowerCase().endsWith('.pdf') ? (
                    <iframe
                      src={invoice.documents.file_url}
                      className="w-full h-[600px]"
                      title="Invoice PDF"
                    />
                  ) : (
                    <div className="relative h-[600px]">
                      <img
                        src={invoice.documents.file_url}
                        alt="Invoice"
                        className="w-full h-full object-contain bg-gray-50"
                      />
                    </div>
                  )}
                </div>
              ) : (
                <div className="border border-gray-200 rounded-lg h-[600px] flex items-center justify-center bg-gray-50">
                  <div className="text-center">
                    <FileText className="w-12 h-12 text-gray-400 mx-auto mb-3" />
                    <p className="text-gray-500">No document available</p>
                  </div>
                </div>
              )}

              {invoice.documents?.file_url && (
                <a
                  href={invoice.documents.file_url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="mt-4 w-full inline-flex items-center justify-center gap-2 px-4 py-2 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 transition-colors"
                >
                  <Download className="w-4 h-4" />
                  Download Original
                </a>
              )}
            </div>
          </div>
        </div>
      </div>
    </DashboardLayout>
  )
}
