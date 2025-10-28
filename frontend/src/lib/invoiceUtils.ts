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
 * Export invoices to Tally XML format (India GST Compliant)
 */
export async function exportInvoicesToTallyXML(invoices: any[]) {
  if (invoices.length === 0) {
    alert('No invoices to export')
    return
  }

  // Validate invoices for required GST fields
  const validationErrors: string[] = []
  invoices.forEach((invoice, index) => {
    if (!invoice.invoice_number) {
      validationErrors.push(`Invoice ${index + 1}: Missing invoice number`)
    }
    if (!invoice.vendor_name) {
      validationErrors.push(`Invoice ${index + 1}: Missing vendor name`)
    }
    if (!invoice.total_amount || invoice.total_amount <= 0) {
      validationErrors.push(`Invoice ${index + 1}: Invalid total amount`)
    }
    if (!invoice.invoice_date) {
      validationErrors.push(`Invoice ${index + 1}: Missing invoice date`)
    }
  })

  if (validationErrors.length > 0) {
    alert(`Export validation failed:\n${validationErrors.join('\n')}`)
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

  // Helper function to escape XML entities
  const escapeXml = (str: string): string => {
    if (!str) return ''
    return str
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&apos;')
  }

  // Generate Tally XML structure with proper GST compliance
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
  const cgst = invoice.cgst || 0
  const sgst = invoice.sgst || 0
  const igst = invoice.igst || 0
  const totalGST = cgst + sgst + igst
  const subtotal = invoice.subtotal || (invoice.total_amount ? invoice.total_amount - totalGST : 0)
  const gstRate = totalGST > 0 ? Math.round((totalGST / subtotal) * 100) : 0

  // Determine GST type and ledgers
  const hasIGST = igst > 0
  const gstType = hasIGST ? 'IGST' : 'CGST+SGST'

  // Use dynamic HSN/SAC code from database, fallback to default
  const hsnCode = invoice.hsn_code || invoice.sac_code || '9983'
  const itemDescription = invoice.supply_type === 'Service' ? 'Service' : 'Goods'
  const placeOfSupply = invoice.place_of_supply || 'Maharashtra'

    // Determine GST treatment
    const hasGSTIN = invoice.gstin && invoice.gstin.trim() !== ''
    const gstTreatment = hasGSTIN ? 'Taxable' : 'Consumer'
    const reverseCharge = invoice.reverse_charge ? 'Yes' : 'No'
    const tdsApplicable = invoice.tds_amount && invoice.tds_amount > 0 ? 'Yes' : 'No'
    const tdsAmount = invoice.tds_amount || 0
    const tdsPercentage = invoice.tds_percentage || 0
    const isCompositionDealer = invoice.vendor_type === 'Composition' || invoice.vendor_type === 'composition'
    const compositionScheme = isCompositionDealer ? 'Yes' : 'No'  // Check if this is a multi-item invoice
  const lineItems = invoice.line_items || []
  const hasMultipleItems = lineItems.length > 1

  if (hasMultipleItems) {
    // Multi-item invoice: create separate entries for each item
    const itemEntries = lineItems.map((item: any, index: number) => {
      const itemHSN = item.hsn_code || item.sac_code || hsnCode
      const itemName = item.item_name || item.description || `Item ${index + 1}`
      const itemQty = item.quantity || 1
      const itemRate = item.rate || item.unit_price || 0
      const itemAmount = item.amount || (itemQty * itemRate)
      const itemGST = item.gst_amount || (itemAmount * gstRate / 100)
      const itemCGST = hasIGST ? 0 : itemGST / 2
      const itemSGST = hasIGST ? 0 : itemGST / 2
      const itemIGST = hasIGST ? itemGST : 0

      return `            <ALLLEDGERENTRIES.LIST>
              <LEDGERNAME>Purchase @ ${gstRate}% - ${escapeXml(itemName)}</LEDGERNAME>
              <GSTCLASS/>
              <AMOUNT>${(-itemAmount).toFixed(2)}</AMOUNT>
            </ALLLEDGERENTRIES.LIST>
${itemCGST > 0 ? `            <ALLLEDGERENTRIES.LIST>
              <LEDGERNAME>CGST Input @ ${(gstRate/2).toFixed(1)}% - ${escapeXml(itemName)}</LEDGERNAME>
              <GSTCLASS/>
              <AMOUNT>${(-itemCGST).toFixed(2)}</AMOUNT>
            </ALLLEDGERENTRIES.LIST>` : ''}
${itemSGST > 0 ? `            <ALLLEDGERENTRIES.LIST>
              <LEDGERNAME>SGST Input @ ${(gstRate/2).toFixed(1)}% - ${escapeXml(itemName)}</LEDGERNAME>
              <GSTCLASS/>
              <AMOUNT>${(-itemSGST).toFixed(2)}</AMOUNT>
            </ALLLEDGERENTRIES.LIST>` : ''}
${itemIGST > 0 ? `            <ALLLEDGERENTRIES.LIST>
              <LEDGERNAME>IGST Input @ ${gstRate}% - ${escapeXml(itemName)}</LEDGERNAME>
              <GSTCLASS/>
              <AMOUNT>${(-itemIGST).toFixed(2)}</AMOUNT>
            </ALLLEDGERENTRIES.LIST>` : ''}`
    }).join('\n')

    return `          <VOUCHER VCHTYPE="Purchase" ACTION="Create">
            <VOUCHERNUMBER>${invoice.invoice_number || 'N/A'}</VOUCHERNUMBER>
            <VOUCHERTYPENAME>Purchase</VOUCHERTYPENAME>
            <DATE>${formatDate(invoice.invoice_date)}</DATE>
            <DUEDATE>${formatDate(invoice.due_date)}</DUEDATE>
            <NARRATION>Purchase Invoice - ${escapeXml(invoice.vendor_name || 'Vendor')} | GSTIN: ${escapeXml(invoice.gstin || 'N/A')} | GST Rate: ${gstRate}% | HSN/SAC: ${escapeXml(hsnCode)} | Place of Supply: ${escapeXml(placeOfSupply)} | GST Treatment: ${escapeXml(gstTreatment)} | Reverse Charge: ${escapeXml(reverseCharge)}${hasMultipleItems ? ` | Multi-Item Invoice (${lineItems.length} items)` : ''}${tdsApplicable === 'Yes' ? ` | TDS Applicable: ${tdsPercentage}% (₹${tdsAmount.toFixed(2)})` : ''}${isCompositionDealer ? ' | Composition Scheme Dealer' : ''}</NARRATION>
            <PARTYLEDGERNAME>${escapeXml(invoice.vendor_name || 'Vendor')}</PARTYLEDGERNAME>
            <VOUCHERAMOUNT>${(invoice.total_amount || 0).toFixed(2)}</VOUCHERAMOUNT>
            <PARTYMAILINGNAME>${escapeXml(invoice.vendor_name || 'Vendor')}</PARTYMAILINGNAME>
            <PARTYADDRESS.LIST>
              <PARTYADDRESS>GSTIN: ${escapeXml(invoice.gstin || 'N/A')}</PARTYADDRESS>
              <PARTYADDRESS>Place of Supply: ${escapeXml(placeOfSupply)}</PARTYADDRESS>
            </PARTYADDRESS.LIST>
            <ALLLEDGERENTRIES.LIST>
              <LEDGERNAME>${escapeXml(invoice.vendor_name || 'Vendor')}</LEDGERNAME>
              <GSTCLASS/>
              <AMOUNT>${(invoice.total_amount || 0).toFixed(2)}</AMOUNT>
              <BILLALLOCATIONS.LIST>
                <NAME>${escapeXml(invoice.invoice_number || 'N/A')}</NAME>
                <BILLTYPE>New Ref</BILLTYPE>
                <AMOUNT>${(invoice.total_amount || 0).toFixed(2)}</AMOUNT>
              </BILLALLOCATIONS.LIST>
            </ALLLEDGERENTRIES.LIST>
${itemEntries}
          </VOUCHER>`
  } else {
    // Single-item invoice (existing logic)
    return `          <VOUCHER VCHTYPE="Purchase" ACTION="Create">
            <VOUCHERNUMBER>${escapeXml(invoice.invoice_number || 'N/A')}</VOUCHERNUMBER>
            <VOUCHERTYPENAME>Purchase</VOUCHERTYPENAME>
            <DATE>${formatDate(invoice.invoice_date)}</DATE>
            <DUEDATE>${formatDate(invoice.due_date)}</DUEDATE>
            <NARRATION>Purchase Invoice - ${escapeXml(invoice.vendor_name || 'Vendor')} | GSTIN: ${escapeXml(invoice.gstin || 'N/A')} | GST Rate: ${gstRate}% | HSN/SAC: ${escapeXml(hsnCode)} | Place of Supply: ${escapeXml(placeOfSupply)} | GST Treatment: ${escapeXml(gstTreatment)} | Reverse Charge: ${escapeXml(reverseCharge)}</NARRATION>
            <PARTYLEDGERNAME>${escapeXml(invoice.vendor_name || 'Vendor')}</PARTYLEDGERNAME>
            <VOUCHERAMOUNT>${(invoice.total_amount || 0).toFixed(2)}</VOUCHERAMOUNT>
            <PARTYMAILINGNAME>${escapeXml(invoice.vendor_name || 'Vendor')}</PARTYMAILINGNAME>
            <PARTYADDRESS.LIST>
              <PARTYADDRESS>GSTIN: ${escapeXml(invoice.gstin || 'N/A')}</PARTYADDRESS>
              <PARTYADDRESS>Place of Supply: ${escapeXml(placeOfSupply)}</PARTYADDRESS>
            </PARTYADDRESS.LIST>
            <ALLLEDGERENTRIES.LIST>
              <LEDGERNAME>${escapeXml(invoice.vendor_name || 'Vendor')}</LEDGERNAME>
              <GSTCLASS/>
              <AMOUNT>${(invoice.total_amount || 0).toFixed(2)}</AMOUNT>
              <BILLALLOCATIONS.LIST>
                <NAME>${escapeXml(invoice.invoice_number || 'N/A')}</NAME>
                <BILLTYPE>New Ref</BILLTYPE>
                <AMOUNT>${(invoice.total_amount || 0).toFixed(2)}</AMOUNT>
              </BILLALLOCATIONS.LIST>
            </ALLLEDGERENTRIES.LIST>
            <ALLLEDGERENTRIES.LIST>
              <LEDGERNAME>Purchase @ ${gstRate}%</LEDGERNAME>
              <GSTCLASS/>
              <AMOUNT>${(-subtotal).toFixed(2)}</AMOUNT>
            </ALLLEDGERENTRIES.LIST>
${cgst > 0 ? `            <ALLLEDGERENTRIES.LIST>
              <LEDGERNAME>CGST Input @ ${(gstRate/2).toFixed(1)}%</LEDGERNAME>
              <GSTCLASS/>
              <AMOUNT>${(-cgst).toFixed(2)}</AMOUNT>
            </ALLLEDGERENTRIES.LIST>` : ''}
${sgst > 0 ? `            <ALLLEDGERENTRIES.LIST>
              <LEDGERNAME>SGST Input @ ${(gstRate/2).toFixed(1)}%</LEDGERNAME>
              <GSTCLASS/>
              <AMOUNT>${(-sgst).toFixed(2)}</AMOUNT>
            </ALLLEDGERENTRIES.LIST>` : ''}
${igst > 0 ? `            <ALLLEDGERENTRIES.LIST>
              <LEDGERNAME>IGST Input @ ${gstRate}%</LEDGERNAME>
              <GSTCLASS/>
              <AMOUNT>${(-igst).toFixed(2)}</AMOUNT>
            </ALLLEDGERENTRIES.LIST>` : ''}
          </VOUCHER>`
  }
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
  link.setAttribute('download', `invoices_tally_gst_compliant_${new Date().toISOString().split('T')[0]}.xml`)
  link.style.visibility = 'hidden'

  document.body.appendChild(link)
  link.click()
  document.body.removeChild(link)
}

/**
 * Export invoices to QuickBooks CSV format (India GST Compliant)
 */
export async function exportInvoicesToQuickBooksCSV(invoices: any[]) {
  if (invoices.length === 0) {
    alert('No invoices to export')
    return
  }

  // Validate invoices for required GST fields
  const validationErrors: string[] = []
  invoices.forEach((invoice, index) => {
    if (!invoice.invoice_number) {
      validationErrors.push(`Invoice ${index + 1}: Missing invoice number`)
    }
    if (!invoice.vendor_name) {
      validationErrors.push(`Invoice ${index + 1}: Missing vendor name`)
    }
    if (!invoice.total_amount || invoice.total_amount <= 0) {
      validationErrors.push(`Invoice ${index + 1}: Invalid total amount`)
    }
    if (!invoice.invoice_date) {
      validationErrors.push(`Invoice ${index + 1}: Missing invoice date`)
    }
  })

  if (validationErrors.length > 0) {
    alert(`Export validation failed:\n${validationErrors.join('\n')}`)
    return
  }

  // QuickBooks India CSV headers (GST compliant)
  const headers = [
    'Invoice No',
    'Invoice Date',
    'Due Date',
    'Customer Name',
    'GSTIN',
    'Item',
    'HSN/SAC',
    'Quantity',
    'Rate',
    'Amount',
    'CGST Rate',
    'CGST Amount',
    'SGST Rate',
    'SGST Amount',
    'IGST Rate',
    'IGST Amount',
    'Total GST',
    'Total Amount',
    'Place of Supply',
    'Invoice Type',
    'Reverse Charge (RCM)',
    'TDS Applicable',
    'TDS Percentage',
    'TDS Amount',
    'Composition Scheme'
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
  const rows: any[] = []

  invoices.forEach(invoice => {
    const cgst = invoice.cgst || 0
    const sgst = invoice.sgst || 0
    const igst = invoice.igst || 0
    const totalGST = cgst + sgst + igst
    const subtotal = invoice.subtotal || (invoice.total_amount ? invoice.total_amount - totalGST : 0)

    // Calculate GST rates
    const cgstRate = subtotal > 0 ? ((cgst / subtotal) * 100).toFixed(2) : '0.00'
    const sgstRate = subtotal > 0 ? ((sgst / subtotal) * 100).toFixed(2) : '0.00'
    const igstRate = subtotal > 0 ? ((igst / subtotal) * 100).toFixed(2) : '0.00'

    // Determine invoice type
    const hasGSTIN = invoice.gstin && invoice.gstin.trim() !== ''
    const invoiceType = hasGSTIN ? 'B2B' : 'B2C'

    // Use dynamic HSN/SAC code from database, fallback to default
    const hsnCode = invoice.hsn_code || invoice.sac_code || '9983'
    const placeOfSupply = invoice.place_of_supply || 'Maharashtra'
    const itemDescription = invoice.supply_type === 'Service' ? 'Invoice Processing Service' : 'Goods'
    const reverseCharge = invoice.reverse_charge ? 'Yes' : 'No'
    const tdsApplicable = invoice.tds_amount && invoice.tds_amount > 0 ? 'Yes' : 'No'
    const tdsAmount = invoice.tds_amount || 0
    const tdsPercentage = invoice.tds_percentage || 0
    const isCompositionDealer = invoice.vendor_type === 'Composition' || invoice.vendor_type === 'composition'
    const compositionScheme = isCompositionDealer ? 'Yes' : 'No'

    // Check if this is a multi-item invoice
    const lineItems = invoice.line_items || []
    const hasMultipleItems = lineItems.length > 1

    if (hasMultipleItems) {
      // Multi-item invoice: create one row per item
      lineItems.forEach((item: any, index: number) => {
        const itemHSN = item.hsn_code || item.sac_code || hsnCode
        const itemName = item.item_name || item.description || `${itemDescription} ${index + 1}`
        const itemQty = item.quantity || 1
        const itemRate = item.rate || item.unit_price || (item.amount || 0) / itemQty
        const itemAmount = item.amount || (itemQty * itemRate)
        const itemGST = item.gst_amount || (itemAmount * (totalGST / subtotal))
        const itemCGST = igst > 0 ? 0 : itemGST / 2
        const itemSGST = igst > 0 ? 0 : itemGST / 2
        const itemIGST = igst > 0 ? itemGST : 0

        rows.push([
          invoice.invoice_number || '',
          formatDate(invoice.invoice_date),
          formatDate(invoice.due_date),
          invoice.vendor_name || '',
          invoice.gstin || '',
          itemName,
          itemHSN,
          itemQty.toString(),
          itemRate.toFixed(2),
          itemAmount.toFixed(2),
          (itemCGST / itemAmount * 100).toFixed(2),
          itemCGST.toFixed(2),
          (itemSGST / itemAmount * 100).toFixed(2),
          itemSGST.toFixed(2),
          (itemIGST / itemAmount * 100).toFixed(2),
          itemIGST.toFixed(2),
          itemGST.toFixed(2),
          (itemAmount + itemGST).toFixed(2),
          placeOfSupply,
          invoiceType,
          reverseCharge,
          tdsApplicable,
          tdsPercentage.toFixed(2),
          tdsAmount.toFixed(2),
          compositionScheme
        ])
      })
    } else {
      // Single-item invoice (existing logic)
      rows.push([
        invoice.invoice_number || '',
        formatDate(invoice.invoice_date),
        formatDate(invoice.due_date),
        invoice.vendor_name || '',
        invoice.gstin || '',
        itemDescription,
        hsnCode,
        '1', // Quantity
        subtotal.toFixed(2), // Rate
        subtotal.toFixed(2), // Amount
        cgstRate,
        cgst.toFixed(2),
        sgstRate,
        sgst.toFixed(2),
        igstRate,
        igst.toFixed(2),
        totalGST.toFixed(2),
        (invoice.total_amount || 0).toFixed(2),
        placeOfSupply,
        invoiceType,
        reverseCharge,
        tdsApplicable,
        tdsPercentage.toFixed(2),
        tdsAmount.toFixed(2),
        compositionScheme
      ])
    }
  })

  // Combine headers and rows
  const csvContent = [
    headers.join(','),
    ...rows.map((row: any[]) => row.map((cell: any) => `"${cell}"`).join(','))
  ].join('\n')

  // Create blob and download
  const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' })
  const link = document.createElement('a')
  const url = URL.createObjectURL(blob)

  link.setAttribute('href', url)
  link.setAttribute('download', `invoices_quickbooks_india_gst_${new Date().toISOString().split('T')[0]}.csv`)
  link.style.visibility = 'hidden'

  document.body.appendChild(link)
  link.click()
  document.body.removeChild(link)
}

/**
 * Export invoices to Zoho Books CSV format (India GST Compliant)
 */
export async function exportInvoicesToZohoBooksCSV(invoices: any[]) {
  if (invoices.length === 0) {
    alert('No invoices to export')
    return
  }

  // Validate invoices for required GST fields
  const validationErrors: string[] = []
  invoices.forEach((invoice, index) => {
    if (!invoice.invoice_number) {
      validationErrors.push(`Invoice ${index + 1}: Missing invoice number`)
    }
    if (!invoice.vendor_name) {
      validationErrors.push(`Invoice ${index + 1}: Missing vendor name`)
    }
    if (!invoice.total_amount || invoice.total_amount <= 0) {
      validationErrors.push(`Invoice ${index + 1}: Invalid total amount`)
    }
    if (!invoice.invoice_date) {
      validationErrors.push(`Invoice ${index + 1}: Missing invoice date`)
    }
  })

  if (validationErrors.length > 0) {
    alert(`Export validation failed:\n${validationErrors.join('\n')}`)
    return
  }

  // Zoho Books India CSV headers (GST compliant)
  const headers = [
    'Invoice Number',
    'Invoice Date',
    'Due Date',
    'Customer Name',
    'GSTIN',
    'Place of Supply',
    'Item Name',
    'HSN/SAC',
    'Item Type',
    'Quantity',
    'Rate',
    'Discount',
    'Tax Rate',
    'CGST Rate',
    'CGST Amount',
    'SGST Rate',
    'SGST Amount',
    'IGST Rate',
    'IGST Amount',
    'Total GST',
    'Item Total',
    'Invoice Total',
    'GST Treatment',
    'Invoice Type',
    'Reverse Charge (RCM)',
    'TDS Applicable',
    'TDS Percentage',
    'TDS Amount',
    'Composition Scheme'
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
  const rows: any[] = []

  invoices.forEach(invoice => {
    const cgst = invoice.cgst || 0
    const sgst = invoice.sgst || 0
    const igst = invoice.igst || 0
    const totalGST = cgst + sgst + igst
    const subtotal = invoice.subtotal || (invoice.total_amount ? invoice.total_amount - totalGST : 0)

    // Calculate GST rates
    const cgstRate = subtotal > 0 ? ((cgst / subtotal) * 100).toFixed(2) : '0.00'
    const sgstRate = subtotal > 0 ? ((sgst / subtotal) * 100).toFixed(2) : '0.00'
    const igstRate = subtotal > 0 ? ((igst / subtotal) * 100).toFixed(2) : '0.00'
    const overallGSTRate = subtotal > 0 ? ((totalGST / subtotal) * 100).toFixed(2) : '0.00'

    // Determine GST treatment and invoice type
    const hasGSTIN = invoice.gstin && invoice.gstin.trim() !== ''
    const gstTreatment = hasGSTIN ? 'Taxable' : 'Consumer'
    const invoiceType = hasGSTIN ? 'B2B' : 'B2C'

    // Use dynamic HSN/SAC code from database, fallback to default
    const hsnCode = invoice.hsn_code || invoice.sac_code || '9983'
    const placeOfSupply = invoice.place_of_supply || 'Maharashtra'
    const itemType = invoice.supply_type || 'Service' // Goods or Service
    const itemName = itemType === 'Service' ? 'Invoice Processing Service' : 'Goods'
    const reverseCharge = invoice.reverse_charge ? 'Yes' : 'No'
    const tdsApplicable = invoice.tds_amount && invoice.tds_amount > 0 ? 'Yes' : 'No'
    const tdsAmount = invoice.tds_amount || 0
    const tdsPercentage = invoice.tds_percentage || 0
    const isCompositionDealer = invoice.vendor_type === 'Composition' || invoice.vendor_type === 'composition'
    const compositionScheme = isCompositionDealer ? 'Yes' : 'No'

    // Check if this is a multi-item invoice
    const lineItems = invoice.line_items || []
    const hasMultipleItems = lineItems.length > 1

    if (hasMultipleItems) {
      // Multi-item invoice: create one row per item
      lineItems.forEach((item: any, index: number) => {
        const itemHSN = item.hsn_code || item.sac_code || hsnCode
        const itemNameActual = item.item_name || item.description || `${itemName} ${index + 1}`
        const itemTypeActual = item.item_type || itemType
        const itemQty = item.quantity || 1
        const itemRate = item.rate || item.unit_price || (item.amount || 0) / itemQty
        const itemAmount = item.amount || (itemQty * itemRate)
        const itemDiscount = item.discount || 0
        const itemGST = item.gst_amount || (itemAmount * (totalGST / subtotal))
        const itemCGST = igst > 0 ? 0 : itemGST / 2
        const itemSGST = igst > 0 ? 0 : itemGST / 2
        const itemIGST = igst > 0 ? itemGST : 0

        rows.push([
          invoice.invoice_number || '',
          formatDate(invoice.invoice_date),
          formatDate(invoice.due_date),
          invoice.vendor_name || '',
          invoice.gstin || '',
          placeOfSupply,
          itemNameActual,
          itemHSN,
          itemTypeActual,
          itemQty.toString(),
          itemRate.toFixed(2),
          itemDiscount.toFixed(2),
          (itemGST / itemAmount * 100).toFixed(2), // Tax Rate
          (itemCGST / itemAmount * 100).toFixed(2),
          itemCGST.toFixed(2),
          (itemSGST / itemAmount * 100).toFixed(2),
          itemSGST.toFixed(2),
          (itemIGST / itemAmount * 100).toFixed(2),
          itemIGST.toFixed(2),
          itemGST.toFixed(2),
          itemAmount.toFixed(2), // Item Total (before GST)
          (itemAmount + itemGST).toFixed(2),
          gstTreatment,
          invoiceType,
          reverseCharge,
          tdsApplicable,
          tdsPercentage.toFixed(2),
          tdsAmount.toFixed(2),
          compositionScheme
        ])
      })
    } else {
      // Single-item invoice (existing logic)
      rows.push([
        invoice.invoice_number || '',
        formatDate(invoice.invoice_date),
        formatDate(invoice.due_date),
        invoice.vendor_name || '',
        invoice.gstin || '',
        placeOfSupply,
        itemName,
        hsnCode,
        itemType,
        '1', // Quantity
        subtotal.toFixed(2), // Rate
        '0.00', // Discount
        overallGSTRate, // Tax Rate
        cgstRate,
        cgst.toFixed(2),
        sgstRate,
        sgst.toFixed(2),
        igstRate,
        igst.toFixed(2),
        totalGST.toFixed(2),
        subtotal.toFixed(2), // Item Total (before GST)
        (invoice.total_amount || 0).toFixed(2),
        gstTreatment,
        invoiceType,
        reverseCharge,
        tdsApplicable,
        tdsPercentage.toFixed(2),
        tdsAmount.toFixed(2),
        compositionScheme
      ])
    }
  })

  // Combine headers and rows
  const csvContent = [
    headers.join(','),
    ...rows.map((row: any[]) => row.map((cell: any) => `"${cell}"`).join(','))
  ].join('\n')

  // Create blob and download
  const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' })
  const link = document.createElement('a')
  const url = URL.createObjectURL(blob)

  link.setAttribute('href', url)
  link.setAttribute('download', `invoices_zoho_books_india_gst_${new Date().toISOString().split('T')[0]}.csv`)
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
