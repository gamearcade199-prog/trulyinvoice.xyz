/**
 * Enterprise Utilities for Invoice Management
 * Includes bulk operations, export, validation, and more
 */

import { supabase } from './supabase'

/**
 * Export invoices to CSV format
 */
export async function exportInvoicesToCSV(invoices: any[]) {
  if (invoices.length === 0) {
    alert('No invoices to export')
    return
  }

  // CSV headers - full names to prevent cutoff
  const headers = [
    'Invoice Number',
    'Vendor Name',
    'Invoice Date',
    'Due Date',
    'Subtotal',
    'Tax Amount',
    'Total Amount',
    'Payment Status',
    'Payment Method',
    'GSTIN',
    'Created At'
  ]

  // Helper function for consistent date formatting (DD/MM/YYYY)
  const formatDate = (dateString: string | null | undefined): string => {
    if (!dateString) return ''
    try {
      const date = new Date(dateString)
      if (isNaN(date.getTime())) return ''
      const day = String(date.getDate()).padStart(2, '0')
      const month = String(date.getMonth() + 1).padStart(2, '0')
      const year = date.getFullYear()
      return `${day}/${month}/${year}`
    } catch {
      return ''
    }
  }

  // Convert invoices to CSV rows
  const rows = invoices.map(invoice => {
    // Calculate subtotal: use stored value or total - tax
    const taxAmount = (invoice.cgst || 0) + (invoice.sgst || 0) + (invoice.igst || 0)
    const subtotal = invoice.subtotal || (invoice.total_amount ? invoice.total_amount - taxAmount : 0)

    return [
      invoice.invoice_number || '',
      invoice.vendor_name || '',
      formatDate(invoice.invoice_date),
      formatDate(invoice.due_date),
      subtotal.toFixed(2),
      taxAmount.toFixed(2),
      (invoice.total_amount || 0).toFixed(2),
      invoice.payment_status || 'pending',
      invoice.payment_method || '',
      invoice.gstin || '',
      formatDate(invoice.created_at)
    ]
  })

  // Combine headers and rows
  const csvContent = [
    headers.join(','),
    ...rows.map(row => row.map(cell => `"${cell}"`).join(','))
  ].join('\n')

  // Create blob and download
  const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' })
  const link = document.createElement('a')
  const url = URL.createObjectURL(blob)
  
  link.setAttribute('href', url)
  link.setAttribute('download', `invoices_${new Date().toISOString().split('T')[0]}.csv`)
  link.style.visibility = 'hidden'
  
  document.body.appendChild(link)
  link.click()
  document.body.removeChild(link)
}

/**
 * Export invoices to Excel format
 */
export async function exportInvoicesToExcel(invoices: any[]) {
  // For now, use CSV format
  // TODO: Implement proper Excel export with xlsx library
  exportInvoicesToCSV(invoices)
}

/**
 * Export invoices to Tally XML format
 */
