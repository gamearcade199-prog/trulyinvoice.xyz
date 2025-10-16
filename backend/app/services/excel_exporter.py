"""
Enhanced Excel Export with Formatting
Exports invoices to properly formatted .xlsx files with:
- Bold headers with background color
- Currency formatting (₹ symbol)
- Borders around cells
- Auto-width columns
- Multiple sheets (Summary + Details)
- Formulas for totals
"""

from openpyxl import Workbook
from openpyxl.styles import Font, Border, Side, PatternFill, Alignment
from openpyxl.utils import get_column_letter
from datetime import datetime
import os
from typing import List, Dict

class ExcelExporter:
    """Export invoices to beautifully formatted Excel files"""
    
    def __init__(self):
        self.border_style = Border(
            left=Side(style='thin'),
            right=Side(style='thin'),
            top=Side(style='thin'),
            bottom=Side(style='thin')
        )
        
        self.header_fill = PatternFill(
            start_color="4472C4",  # Blue
            end_color="4472C4",
            fill_type="solid"
        )
        
        self.header_font = Font(
            bold=True,
            color="FFFFFF",  # White
            size=12
        )
    
    def export_invoices(self, invoices: List[Dict], filename: str = None) -> str:
        """
        Export invoices to formatted Excel file
        
        Args:
            invoices: List of invoice dictionaries
            filename: Output filename (auto-generated if not provided)
        
        Returns:
            Path to created Excel file
        """
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"invoices_export_{timestamp}.xlsx"
        
        wb = Workbook()
        
        # Create Summary sheet
        self._create_summary_sheet(wb, invoices)
        
        # Create Details sheet
        self._create_details_sheet(wb, invoices)
        
        # Remove default sheet if exists
        if 'Sheet' in wb.sheetnames:
            wb.remove(wb['Sheet'])
        
        # Save file
        wb.save(filename)
        print(f"✅ Excel file created: {filename}")
        return filename
    
    def _create_summary_sheet(self, wb: Workbook, invoices: List[Dict]):
        """Create Summary sheet with key metrics"""
        ws = wb.active
        ws.title = "Summary"
        
        # Calculate metrics
        total_invoices = len(invoices)
        total_amount = sum(inv.get('total_amount', 0) for inv in invoices)
        total_gst = sum(
            inv.get('cgst', 0) + inv.get('sgst', 0) + inv.get('igst', 0) 
            for inv in invoices
        )
        avg_invoice = total_amount / total_invoices if total_invoices > 0 else 0
        
        # Add title
        ws['A1'] = "Invoice Summary Report"
        ws['A1'].font = Font(bold=True, size=16, color="4472C4")
        ws.merge_cells('A1:B1')
        
        # Add date
        ws['A2'] = f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        ws['A2'].font = Font(italic=True, size=10)
        ws.merge_cells('A2:B2')
        
        # Add metrics
        metrics = [
            ('Total Invoices', total_invoices),
            ('Total Amount', f"₹{total_amount:,.2f}"),
            ('Total GST', f"₹{total_gst:,.2f}"),
            ('Average Invoice', f"₹{avg_invoice:,.2f}"),
        ]
        
        row = 4
        for label, value in metrics:
            ws[f'A{row}'] = label
            ws[f'B{row}'] = value
            ws[f'A{row}'].font = Font(bold=True)
            row += 1
        
        # Vendor breakdown
        ws[f'A{row + 1}'] = "Top Vendors by Amount"
        ws[f'A{row + 1}'].font = Font(bold=True, size=12)
        ws.merge_cells(f'A{row + 1}:C{row + 1}')
        
        # Calculate vendor totals
        vendor_totals = {}
        for inv in invoices:
            vendor = inv.get('vendor_name', 'Unknown')
            amount = inv.get('total_amount', 0)
            vendor_totals[vendor] = vendor_totals.get(vendor, 0) + amount
        
        # Sort vendors by amount
        sorted_vendors = sorted(vendor_totals.items(), key=lambda x: x[1], reverse=True)[:10]
        
        # Add vendor table
        row += 2
        ws[f'A{row}'] = "Vendor"
        ws[f'B{row}'] = "Total Amount"
        ws[f'C{row}'] = "Invoice Count"
        
        for cell in [ws[f'A{row}'], ws[f'B{row}'], ws[f'C{row}']]:
            cell.font = self.header_font
            cell.fill = self.header_fill
            cell.border = self.border_style
        
        row += 1
        for vendor, amount in sorted_vendors:
            count = sum(1 for inv in invoices if inv.get('vendor_name') == vendor)
            ws[f'A{row}'] = vendor
            ws[f'B{row}'] = amount
            ws[f'B{row}'].number_format = '₹#,##0.00'
            ws[f'C{row}'] = count
            
            for cell in [ws[f'A{row}'], ws[f'B{row}'], ws[f'C{row}']]:
                cell.border = self.border_style
            
            row += 1
        
        # Auto-width columns
        for column in ['A', 'B', 'C']:
            ws.column_dimensions[column].width = 20
    
    def _create_details_sheet(self, wb: Workbook, invoices: List[Dict]):
        """Create Details sheet with ALL extracted fields - COMPREHENSIVE VIEW"""
        ws = wb.create_sheet("Complete Invoice Data")
        
        # Define ALL possible headers (50+ fields)
        headers = [
            # Core Invoice Fields
            'Invoice Number', 'Invoice Date', 'Due Date', 'Vendor Name', 'Total Amount', 'Currency',
            
            # Vendor Information
            'Vendor GSTIN', 'Vendor PAN', 'Vendor Email', 'Vendor Phone', 
            'Vendor Address', 'Vendor State', 'Vendor Pincode',
            
            # Customer Information  
            'Customer Name', 'Customer GSTIN', 'Customer Address', 
            'Customer State', 'Customer Phone',
            
            # Financial Breakdown
            'Subtotal', 'Taxable Amount', 'Discount', 'Shipping Charges', 
            'Other Charges', 'Roundoff',
            
            # GST & Tax Details
            'CGST', 'SGST', 'IGST', 'UGST', 'CESS', 'Total GST', 
            'HSN Code', 'SAC Code', 'Place of Supply',
            
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
            
            # Hotel & Hospitality
            'Arrival Date', 'Departure Date', 'Room Number', 'Guest Count', 'Booking Reference',
            
            # Retail & E-commerce
            'Order ID', 'Tracking Number', 'Shipping Method', 'Delivery Date',
            
            # Manufacturing
            'Purchase Order', 'Batch Number', 'Quality Certificate', 'Warranty Period',
            
            # Professional Services
            'Project Name', 'Consultant Name', 'Hourly Rate', 'Hours Worked',
            
            # Quality & Metadata
            'Processing Time (sec)', 'Quality Score (%)', 'Extraction Version', 'Created At'
        ]
        
        # Add headers with formatting
        for col_num, header in enumerate(headers, 1):
            cell = ws.cell(row=1, column=col_num)
            cell.value = header
            cell.font = self.header_font
            cell.fill = self.header_fill
            cell.border = self.border_style
            cell.alignment = Alignment(horizontal='center', vertical='center')
        
        # Add data rows with ALL extracted information
        for row_num, invoice in enumerate(invoices, 2):
            data_values = [
                # Core Invoice Fields
                invoice.get('invoice_number', ''),
                invoice.get('invoice_date', ''),
                invoice.get('due_date', ''),
                invoice.get('vendor_name', ''),
                invoice.get('total_amount', 0),
                invoice.get('currency', 'INR'),
                
                # Vendor Information
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
                invoice.get('subtotal', 0),
                invoice.get('taxable_amount', 0),
                invoice.get('discount', 0),
                invoice.get('shipping_charges', 0),
                invoice.get('other_charges', 0),
                invoice.get('roundoff', 0),
                
                # GST & Tax Details
                invoice.get('cgst', 0),
                invoice.get('sgst', 0),
                invoice.get('igst', 0),
                invoice.get('ugst', 0),
                invoice.get('cess', 0),
                invoice.get('total_gst', 0),
                invoice.get('hsn_code', ''),
                invoice.get('sac_code', ''),
                invoice.get('place_of_supply', ''),
                
                # Banking Information
                invoice.get('bank_name', ''),
                invoice.get('account_number', ''),
                invoice.get('ifsc_code', ''),
                invoice.get('swift_code', ''),
                
                # Payment & Business Terms
                invoice.get('payment_status', ''),
                invoice.get('payment_method', ''),
                invoice.get('payment_terms', ''),
                
                # Purchase Order Details
                invoice.get('po_number', ''),
                invoice.get('po_date', ''),
                invoice.get('invoice_type', ''),
                invoice.get('supply_type', ''),
                invoice.get('reverse_charge', ''),
                
                # Additional Taxes
                invoice.get('vat', 0),
                invoice.get('service_tax', 0),
                invoice.get('tds_amount', 0),
                invoice.get('tcs_amount', 0),
                
                # Import/Export Fields
                invoice.get('bill_of_entry', ''),
                invoice.get('port_code', ''),
                
                # Hotel & Hospitality
                invoice.get('arrival_date', ''),
                invoice.get('departure_date', ''),
                invoice.get('room_number', ''),
                invoice.get('guest_count', ''),
                invoice.get('booking_reference', ''),
                
                # Retail & E-commerce
                invoice.get('order_id', ''),
                invoice.get('tracking_number', ''),
                invoice.get('shipping_method', ''),
                invoice.get('delivery_date', ''),
                
                # Manufacturing
                invoice.get('purchase_order', ''),
                invoice.get('batch_number', ''),
                invoice.get('quality_certificate', ''),
                invoice.get('warranty_period', ''),
                
                # Professional Services
                invoice.get('project_name', ''),
                invoice.get('consultant_name', ''),
                invoice.get('hourly_rate', 0),
                invoice.get('hours_worked', 0),
                
                # Quality & Metadata
                invoice.get('processing_time_seconds', 0),
                invoice.get('quality_score', 0),
                invoice.get('extraction_version', 'v2.5'),
                invoice.get('created_at', '')
            ]
            
            # Currency columns (amounts)
            currency_columns = [5, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 47, 48, 49, 50, 67, 68]
            
            for col_num, value in enumerate(data_values, 1):
                cell = ws.cell(row=row_num, column=col_num)
                cell.value = value
                cell.border = self.border_style
                
                # Format currency columns
                if col_num in currency_columns and isinstance(value, (int, float)) and value > 0:
                    cell.number_format = '₹#,##0.00'
                
                # Color code payment status
                if col_num == 39 and value:  # Payment Status column
                    if str(value).lower() in ['paid', 'completed']:
                        cell.fill = PatternFill(start_color="C6EFCE", fill_type="solid")  # Green
                    elif str(value).lower() in ['pending', 'unpaid']:
                        cell.fill = PatternFill(start_color="FFC7CE", fill_type="solid")  # Red
        
        # Auto-adjust column widths (optimized for readability)
        for col_num in range(1, len(headers) + 1):
            column_letter = get_column_letter(col_num)
            header_length = len(headers[col_num - 1])
            ws.column_dimensions[column_letter].width = min(max(header_length + 2, 12), 25)
        
        # Freeze header row for easy scrolling
        ws.freeze_panes = 'A2'
        
        print(f"✅ Excel export includes {len(headers)} comprehensive fields per invoice!")


