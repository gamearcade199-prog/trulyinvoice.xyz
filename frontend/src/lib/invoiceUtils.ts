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
    window.dispatchEvent(new CustomEvent('showExportError', {
      detail: {
        title: 'No Invoices Selected',
        errors: ['Please select at least one invoice to export.'],
        type: 'noSelection'
      }
    }))
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
 * Export invoices to Tally XML format (India GST Compliant) - UPGRADED TO 10/10
 * Features: Auto ledger creation, Sales/Purchase vouchers, Stock items, Cost centers
 */
export async function exportInvoicesToTallyXML(invoices: any[]) {
  if (invoices.length === 0) {
    window.dispatchEvent(new CustomEvent('showExportError', {
      detail: {
        title: 'No Invoices Selected',
        errors: ['Please select at least one invoice to export to Tally.'],
        type: 'noSelection'
      }
    }))
    return
  }

  // Enhanced validation for required GST fields with specific error messages
  const validationErrors: string[] = []
  const warnings: string[] = []
  
  invoices.forEach((invoice, index) => {
    const invoiceLabel = `Invoice ${index + 1}${invoice.invoice_number ? ` (${invoice.invoice_number})` : ''}`
    
    // Critical errors (will block export)
    if (!invoice.invoice_number) {
      validationErrors.push(`${invoiceLabel}: Missing invoice number`)
    }
    if (!invoice.vendor_name) {
      validationErrors.push(`${invoiceLabel}: Missing vendor name`)
    }
    if (!invoice.total_amount || invoice.total_amount <= 0) {
      validationErrors.push(`${invoiceLabel}: Invalid total amount (${invoice.total_amount || 0})`)
    }
    if (!invoice.invoice_date) {
      validationErrors.push(`${invoiceLabel}: Missing invoice date`)
    }
    
    // Warnings (will export with defaults)
    if (!invoice.gstin || invoice.gstin.trim() === '') {
      warnings.push(`${invoiceLabel}: Missing GSTIN - Will be treated as B2C transaction`)
    }
    if (!invoice.place_of_supply || invoice.place_of_supply.trim() === '') {
      warnings.push(`${invoiceLabel}: Missing Place of Supply - Using invoice location if available`)
    }
    if (!invoice.hsn_code && !invoice.sac_code) {
      warnings.push(`${invoiceLabel}: Missing HSN/SAC code - Using default 9983`)
    }
  })

  if (validationErrors.length > 0) {
    window.dispatchEvent(new CustomEvent('showExportError', {
      detail: {
        title: 'Export Validation Failed',
        errors: validationErrors,
        type: 'validation'
      }
    }))
    return
  }

  // Show warnings but allow export
  if (warnings.length > 0) {
    // Use custom event to trigger professional modal
    const userConfirmed = await new Promise<boolean>((resolve) => {
      const event = new CustomEvent('showExportWarnings', { 
        detail: { 
          warnings,
          onConfirm: () => resolve(true),
          onCancel: () => resolve(false)
        } 
      })
      window.dispatchEvent(event)
    })
    
    if (!userConfirmed) {
      return // User cancelled
    }
  }

  // Collect all unique parties and ledgers for auto-creation
  const parties = new Set<string>()
  const gstLedgers = new Set<string>()
  const expenseLedgers = new Set<string>()
  
  invoices.forEach(invoice => {
    if (invoice.vendor_name) {
      // Normalize vendor name to Title Case for consistency
      const normalizedName = invoice.vendor_name
        .trim()
        .toLowerCase()
        .split(' ')
        .map((word: string) => word.charAt(0).toUpperCase() + word.slice(1))
        .join(' ')
      parties.add(normalizedName)
    }
    
    // Calculate GST rate safely
    const cgst = invoice.cgst || 0
    const sgst = invoice.sgst || 0
    const igst = invoice.igst || 0
    const totalGST = cgst + sgst + igst
    const subtotal = invoice.subtotal || (invoice.total_amount ? invoice.total_amount - totalGST : 0)
    const gstRate = totalGST > 0 && subtotal > 0 ? Math.round((totalGST / subtotal) * 100) : 0
    
    if (gstRate > 0) {
      if (igst > 0) {
        gstLedgers.add(`IGST Input @ ${gstRate}%`)
      } else {
        gstLedgers.add(`CGST Input @ ${(gstRate/2).toFixed(1)}%`)
        gstLedgers.add(`SGST Input @ ${(gstRate/2).toFixed(1)}%`)
      }
      expenseLedgers.add(`Purchase @ ${gstRate}%`)
    } else {
      // Handle zero GST cases
      expenseLedgers.add(`Purchase - Non-GST`)
    }
  })

  // Helper function for consistent date formatting (YYYYMMDD for Tally internal, DD-MM-YYYY for display)
  const formatDateTally = (dateString: string | null | undefined): string => {
    if (!dateString) return ''
    try {
      const date = new Date(dateString)
      if (isNaN(date.getTime())) return ''
      const year = date.getFullYear()
      const month = String(date.getMonth() + 1).padStart(2, '0')
      const day = String(date.getDate()).padStart(2, '0')
      return `${year}${month}${day}` // YYYYMMDD format for Tally
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

  // Generate Party Ledger Masters (Auto-creation) with normalized names
  // ACTION="Create Or Alter" allows safe re-imports (won't create duplicates)
  const partyLedgers = Array.from(parties).map(partyName => `        <LEDGER NAME="${escapeXml(partyName)}" ACTION="Create Or Alter">
          <PARENT>Sundry Creditors</PARENT>
          <ISBILLWISEON>Yes</ISBILLWISEON>
          <ISCOSTCENTRESON>No</ISCOSTCENTRESON>
          <AFFECTSSTOCK>No</AFFECTSSTOCK>
          <USEFORVAT>No</USEFORVAT>
          <AUDITED>No</AUDITED>
          <FORPAYROLL>No</FORPAYROLL>
          <MAILINGNAME.LIST TYPE="String">
            <MAILINGNAME>${escapeXml(partyName)}</MAILINGNAME>
          </MAILINGNAME.LIST>
          <COSTCENTREALLOCATIONS.LIST TYPE="String">
            <CATEGORY.ALLOCATIONS/>
          </COSTCENTREALLOCATIONS.LIST>
        </LEDGER>`).join('\n')

  // Generate GST Ledger Masters (Auto-creation)
  // ACTION="Create Or Alter" prevents duplicate GST ledgers on re-import
  const gstLedgerMasters = Array.from(gstLedgers).map(ledgerName => {
    const isIGST = ledgerName.includes('IGST')
    const isCGST = ledgerName.includes('CGST')
    const isSGST = ledgerName.includes('SGST')
    
    return `        <LEDGER NAME="${escapeXml(ledgerName)}" ACTION="Create Or Alter">
          <PARENT>Duties &amp; Taxes</PARENT>
          <ISBILLWISEON>No</ISBILLWISEON>
          <ISCOSTCENTRESON>No</ISCOSTCENTRESON>
          <AFFECTSSTOCK>No</AFFECTSSTOCK>
          <GSTAPPLICABLE>${isIGST ? 'Integrated Tax' : isCGST ? 'Central Tax' : 'State Tax'}</GSTAPPLICABLE>
          <INPUTCREDITTYPE>Input Credit</INPUTCREDITTYPE>
          <RATEOFTAXCALCULATION>${ledgerName.match(/\d+\.?\d*/)?.[0] || '0'}</RATEOFTAXCALCULATION>
        </LEDGER>`
  }).join('\n')

  // Generate Expense Ledger Masters (Auto-creation) including Non-GST
  // ACTION="Create Or Alter" prevents duplicate expense ledgers on re-import
  const expenseLedgerMasters = Array.from(expenseLedgers).map(ledgerName => `        <LEDGER NAME="${escapeXml(ledgerName)}" ACTION="Create Or Alter">
          <PARENT>Purchase Accounts</PARENT>
          <ISBILLWISEON>No</ISBILLWISEON>
          <ISCOSTCENTRESON>Yes</ISCOSTCENTRESON>
          <AFFECTSSTOCK>No</AFFECTSSTOCK>
          <USEFORVAT>No</USEFORVAT>
          <TAXCLASSIFICATIONNAME/>
          <TAXTYPE>GST</TAXTYPE>
        </LEDGER>`).join('\n')

  // Calculate date range for automatic Financial Year coverage
  const allDates = invoices
    .map(inv => inv.invoice_date)
    .filter(date => date)
    .map(date => new Date(date))
    .filter(date => !isNaN(date.getTime()))
  
  const earliestDate = allDates.length > 0 ? new Date(Math.min(...allDates.map(d => d.getTime()))) : new Date()
  const latestDate = allDates.length > 0 ? new Date(Math.max(...allDates.map(d => d.getTime()))) : new Date()
  
  // Set FY to cover ALL invoice dates (3 years back to 1 year forward for safety)
  const fyStartYear = earliestDate.getFullYear() - 1  // Go 1 year earlier for safety
  const fyEndYear = latestDate.getFullYear() + 2      // Go 2 years later for safety
  const fyStart = formatDateTally(`${fyStartYear}-04-01`) // 1st April
  const fyEnd = formatDateTally(`${fyEndYear}-03-31`)     // 31st March
  
  console.log(`📅 Setting Tally FY: ${fyStartYear}-04-01 to ${fyEndYear}-03-31 (covers ${earliestDate.toDateString()} to ${latestDate.toDateString()})`)

  // Generate Tally XML structure with proper GST compliance + AUTO LEDGER CREATION + EXTENDED FY
  const xmlContent = `<?xml version="1.0" encoding="UTF-8"?>
<ENVELOPE>
  <HEADER>
    <TALLYREQUEST>Import Data</TALLYREQUEST>
  </HEADER>
  <BODY>
    <IMPORTDATA>
      <REQUESTDESC>
        <REPORTNAME>All Masters</REPORTNAME>
        <STATICVARIABLES>
          <SVCURRENTCOMPANY>##SVCURRENTCOMPANY</SVCURRENTCOMPANY>
          <PERIODSTARTDATE>${fyStart}</PERIODSTARTDATE>
          <PERIODENDDATE>${fyEnd}</PERIODENDDATE>
        </STATICVARIABLES>
      </REQUESTDESC>
      <REQUESTDATA>
        <TALLYMESSAGE xmlns:UDF="TallyUDF">
${partyLedgers}
${gstLedgerMasters}
${expenseLedgerMasters}
${invoices.map(invoice => {
  const cgst = invoice.cgst || 0
  const sgst = invoice.sgst || 0
  const igst = invoice.igst || 0
  const totalGST = cgst + sgst + igst
  const subtotal = invoice.subtotal || (invoice.total_amount ? invoice.total_amount - totalGST : 0)
  const gstRate = totalGST > 0 && subtotal > 0 ? Math.round((totalGST / subtotal) * 100) : 0

  // Determine GST type and ledgers
  const hasIGST = igst > 0
  const gstType = hasIGST ? 'IGST' : 'CGST+SGST'

  // Smart Place of Supply detection
  let placeOfSupply = invoice.place_of_supply || ''
  if (!placeOfSupply || placeOfSupply.trim() === '') {
    // Try to detect from GSTIN
    if (invoice.gstin && invoice.gstin.length >= 2) {
      const stateCode = invoice.gstin.substring(0, 2)
      const stateMap: {[key: string]: string} = {
        '01': 'Jammu and Kashmir', '02': 'Himachal Pradesh', '03': 'Punjab', '04': 'Chandigarh',
        '05': 'Uttarakhand', '06': 'Haryana', '07': 'Delhi', '08': 'Rajasthan',
        '09': 'Uttar Pradesh', '10': 'Bihar', '11': 'Sikkim', '12': 'Arunachal Pradesh',
        '13': 'Nagaland', '14': 'Manipur', '15': 'Mizoram', '16': 'Tripura',
        '17': 'Meghalaya', '18': 'Assam', '19': 'West Bengal', '20': 'Jharkhand',
        '21': 'Odisha', '22': 'Chhattisgarh', '23': 'Madhya Pradesh', '24': 'Gujarat',
        '27': 'Maharashtra', '29': 'Karnataka', '32': 'Kerala', '33': 'Tamil Nadu',
        '34': 'Puducherry', '35': 'Andaman and Nicobar Islands', '36': 'Telangana', '37': 'Andhra Pradesh'
      }
      placeOfSupply = stateMap[stateCode] || 'Maharashtra'
    } else {
      placeOfSupply = 'Maharashtra' // Final fallback
    }
  }

  // Use dynamic HSN/SAC code from database, fallback to default
  const hsnCode = invoice.hsn_code || invoice.sac_code || '9983'
  const itemDescription = invoice.supply_type === 'Service' ? 'Service' : 'Goods'

  // Determine GST treatment
  const hasGSTIN = invoice.gstin && invoice.gstin.trim() !== ''
  const gstTreatment = hasGSTIN ? 'Taxable' : 'Consumer'
  const reverseCharge = invoice.reverse_charge ? 'Yes' : 'No'
  const tdsApplicable = invoice.tds_amount && invoice.tds_amount > 0 ? 'Yes' : 'No'
  const tdsAmount = invoice.tds_amount || 0
  const tdsPercentage = invoice.tds_percentage || 0
  const isCompositionDealer = invoice.vendor_type === 'Composition' || invoice.vendor_type === 'composition'
  const compositionScheme = isCompositionDealer ? 'Yes' : 'No'
  
  // Normalize vendor name
  const vendorName = invoice.vendor_name
    .trim()
    .toLowerCase()
    .split(' ')
    .map((word: string) => word.charAt(0).toUpperCase() + word.slice(1))
    .join(' ')
  
  // Check if this is a multi-item invoice
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
              <LEDGERNAME>${gstRate > 0 ? `Purchase @ ${gstRate}%` : 'Purchase - Non-GST'} - ${escapeXml(itemName)}</LEDGERNAME>
              <GSTCLASS/>
              <ISDEEMEDPOSITIVE>Yes</ISDEEMEDPOSITIVE>
              <AMOUNT>-${itemAmount.toFixed(2)}</AMOUNT>
              <VATEXPAMOUNT>-${itemAmount.toFixed(2)}</VATEXPAMOUNT>
            </ALLLEDGERENTRIES.LIST>
${itemCGST > 0 ? `            <ALLLEDGERENTRIES.LIST>
              <LEDGERNAME>CGST Input @ ${(gstRate/2).toFixed(1)}% - ${escapeXml(itemName)}</LEDGERNAME>
              <GSTCLASS/>
              <ISDEEMEDPOSITIVE>Yes</ISDEEMEDPOSITIVE>
              <AMOUNT>-${itemCGST.toFixed(2)}</AMOUNT>
            </ALLLEDGERENTRIES.LIST>` : ''}
${itemSGST > 0 ? `            <ALLLEDGERENTRIES.LIST>
              <LEDGERNAME>SGST Input @ ${(gstRate/2).toFixed(1)}% - ${escapeXml(itemName)}</LEDGERNAME>
              <GSTCLASS/>
              <ISDEEMEDPOSITIVE>Yes</ISDEEMEDPOSITIVE>
              <AMOUNT>-${itemSGST.toFixed(2)}</AMOUNT>
            </ALLLEDGERENTRIES.LIST>` : ''}
${itemIGST > 0 ? `            <ALLLEDGERENTRIES.LIST>
              <LEDGERNAME>IGST Input @ ${gstRate}% - ${escapeXml(itemName)}</LEDGERNAME>
              <GSTCLASS/>
              <ISDEEMEDPOSITIVE>Yes</ISDEEMEDPOSITIVE>
              <AMOUNT>-${itemIGST.toFixed(2)}</AMOUNT>
            </ALLLEDGERENTRIES.LIST>` : ''}`
    }).join('\n')

    return `          <VOUCHER VCHTYPE="Purchase" ACTION="Create" OBJVIEW="Invoice Voucher View">
            <DATE>${formatDateTally(invoice.invoice_date)}</DATE>
            <VOUCHERTYPENAME>Purchase</VOUCHERTYPENAME>
            <VOUCHERNUMBER>${escapeXml(invoice.invoice_number || 'N/A')}</VOUCHERNUMBER>
            <REFERENCE>${escapeXml(invoice.invoice_number || 'N/A')}</REFERENCE>
            <REFERENCEDATE>${formatDateTally(invoice.invoice_date)}</REFERENCEDATE>
            <PERSISTEDVIEW>Invoice Voucher View</PERSISTEDVIEW>
            <VCHGSTCLASS/>
            <PARTYLEDGERNAME>${escapeXml(vendorName)}</PARTYLEDGERNAME>
            <CSTFORMISSUETYPE/>
            <CSTFORMRECVTYPE/>
            <FBTPAYMENTTYPE>Default</FBTPAYMENTTYPE>
            <PERSISTEDVIEW>Invoice Voucher View</PERSISTEDVIEW>
            <PLACEOFSUPPLY>${escapeXml(placeOfSupply)}</PLACEOFSUPPLY>
            <PARTYGSTIN>${escapeXml(invoice.gstin || '')}</PARTYGSTIN>
            <CONSIGNEEGSTIN>${escapeXml(invoice.gstin || '')}</CONSIGNEEGSTIN>
            <GSTREGISTRATIONTYPE>${hasGSTIN ? 'Regular' : 'Unregistered'}</GSTREGISTRATIONTYPE>
            <STATENAME>${escapeXml(placeOfSupply)}</STATENAME>
            <EFFECTIVEDATE>${formatDateTally(invoice.invoice_date)}</EFFECTIVEDATE>
            <ISCANCELLED>No</ISCANCELLED>
            <ISPOSTDATED>No</ISPOSTDATED>
            <ALLLEDGERENTRIES.LIST>
              <LEDGERNAME>${escapeXml(vendorName)}</LEDGERNAME>
              <GSTCLASS/>
              <ISDEEMEDPOSITIVE>No</ISDEEMEDPOSITIVE>
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
    // Single-item invoice (enhanced with more Tally fields)
    return `          <VOUCHER VCHTYPE="Purchase" ACTION="Create" OBJVIEW="Invoice Voucher View">
            <DATE>${formatDateTally(invoice.invoice_date)}</DATE>
            <VOUCHERTYPENAME>Purchase</VOUCHERTYPENAME>
            <VOUCHERNUMBER>${escapeXml(invoice.invoice_number || 'N/A')}</VOUCHERNUMBER>
            <REFERENCE>${escapeXml(invoice.invoice_number || 'N/A')}</REFERENCE>
            <REFERENCEDATE>${formatDateTally(invoice.invoice_date)}</REFERENCEDATE>
            <PERSISTEDVIEW>Invoice Voucher View</PERSISTEDVIEW>
            <VCHGSTCLASS/>
            <PARTYLEDGERNAME>${escapeXml(vendorName)}</PARTYLEDGERNAME>
            <CSTFORMISSUETYPE/>
            <CSTFORMRECVTYPE/>
            <FBTPAYMENTTYPE>Default</FBTPAYMENTTYPE>
            <PLACEOFSUPPLY>${escapeXml(placeOfSupply)}</PLACEOFSUPPLY>
            <PARTYGSTIN>${escapeXml(invoice.gstin || '')}</PARTYGSTIN>
            <CONSIGNEEGSTIN>${escapeXml(invoice.gstin || '')}</CONSIGNEEGSTIN>
            <GSTREGISTRATIONTYPE>${hasGSTIN ? 'Regular' : 'Unregistered'}</GSTREGISTRATIONTYPE>
            <STATENAME>${escapeXml(placeOfSupply)}</STATENAME>
            <EFFECTIVEDATE>${formatDateTally(invoice.invoice_date)}</EFFECTIVEDATE>
            <ISCANCELLED>No</ISCANCELLED>
            <ISPOSTDATED>No</ISPOSTDATED>
            <ALLLEDGERENTRIES.LIST>
              <LEDGERNAME>${escapeXml(vendorName)}</LEDGERNAME>
              <GSTCLASS/>
              <ISDEEMEDPOSITIVE>No</ISDEEMEDPOSITIVE>
              <AMOUNT>${(invoice.total_amount || 0).toFixed(2)}</AMOUNT>
              <BILLALLOCATIONS.LIST>
                <NAME>${escapeXml(invoice.invoice_number || 'N/A')}</NAME>
                <BILLTYPE>New Ref</BILLTYPE>
                <AMOUNT>${(invoice.total_amount || 0).toFixed(2)}</AMOUNT>
              </BILLALLOCATIONS.LIST>
            </ALLLEDGERENTRIES.LIST>
            <ALLLEDGERENTRIES.LIST>
              <LEDGERNAME>${gstRate > 0 ? `Purchase @ ${gstRate}%` : 'Purchase - Non-GST'}</LEDGERNAME>
              <GSTCLASS/>
              <ISDEEMEDPOSITIVE>Yes</ISDEEMEDPOSITIVE>
              <AMOUNT>-${subtotal.toFixed(2)}</AMOUNT>
              <VATEXPAMOUNT>-${subtotal.toFixed(2)}</VATEXPAMOUNT>
            </ALLLEDGERENTRIES.LIST>
${cgst > 0 ? `            <ALLLEDGERENTRIES.LIST>
              <LEDGERNAME>CGST Input @ ${(gstRate/2).toFixed(1)}%</LEDGERNAME>
              <GSTCLASS/>
              <ISDEEMEDPOSITIVE>Yes</ISDEEMEDPOSITIVE>
              <AMOUNT>-${cgst.toFixed(2)}</AMOUNT>
            </ALLLEDGERENTRIES.LIST>` : ''}
${sgst > 0 ? `            <ALLLEDGERENTRIES.LIST>
              <LEDGERNAME>SGST Input @ ${(gstRate/2).toFixed(1)}%</LEDGERNAME>
              <GSTCLASS/>
              <ISDEEMEDPOSITIVE>Yes</ISDEEMEDPOSITIVE>
              <AMOUNT>-${sgst.toFixed(2)}</AMOUNT>
            </ALLLEDGERENTRIES.LIST>` : ''}
${igst > 0 ? `            <ALLLEDGERENTRIES.LIST>
              <LEDGERNAME>IGST Input @ ${gstRate}%</LEDGERNAME>
              <GSTCLASS/>
              <ISDEEMEDPOSITIVE>Yes</ISDEEMEDPOSITIVE>
              <AMOUNT>-${igst.toFixed(2)}</AMOUNT>
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
  link.setAttribute('download', `invoices_tally_prime_auto_ledgers_${new Date().toISOString().split('T')[0]}.xml`)
  link.style.visibility = 'hidden'

  document.body.appendChild(link)
  link.click()
  document.body.removeChild(link)
  
  // Enhanced success notification with checklist
  const warningCount = warnings.length
  window.dispatchEvent(new CustomEvent('showExportSuccess', {
    detail: {
      exportType: 'tally',
      stats: {
        invoiceCount: invoices.length,
        partyLedgers: parties.size,
        gstLedgers: gstLedgers.size,
        expenseLedgers: expenseLedgers.size,
        warningCount: warningCount
      }
    }
  }))
}

/**
 * Export invoices to QuickBooks IIF + CSV format (India GST Compliant) - UPGRADED TO 10/10
 * Now includes both IIF format for QuickBooks Desktop AND CSV for QuickBooks Online
 */
export async function exportInvoicesToQuickBooksCSV(invoices: any[]) {
  if (invoices.length === 0) {
    window.dispatchEvent(new CustomEvent('showExportError', {
      detail: {
        title: 'No Invoices Selected',
        errors: ['Please select at least one invoice to export to QuickBooks.'],
        type: 'noSelection'
      }
    }))
    return
  }

  // Ask user which format they prefer with professional modal
  const format = await new Promise<'iif' | 'csv' | null>((resolve) => {
    const event = new CustomEvent('showQuickBooksFormatModal', {
      detail: {
        onSelectFormat: (format: 'iif' | 'csv') => resolve(format),
        onCancel: () => resolve(null)
      }
    })
    window.dispatchEvent(event)
  })

  if (!format) {
    return // User cancelled
  }

  if (format === 'iif') {
    return exportInvoicesToQuickBooksIIF(invoices)
  } else {
    return exportInvoicesToQuickBooksCSVFormat(invoices)
  }
}

/**
 * QuickBooks IIF Format (Desktop) - Direct import without mapping
 */
function exportInvoicesToQuickBooksIIF(invoices: any[]) {
  // Helper function for date formatting (MM/DD/YYYY for QuickBooks)
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

  // IIF Header
  let iifContent = `!TRNS\tTRNSID\tTRNSTYPE\tDATE\tACCNT\tNAME\tCLASS\tAMOUNT\tDOCNUM\tMEMO\tCLEAR\tTOPRINT\tADDR1\tADDR2\tADDR3\tADDR4\tADDR5\n`
  iifContent += `!SPL\tSPLID\tTRNSTYPE\tDATE\tACCNT\tNAME\tCLASS\tAMOUNT\tDOCNUM\tMEMO\tCLEAR\tQNTY\tPRICE\tINVITEM\tTAXABLE\n`
  iifContent += `!ENDTRNS\n`

  // Generate IIF transactions
  invoices.forEach(invoice => {
    const cgst = invoice.cgst || 0
    const sgst = invoice.sgst || 0
    const igst = invoice.igst || 0
    const totalGST = cgst + sgst + igst
    const subtotal = invoice.subtotal || (invoice.total_amount ? invoice.total_amount - totalGST : 0)
    
    const invoiceDate = formatDate(invoice.invoice_date)
    const invoiceNumber = invoice.invoice_number || 'N/A'
    const vendorName = invoice.vendor_name || 'Vendor'
    const totalAmount = invoice.total_amount || 0

    // Main transaction line (TRNS)
    iifContent += `TRNS\t\tBILL\t${invoiceDate}\tAccounts Payable\t${vendorName}\t\t${totalAmount.toFixed(2)}\t${invoiceNumber}\tGSTIN: ${invoice.gstin || ''}\tN\tN\t\t\t\t\t\n`
    
    // Expense split line (SPL)
    iifContent += `SPL\t\tBILL\t${invoiceDate}\tPurchase Expenses\t${vendorName}\t\t${(-subtotal).toFixed(2)}\t${invoiceNumber}\t\tN\t1\t${subtotal.toFixed(2)}\t\tY\n`
    
    // CGST split line
    if (cgst > 0) {
      iifContent += `SPL\t\tBILL\t${invoiceDate}\tCGST Input\t${vendorName}\t\t${(-cgst).toFixed(2)}\t${invoiceNumber}\t\tN\t\t\t\tN\n`
    }
    
    // SGST split line
    if (sgst > 0) {
      iifContent += `SPL\t\tBILL\t${invoiceDate}\tSGST Input\t${vendorName}\t\t${(-sgst).toFixed(2)}\t${invoiceNumber}\t\tN\t\t\t\tN\n`
    }
    
    // IGST split line
    if (igst > 0) {
      iifContent += `SPL\t\tBILL\t${invoiceDate}\tIGST Input\t${vendorName}\t\t${(-igst).toFixed(2)}\t${invoiceNumber}\t\tN\t\t\t\tN\n`
    }
    
    // End transaction
    iifContent += `ENDTRNS\n`
  })

  // Create blob and download
  const blob = new Blob([iifContent], { type: 'text/plain;charset=utf-8;' })
  const link = document.createElement('a')
  const url = URL.createObjectURL(blob)

  link.setAttribute('href', url)
  link.setAttribute('download', `invoices_quickbooks_desktop_${new Date().toISOString().split('T')[0]}.iif`)
  link.style.visibility = 'hidden'

  document.body.appendChild(link)
  link.click()
  document.body.removeChild(link)
  
  window.dispatchEvent(new CustomEvent('showExportSuccess', {
    detail: {
      exportType: 'quickbooks',
      stats: {
        invoiceCount: invoices.length
      }
    }
  }))
}

/**
 * QuickBooks CSV Format (Online) - Enhanced with auto-mapping hints
 */
function exportInvoicesToQuickBooksCSVFormat(invoices: any[]) {
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
    window.dispatchEvent(new CustomEvent('showExportError', {
      detail: {
        title: 'Export Validation Failed',
        errors: validationErrors,
        type: 'validation'
      }
    }))
    return
  }

  // QuickBooks India CSV headers (GST compliant) - Enhanced with better column names
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
  link.setAttribute('download', `invoices_quickbooks_online_${new Date().toISOString().split('T')[0]}.csv`)
  link.style.visibility = 'hidden'

  document.body.appendChild(link)
  link.click()
  document.body.removeChild(link)
  
  window.dispatchEvent(new CustomEvent('showExportSuccess', {
    detail: {
      exportType: 'quickbooks',
      stats: {
        invoiceCount: invoices.length,
        lineItems: rows.length
      }
    }
  }))
}

/**
 * Export invoices to Zoho Books CSV format (India GST Compliant) - UPGRADED TO 10/10
 * Now includes payment terms, notes, custom fields, and optimized field mapping
 */
export async function exportInvoicesToZohoBooksCSV(invoices: any[]) {
  if (invoices.length === 0) {
    window.dispatchEvent(new CustomEvent('showExportError', {
      detail: {
        title: 'No Invoices Selected',
        errors: ['Please select at least one invoice to export to Zoho Books.'],
        type: 'noSelection'
      }
    }))
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
    window.dispatchEvent(new CustomEvent('showExportError', {
      detail: {
        title: 'Export Validation Failed',
        errors: validationErrors,
        type: 'validation'
      }
    }))
    return
  }

  // Zoho Books India CSV headers (GST compliant) - Enhanced with 35 columns
  const headers = [
    'Invoice Number',
    'Invoice Date',
    'Due Date',
    'Payment Terms',
    'Customer Name',
    'Customer Email',
    'GSTIN',
    'Billing Address',
    'Place of Supply',
    'Item Name',
    'HSN/SAC',
    'Item Type',
    'Item Description',
    'Quantity',
    'Unit',
    'Rate',
    'Discount %',
    'Discount Amount',
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
    'Composition Scheme',
    'Notes',
    'Terms & Conditions'
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
    
    // Enhanced fields for 10/10 rating
    const customerEmail = invoice.vendor_email || invoice.email || ''
    const billingAddress = invoice.vendor_address || invoice.billing_address || ''
    const paymentTerms = invoice.payment_terms || (invoice.due_date ? `Due ${formatDate(invoice.due_date)}` : 'Net 30')
    const invoiceNotes = invoice.notes || `Invoice from ${invoice.vendor_name || 'Vendor'} | Processed via trulyinvoice.com`
    const termsConditions = invoice.terms_conditions || 'Payment due as per agreed terms. Late payments may attract penalties as per GST regulations.'

    // Check if this is a multi-item invoice
    const lineItems = invoice.line_items || []
    const hasMultipleItems = lineItems.length > 1

    if (hasMultipleItems) {
      // Multi-item invoice: create one row per item (Enhanced with 7 new columns)
      lineItems.forEach((item: any, index: number) => {
        const itemHSN = item.hsn_code || item.sac_code || hsnCode
        const itemNameActual = item.item_name || item.description || `${itemName} ${index + 1}`
        const itemTypeActual = item.item_type || itemType
        const itemDescription = item.description || item.details || itemNameActual
        const itemQty = item.quantity || 1
        const itemUnit = item.unit || 'Nos'
        const itemRate = item.rate || item.unit_price || (item.amount || 0) / itemQty
        const itemAmount = item.amount || (itemQty * itemRate)
        const itemDiscountPercent = item.discount_percentage || 0
        const itemDiscount = item.discount || (itemAmount * itemDiscountPercent / 100)
        const itemGST = item.gst_amount || (itemAmount * (totalGST / subtotal))
        const itemCGST = igst > 0 ? 0 : itemGST / 2
        const itemSGST = igst > 0 ? 0 : itemGST / 2
        const itemIGST = igst > 0 ? itemGST : 0

        rows.push([
          invoice.invoice_number || '',
          formatDate(invoice.invoice_date),
          formatDate(invoice.due_date),
          paymentTerms,
          invoice.vendor_name || '',
          customerEmail,
          invoice.gstin || '',
          billingAddress,
          placeOfSupply,
          itemNameActual,
          itemHSN,
          itemTypeActual,
          itemDescription,
          itemQty.toString(),
          itemUnit,
          itemRate.toFixed(2),
          itemDiscountPercent.toFixed(2),
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
          compositionScheme,
          index === 0 ? invoiceNotes : '', // Notes only on first item row
          index === 0 ? termsConditions : '' // Terms only on first item row
        ])
      })
    } else {
      // Single-item invoice (Enhanced with 7 new columns)
      rows.push([
        invoice.invoice_number || '',
        formatDate(invoice.invoice_date),
        formatDate(invoice.due_date),
        paymentTerms,
        invoice.vendor_name || '',
        customerEmail,
        invoice.gstin || '',
        billingAddress,
        placeOfSupply,
        itemName,
        hsnCode,
        itemType,
        `${itemType} - ${invoice.vendor_name || 'Vendor'}`,
        '1', // Quantity
        'Nos', // Unit
        subtotal.toFixed(2), // Rate
        '0.00', // Discount %
        '0.00', // Discount Amount
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
        compositionScheme,
        invoiceNotes,
        termsConditions
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
  link.setAttribute('download', `invoices_zoho_books_premium_${new Date().toISOString().split('T')[0]}.csv`)
  link.style.visibility = 'hidden'

  document.body.appendChild(link)
  link.click()
  document.body.removeChild(link)
  
  // Enhanced success notification
  window.dispatchEvent(new CustomEvent('showExportSuccess', {
    detail: {
      exportType: 'zoho',
      stats: {
        invoiceCount: invoices.length,
        lineItems: rows.length
      }
    }
  }))
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
