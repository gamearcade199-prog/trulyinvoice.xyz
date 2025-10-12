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
        """Create Details sheet with all invoice data"""
        ws = wb.create_sheet("Invoice Details")
        
        # Define headers
        headers = [
            'Invoice Number',
            'Vendor Name',
            'Invoice Date',
            'Due Date',
            'Subtotal',
            'CGST',
            'SGST',
            'IGST',
            'Total GST',
            'Total Amount',
            'Payment Status',
            'Created At'
        ]
        
        # Add headers
        for col_num, header in enumerate(headers, 1):
            cell = ws.cell(row=1, column=col_num)
            cell.value = header
            cell.font = self.header_font
            cell.fill = self.header_fill
            cell.border = self.border_style
            cell.alignment = Alignment(horizontal='center', vertical='center')
        
        # Add data rows
        for row_num, invoice in enumerate(invoices, 2):
            # Invoice Number
            ws.cell(row=row_num, column=1).value = invoice.get('invoice_number', 'N/A')
            
            # Vendor Name
            ws.cell(row=row_num, column=2).value = invoice.get('vendor_name', 'N/A')
            
            # Invoice Date
            ws.cell(row=row_num, column=3).value = invoice.get('invoice_date', 'N/A')
            
            # Due Date
            ws.cell(row=row_num, column=4).value = invoice.get('due_date', 'N/A')
            
            # Subtotal
            cell = ws.cell(row=row_num, column=5)
            cell.value = invoice.get('subtotal', 0)
            cell.number_format = '₹#,##0.00'
            
            # CGST
            cell = ws.cell(row=row_num, column=6)
            cell.value = invoice.get('cgst', 0)
            cell.number_format = '₹#,##0.00'
            
            # SGST
            cell = ws.cell(row=row_num, column=7)
            cell.value = invoice.get('sgst', 0)
            cell.number_format = '₹#,##0.00'
            
            # IGST
            cell = ws.cell(row=row_num, column=8)
            cell.value = invoice.get('igst', 0)
            cell.number_format = '₹#,##0.00'
            
            # Total GST (Formula)
            cell = ws.cell(row=row_num, column=9)
            cell.value = f"=F{row_num}+G{row_num}+H{row_num}"
            cell.number_format = '₹#,##0.00'
            
            # Total Amount
            cell = ws.cell(row=row_num, column=10)
            cell.value = invoice.get('total_amount', 0)
            cell.number_format = '₹#,##0.00'
            cell.font = Font(bold=True)
            
            # Payment Status
            status = invoice.get('payment_status', 'Unpaid')
            cell = ws.cell(row=row_num, column=11)
            cell.value = status
            if status.lower() == 'paid':
                cell.fill = PatternFill(start_color="C6EFCE", fill_type="solid")  # Light green
            else:
                cell.fill = PatternFill(start_color="FFC7CE", fill_type="solid")  # Light red
            
            # Created At
            ws.cell(row=row_num, column=12).value = invoice.get('created_at', 'N/A')
            
            # Apply borders to all cells in row
            for col_num in range(1, len(headers) + 1):
                ws.cell(row=row_num, column=col_num).border = self.border_style
        
        # Add total row
        total_row = len(invoices) + 2
        ws.cell(row=total_row, column=1).value = "TOTAL"
        ws.cell(row=total_row, column=1).font = Font(bold=True, size=12)
        
        # Total formulas
        for col_num, col_letter in [(5, 'E'), (6, 'F'), (7, 'G'), (8, 'H'), (9, 'I'), (10, 'J')]:
            cell = ws.cell(row=total_row, column=col_num)
            cell.value = f"=SUM({col_letter}2:{col_letter}{total_row - 1})"
            cell.number_format = '₹#,##0.00'
            cell.font = Font(bold=True)
            cell.fill = PatternFill(start_color="D9D9D9", fill_type="solid")  # Light gray
            cell.border = self.border_style
        
        # Auto-width columns
        for col_num in range(1, len(headers) + 1):
            column_letter = get_column_letter(col_num)
            max_length = len(headers[col_num - 1])
            
            # Check data length
            for row in ws.iter_rows(min_row=2, max_row=len(invoices) + 1, min_col=col_num, max_col=col_num):
                for cell in row:
                    if cell.value:
                        max_length = max(max_length, len(str(cell.value)))
            
            ws.column_dimensions[column_letter].width = min(max_length + 2, 50)
        
        # Freeze header row
        ws.freeze_panes = 'A2'


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