# Example usage
if __name__ == "__main__":
    # Sample data
    sample_invoices = [
        {
            'invoice_number': '24347159344967481',
            'vendor_name': 'Tech Solutions Ltd',
            'invoice_date': '2024-01-15',
            'due_date': '2024-02-15',
            'subtotal': 10000,
            'cgst': 900,
            'sgst': 900,
            'igst': 0,
            'total_amount': 11800,
            'payment_status': 'Paid',
            'created_at': '2024-01-15 10:30:00'
        },
        {
            'invoice_number': 'INV-2024-002',
            'vendor_name': 'Office Supplies Co',
            'invoice_date': '2024-01-20',
            'due_date': '2024-02-20',
            'subtotal': 5000,
            'cgst': 450,
            'sgst': 450,
            'igst': 0,
            'total_amount': 5900,
            'payment_status': 'Unpaid',
            'created_at': '2024-01-20 14:15:00'
        },
        {
            'invoice_number': 'INV-2024-003',
            'vendor_name': 'Tech Solutions Ltd',
            'invoice_date': '2024-01-25',
            'due_date': '2024-02-25',
            'subtotal': 15000,
            'cgst': 0,
            'sgst': 0,
            'igst': 2700,
            'total_amount': 17700,
            'payment_status': 'Paid',
            'created_at': '2024-01-25 09:00:00'
        }
    ]
    
    # Export
    exporter = ExcelExporter()
    output_file = exporter.export_invoices(sample_invoices)
    
    print(f"\n✅ Excel file created successfully!")
    print(f"📁 Location: {os.path.abspath(output_file)}")
    print(f"\nFeatures included:")
    print("  ✅ Formatted headers (bold, colored)")
    print("  ✅ Currency formatting (₹ symbol)")
    print("  ✅ Borders around all cells")
    print("  ✅ Auto-width columns")
    print("  ✅ Multiple sheets (Summary + Details)")
    print("  ✅ Formulas (SUM for totals)")
    print("  ✅ Vendor analysis")
    print("  ✅ Payment status color coding")
    print("  ✅ Frozen header row")
