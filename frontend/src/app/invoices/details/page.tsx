'use client'

import { useState, useEffect } from 'react'
import { useSearchParams, useRouter } from 'next/navigation'
import DashboardLayout from '@/components/DashboardLayout'
import { ArrowLeft, Calendar, DollarSign, Building2, FileText, Edit2, Save, X } from 'lucide-react'

export default function InvoiceDetailsPage() {
  const searchParams = useSearchParams()
  const router = useRouter()
  const invoiceId = searchParams.get('id')

  const [invoice, setInvoice] = useState<any>(null)
  const [loading, setLoading] = useState(false)
  const [isEditing, setIsEditing] = useState(false)
  const [editedInvoice, setEditedInvoice] = useState<any>(null)
  const [saving, setSaving] = useState(false)

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
      setEditedInvoice({...data}) // Initialize edit form
      
    } catch (error) {
      console.error('❌ Error:', error)
      alert('Could not load invoice details')
    } finally {
      setLoading(false)
    }
  }

  const handleSave = async () => {
    try {
      setSaving(true)
      console.log('💾 Saving invoice changes:', editedInvoice)
      
      const response = await fetch(`https://trulyinvoice-backend.onrender.com/api/invoices/${invoiceId}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(editedInvoice)
      })
      
      if (!response.ok) {
        throw new Error(`Failed to save: ${response.status}`)
      }
      
      const updatedInvoice = await response.json()
      setInvoice(updatedInvoice)
      setEditedInvoice({...updatedInvoice})
      setIsEditing(false)
      
      console.log('✅ Invoice saved successfully')
      alert('Invoice updated successfully!')
      
    } catch (error) {
      console.error('❌ Save error:', error)
      alert('Failed to save invoice changes')
    } finally {
      setSaving(false)
    }
  }

  const handleCancel = () => {
    setEditedInvoice({...invoice}) // Reset to original
    setIsEditing(false)
  }

  const handleFieldChange = (field: string, value: any) => {
    setEditedInvoice((prev: any) => ({
      ...prev,
      [field]: value
    }))
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
        <div className="flex items-center justify-between mb-6">
          <div className="flex items-center gap-4">
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
          
          {/* Edit/Save/Cancel Buttons */}
          <div className="flex items-center gap-2">
            {!isEditing ? (
              <button
                onClick={() => setIsEditing(true)}
                className="flex items-center gap-2 px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-md transition-colors"
              >
                <Edit2 className="w-4 h-4" />
                Edit Invoice
              </button>
            ) : (
              <div className="flex gap-2">
                <button
                  onClick={handleSave}
                  disabled={saving}
                  className="flex items-center gap-2 px-4 py-2 bg-green-600 hover:bg-green-700 text-white rounded-md transition-colors disabled:opacity-50"
                >
                  <Save className="w-4 h-4" />
                  {saving ? 'Saving...' : 'Save'}
                </button>
                <button
                  onClick={handleCancel}
                  disabled={saving}
                  className="flex items-center gap-2 px-4 py-2 bg-gray-600 hover:bg-gray-700 text-white rounded-md transition-colors"
                >
                  <X className="w-4 h-4" />
                  Cancel
                </button>
              </div>
            )}
          </div>
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
                  {isEditing ? (
                    <input
                      type="text"
                      value={editedInvoice?.vendor_name || ''}
                      onChange={(e) => handleFieldChange('vendor_name', e.target.value)}
                      className="w-full px-3 py-2 border border-gray-300 rounded-md dark:border-gray-600 dark:bg-gray-700 dark:text-white"
                    />
                  ) : (
                    <p className="text-gray-900 dark:text-white font-medium">
                      {invoice.vendor_name || 'N/A'}
                    </p>
                  )}
                </div>
                
                <div>
                  <label className="block text-sm font-medium text-gray-500 dark:text-gray-400 mb-1">
                    Invoice Number
                  </label>
                  {isEditing ? (
                    <input
                      type="text"
                      value={editedInvoice?.invoice_number || ''}
                      onChange={(e) => handleFieldChange('invoice_number', e.target.value)}
                      className="w-full px-3 py-2 border border-gray-300 rounded-md dark:border-gray-600 dark:bg-gray-700 dark:text-white"
                    />
                  ) : (
                    <p className="text-gray-900 dark:text-white">
                      {invoice.invoice_number || 'N/A'}
                    </p>
                  )}
                </div>
                
                <div>
                  <label className="block text-sm font-medium text-gray-500 dark:text-gray-400 mb-1">
                    Invoice Date
                  </label>
                  {isEditing ? (
                    <input
                      type="date"
                      value={editedInvoice?.invoice_date || ''}
                      onChange={(e) => handleFieldChange('invoice_date', e.target.value)}
                      className="w-full px-3 py-2 border border-gray-300 rounded-md dark:border-gray-600 dark:bg-gray-700 dark:text-white"
                    />
                  ) : (
                    <p className="text-gray-900 dark:text-white flex items-center gap-2">
                      <Calendar className="w-4 h-4 text-gray-400" />
                      {invoice.invoice_date || 'N/A'}
                    </p>
                  )}
                </div>
                
                <div>
                  <label className="block text-sm font-medium text-gray-500 dark:text-gray-400 mb-1">
                    Total Amount
                  </label>
                  {isEditing ? (
                    <input
                      type="number"
                      value={editedInvoice?.total_amount || ''}
                      onChange={(e) => handleFieldChange('total_amount', parseFloat(e.target.value) || 0)}
                      className="w-full px-3 py-2 border border-gray-300 rounded-md dark:border-gray-600 dark:bg-gray-700 dark:text-white"
                    />
                  ) : (
                    <p className="text-gray-900 dark:text-white font-bold text-lg flex items-center gap-2">
                      <DollarSign className="w-4 h-4 text-green-600" />
                      ₹{invoice.total_amount?.toLocaleString() || '0'}
                    </p>
                  )}
                </div>
                
                <div>
                  <label className="block text-sm font-medium text-gray-500 dark:text-gray-400 mb-1">
                    Payment Status
                  </label>
                  {isEditing ? (
                    <select
                      value={editedInvoice?.payment_status || 'pending'}
                      onChange={(e) => handleFieldChange('payment_status', e.target.value)}
                      className="w-full px-3 py-2 border border-gray-300 rounded-md dark:border-gray-600 dark:bg-gray-700 dark:text-white"
                    >
                      <option value="pending">Pending</option>
                      <option value="paid">Paid</option>
                      <option value="overdue">Overdue</option>
                      <option value="cancelled">Cancelled</option>
                    </select>
                  ) : (
                    <span className={`inline-flex px-2 py-1 text-xs rounded-full ${
                      invoice.payment_status === 'paid' 
                        ? 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200'
                        : invoice.payment_status === 'overdue'
                        ? 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200'
                        : 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-200'
                    }`}>
                      {(invoice.payment_status || 'pending').charAt(0).toUpperCase() + 
                       (invoice.payment_status || 'pending').slice(1)}
                    </span>
                  )}
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
                <div className="flex justify-between items-center">
                  <span className="text-gray-600 dark:text-gray-400">Subtotal:</span>
                  {isEditing ? (
                    <input
                      type="number"
                      value={editedInvoice?.subtotal || ''}
                      onChange={(e) => handleFieldChange('subtotal', parseFloat(e.target.value) || 0)}
                      className="w-32 px-2 py-1 border border-gray-300 rounded-md dark:border-gray-600 dark:bg-gray-700 dark:text-white text-right"
                    />
                  ) : (
                    <span className="text-gray-900 dark:text-white">₹{invoice.subtotal?.toLocaleString() || '0'}</span>
                  )}
                </div>
                
                <div className="flex justify-between items-center">
                  <span className="text-gray-600 dark:text-gray-400">CGST:</span>
                  {isEditing ? (
                    <input
                      type="number"
                      value={editedInvoice?.cgst || ''}
                      onChange={(e) => handleFieldChange('cgst', parseFloat(e.target.value) || 0)}
                      className="w-32 px-2 py-1 border border-gray-300 rounded-md dark:border-gray-600 dark:bg-gray-700 dark:text-white text-right"
                    />
                  ) : (
                    <span className="text-gray-900 dark:text-white">₹{invoice.cgst?.toLocaleString() || '0'}</span>
                  )}
                </div>
                
                <div className="flex justify-between items-center">
                  <span className="text-gray-600 dark:text-gray-400">SGST:</span>
                  {isEditing ? (
                    <input
                      type="number"
                      value={editedInvoice?.sgst || ''}
                      onChange={(e) => handleFieldChange('sgst', parseFloat(e.target.value) || 0)}
                      className="w-32 px-2 py-1 border border-gray-300 rounded-md dark:border-gray-600 dark:bg-gray-700 dark:text-white text-right"
                    />
                  ) : (
                    <span className="text-gray-900 dark:text-white">₹{invoice.sgst?.toLocaleString() || '0'}</span>
                  )}
                </div>
                
                <div className="flex justify-between items-center">
                  <span className="text-gray-600 dark:text-gray-400">IGST:</span>
                  {isEditing ? (
                    <input
                      type="number"
                      value={editedInvoice?.igst || ''}
                      onChange={(e) => handleFieldChange('igst', parseFloat(e.target.value) || 0)}
                      className="w-32 px-2 py-1 border border-gray-300 rounded-md dark:border-gray-600 dark:bg-gray-700 dark:text-white text-right"
                    />
                  ) : (
                    <span className="text-gray-900 dark:text-white">₹{invoice.igst?.toLocaleString() || '0'}</span>
                  )}
                </div>
                
                <div className="border-t border-gray-200 dark:border-gray-700 pt-3">
                  <div className="flex justify-between text-lg font-semibold">
                    <span className="text-gray-900 dark:text-white">Total Amount:</span>
                    <span className="text-gray-900 dark:text-white">₹{(isEditing ? editedInvoice?.total_amount : invoice.total_amount)?.toLocaleString() || '0'}</span>
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