export async function exportInvoicesToTallyXML(invoices: any[]) {
  if (invoices.length === 0) {
    alert('No invoices to export')
    return
  }

  // Helper function for consistent date formatting (DD-MM-YYYY for Tally)
  const formatDate = (dateString: string | null | undefined): string => {
    if (!dateString) return ''
    try {
      const date = new Date(dateString)
      if (isNaN(date.getTime())) return ''
      const day = String(date.getDate()).padStart(2, '0')
      const month = String(date.getMonth() + 1).padStart(2, '0')
      const year = date.getFullYear()
      return `${day}-${month}-${year}`
    } catch {
      return ''
    }
  }

  // Generate Tally XML structure
  const xmlContent = `<?xml version="1.0" encoding="UTF-8"?>
<ENVELOPE>
  <HEADER>
    <TALLYREQUEST>Import Data</TALLYREQUEST>
  </HEADER>
  <BODY>
    <IMPORTDATA>
      <REQUESTDESC>
        <REPORTNAME>Vouchers</REPORTNAME>
      </REQUESTDESC>
      <REQUESTDATA>
        <TALLYMESSAGE xmlns:UDF="TallyUDF">
${invoices.map(invoice => {
  const taxAmount = (invoice.cgst || 0) + (invoice.sgst || 0) + (invoice.igst || 0)
  const subtotal = invoice.subtotal || (invoice.total_amount ? invoice.total_amount - taxAmount : 0)

  return `          <VOUCHER VCHTYPE="Purchase" ACTION="Create">
            <VOUCHERNUMBER>${invoice.invoice_number || 'N/A'}</VOUCHERNUMBER>
            <VOUCHERTYPENAME>Purchase</VOUCHERTYPENAME>
            <DATE>${formatDate(invoice.invoice_date)}</DATE>
            <NARRATION>Purchase Invoice - ${invoice.vendor_name || 'Vendor'}</NARRATION>
            <PARTYLEDGERNAME>${invoice.vendor_name || 'Vendor'}</PARTYLEDGERNAME>
            <VOUCHERAMOUNT>${(invoice.total_amount || 0).toFixed(2)}</VOUCHERAMOUNT>
            <ALLLEDGERENTRIES.LIST>
              <LEDGERNAME>${invoice.vendor_name || 'Vendor'}</LEDGERNAME>
              <AMOUNT>${(invoice.total_amount || 0).toFixed(2)}</AMOUNT>
              <BILLALLOCATIONS.LIST>
                <NAME>${invoice.invoice_number || 'N/A'}</NAME>
                <BILLTYPE>New Ref</BILLTYPE>
                <AMOUNT>${(invoice.total_amount || 0).toFixed(2)}</AMOUNT>
              </BILLALLOCATIONS.LIST>
            </ALLLEDGERENTRIES.LIST>
            <ALLLEDGERENTRIES.LIST>
              <LEDGERNAME>Purchase Account</LEDGERNAME>
              <AMOUNT>${(-subtotal).toFixed(2)}</AMOUNT>
            </ALLLEDGERENTRIES.LIST>
${taxAmount > 0 ? `            <ALLLEDGERENTRIES.LIST>
              <LEDGERNAME>Input GST</LEDGERNAME>
              <AMOUNT>${(-taxAmount).toFixed(2)}</AMOUNT>
            </ALLLEDGERENTRIES.LIST>` : ''}
          </VOUCHER>`
}).join('\n')}
        </TALLYMESSAGE>
      </REQUESTDATA>
    </IMPORTDATA>
  </BODY>
</ENVELOPE>`

  // Create blob and download
  const blob = new Blob([xmlContent], { type: 'application/xml;charset=utf-8;' })
  const link = document.createElement('a')
  const url = URL.createObjectURL(blob)

  link.setAttribute('href', url)
  link.setAttribute('download', `invoices_tally_${new Date().toISOString().split('T')[0]}.xml`)
  link.style.visibility = 'hidden'

  document.body.appendChild(link)
  link.click()
  document.body.removeChild(link)
}

/**
 * Export invoices to QuickBooks CSV format
 */
export async function exportInvoicesToQuickBooksCSV(invoices: any[]) {
  if (invoices.length === 0) {
    alert('No invoices to export')
    return
  }

  // QuickBooks CSV headers
  const headers = [
    'Invoice No',
    'Date',
    'Customer Name',
    'Item',
    'Amount',
    'GST',
    'Total'
  ]

  // Helper function for consistent date formatting (MM/DD/YYYY for QuickBooks)
  const formatDate = (dateString: string | null | undefined): string => {
    if (!dateString) return ''
    try {
      const date = new Date(dateString)
      if (isNaN(date.getTime())) return ''
      const month = String(date.getMonth() + 1).padStart(2, '0')
      const day = String(date.getDate()).padStart(2, '0')
      const year = date.getFullYear()
      return `${month}/${day}/${year}`
    } catch {
      return ''
    }
  }

  // Convert invoices to CSV rows
  const rows = invoices.map(invoice => {
    const taxAmount = (invoice.cgst || 0) + (invoice.sgst || 0) + (invoice.igst || 0)
    const subtotal = invoice.subtotal || (invoice.total_amount ? invoice.total_amount - taxAmount : 0)

    return [
      invoice.invoice_number || '',
      formatDate(invoice.invoice_date),
      invoice.vendor_name || '',
      'Invoice Processing', // Generic item description
      subtotal.toFixed(2),
      taxAmount.toFixed(2),
      (invoice.total_amount || 0).toFixed(2)
    ]
  })

  // Combine headers and rows
  const csvContent = [
    headers.join(','),
    ...rows.map(row => row.map(cell => `"${cell}"`).join(','))
  ].join('\n')

  // Create blob and download
  const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' })
  const link = document.createElement('a')
  const url = URL.createObjectURL(blob)

  link.setAttribute('href', url)
  link.setAttribute('download', `invoices_quickbooks_${new Date().toISOString().split('T')[0]}.csv`)
  link.style.visibility = 'hidden'

  document.body.appendChild(link)
  link.click()
  document.body.removeChild(link)
}

/**
 * Export invoices to Zoho Books CSV format
 */
