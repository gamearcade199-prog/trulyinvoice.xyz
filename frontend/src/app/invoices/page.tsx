'use client'

export const dynamic = 'force-dynamic'

import { useState, useEffect } from 'react'
import DashboardLayout from '@/components/DashboardLayout'
import Link from 'next/link'
import { 
  Search, 
  Filter, 
  Trash2,
  Plus,
  ChevronDown
} from 'lucide-react'
import { createClient } from '@supabase/supabase-js'
import { exportInvoicesToCSV, exportInvoicesToTallyXML, exportInvoicesToQuickBooksCSV, exportInvoicesToZohoBooksCSV } from '@/lib/invoiceUtils'
import { formatCurrency } from '@/lib/currency'
import ConfidenceIndicator from '@/components/ConfidenceIndicator'
import ExportWarningModal from '@/components/ExportWarningModal'
import ExportSuccessModal from '@/components/ExportSuccessModal'
import ExportErrorModal from '@/components/ExportErrorModal'
import QuickBooksFormatModal from '@/components/QuickBooksFormatModal'
import toast from 'react-hot-toast'

const supabase = createClient(
  process.env.NEXT_PUBLIC_SUPABASE_URL || 'https://placeholder.supabase.co',
  process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY || 'placeholder-anon-key'
)

