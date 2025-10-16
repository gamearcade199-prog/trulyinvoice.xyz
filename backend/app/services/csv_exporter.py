"""
📄 RAW CSV EXPORTER - Machine-Readable
======================================

Plain text, no formatting, for automation and ERP integration

Target Users: Developers, ERP/CRM Systems, Automation Scripts
"""

import csv
import io
from datetime import datetime
from typing import Dict, List


class CSVExporter:
    """
    CSV exporter for machine-readable data
    - No formatting whatsoever
    - Plain text, comma-separated
    - Consistent column order (same as Excel)
    - UTF-8 encoding for ₹ symbols
    """
    
    def export_invoice(self, invoice_data: Dict, filename: str = None) -> str:
        """
        Export invoice to comprehensive CSV format with ALL extracted fields
        
        Args:
            invoice_data: Invoice data dictionary
            filename: Optional custom filename
            
        Returns:
            Path to created CSV file
        """
        
        if not filename:
            invoice_num = invoice_data.get('invoice_number', 'INVOICE').replace('/', '_')
            filename = f"Invoice_{invoice_num}_{datetime.now().strftime('%Y%m%d')}.csv"
        
        # Create comprehensive CSV content with ALL fields
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            
            # ============ COMPLETE INVOICE DATA ============
            # Core Invoice Information
            writer.writerow(['Invoice Number', invoice_data.get('invoice_number', '')])
            writer.writerow(['Invoice Date', invoice_data.get('invoice_date', '')])
            writer.writerow(['Due Date', invoice_data.get('due_date', '')])
            writer.writerow(['Total Amount', invoice_data.get('total_amount', 0)])
            writer.writerow(['Currency', invoice_data.get('currency', 'INR')])
            
            # Vendor Information
            writer.writerow(['Vendor Name', invoice_data.get('vendor_name', '')])
            writer.writerow(['Vendor GSTIN', invoice_data.get('vendor_gstin', '')])
            writer.writerow(['Vendor PAN', invoice_data.get('vendor_pan', '')])
            writer.writerow(['Vendor Email', invoice_data.get('vendor_email', '')])
            writer.writerow(['Vendor Phone', invoice_data.get('vendor_phone', '')])
            writer.writerow(['Vendor Address', invoice_data.get('vendor_address', '')])
            writer.writerow(['Vendor State', invoice_data.get('vendor_state', '')])
            writer.writerow(['Vendor Pincode', invoice_data.get('vendor_pincode', '')])
            
            # Customer Information
            writer.writerow(['Customer Name', invoice_data.get('customer_name', '')])
            writer.writerow(['Customer GSTIN', invoice_data.get('customer_gstin', '')])
            writer.writerow(['Customer Address', invoice_data.get('customer_address', '')])
            writer.writerow(['Customer State', invoice_data.get('customer_state', '')])
            writer.writerow(['Customer Phone', invoice_data.get('customer_phone', '')])
            
            # Financial Breakdown
            writer.writerow(['Subtotal', invoice_data.get('subtotal', 0)])
            writer.writerow(['Taxable Amount', invoice_data.get('taxable_amount', 0)])
            writer.writerow(['Discount', invoice_data.get('discount', 0)])
            writer.writerow(['Shipping Charges', invoice_data.get('shipping_charges', 0)])
            writer.writerow(['Other Charges', invoice_data.get('other_charges', 0)])
            writer.writerow(['Roundoff', invoice_data.get('roundoff', 0)])
            
            # GST & Tax Details
            writer.writerow(['CGST', invoice_data.get('cgst', 0)])
            writer.writerow(['SGST', invoice_data.get('sgst', 0)])
            writer.writerow(['IGST', invoice_data.get('igst', 0)])
            writer.writerow(['UGST', invoice_data.get('ugst', 0)])
            writer.writerow(['CESS', invoice_data.get('cess', 0)])
            writer.writerow(['Total GST', invoice_data.get('total_gst', 0)])
            writer.writerow(['HSN Code', invoice_data.get('hsn_code', '')])
            writer.writerow(['SAC Code', invoice_data.get('sac_code', '')])
            writer.writerow(['Place of Supply', invoice_data.get('place_of_supply', '')])
            
            # Banking Information
            writer.writerow(['Bank Name', invoice_data.get('bank_name', '')])
            writer.writerow(['Account Number', invoice_data.get('account_number', '')])
            writer.writerow(['IFSC Code', invoice_data.get('ifsc_code', '')])
            writer.writerow(['SWIFT Code', invoice_data.get('swift_code', '')])
            
            # Payment & Business Terms
            writer.writerow(['Payment Status', invoice_data.get('payment_status', 'pending')])
            writer.writerow(['Payment Method', invoice_data.get('payment_method', '')])
            writer.writerow(['Payment Terms', invoice_data.get('payment_terms', '')])
            
            # Purchase Order Details
            writer.writerow(['PO Number', invoice_data.get('po_number', '')])
            writer.writerow(['PO Date', invoice_data.get('po_date', '')])
            writer.writerow(['Invoice Type', invoice_data.get('invoice_type', '')])
            writer.writerow(['Supply Type', invoice_data.get('supply_type', '')])
            writer.writerow(['Reverse Charge', invoice_data.get('reverse_charge', '')])
            
            # Additional Taxes
            writer.writerow(['VAT', invoice_data.get('vat', 0)])
            writer.writerow(['Service Tax', invoice_data.get('service_tax', 0)])
            writer.writerow(['TDS Amount', invoice_data.get('tds_amount', 0)])
            writer.writerow(['TCS Amount', invoice_data.get('tcs_amount', 0)])
            
            # Import/Export Fields
            writer.writerow(['Bill of Entry', invoice_data.get('bill_of_entry', '')])
            writer.writerow(['Port Code', invoice_data.get('port_code', '')])
            
            # Industry-Specific Fields
            # Hotel & Hospitality
            if invoice_data.get('arrival_date') or invoice_data.get('room_number'):
                writer.writerow(['=== HOTEL & HOSPITALITY ===', ''])
                writer.writerow(['Arrival Date', invoice_data.get('arrival_date', '')])
                writer.writerow(['Departure Date', invoice_data.get('departure_date', '')])
                writer.writerow(['Room Number', invoice_data.get('room_number', '')])
                writer.writerow(['Guest Count', invoice_data.get('guest_count', '')])
                writer.writerow(['Booking Reference', invoice_data.get('booking_reference', '')])
            
            # Retail & E-commerce
            if invoice_data.get('order_id') or invoice_data.get('tracking_number'):
                writer.writerow(['=== RETAIL & E-COMMERCE ===', ''])
                writer.writerow(['Order ID', invoice_data.get('order_id', '')])
                writer.writerow(['Tracking Number', invoice_data.get('tracking_number', '')])
                writer.writerow(['Shipping Method', invoice_data.get('shipping_method', '')])
                writer.writerow(['Delivery Date', invoice_data.get('delivery_date', '')])
            
            # Manufacturing
            if invoice_data.get('purchase_order') or invoice_data.get('batch_number'):
                writer.writerow(['=== MANUFACTURING ===', ''])
                writer.writerow(['Purchase Order', invoice_data.get('purchase_order', '')])
                writer.writerow(['Batch Number', invoice_data.get('batch_number', '')])
                writer.writerow(['Quality Certificate', invoice_data.get('quality_certificate', '')])
                writer.writerow(['Warranty Period', invoice_data.get('warranty_period', '')])
            
            # Professional Services
            if invoice_data.get('project_name') or invoice_data.get('consultant_name'):
                writer.writerow(['=== PROFESSIONAL SERVICES ===', ''])
                writer.writerow(['Project Name', invoice_data.get('project_name', '')])
                writer.writerow(['Consultant Name', invoice_data.get('consultant_name', '')])
                writer.writerow(['Hourly Rate', invoice_data.get('hourly_rate', 0)])
                writer.writerow(['Hours Worked', invoice_data.get('hours_worked', 0)])
            
            # Quality & Metadata
            writer.writerow(['=== EXTRACTION QUALITY ===', ''])
            writer.writerow(['Processing Time (seconds)', invoice_data.get('processing_time_seconds', 0)])
            writer.writerow(['Quality Score (%)', invoice_data.get('quality_score', 0)])
            writer.writerow(['Extraction Version', invoice_data.get('extraction_version', 'v2.5')])
            writer.writerow(['Data Source', invoice_data.get('data_source', 'gemini-2.5-flash')])
            
            # Empty row before line items
            writer.writerow(['', ''])
            
            # ============ LINE ITEMS SECTION ============
            writer.writerow([])  # Blank row separator
            
            # ============ LINE ITEMS ============
            # CONSISTENT COLUMN ORDER (same as Excel)
            headers = [
                '#',
                'Description',
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
                'Line Total'
            ]
            writer.writerow(headers)
            
            # Write line items (calculated values, no formulas)
            line_items = invoice_data.get('line_items', [])
            for idx, item in enumerate(line_items, start=1):
                qty = float(item.get('quantity', 1))
                rate = float(item.get('rate', 0))
                amount = qty * rate
                
                cgst_rate = float(item.get('cgst_rate', 0.0))  # Default 0% - only if present
                sgst_rate = float(item.get('sgst_rate', 0.0))  # Default 0% - only if present
                igst_rate = float(item.get('igst_rate', 0.0))
                
                cgst_amount = amount * cgst_rate / 100
                sgst_amount = amount * sgst_rate / 100
                igst_amount = amount * igst_rate / 100
                
                line_total = amount + cgst_amount + sgst_amount + igst_amount
                
                row = [
                    idx,
                    item.get('description', 'N/A'),
                    item.get('hsn_sac', item.get('hsn', 'N/A')),
                    f"{qty:.2f}",
                    f"{rate:.2f}",
                    f"{amount:.2f}",
                    f"{cgst_rate:.1f}",
                    f"{cgst_amount:.2f}",
                    f"{sgst_rate:.1f}",
                    f"{sgst_amount:.2f}",
                    f"{igst_rate:.1f}",
                    f"{igst_amount:.2f}",
                    f"{line_total:.2f}"
                ]
                writer.writerow(row)
            
            # ============ TOTALS ROW ============
            writer.writerow([])  # Blank row
            
            # Handle None values properly
            subtotal = invoice_data.get('subtotal') or 0
            cgst = invoice_data.get('cgst') or 0
            sgst = invoice_data.get('sgst') or 0
            igst = invoice_data.get('igst') or 0
            total_amount = invoice_data.get('total_amount') or 0
            
            writer.writerow([
                '',
                '',
                '',
                '',
                'TOTALS:',
                f"{float(subtotal):.2f}",
                '',
                f"{float(cgst):.2f}",
                '',
                f"{float(sgst):.2f}",
                '',
                f"{float(igst):.2f}",
                f"{float(total_amount):.2f}"
            ])
        
        print(f"✅ Raw CSV exported: {filename}")
        return filename
    
    def export_bulk_invoices(self, invoices: List[Dict], filename: str = None) -> str:
        """
        Export multiple invoices to single comprehensive CSV (for bulk processing)
        
        Args:
            invoices: List of invoice data dictionaries
            filename: Optional custom filename
            
        Returns:
            Path to created CSV file
        """
        
        if not filename:
            filename = f"Invoices_Bulk_Comprehensive_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            
            # Comprehensive headers for bulk export (ALL fields)
            headers = [
                # Core Invoice Information
                'Invoice Number', 'Invoice Date', 'Due Date', 'Total Amount', 'Currency',
                
                # Vendor Information
                'Vendor Name', 'Vendor GSTIN', 'Vendor PAN', 'Vendor Email', 'Vendor Phone',
                'Vendor Address', 'Vendor State', 'Vendor Pincode',
                
                # Customer Information
                'Customer Name', 'Customer GSTIN', 'Customer Address', 'Customer State', 'Customer Phone',
                
                # Financial Breakdown
                'Subtotal', 'Taxable Amount', 'Discount', 'Shipping Charges', 'Other Charges', 'Roundoff',
                
                # GST & Tax Details
                'CGST', 'SGST', 'IGST', 'UGST', 'CESS', 'Total GST', 'HSN Code', 'SAC Code', 'Place of Supply',
                
                # Banking Information
                'Bank Name', 'Account Number', 'IFSC Code', 'SWIFT Code',
                
                # Payment & Business Terms
                'Payment Status', 'Payment Method', 'Payment Terms',
                
                # Purchase Order Details
                'PO Number', 'PO Date', 'Invoice Type', 'Supply Type', 'Reverse Charge',
                
                # Additional Taxes
                'VAT', 'Service Tax', 'TDS Amount', 'TCS Amount',
                
                # Import/Export Fields
                'Bill of Entry', 'Port Code',
                
                # Industry-Specific Fields
                'Arrival Date', 'Departure Date', 'Room Number', 'Guest Count', 'Booking Reference',
                'Order ID', 'Tracking Number', 'Shipping Method', 'Delivery Date',
                'Purchase Order', 'Batch Number', 'Quality Certificate', 'Warranty Period',
                'Project Name', 'Consultant Name', 'Hourly Rate', 'Hours Worked',
                
                # Quality & Metadata
                'Processing Time (seconds)', 'Quality Score (%)', 'Extraction Version', 'Data Source'
            ]
            writer.writerow(headers)
            
            # Write each invoice as a row with ALL fields
            for invoice in invoices:
                # Handle None values properly and create comprehensive row
                row = [
                    # Core Invoice Information
                    invoice.get('invoice_number', ''),
                    invoice.get('invoice_date', ''),
                    invoice.get('due_date', ''),
                    f"{float(invoice.get('total_amount', 0)):.2f}",
                    invoice.get('currency', 'INR'),
                    
                    # Vendor Information
                    invoice.get('vendor_name', ''),
                    invoice.get('vendor_gstin', ''),
                    invoice.get('vendor_pan', ''),
                    invoice.get('vendor_email', ''),
                    invoice.get('vendor_phone', ''),
                    invoice.get('vendor_address', ''),
                    invoice.get('vendor_state', ''),
                    invoice.get('vendor_pincode', ''),
                    
                    # Customer Information
                    invoice.get('customer_name', ''),
                    invoice.get('customer_gstin', ''),
                    invoice.get('customer_address', ''),
                    invoice.get('customer_state', ''),
                    invoice.get('customer_phone', ''),
                    
                    # Financial Breakdown
                    f"{float(invoice.get('subtotal', 0)):.2f}",
                    f"{float(invoice.get('taxable_amount', 0)):.2f}",
                    f"{float(invoice.get('discount', 0)):.2f}",
                    f"{float(invoice.get('shipping_charges', 0)):.2f}",
                    f"{float(invoice.get('other_charges', 0)):.2f}",
                    f"{float(invoice.get('roundoff', 0)):.2f}",
                    
                    # GST & Tax Details
                    f"{float(invoice.get('cgst', 0)):.2f}",
                    f"{float(invoice.get('sgst', 0)):.2f}",
                    f"{float(invoice.get('igst', 0)):.2f}",
                    f"{float(invoice.get('ugst', 0)):.2f}",
                    f"{float(invoice.get('cess', 0)):.2f}",
                    f"{float(invoice.get('total_gst', 0)):.2f}",
                    invoice.get('hsn_code', ''),
                    invoice.get('sac_code', ''),
                    invoice.get('place_of_supply', ''),
                    
                    # Banking Information
                    invoice.get('bank_name', ''),
                    invoice.get('account_number', ''),
                    invoice.get('ifsc_code', ''),
                    invoice.get('swift_code', ''),
                    
                    # Payment & Business Terms
                    invoice.get('payment_status', 'pending'),
                    invoice.get('payment_method', ''),
                    invoice.get('payment_terms', ''),
                    
                    # Purchase Order Details
                    invoice.get('po_number', ''),
                    invoice.get('po_date', ''),
                    invoice.get('invoice_type', ''),
                    invoice.get('supply_type', ''),
                    invoice.get('reverse_charge', ''),
                    
                    # Additional Taxes
                    f"{float(invoice.get('vat', 0)):.2f}",
                    f"{float(invoice.get('service_tax', 0)):.2f}",
                    f"{float(invoice.get('tds_amount', 0)):.2f}",
                    f"{float(invoice.get('tcs_amount', 0)):.2f}",
                    
                    # Import/Export Fields
                    invoice.get('bill_of_entry', ''),
                    invoice.get('port_code', ''),
                    
                    # Industry-Specific Fields
                    invoice.get('arrival_date', ''),
                    invoice.get('departure_date', ''),
                    invoice.get('room_number', ''),
                    invoice.get('guest_count', ''),
                    invoice.get('booking_reference', ''),
                    invoice.get('order_id', ''),
                    invoice.get('tracking_number', ''),
                    invoice.get('shipping_method', ''),
                    invoice.get('delivery_date', ''),
                    invoice.get('purchase_order', ''),
                    invoice.get('batch_number', ''),
                    invoice.get('quality_certificate', ''),
                    invoice.get('warranty_period', ''),
                    invoice.get('project_name', ''),
                    invoice.get('consultant_name', ''),
                    f"{float(invoice.get('hourly_rate', 0)):.2f}",
                    f"{float(invoice.get('hours_worked', 0)):.2f}",
                    
                    # Quality & Metadata
                    f"{float(invoice.get('processing_time_seconds', 0)):.2f}",
                    f"{float(invoice.get('quality_score', 0)):.1f}",
                    invoice.get('extraction_version', 'v2.5'),
                    invoice.get('data_source', 'gemini-2.5-flash')
                ]
                writer.writerow(row)
        
        print(f"✅ Comprehensive Bulk CSV exported: {filename} ({len(invoices)} invoices)")
        return filename