export async function exportInvoicesToZohoBooksCSV(invoices: any[]) {
  if (invoices.length === 0) {
    alert('No invoices to export')
    return
  }

  // Zoho Books CSV headers
  const headers = [
    'Invoice Number',
    'Invoice Date',
    'Customer Name',
    'Item Name',
    'Quantity',
    'Rate',
    'GST',
    'Total'
  ]

  // Helper function for consistent date formatting (DD/MM/YYYY for Zoho)
  const formatDate = (dateString: string | null | undefined): string => {
    if (!dateString) return ''
    try {
      const date = new Date(dateString)
      if (isNaN(date.getTime())) return ''
      const day = String(date.getDate()).padStart(2, '0')
      const month = String(date.getMonth() + 1).padStart(2, '0')
      const year = date.getFullYear()
      return `${day}/${month}/${year}`
    } catch {
      return ''
    }
  }

  // Convert invoices to CSV rows
  const rows = invoices.map(invoice => {
    const taxAmount = (invoice.cgst || 0) + (invoice.sgst || 0) + (invoice.igst || 0)
    const subtotal = invoice.subtotal || (invoice.total_amount ? invoice.total_amount - taxAmount : 0)
    const quantity = 1 // Default quantity
    const rate = subtotal.toFixed(2) // Rate per unit

    return [
      invoice.invoice_number || '',
      formatDate(invoice.invoice_date),
      invoice.vendor_name || '',
      'Invoice Processing Service', // Item description
      quantity.toString(),
      rate,
      taxAmount.toFixed(2),
      (invoice.total_amount || 0).toFixed(2)
    ]
  })

  // Combine headers and rows
  const csvContent = [
    headers.join(','),
    ...rows.map(row => row.map(cell => `"${cell}"`).join(','))
  ].join('\n')

  // Create blob and download
  const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' })
  const link = document.createElement('a')
  const url = URL.createObjectURL(blob)

  link.setAttribute('href', url)
  link.setAttribute('download', `invoices_zoho_books_${new Date().toISOString().split('T')[0]}.csv`)
  link.style.visibility = 'hidden'

  document.body.appendChild(link)
  link.click()
  document.body.removeChild(link)
}

/**
 * Bulk update payment status
 */
export async function bulkUpdatePaymentStatus(
  invoiceIds: number[],
  status: 'paid' | 'unpaid' | 'pending' | 'overdue'
) {
  try {
    const { error } = await supabase
      .from('invoices')
      .update({ payment_status: status })
      .in('id', invoiceIds)

    if (error) throw error

    return { success: true, count: invoiceIds.length }
  } catch (error: any) {
    console.error('Bulk update error:', error)
    throw new Error(`Failed to update invoices: ${error.message}`)
  }
}

/**
 * Bulk delete invoices
 */
export async function bulkDeleteInvoices(invoiceIds: number[]) {
  try {
    // First, get associated documents
    const { data: invoices, error: fetchError } = await supabase
      .from('invoices')
      .select('document_id')
      .in('id', invoiceIds)

    if (fetchError) throw fetchError

    const documentIds = invoices?.map(inv => inv.document_id).filter(Boolean) || []

    // Delete invoices
    const { error: deleteInvoicesError } = await supabase
      .from('invoices')
      .delete()
      .in('id', invoiceIds)

    if (deleteInvoicesError) throw deleteInvoicesError

    // Delete associated documents
    if (documentIds.length > 0) {
      const { error: deleteDocsError } = await supabase
        .from('documents')
        .delete()
        .in('id', documentIds)

      if (deleteDocsError) console.warn('Failed to delete some documents:', deleteDocsError)
    }

    return { success: true, count: invoiceIds.length }
  } catch (error: any) {
    console.error('Bulk delete error:', error)
    throw new Error(`Failed to delete invoices: ${error.message}`)
  }
}

/**
 * Detect duplicate invoices
 */
export async function detectDuplicateInvoices(userId: string) {
  try {
    const { data: invoices, error } = await supabase
      .from('invoices')
      .select('id, invoice_number, vendor_name, total_amount, invoice_date')
      .eq('user_id', userId)

    if (error) throw error

    const duplicates: any[] = []
    const seen = new Map<string, any[]>()

    invoices?.forEach(invoice => {
      const key = `${invoice.invoice_number}-${invoice.vendor_name}-${invoice.total_amount}`
      
      if (seen.has(key)) {
        const existing = seen.get(key)!
        duplicates.push({ original: existing[0], duplicate: invoice })
      } else {
        seen.set(key, [invoice])
      }
    })

    return duplicates
  } catch (error: any) {
    console.error('Duplicate detection error:', error)
    return []
  }
}

/**
 * Calculate invoice statistics
 */