export default function InvoicesPageClean() {
  const [searchQuery, setSearchQuery] = useState('')
  const [filterStatus, setFilterStatus] = useState('all')
  const [invoices, setInvoices] = useState<any[]>([])
  const [loading, setLoading] = useState(true)
  const [selectedInvoices, setSelectedInvoices] = useState<Set<number>>(new Set())
  const [showMainExportDropdown, setShowMainExportDropdown] = useState(false)
  const [showBulkExportDropdown, setShowBulkExportDropdown] = useState(false)
  const [showRowExportDropdown, setShowRowExportDropdown] = useState<{[key: string]: boolean}>({})
  const [showMobileExportDropdown, setShowMobileExportDropdown] = useState<{[key: string]: boolean}>({})
  const [userExportTemplate, setUserExportTemplate] = useState('simple')
  const [currentPage, setCurrentPage] = useState(0)
  const [hasMore, setHasMore] = useState(true)
  const INVOICES_PER_PAGE = 20
  
  // Export warning modal state
  const [showWarningModal, setShowWarningModal] = useState(false)
  const [exportWarnings, setExportWarnings] = useState<string[]>([])
  const [warningCallbacks, setWarningCallbacks] = useState<{ onConfirm: () => void, onCancel: () => void } | null>(null)
  
  // Export success modal state
  const [showSuccessModal, setShowSuccessModal] = useState(false)
  const [successData, setSuccessData] = useState<any>(null)
  
  // Export error modal state
  const [showErrorModal, setShowErrorModal] = useState(false)
  const [errorData, setErrorData] = useState<any>(null)
  
  // QuickBooks format selection modal state
  const [showQuickBooksFormatModal, setShowQuickBooksFormatModal] = useState(false)
  const [quickBooksCallbacks, setQuickBooksCallbacks] = useState<{ onSelectFormat: (format: 'iif' | 'csv') => void, onCancel: () => void } | null>(null)

  useEffect(() => {
    fetchInvoices()
    // Auto-refresh removed - was annoying. User can manually refresh if needed.
    
    // Load user's preferred export template
    const loadUserTemplate = async () => {
      try {
        const { data: { user } } = await supabase.auth.getUser()
        if (user) {
          try {
            const savedTemplate = localStorage.getItem(`export_template_${user.id}`)
            if (savedTemplate && ['simple', 'accountant', 'analyst', 'compliance'].includes(savedTemplate)) {
              setUserExportTemplate(savedTemplate)
            }
          } catch (storageError) {
            // localStorage not available (Safari private mode, quota exceeded, etc.)
            // Use default template
          }
        }
      } catch (error) {
        console.error('Error loading template preference:', error)
      }
    }
    loadUserTemplate()
  }, [])

  // Listen for export warning events
  useEffect(() => {
    const handleWarnings = (e: any) => {
      setExportWarnings(e.detail.warnings)
      setWarningCallbacks({
        onConfirm: e.detail.onConfirm,
        onCancel: e.detail.onCancel
      })
      setShowWarningModal(true)
    }
    
    const handleSuccess = (e: any) => {
      setSuccessData(e.detail)
      setShowSuccessModal(true)
    }
    
    const handleError = (e: any) => {
      setErrorData(e.detail)
      setShowErrorModal(true)
    }
    
    const handleQuickBooksFormat = (e: any) => {
      setQuickBooksCallbacks({
        onSelectFormat: e.detail.onSelectFormat,
        onCancel: e.detail.onCancel
      })
      setShowQuickBooksFormatModal(true)
    }
    
    window.addEventListener('showExportWarnings', handleWarnings)
    window.addEventListener('showExportSuccess', handleSuccess)
    window.addEventListener('showExportError', handleError)
    window.addEventListener('showQuickBooksFormatModal', handleQuickBooksFormat)
    
    return () => {
      window.removeEventListener('showExportWarnings', handleWarnings)
      window.removeEventListener('showExportSuccess', handleSuccess)
      window.removeEventListener('showExportError', handleError)
      window.removeEventListener('showQuickBooksFormatModal', handleQuickBooksFormat)
    }
  }, [])


  // Close dropdowns when clicking outside
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      const target = event.target as HTMLElement
      
      // Check if click is inside any dropdown or dropdown button
      const isInsideDropdown = target.closest('.export-dropdown') || 
                              target.closest('[data-dropdown-button]')
      
      if (!isInsideDropdown) {
        setShowMainExportDropdown(false)
        setShowBulkExportDropdown(false)
        setShowRowExportDropdown({})
        setShowMobileExportDropdown({})
      }
    }

    document.addEventListener('click', handleClickOutside)
    return () => document.removeEventListener('click', handleClickOutside)
  }, [])

  const fetchInvoices = async (page: number = 0) => {
    try {
      setLoading(true)
      
      const { data: { user } } = await supabase.auth.getUser()
      if (!user) {
        setLoading(false)
        return
      }

      const from = page * INVOICES_PER_PAGE
      const to = from + INVOICES_PER_PAGE - 1

      // Fetch paginated user invoices
      const { data: invoicesData, error: invoicesError, count } = await supabase
        .from('invoices')
        .select(`
          *,
          documents:document_id (
            storage_path,
            file_url,
            file_name
          )
        `, { count: 'exact' })
        .eq('user_id', user.id)
        .order('created_at', { ascending: false })
        .range(from, to)

      if (invoicesError) {
        setInvoices([])
        return
      }

      // Append to existing invoices if loading more pages
      if (page === 0) {
        setInvoices(invoicesData || [])
      } else {
        setInvoices(prev => [...prev, ...(invoicesData || [])])
      }
      
      // Check if there are more invoices to load
      const totalFetched = (page + 1) * INVOICES_PER_PAGE
      setHasMore((count || 0) > totalFetched)
      
    } catch (error) {
      setInvoices([])
    } finally {
      setLoading(false)
    }
  }

  const handleExport = () => {
    try {
      exportInvoicesToCSV(invoices)
    } catch (error) {
      window.dispatchEvent(new CustomEvent('show-export-error', { 
        detail: { 
          title: 'Export Failed',
          message: 'Failed to export invoices. Please try again.'
        } 
      }))
    }
  }

  const exportSingleInvoice = (invoice: any) => {
    try {
      exportInvoicesToCSV([invoice])
    } catch (error) {
      window.dispatchEvent(new CustomEvent('show-export-error', { 
        detail: { 
          title: 'Export Failed',
          message: 'Failed to export invoice. Please try again.'
        } 
      }))
    }
  }

  const loadMoreInvoices = () => {
    const nextPage = currentPage + 1
    setCurrentPage(nextPage)
    fetchInvoices(nextPage)
  }

  const handleExcelExport = async () => {
    try {
      const { data: { session } } = await supabase.auth.getSession()
      if (!session?.access_token) {
        window.dispatchEvent(new CustomEvent('show-export-error', { 
          detail: { 
            title: 'Authentication Required',
            message: 'Please log in to export Excel files.'
          } 
        }))
        return
      }

      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/bulk/export-excel`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${session.access_token}`
        },
        body: JSON.stringify({
          invoice_ids: invoices.map(inv => inv.id),
          template: userExportTemplate
        })
      })

      if (!response.ok) {
        throw new Error(`Export failed: ${response.statusText}`)
      }

      const blob = await response.blob()
      const url = window.URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.style.display = 'none'
      a.href = url
      a.download = `all_invoices_${new Date().toISOString().split('T')[0]}.xlsx`
      document.body.appendChild(a)
      a.click()
      window.URL.revokeObjectURL(url)
      document.body.removeChild(a)
    } catch (error) {
      console.error('Excel Export error:', error)
      window.dispatchEvent(new CustomEvent('show-export-error', { 
        detail: { 
          title: 'Export Failed',
          message: 'Failed to export Excel. Please try again.'
        } 
      }))
    }
  }

  const exportSingleInvoiceToExcel = async (invoice: any) => {
    try {
      const { data: { session } } = await supabase.auth.getSession()
      if (!session?.access_token) {
        window.dispatchEvent(new CustomEvent('show-export-error', { 
          detail: { 
            title: 'Authentication Required',
            message: 'Please log in to export Excel files.'
          } 
        }))
        return
      }

      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/bulk/export-excel`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${session.access_token}`
        },
        body: JSON.stringify({
          invoice_ids: [invoice.id],
          template: userExportTemplate
        })
      })

      if (!response.ok) {
        throw new Error(`Export failed: ${response.statusText}`)
      }

      const blob = await response.blob()
      const url = window.URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.style.display = 'none'
      a.href = url
      a.download = `invoice_${invoice.invoice_number || invoice.id}.xlsx`
      document.body.appendChild(a)
      a.click()
      window.URL.revokeObjectURL(url)
      document.body.removeChild(a)
    } catch (error) {
      console.error('Excel Export error:', error)
      window.dispatchEvent(new CustomEvent('show-export-error', { 
        detail: { 
          title: 'Export Failed',
          message: 'Failed to export Excel. Please try again.'
        } 
      }))
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
      window.dispatchEvent(new CustomEvent('show-export-error', { 
        detail: { 
          title: 'No Selection',
          message: 'Please select at least one invoice to export.'
        } 
      }))
      return
    }
    try {
      exportInvoicesToCSV(selected)
    } catch (error) {
      console.error('Export error:', error)
      window.dispatchEvent(new CustomEvent('show-export-error', { 
        detail: { 
          title: 'Export Failed',
          message: 'Failed to export selected invoices. Please try again.'
        } 
      }))
    }
  }

  const exportSelectedInvoicesExcel = async () => {
    const selected = invoices.filter(inv => selectedInvoices.has(inv.id))
    if (selected.length === 0) {
      window.dispatchEvent(new CustomEvent('show-export-error', { 
        detail: { 
          title: 'No Selection',
          message: 'Please select at least one invoice to export.'
        } 
      }))
      return
    }
    
    try {
      const { data: { session } } = await supabase.auth.getSession()
      if (!session?.access_token) {
        window.dispatchEvent(new CustomEvent('show-export-error', { 
          detail: { 
            title: 'Authentication Required',
            message: 'Please log in to export Excel files.'
          } 
        }))
        return
      }

      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/bulk/export-excel`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${session.access_token}`
        },
        body: JSON.stringify({
          invoice_ids: selected.map(inv => inv.id),
          template: userExportTemplate
        })
      })

      if (!response.ok) {
        throw new Error(`Export failed: ${response.statusText}`)
      }

      const blob = await response.blob()
      const url = window.URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.style.display = 'none'
      a.href = url
      a.download = `selected_invoices_${new Date().toISOString().split('T')[0]}.xlsx`
      document.body.appendChild(a)
      a.click()
      window.URL.revokeObjectURL(url)
      document.body.removeChild(a)
    } catch (error) {
      console.error('Excel Export error:', error)
      window.dispatchEvent(new CustomEvent('show-export-error', { 
        detail: { 
          title: 'Export Failed',
          message: 'Failed to export Excel. Please try again.'
        } 
      }))
    }
  }

  // Dropdown helper functions
  const toggleRowExportDropdown = (invoiceId: string) => {
    setShowRowExportDropdown(prev => ({
      ...prev,
      [invoiceId]: !prev[invoiceId]
    }))
  }

  const toggleMobileExportDropdown = (invoiceId: string) => {
    setShowMobileExportDropdown(prev => ({
      ...prev,
      [invoiceId]: !prev[invoiceId]
    }))
  }

  const handleMainExport = (format: 'excel' | 'csv' | 'tally' | 'quickbooks' | 'zoho') => {
    console.log('Export format selected:', format)
    setShowMainExportDropdown(false)
    switch(format) {
      case 'excel':
        handleExcelExport()
        break
      case 'csv':
        handleExport()
        break
      case 'tally':
        exportInvoicesToTallyXML(invoices)
        break
      case 'quickbooks':
        exportInvoicesToQuickBooksCSV(invoices)
        break
      case 'zoho':
        exportInvoicesToZohoBooksCSV(invoices)
        break
    }
  }

  const handleBulkExport = (format: 'excel' | 'csv' | 'tally' | 'quickbooks' | 'zoho') => {
    setShowBulkExportDropdown(false)
    switch(format) {
      case 'excel':
        exportSelectedInvoicesExcel()
        break
      case 'csv':
        exportSelectedInvoices()
        break
      case 'tally':
        const selectedForTally = invoices.filter(inv => selectedInvoices.has(inv.id))
        exportInvoicesToTallyXML(selectedForTally)
        break
      case 'quickbooks':
        const selectedForQuickBooks = invoices.filter(inv => selectedInvoices.has(inv.id))
        exportInvoicesToQuickBooksCSV(selectedForQuickBooks)
        break
      case 'zoho':
        const selectedForZoho = invoices.filter(inv => selectedInvoices.has(inv.id))
        exportInvoicesToZohoBooksCSV(selectedForZoho)
        break
    }
  }

  const handleRowExport = (invoice: any, format: 'excel' | 'csv' | 'tally' | 'quickbooks' | 'zoho') => {
    setShowRowExportDropdown({})
    switch(format) {
      case 'excel':
        exportSingleInvoiceToExcel(invoice)
        break
      case 'csv':
        exportSingleInvoice(invoice)
        break
      case 'tally':
        exportInvoicesToTallyXML([invoice])
        break
      case 'quickbooks':
        exportInvoicesToQuickBooksCSV([invoice])
        break
      case 'zoho':
        exportInvoicesToZohoBooksCSV([invoice])
        break
    }
  }

  const handleMobileExport = (invoice: any, format: 'excel' | 'csv' | 'tally' | 'quickbooks' | 'zoho') => {
    setShowMobileExportDropdown({})
    switch(format) {
      case 'excel':
        exportSingleInvoiceToExcel(invoice)
        break
      case 'csv':
        exportSingleInvoice(invoice)
        break
      case 'tally':
        exportInvoicesToTallyXML([invoice])
        break
      case 'quickbooks':
        exportInvoicesToQuickBooksCSV([invoice])
        break
      case 'zoho':
        exportInvoicesToZohoBooksCSV([invoice])
        break
    }
  }

  const deleteSelectedInvoices = async () => {
    if (selectedInvoices.size === 0) {
      window.dispatchEvent(new CustomEvent('show-export-error', { 
        detail: { 
          title: 'No Selection',
          message: 'Please select at least one invoice to delete.'
        } 
      }))
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
      
      window.dispatchEvent(new CustomEvent('show-export-success', { 
        detail: { 
          title: 'Deleted Successfully',
          message: `Successfully deleted ${selectedInvoices.size} invoice(s).`,
          stats: [
            { label: 'Deleted', value: selectedInvoices.size.toString() }
          ]
        } 
      }))
    } catch (error) {
      console.error('Delete error:', error)
      window.dispatchEvent(new CustomEvent('show-export-error', { 
        detail: { 
          title: 'Delete Failed',
          message: 'Failed to delete selected invoices. Please try again.'
        } 
      }))
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
          window.dispatchEvent(new CustomEvent('show-export-error', { 
            detail: { 
              title: 'View Failed',
              message: 'Unable to generate view URL for this document.'
            } 
          }))
        }
      } else {
        window.dispatchEvent(new CustomEvent('show-export-error', { 
          detail: { 
            title: 'No Document',
            message: 'No document file available for this invoice.'
          } 
        }))
      }
    } catch (error) {
      console.error('View error:', error)
      window.dispatchEvent(new CustomEvent('show-export-error', { 
        detail: { 
          title: 'View Failed',
          message: 'Failed to open document. Please try again.'
        } 
      }))
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
      toast.error('Failed to delete invoice')
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
      <div className="max-w-full mx-auto p-6">
        {/* Header */}
        <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 mb-8">
          <div>
            <h1 className="text-3xl font-bold text-gray-900 dark:text-white">Invoices</h1>
            <p className="text-gray-600 dark:text-gray-400 mt-1">Manage and track all your invoices in one place</p>
          </div>
          <div className="flex items-center gap-3">
            {/* Template Selector */}
            <div className="flex items-center gap-2">
              <label htmlFor="excel-template" className="text-sm font-medium text-gray-700 dark:text-gray-300 whitespace-nowrap">
                Excel Template:
              </label>
              <select
                id="excel-template"
                value={userExportTemplate}
                onChange={async (e) => {
                  const newTemplate = e.target.value
                  setUserExportTemplate(newTemplate)
                  try {
                    const { data: { user } } = await supabase.auth.getUser()
                    if (user) {
                      try {
                        localStorage.setItem(`export_template_${user.id}`, newTemplate)
                      } catch (storageError) {
                        // localStorage not available - silent fail
                      }
                    }
                  } catch (error) {
                    // Silent fail - preference not critical
                  }
                }}
                className="px-3 py-2 text-sm border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-white rounded-lg focus:ring-2 focus:ring-blue-500 dark:focus:ring-blue-400 focus:border-transparent"
                title="Excel export template - controls structure of Excel file (only applies to Excel exports, not CSV/Tally/QuickBooks)"
              >
                <option value="simple">Simple (3 sheets)</option>
                <option value="accountant">Accountant (6 sheets)</option>
              </select>
            </div>
            
            <Link
              href="/upload"
              className="inline-flex items-center gap-2 px-4 py-2 bg-blue-600 dark:bg-blue-500 text-white rounded-lg hover:bg-blue-700 dark:hover:bg-blue-600 transition-colors font-semibold"
            >
              <Plus className="w-4 h-4" />
              Upload Invoice
            </Link>
          </div>
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
            
            {/* Export Dropdown */}
            {invoices.length > 0 && (
              <div className="relative export-dropdown">
                <button
                  data-dropdown-button
                  onClick={(e) => {
                    e.stopPropagation()
                    console.log('Main export dropdown clicked, current state:', showMainExportDropdown)
                    setShowMainExportDropdown(!showMainExportDropdown)
                  }}
                  className="px-4 py-2 bg-blue-600 dark:bg-blue-500 text-white rounded-lg hover:bg-blue-700 dark:hover:bg-blue-600 transition-colors flex items-center gap-2 font-semibold"
                >
                  Export
                  <ChevronDown className="w-4 h-4" />
                </button>
                {showMainExportDropdown && (
                  <div className="absolute right-0 mt-2 w-40 bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg shadow-lg z-50">
                    <button
                      onClick={() => handleMainExport('excel')}
                      className="w-full text-left px-4 py-2 text-blue-600 dark:text-blue-400 hover:bg-blue-50 dark:hover:bg-blue-900/30 rounded-t-lg font-semibold"
                    >
                      Excel
                    </button>
                    <button
                      onClick={() => handleMainExport('csv')}
                      className="w-full text-left px-4 py-2 text-green-600 dark:text-green-400 hover:bg-green-50 dark:hover:bg-green-900/30 font-semibold"
                    >
                      CSV
                    </button>
                    <button
                      onClick={() => handleMainExport('tally')}
                      className="w-full text-left px-4 py-2 text-purple-600 dark:text-purple-400 hover:bg-purple-50 dark:hover:bg-purple-900/30 font-semibold"
                    >
                      Tally XML
                    </button>
                    <button
                      onClick={() => handleMainExport('quickbooks')}
                      className="w-full text-left px-4 py-2 text-orange-600 dark:text-orange-400 hover:bg-orange-50 dark:hover:bg-orange-900/30 font-semibold"
                    >
                      QuickBooks CSV
                    </button>
                    <button
                      onClick={() => handleMainExport('zoho')}
                      className="w-full text-left px-4 py-2 text-indigo-600 dark:text-indigo-400 hover:bg-indigo-50 dark:hover:bg-indigo-900/30 rounded-b-lg font-semibold"
                    >
                      Zoho Books CSV
                    </button>
                  </div>
                )}
              </div>
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
              <div className="relative export-dropdown">
                <button
                  data-dropdown-button
                  onClick={(e) => {
                    e.stopPropagation()
                    setShowBulkExportDropdown(!showBulkExportDropdown)
                  }}
                  className="px-4 py-2 bg-blue-600 dark:bg-blue-500 text-white rounded-lg hover:bg-blue-700 dark:hover:bg-blue-600 transition-colors flex items-center gap-2 text-sm font-semibold"
                >
                  Export
                  <ChevronDown className="w-4 h-4" />
                </button>
                {showBulkExportDropdown && (
                  <div className="absolute left-0 mt-2 w-40 bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg shadow-lg z-50">
                    <button
                      onClick={() => handleBulkExport('excel')}
                      className="w-full text-left px-4 py-2 text-blue-600 dark:text-blue-400 hover:bg-blue-50 dark:hover:bg-blue-900/30 rounded-t-lg font-semibold"
                    >
                      Excel
                    </button>
                    <button
                      onClick={() => handleBulkExport('csv')}
                      className="w-full text-left px-4 py-2 text-green-600 dark:text-green-400 hover:bg-green-50 dark:hover:bg-green-900/30 font-semibold"
                    >
                      CSV
                    </button>
                    <button
                      onClick={() => handleBulkExport('tally')}
                      className="w-full text-left px-4 py-2 text-purple-600 dark:text-purple-400 hover:bg-purple-50 dark:hover:bg-purple-900/30 font-semibold"
                    >
                      Tally XML
                    </button>
                    <button
                      onClick={() => handleBulkExport('quickbooks')}
                      className="w-full text-left px-4 py-2 text-orange-600 dark:text-orange-400 hover:bg-orange-50 dark:hover:bg-orange-900/30 font-semibold"
                    >
                      QuickBooks CSV
                    </button>
                    <button
                      onClick={() => handleBulkExport('zoho')}
                      className="w-full text-left px-4 py-2 text-indigo-600 dark:text-indigo-400 hover:bg-indigo-50 dark:hover:bg-indigo-900/30 rounded-b-lg font-semibold"
                    >
                      Zoho Books CSV
                    </button>
                  </div>
                )}
              </div>
              <button
                onClick={deleteSelectedInvoices}
                className="px-4 py-2 bg-gray-600 dark:bg-gray-500 text-white rounded-lg hover:bg-gray-700 dark:hover:bg-gray-600 transition-colors flex items-center gap-2 text-sm font-semibold"
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
            <div className="hidden sm:block bg-gray-50 dark:bg-gray-900 rounded-xl border border-gray-200 dark:border-gray-800 overflow-x-auto">
              <div className="min-w-[1200px]">
                <table className="w-full table-auto">
                <thead className="bg-gray-100 dark:bg-gray-950">
                  <tr>
                    <th className="px-4 py-4 w-12">
                      <input
                        type="checkbox"
                        checked={selectedInvoices.size === filteredInvoices.length && filteredInvoices.length > 0}
                        onChange={toggleSelectAll}
                        className="w-4 h-4 text-blue-600 border-gray-300 dark:border-gray-600 rounded focus:ring-blue-500 cursor-pointer"
                      />
                    </th>
                    <th className="text-left px-4 py-4 font-semibold text-gray-900 dark:text-gray-300">VENDOR</th>
                    <th className="text-left px-4 py-4 font-semibold text-gray-900 dark:text-gray-300 w-32">INVOICE #</th>
                    <th className="text-left px-4 py-4 font-semibold text-gray-900 dark:text-gray-300 w-32">DATE</th>
                    <th className="text-left px-4 py-4 font-semibold text-gray-900 dark:text-gray-300 w-32 hidden lg:table-cell">DUE DATE</th>
                    <th className="text-left px-4 py-4 font-semibold text-gray-900 dark:text-gray-300 w-40">AMOUNT</th>
                    <th className="text-left px-4 py-4 font-semibold text-gray-900 dark:text-gray-300 w-32 hidden xl:table-cell">GST</th>
                    <th className="text-left px-4 py-4 font-semibold text-gray-900 dark:text-gray-300 w-32">STATUS</th>
                    <th className="text-left px-4 py-4 font-semibold text-gray-900 dark:text-gray-300 w-36 hidden lg:table-cell">CONFIDENCE</th>
                    <th className="text-left px-4 py-4 font-semibold text-gray-900 dark:text-gray-300 w-48">ACTIONS</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-gray-200 dark:divide-gray-800">
                  {filteredInvoices.map((invoice) => (
                    <tr key={invoice.id} className="hover:bg-gray-50 dark:hover:bg-gray-900/50">
                      <td className="px-4 py-4">
                        <input
                          type="checkbox"
                          checked={selectedInvoices.has(invoice.id)}
                          onChange={() => toggleSelectInvoice(invoice.id)}
                          className="w-4 h-4 text-blue-600 border-gray-300 dark:border-gray-600 rounded focus:ring-blue-500 cursor-pointer"
                        />
                      </td>
                      <td className="px-4 py-4">
                        <div className="font-medium text-gray-900 dark:text-white truncate max-w-xs" title={invoice.vendor_name || 'Unknown Vendor'}>
                          {invoice.vendor_name || 'Unknown Vendor'}
                        </div>
                      </td>
                      <td className="px-4 py-4 text-gray-600 dark:text-gray-400 truncate" title={invoice.invoice_number || 'N/A'}>
                        {invoice.invoice_number || 'N/A'}
                      </td>
                      <td className="px-4 py-4 text-gray-600 dark:text-gray-400 text-sm">
                        {invoice.invoice_date ? new Date(invoice.invoice_date).toLocaleDateString() : 'N/A'}
                      </td>
                      <td className="px-4 py-4 text-gray-600 dark:text-gray-400 text-sm hidden lg:table-cell">
                        {invoice.due_date ? new Date(invoice.due_date).toLocaleDateString() : 'N/A'}
                      </td>
                      <td className="px-4 py-4 font-semibold text-gray-900 dark:text-white">
                        {formatCurrency(invoice.total_amount || 0, invoice.currency)}
                      </td>
                      <td className="px-4 py-4 text-gray-600 dark:text-gray-400 hidden xl:table-cell">
                        {formatCurrency((invoice.cgst + invoice.sgst + invoice.igst || 0), invoice.currency)}
                      </td>
                      <td className="px-4 py-4">
                        <span className={`inline-flex items-center px-2 py-1 rounded-full text-xs font-medium ${
                          invoice.payment_status === 'paid' 
                            ? 'bg-green-100 dark:bg-green-900/50 text-green-800 dark:text-green-300'
                            : invoice.payment_status === 'overdue'
                            ? 'bg-red-100 dark:bg-red-900/50 text-red-800 dark:text-red-300'
                            : 'bg-yellow-100 dark:bg-yellow-900/50 text-yellow-800 dark:text-yellow-300'
                        }`}>
                          {(invoice.payment_status || 'pending').charAt(0).toUpperCase() + (invoice.payment_status || 'pending').slice(1)}
                        </span>
                      </td>
                      <td className="px-4 py-4 hidden lg:table-cell">
                        <ConfidenceIndicator 
                          confidence={invoice.confidence_score || 0}
                          size="sm"
                        />
                      </td>
                      <td className="px-4 py-4">
                        <div className="flex items-center gap-2">
                          {/* View Details Button */}
                          <Link
                            href={`/invoices/details?id=${invoice.id}`}
                            className="px-3 py-1.5 bg-blue-600 hover:bg-blue-700 text-white text-sm font-medium rounded-md transition-colors"
                          >
                            View
                          </Link>
                          {/* Export Dropdown */}
                          <div className="relative export-dropdown">
                            <button
                              data-dropdown-button
                              onClick={(e) => {
                                e.stopPropagation()
                                toggleRowExportDropdown(invoice.id)
                              }}
                              className="px-1.5 py-1 hover:bg-blue-50 dark:hover:bg-blue-900/30 rounded-md transition-colors group flex items-center gap-1 text-xs"
                              title="Export Options"
                            >
                              <span className="text-gray-600 dark:text-gray-400 group-hover:text-blue-600 dark:group-hover:text-blue-400 text-xs">Export</span>
                              <ChevronDown className="w-3 h-3 text-gray-600 dark:text-gray-400 group-hover:text-blue-600 dark:group-hover:text-blue-400" />
                            </button>
                            {showRowExportDropdown[invoice.id] && (
                              <div className="absolute right-0 mt-1 w-32 bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg shadow-lg z-50">
                                <button
                                  onClick={() => handleRowExport(invoice, 'excel')}
                                  className="w-full text-left px-3 py-2 text-xs text-blue-600 dark:text-blue-400 hover:bg-blue-50 dark:hover:bg-blue-900/30 rounded-t-lg font-semibold"
                                >
                                  Excel
                                </button>
                                <button
                                  onClick={() => handleRowExport(invoice, 'csv')}
                                  className="w-full text-left px-3 py-2 text-xs text-green-600 dark:text-green-400 hover:bg-green-50 dark:hover:bg-green-900/30 font-semibold"
                                >
                                  CSV
                                </button>
                                <button
                                  onClick={() => handleRowExport(invoice, 'tally')}
                                  className="w-full text-left px-3 py-2 text-xs text-purple-600 dark:text-purple-400 hover:bg-purple-50 dark:hover:bg-purple-900/30 font-semibold"
                                >
                                  Tally
                                </button>
                                <button
                                  onClick={() => handleRowExport(invoice, 'quickbooks')}
                                  className="w-full text-left px-3 py-2 text-xs text-orange-600 dark:text-orange-400 hover:bg-orange-50 dark:hover:bg-orange-900/30 font-semibold"
                                >
                                  QuickBooks
                                </button>
                                <button
                                  onClick={() => handleRowExport(invoice, 'zoho')}
                                  className="w-full text-left px-3 py-2 text-xs text-indigo-600 dark:text-indigo-400 hover:bg-indigo-50 dark:hover:bg-indigo-900/30 rounded-b-lg font-semibold"
                                >
                                  Zoho
                                </button>
                              </div>
                            )}
                          </div>
                          <button
                            onClick={() => deleteDocument(invoice.id)}
                            className="p-1.5 hover:bg-red-50 dark:hover:bg-red-900/30 rounded-md transition-colors group mr-2"
                            title="Delete"
                          >
                            <Trash2 className="w-4 h-4 text-gray-600 dark:text-gray-400 group-hover:text-red-600 dark:group-hover:text-red-400" />
                          </button>
                        </div>
                      </td>
                    </tr>
                  ))}
                </tbody>
                </table>
              </div>
            </div>

            {/* Mobile Cards */}
            <div className="sm:hidden space-y-4">
              {filteredInvoices.map((invoice) => (
                <div key={invoice.id} className="bg-gray-50 dark:bg-gray-900 rounded-xl border border-gray-200 dark:border-gray-800 p-4">
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
                        <div className="flex flex-col items-end gap-1">
                          <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                            invoice.payment_status === 'paid' 
                              ? 'bg-green-100 dark:bg-green-900/50 text-green-800 dark:text-green-300'
                              : invoice.payment_status === 'overdue'
                              ? 'bg-red-100 dark:bg-red-900/50 text-red-800 dark:text-red-300'
                              : 'bg-yellow-100 dark:bg-yellow-900/50 text-yellow-800 dark:text-yellow-300'
                          }`}>
                            {(invoice.payment_status || 'unpaid').charAt(0).toUpperCase() + (invoice.payment_status || 'unpaid').slice(1)}
                          </span>
                          <ConfidenceIndicator 
                            confidence={invoice.confidence_score || 0}
                            size="sm"
                          />
                        </div>
                      </div>
                    </div>
                  </div>
                  <div className="space-y-2 mb-4">
                    <div className="flex justify-between text-sm">
                      <span className="text-gray-600 dark:text-gray-400">Amount:</span>
                      <span className="font-semibold text-gray-900 dark:text-white">
                        {formatCurrency(invoice.total_amount || 0, invoice.currency)}
                      </span>
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
                      href={`/invoices/details?id=${invoice.id}`}
                      className="flex-1 py-2 px-3 bg-blue-50 dark:bg-blue-900/30 text-blue-600 dark:text-blue-400 rounded-lg hover:bg-blue-100 dark:hover:bg-blue-900/50 transition-colors text-sm font-medium text-center"
                    >
                      Details
                    </Link>
                    <div className="relative flex-1 export-dropdown">
                      <button
                        data-dropdown-button
                        onClick={(e) => {
                          e.stopPropagation()
                          toggleMobileExportDropdown(invoice.id)
                        }}
                        className="w-full py-2 px-3 bg-blue-50 dark:bg-blue-900/30 text-blue-600 dark:text-blue-400 rounded-lg hover:bg-blue-100 dark:hover:bg-blue-900/50 transition-colors text-sm font-medium flex items-center justify-center gap-1"
                      >
                        Export <ChevronDown className="w-3 h-3" />
                      </button>
                      {showMobileExportDropdown[invoice.id] && (
                        <div className="absolute bottom-full left-0 right-0 mb-1 bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg shadow-lg z-50">
                          <button
                            onClick={() => handleMobileExport(invoice, 'excel')}
                            className="w-full text-left px-3 py-2 text-sm text-blue-600 dark:text-blue-400 hover:bg-blue-50 dark:hover:bg-blue-900/30 rounded-t-lg font-semibold"
                          >
                            Excel
                          </button>
                          <button
                            onClick={() => handleMobileExport(invoice, 'csv')}
                            className="w-full text-left px-3 py-2 text-sm text-green-600 dark:text-green-400 hover:bg-green-50 dark:hover:bg-green-900/30 font-semibold"
                          >
                            CSV
                          </button>
                          <button
                            onClick={() => handleMobileExport(invoice, 'tally')}
                            className="w-full text-left px-3 py-2 text-sm text-purple-600 dark:text-purple-400 hover:bg-purple-50 dark:hover:bg-purple-900/30 font-semibold"
                          >
                            Tally XML
                          </button>
                          <button
                            onClick={() => handleMobileExport(invoice, 'quickbooks')}
                            className="w-full text-left px-3 py-2 text-sm text-orange-600 dark:text-orange-400 hover:bg-orange-50 dark:hover:bg-orange-900/30 font-semibold"
                          >
                            QuickBooks
                          </button>
                          <button
                            onClick={() => handleMobileExport(invoice, 'zoho')}
                            className="w-full text-left px-3 py-2 text-sm text-indigo-600 dark:text-indigo-400 hover:bg-indigo-50 dark:hover:bg-indigo-900/30 rounded-b-lg font-semibold"
                          >
                            Zoho Books
                          </button>
                        </div>
                      )}
                    </div>
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
                <button className="px-4 py-2 text-gray-600 dark:text-gray-400 border border-gray-300 dark:border-gray-600 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-950">
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
      
      {/* Export Warning Modal */}
      {showWarningModal && warningCallbacks && (
        <ExportWarningModal
          warnings={exportWarnings}
          onConfirm={() => {
            setShowWarningModal(false)
            warningCallbacks.onConfirm()
          }}
          onCancel={() => {
            setShowWarningModal(false)
            warningCallbacks.onCancel()
          }}
        />
      )}
      
      {/* Export Success Modal */}
      {showSuccessModal && successData && (
        <ExportSuccessModal
          exportType={successData.exportType}
          stats={successData.stats}
          onClose={() => setShowSuccessModal(false)}
        />
      )}
      
      {/* Export Error Modal */}
      {showErrorModal && errorData && (
        <ExportErrorModal
          title={errorData.title}
          errors={errorData.errors}
          type={errorData.type}
          onClose={() => setShowErrorModal(false)}
        />
      )}
      
      {/* QuickBooks Format Selection Modal */}
      {showQuickBooksFormatModal && quickBooksCallbacks && (
        <QuickBooksFormatModal
          onSelectFormat={(format) => {
            setShowQuickBooksFormatModal(false)
            quickBooksCallbacks.onSelectFormat(format)
          }}
          onCancel={() => {
            setShowQuickBooksFormatModal(false)
            quickBooksCallbacks.onCancel()
          }}
        />
      )}
    </DashboardLayout>
  )
}