# ============ USAGE EXAMPLE ============
if __name__ == "__main__":
    # Sample invoice data
    sample_invoice = {
        'invoice_number': 'IN67/2025-26',
        'invoice_date': '2025-06-04',
        'vendor_name': 'INNOVATION',
        'vendor_gstin': '18AABCI4851C1ZB',
        'line_items': [
            {
                'description': 'Product A - Professional Services',
                'hsn_sac': '998314',
                'quantity': 2,
                'rate': 15000.00,
                'cgst_rate': 9.0,
                'sgst_rate': 9.0,
                'igst_rate': 0.0
            },
            {
                'description': 'Product B - Consulting',
                'hsn_sac': '998315',
                'quantity': 1,
                'rate': 3898.31,
                'cgst_rate': 9.0,
                'sgst_rate': 9.0,
                'igst_rate': 0.0
            }
        ],
        'subtotal': 33898.31,
        'cgst': 3050.85,
        'sgst': 3050.85,
        'igst': 0,
        'total_amount': 40000.00,
        'payment_status': 'unpaid'
    }
    
    exporter = CSVExporter()
    exporter.export_invoice(sample_invoice, 'Raw_Invoice_Demo.csv')
    
    print("\n✅ Raw CSV created!")
    print("Features:")
    print("  - Plain text, no formatting")
    print("  - Comma-separated values")
    print("  - UTF-8 encoding for ₹ symbols")
    print("  - Consistent column order (same as Excel)")
    print("  - Perfect for bulk processing and ERP import")
    print("Open 'Raw_Invoice_Demo.csv' to see the format")
