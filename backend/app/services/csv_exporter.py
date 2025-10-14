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
        Export invoice to plain CSV format
        
        Args:
            invoice_data: Invoice data dictionary
            filename: Optional custom filename
            
        Returns:
            Path to created CSV file
        """
        
        if not filename:
            invoice_num = invoice_data.get('invoice_number', 'INVOICE').replace('/', '_')
            filename = f"Invoice_{invoice_num}_{datetime.now().strftime('%Y%m%d')}.csv"
        
        # Create CSV content
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            
            # ============ HEADER SECTION ============
            writer.writerow(['Invoice Number', invoice_data.get('invoice_number', 'N/A')])
            writer.writerow(['Invoice Date', invoice_data.get('invoice_date', 'N/A')])
            writer.writerow(['Vendor Name', invoice_data.get('vendor_name', 'N/A')])
            writer.writerow(['Vendor GSTIN', invoice_data.get('vendor_gstin', 'N/A')])
            writer.writerow(['Payment Status', invoice_data.get('payment_status', 'unpaid').upper()])
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
        Export multiple invoices to single CSV (for bulk processing)
        
        Args:
            invoices: List of invoice data dictionaries
            filename: Optional custom filename
            
        Returns:
            Path to created CSV file
        """
        
        if not filename:
            filename = f"Invoices_Bulk_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            
            # Headers for bulk export
            headers = [
                'Invoice Number',
                'Invoice Date',
                'Vendor Name',
                'Vendor GSTIN',
                'Subtotal',
                'CGST',
                'SGST',
                'IGST',
                'Total Amount',
                'Payment Status'
            ]
            writer.writerow(headers)
            
            # Write each invoice as a row
            for invoice in invoices:
                # Handle None values properly
                subtotal = invoice.get('subtotal') or 0
                cgst = invoice.get('cgst') or 0
                sgst = invoice.get('sgst') or 0
                igst = invoice.get('igst') or 0
                total_amount = invoice.get('total_amount') or 0
                
                row = [
                    invoice.get('invoice_number', 'N/A'),
                    invoice.get('invoice_date', 'N/A'),
                    invoice.get('vendor_name', 'N/A'),
                    invoice.get('vendor_gstin', 'N/A'),
                    f"{float(subtotal):.2f}",
                    f"{float(cgst):.2f}",
                    f"{float(sgst):.2f}",
                    f"{float(igst):.2f}",
                    f"{float(total_amount):.2f}",
                    str(invoice.get('payment_status', 'unpaid')).upper()
                ]
                writer.writerow(row)
        
        print(f"✅ Bulk CSV exported: {filename} ({len(invoices)} invoices)")
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
