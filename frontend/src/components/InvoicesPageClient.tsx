'use client'

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
import { exportInvoicesToCSV } from '@/lib/invoiceUtils'
import { formatCurrency } from '@/lib/currency'
import ConfidenceIndicator from '@/components/ConfidenceIndicator'

const supabase = createClient(
  process.env.NEXT_PUBLIC_SUPABASE_URL || 'https://placeholder.supabase.co',
  process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY || 'placeholder-anon-key'
);

export default function InvoicesPageClient({ initialInvoices }) {
  const [searchQuery, setSearchQuery] = useState('')
  const [filterStatus, setFilterStatus] = useState('all')
  const [invoices, setInvoices] = useState<any[]>(initialInvoices)
  const [loading, setLoading] = useState(false)
  const [selectedInvoices, setSelectedInvoices] = useState<Set<number>>(new Set())
  const [showMainExportDropdown, setShowMainExportDropdown] = useState(false)
  const [showBulkExportDropdown, setShowBulkExportDropdown] = useState(false)
  const [showRowExportDropdown, setShowRowExportDropdown] = useState<{[key: string]: boolean}>({})
  const [showMobileExportDropdown, setShowMobileExportDropdown] = useState<{[key: string]: boolean}>({})

  // Close dropdowns when clicking outside
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      const target = event.target as HTMLElement
      
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

  const fetchInvoices = async () => {
    try {
      setLoading(true)
      
      const { data: { user } } = await supabase.auth.getUser()
      if (!user) {
        setLoading(false)
        return
      }

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
        setInvoices([])
        return
      }

      setInvoices(invoicesData || [])
      
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
      alert('Failed to export invoices')
    }
  }

  const exportSingleInvoice = (invoice: any) => {
    try {
      exportInvoicesToCSV([invoice])
    } catch (error) {
      alert('Failed to export invoice')
    }
  }

  const exportSingleInvoiceToPDF = async (invoice: any) => {
    try {
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/bulk/export-pdf`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          invoice_ids: [invoice.id]
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
      a.download = `invoice_${invoice.invoice_number || invoice.id}.pdf`
      document.body.appendChild(a)
      a.click()
      window.URL.revokeObjectURL(url)
      document.body.removeChild(a)
    } catch (error) {
      alert('Failed to export PDF. Please try again.')
    }
  }

  const handlePDFExport = async () => {
    try {
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/bulk/export-pdf`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          invoice_ids: invoices.map(inv => inv.id)
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
      a.download = `all_invoices_${new Date().toISOString().split('T')[0]}.pdf`
      document.body.appendChild(a)
      a.click()
      window.URL.revokeObjectURL(url)
      document.body.removeChild(a)
    } catch (error) {
      alert('Failed to export PDF. Please try again.')
    }
  }

  const handleExcelExport = async () => {
    try {
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/bulk/export-excel`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          invoice_ids: invoices.map(inv => inv.id)
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
      alert('Failed to export Excel. Please try again.')
    }
  }

  const exportSingleInvoiceToExcel = async (invoice: any) => {
    try {
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/bulk/export-excel`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          invoice_ids: [invoice.id]
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
      alert('Failed to export Excel. Please try again.')
    }
  }

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
      alert('Failed to export selected invoices')
    }
  }

  const exportSelectedInvoicesExcel = async () => {
    const selected = invoices.filter(inv => selectedInvoices.has(inv.id))
    if (selected.length === 0) {
      alert('Please select invoices to export')
      return
    }
    
    try {
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/bulk/export-excel`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          invoice_ids: selected.map(inv => inv.id)
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
      alert('Failed to export Excel. Please try again.')
    }
  }

  const exportSelectedInvoicesPDF = async () => {
    const selected = invoices.filter(inv => selectedInvoices.has(inv.id))
    if (selected.length === 0) {
      alert('Please select invoices to export')
      return
    }
    
    try {
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/bulk/export-pdf`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          invoice_ids: selected.map(inv => inv.id)
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
      a.download = `selected_invoices_${new Date().toISOString().split('T')[0]}.pdf`
      document.body.appendChild(a)
      a.click()
      window.URL.revokeObjectURL(url)
      document.body.removeChild(a)
    } catch (error) {
      alert('Failed to export PDF. Please try again.')
    }
  }

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

  const handleMainExport = (format: 'excel' | 'csv' | 'pdf') => {
    setShowMainExportDropdown(false)
    switch(format) {
      case 'excel':
        handleExcelExport()
        break
      case 'csv':
        handleExport()
        break
      case 'pdf':
        handlePDFExport()
        break
    }
  }

  const handleBulkExport = (format: 'excel' | 'csv' | 'pdf') => {
    setShowBulkExportDropdown(false)
    switch(format) {
      case 'excel':
        exportSelectedInvoicesExcel()
        break
      case 'csv':
        exportSelectedInvoices()
        break
      case 'pdf':
        exportSelectedInvoicesPDF()
        break
    }
  }

  const handleRowExport = (invoice: any, format: 'excel' | 'csv' | 'pdf') => {
    setShowRowExportDropdown({})
    switch(format) {
      case 'excel':
        exportSingleInvoiceToExcel(invoice)
        break
      case 'csv':
        exportSingleInvoice(invoice)
        break
      case 'pdf':
        exportSingleInvoiceToPDF(invoice)
        break
    }
  }

  const handleMobileExport = (invoice: any, format: 'excel' | 'csv' | 'pdf') => {
    setShowMobileExportDropdown({})
    switch(format) {
      case 'excel':
        exportSingleInvoiceToExcel(invoice)
        break
      case 'csv':
        exportSingleInvoice(invoice)
        break
      case 'pdf':
        exportSingleInvoiceToPDF(invoice)
        break
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
      
      await fetchInvoices()
    } catch (error) {
      alert('Failed to delete invoice')
    }
  }

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
        {/* Header, Search, Filter, Bulk Actions, etc. */}
      </div>
    </DashboardLayout>
  )
}
