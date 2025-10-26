// =====================================================
// 📱 MOBILE-RESPONSIVE INVOICE CARD COMPONENT
// =====================================================
// Add to: frontend/src/components/InvoiceCard.tsx

import Link from 'next/link'
import { Eye, Download, Trash2, MoreVertical } from 'lucide-react'
import { useState } from 'react'

interface Invoice {
  id: string
  invoice_number: string
  vendor_name: string
  total_amount: number
  invoice_date: string
  payment_status: 'paid' | 'unpaid' | 'pending' | 'overdue'
  currency: string
}

interface InvoiceCardProps {
  invoice: Invoice
  onExport?: (invoice: Invoice) => void
  onDelete?: (invoiceId: string) => void
}

export default function InvoiceCard({ invoice, onExport, onDelete }: InvoiceCardProps) {
  const [showActions, setShowActions] = useState(false)

  const statusConfig = {
    paid: {
      bg: 'bg-green-100 dark:bg-green-900/30',
      text: 'text-green-800 dark:text-green-300',
      label: 'Paid'
    },
    unpaid: {
      bg: 'bg-red-100 dark:bg-red-900/30',
      text: 'text-red-800 dark:text-red-300',
      label: 'Unpaid'
    },
    pending: {
      bg: 'bg-yellow-100 dark:bg-yellow-900/30',
      text: 'text-yellow-800 dark:text-yellow-300',
      label: 'Pending'
    },
    overdue: {
      bg: 'bg-orange-100 dark:bg-orange-900/30',
      text: 'text-orange-800 dark:text-orange-300',
      label: 'Overdue'
    }
  }

  const status = statusConfig[invoice.payment_status] || statusConfig.pending

  return (
    <div 
      className="bg-white dark:bg-gray-800 rounded-lg shadow-sm hover:shadow-md transition-all border border-gray-200 dark:border-gray-700 p-4"
      role="article"
      aria-label={`Invoice ${invoice.invoice_number}`}
    >
      {/* Header Row */}
      <div className="flex justify-between items-start mb-3">
        <div className="flex-1 min-w-0">
          {/* Invoice Number */}
          <h3 className="font-semibold text-lg text-gray-900 dark:text-white truncate">
            {invoice.invoice_number || 'No Number'}
          </h3>
          
          {/* Vendor Name */}
          <p className="text-sm text-gray-600 dark:text-gray-400 truncate mt-1">
            {invoice.vendor_name || 'Unknown Vendor'}
          </p>
        </div>

        {/* Status Badge */}
        <span 
          className={`px-3 py-1 rounded-full text-xs font-medium whitespace-nowrap ml-2 ${status.bg} ${status.text}`}
          role="status"
          aria-label={`Payment status: ${status.label}`}
        >
          {status.label}
        </span>
      </div>

      {/* Amount Row */}
      <div className="mb-4">
        <div className="flex items-baseline gap-2">
          <span className="text-3xl font-bold text-gray-900 dark:text-white">
            {invoice.currency === 'INR' ? '₹' : invoice.currency}
            {invoice.total_amount?.toLocaleString('en-IN') || '0.00'}
          </span>
        </div>
        
        {/* Date */}
        <p className="text-sm text-gray-500 dark:text-gray-400 mt-1">
          {invoice.invoice_date ? new Date(invoice.invoice_date).toLocaleDateString('en-IN', {
            day: 'numeric',
            month: 'short',
            year: 'numeric'
          }) : 'No date'}
        </p>
      </div>

      {/* Action Buttons */}
      <div className="flex gap-2">
        {/* View Details Button */}
        <Link
          href={`/invoices/details?id=${invoice.id}`}
          className="flex-1 flex items-center justify-center gap-2 py-2.5 px-4 bg-blue-600 hover:bg-blue-700 active:bg-blue-800 text-white text-sm font-medium rounded-md transition-colors touch-manipulation"
          aria-label={`View details for invoice ${invoice.invoice_number}`}
        >
          <Eye className="w-4 h-4" aria-hidden="true" />
          <span>View</span>
        </Link>

        {/* Export Button */}
        {onExport && (
          <button
            onClick={() => onExport(invoice)}
            className="flex items-center justify-center gap-2 py-2.5 px-4 bg-gray-600 hover:bg-gray-700 active:bg-gray-800 text-white text-sm font-medium rounded-md transition-colors touch-manipulation"
            aria-label={`Export invoice ${invoice.invoice_number}`}
          >
            <Download className="w-4 h-4" aria-hidden="true" />
            <span className="hidden sm:inline">Export</span>
          </button>
        )}

        {/* More Actions Button */}
        <div className="relative">
          <button
            onClick={() => setShowActions(!showActions)}
            className="flex items-center justify-center w-10 h-10 bg-gray-100 hover:bg-gray-200 dark:bg-gray-700 dark:hover:bg-gray-600 text-gray-700 dark:text-gray-300 rounded-md transition-colors touch-manipulation"
            aria-label="More actions"
            aria-expanded={showActions}
            aria-haspopup="true"
          >
            <MoreVertical className="w-4 h-4" aria-hidden="true" />
          </button>

          {/* Dropdown Menu */}
          {showActions && (
            <div 
              className="absolute right-0 mt-2 w-48 bg-white dark:bg-gray-800 rounded-lg shadow-lg border border-gray-200 dark:border-gray-700 z-10"
              role="menu"
              aria-orientation="vertical"
            >
              <button
                onClick={() => {
                  if (onDelete) onDelete(invoice.id)
                  setShowActions(false)
                }}
                className="w-full flex items-center gap-2 px-4 py-2.5 text-left text-sm text-red-600 dark:text-red-400 hover:bg-red-50 dark:hover:bg-red-900/20 rounded-lg transition-colors"
                role="menuitem"
              >
                <Trash2 className="w-4 h-4" aria-hidden="true" />
                Delete
              </button>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