export function calculateInvoiceStats(invoices: any[]) {
  const stats = {
    total: invoices.length,
    totalAmount: 0,
    paid: 0,
    unpaid: 0,
    overdue: 0,
    pending: 0,
    avgAmount: 0,
    taxTotal: 0,
    vendors: new Set<string>()
  }

  invoices.forEach(invoice => {
    stats.totalAmount += invoice.total_amount || 0
    stats.taxTotal += invoice.tax_amount || 0
    
    if (invoice.vendor_name) {
      stats.vendors.add(invoice.vendor_name)
    }

    switch (invoice.payment_status) {
      case 'paid':
        stats.paid++
        break
      case 'unpaid':
        stats.unpaid++
        break
      case 'overdue':
        stats.overdue++
        break
      case 'pending':
        stats.pending++
        break
    }
  })

  stats.avgAmount = stats.total > 0 ? stats.totalAmount / stats.total : 0

  return {
    ...stats,
    vendorCount: stats.vendors.size
  }
}

/**
 * Validate invoice data
 */
export function validateInvoiceData(invoice: any): { valid: boolean; errors: string[] } {
  const errors: string[] = []

  if (!invoice.vendor_name || invoice.vendor_name.trim() === '') {
    errors.push('Vendor name is required')
  }

  if (!invoice.invoice_number || invoice.invoice_number.trim() === '') {
    errors.push('Invoice number is required')
  }

  if (!invoice.total_amount || invoice.total_amount <= 0) {
    errors.push('Total amount must be greater than 0')
  }

  if (invoice.invoice_date) {
    const invoiceDate = new Date(invoice.invoice_date)
    if (isNaN(invoiceDate.getTime())) {
      errors.push('Invalid invoice date')
    }
  }

  if (invoice.due_date) {
    const dueDate = new Date(invoice.due_date)
    if (isNaN(dueDate.getTime())) {
      errors.push('Invalid due date')
    }
  }

  return {
    valid: errors.length === 0,
    errors
  }
}

/**
 * Format currency in Indian Rupees
 */
export function formatINR(amount: number): string {
  return new Intl.NumberFormat('en-IN', {
    style: 'currency',
    currency: 'INR',
    minimumFractionDigits: 0,
    maximumFractionDigits: 0
  }).format(amount)
}

/**
 * Calculate GST breakdown
 */
export function calculateGSTBreakdown(amount: number, gstRate: number = 18) {
  const gstAmount = (amount * gstRate) / 100
  const cgst = gstAmount / 2
  const sgst = gstAmount / 2
  const total = amount + gstAmount

  return {
    amount,
    gstRate,
    gstAmount,
    cgst,
    sgst,
    total
  }
}

/**
 * Generate invoice report
 */
export function generateInvoiceReport(invoices: any[]) {
  const stats = calculateInvoiceStats(invoices)
  
  const report = {
    summary: {
      totalInvoices: stats.total,
      totalAmount: formatINR(stats.totalAmount),
      totalTax: formatINR(stats.taxTotal),
      averageAmount: formatINR(stats.avgAmount),
      uniqueVendors: stats.vendorCount
    },
    paymentStatus: {
      paid: `${stats.paid} (${((stats.paid / stats.total) * 100).toFixed(1)}%)`,
      unpaid: `${stats.unpaid} (${((stats.unpaid / stats.total) * 100).toFixed(1)}%)`,
      overdue: `${stats.overdue} (${((stats.overdue / stats.total) * 100).toFixed(1)}%)`,
      pending: `${stats.pending} (${((stats.pending / stats.total) * 100).toFixed(1)}%)`
    },
    generated: new Date().toLocaleString()
  }

  return report
}

/**
 * Search invoices with fuzzy matching
 */
export function searchInvoices(invoices: any[], query: string) {
  const lowerQuery = query.toLowerCase().trim()
  
  if (!lowerQuery) return invoices

  return invoices.filter(invoice => {
    return (
      invoice.vendor_name?.toLowerCase().includes(lowerQuery) ||
      invoice.invoice_number?.toLowerCase().includes(lowerQuery) ||
      invoice.gstin?.toLowerCase().includes(lowerQuery) ||
      invoice.payment_method?.toLowerCase().includes(lowerQuery)
    )
  })
}

/**
 * Sort invoices
 */
export function sortInvoices(
  invoices: any[],
  field: string,
  direction: 'asc' | 'desc' = 'desc'
) {
  return [...invoices].sort((a, b) => {
    let aVal = a[field]
    let bVal = b[field]

    // Handle dates
    if (field.includes('date')) {
      aVal = aVal ? new Date(aVal).getTime() : 0
      bVal = bVal ? new Date(bVal).getTime() : 0
    }

    // Handle numbers
    if (typeof aVal === 'number' && typeof bVal === 'number') {
      return direction === 'asc' ? aVal - bVal : bVal - aVal
    }

    // Handle strings
    const aStr = String(aVal || '').toLowerCase()
    const bStr = String(bVal || '').toLowerCase()

    if (direction === 'asc') {
      return aStr.localeCompare(bStr)
    } else {
      return bStr.localeCompare(aStr)
    }
  })
}
