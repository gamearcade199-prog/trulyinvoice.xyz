"""
📊 ACCOUNTANT-FRIENDLY EXCEL EXPORTER
====================================

Light styling ONLY - for import to Tally/Zoho/QuickBooks
NO flashy colors, NO merged cells, FORMULAS included

Target Users: Accountants, SMEs, Bookkeeping Teams
"""

from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from datetime import datetime
from typing import Dict, List, Any


class AccountantExcelExporter:
    """
    Excel exporter optimized for accountants
    - Light styling (minimal colors)
    - Formulas for calculations
    - Import-ready for accounting software
    - Consistent column structure
    """
    
    def __init__(self):
        # MINIMAL STYLING - Only for readability
        self.header_fill = PatternFill(
            start_color='E7E6E6',  # Very light grey (not flashy)
            end_color='E7E6E6',
            fill_type='solid'
        )
        
        self.header_font = Font(
            name='Arial',
            size=10,
            bold=True  # Bold headers only
        )
        
        self.total_font = Font(
            name='Arial',
            size=10,
            bold=True  # Bold totals only
        )
        
        self.normal_font = Font(
            name='Arial',
            size=10
        )
        
        # Thin borders for tables
        self.thin_border = Border(
            left=Side(style='thin'),
            right=Side(style='thin'),
            top=Side(style='thin'),
            bottom=Side(style='thin')
        )
    
    def export_invoice(self, invoice_data: Dict, filename: str = None) -> str:
        """
        Export invoice to accountant-friendly Excel format
        
        Args:
            invoice_data: Invoice data dictionary
            filename: Optional custom filename
            
        Returns:
            Path to created Excel file
        """
        
        if not filename:
            invoice_num = invoice_data.get('invoice_number', 'INVOICE').replace('/', '_')
            filename = f"Invoice_{invoice_num}_{datetime.now().strftime('%Y%m%d')}.xlsx"
        
        # Create workbook
        wb = Workbook()
        
        # Sheet 1: Invoice Data (for import to accounting software)
        ws_data = wb.active
        ws_data.title = "Invoice Data"
        self._build_data_sheet(ws_data, invoice_data)
        
        # Sheet 2: Summary (totals by GST type)
        ws_summary = wb.create_sheet("Summary")
        self._build_summary_sheet(ws_summary, invoice_data)
        
        # Save workbook
        wb.save(filename)
        
        print(f"✅ Accountant-friendly Excel exported: {filename}")
        return filename
    
    def export_invoices_bulk(self, invoices: List[Dict], filename: str = None) -> str:
        """Export multiple invoices to a single Excel file with separate sheets"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"bulk_invoices_accountant_{timestamp}.xlsx"
        
        wb = Workbook()
        
        # Remove default sheet
        wb.remove(wb.active)
        
        # Create summary sheet first
        ws_summary = wb.create_sheet("Summary")
        self._build_bulk_summary_sheet(ws_summary, invoices)
        
        # Create individual sheets for each invoice
        for i, invoice in enumerate(invoices[:10]):  # Limit to 10 invoices per file
            sheet_name = f"Invoice_{i+1}"
            if invoice.get('invoice_number'):
                # Clean sheet name (remove invalid characters)
                clean_name = str(invoice['invoice_number'])[:20].replace('/', '_').replace('\\', '_')
                sheet_name = f"INV_{clean_name}"
            
            ws = wb.create_sheet(sheet_name)
            self._build_data_sheet(ws, invoice)
        
        wb.save(filename)
        print(f"✅ Bulk Excel exported: {filename} ({len(invoices)} invoices)")
        return filename
    
    def _build_bulk_summary_sheet(self, ws, invoices: List[Dict]):
        """Build summary sheet for bulk export"""
        # Header
        ws['A1'] = 'INVOICE SUMMARY REPORT'
        ws['A1'].font = Font(name='Arial', size=14, bold=True)
        
        # Column headers
        headers = ['S.No', 'Invoice Number', 'Date', 'Vendor', 'Amount', 'Status', 'GST']
        for col, header in enumerate(headers, 1):
            cell = ws.cell(row=3, column=col, value=header)
            cell.font = self.header_font
            cell.fill = self.header_fill
        
        # Data rows
        total_amount = 0
        for row, invoice in enumerate(invoices, 4):
            ws.cell(row=row, column=1, value=row-3)
            ws.cell(row=row, column=2, value=invoice.get('invoice_number', 'N/A'))
            ws.cell(row=row, column=3, value=invoice.get('invoice_date', 'N/A'))
            ws.cell(row=row, column=4, value=invoice.get('vendor_name', 'N/A'))
            
            amount = invoice.get('total_amount', 0) or 0
            ws.cell(row=row, column=5, value=amount)
            total_amount += amount
            
            ws.cell(row=row, column=6, value=invoice.get('payment_status', 'N/A'))
            
            gst_total = (invoice.get('cgst', 0) or 0) + (invoice.get('sgst', 0) or 0) + (invoice.get('igst', 0) or 0)
            ws.cell(row=row, column=7, value=gst_total)
        
        # Total row
        total_row = len(invoices) + 5
        ws.cell(row=total_row, column=4, value='TOTAL:').font = self.total_font
        ws.cell(row=total_row, column=5, value=total_amount).font = self.total_font
        
        # Auto-adjust column widths
        for column in ws.columns:
            max_length = 0
            column_letter = get_column_letter(column[0].column)
            for cell in column:
                if cell.value:
                    max_length = max(max_length, len(str(cell.value)))
            ws.column_dimensions[column_letter].width = min(max_length + 2, 30)
    
    def _build_data_sheet(self, ws, data: Dict):
        """Build main data sheet with invoice details"""
        
        # ============ INVOICE HEADER INFO ============
        # Keep it simple - just key-value pairs
        ws['A1'] = 'Invoice Number:'
        ws['B1'] = data.get('invoice_number', 'N/A')
        ws['A2'] = 'Invoice Date:'
        ws['B2'] = data.get('invoice_date', 'N/A')
        ws['A3'] = 'Vendor Name:'
        ws['B3'] = data.get('vendor_name', 'N/A')
        ws['A4'] = 'Vendor GSTIN:'
        ws['B4'] = data.get('vendor_gstin', 'N/A')
        ws['A5'] = 'Payment Status:'
        ws['B5'] = data.get('payment_status', 'unpaid').upper()
        
        # Bold labels only
        for row in range(1, 6):
            ws[f'A{row}'].font = self.total_font
        
        # ============ LINE ITEMS TABLE ============
        # Start table at row 7 (leave space after header)
        table_start_row = 7
        
        # CONSISTENT COLUMN STRUCTURE (CRITICAL for import)
        headers = [
            '#',              # A
            'Description',    # B
            'HSN/SAC',        # C
            'Quantity',       # D
            'Rate',           # E
            'Amount',         # F (formula: =D*E)
            'CGST Rate',      # G
            'CGST Amount',    # H (formula: =F*G/100)
            'SGST Rate',      # I
            'SGST Amount',    # J (formula: =F*I/100)
            'IGST Rate',      # K
            'IGST Amount',    # L (formula: =F*K/100)
            'Line Total'      # M (formula: =F+H+J+L)
        ]
        
        # Write headers
        for col_idx, header in enumerate(headers, start=1):
            cell = ws.cell(row=table_start_row, column=col_idx)
            cell.value = header
            cell.font = self.header_font
            cell.fill = self.header_fill  # Light grey background ONLY
            cell.alignment = Alignment(horizontal='center', vertical='center', wrap_text=True)
            cell.border = self.thin_border
        
        # Set header row height to fit wrapped text
        ws.row_dimensions[table_start_row].height = 30
        
        # Calculate tax rates from invoice totals (for applying to line items)
        # Handle None values by converting to 0
        subtotal = float(data.get('subtotal') or 0)
        cgst_total = float(data.get('cgst') or 0)
        sgst_total = float(data.get('sgst') or 0)
        igst_total = float(data.get('igst') or 0)
        
        # Calculate effective tax rates
        cgst_rate = (cgst_total / subtotal * 100) if subtotal > 0 else 0.0
        sgst_rate = (sgst_total / subtotal * 100) if subtotal > 0 else 0.0
        igst_rate = (igst_total / subtotal * 100) if subtotal > 0 else 0.0
        
        # Write line items with FORMULAS
        line_items = data.get('line_items', [])
        
        if line_items:
            for item_idx, item in enumerate(line_items, start=1):
                row = table_start_row + item_idx
                
                # Column A: Item number
                ws[f'A{row}'] = item_idx
                ws[f'A{row}'].alignment = Alignment(horizontal='center')
                ws[f'A{row}'].border = self.thin_border
                
                # Column B: Description
                ws[f'B{row}'] = item.get('description', 'N/A')
                ws[f'B{row}'].border = self.thin_border
                
                # Column C: HSN/SAC
                ws[f'C{row}'] = item.get('hsn_sac', item.get('hsn', 'N/A'))
                ws[f'C{row}'].alignment = Alignment(horizontal='center')
                ws[f'C{row}'].border = self.thin_border
                
                # Column D: Quantity
                ws[f'D{row}'] = item.get('quantity', 1)
                ws[f'D{row}'].alignment = Alignment(horizontal='right')
                ws[f'D{row}'].border = self.thin_border
                
                # Column E: Rate
                ws[f'E{row}'] = item.get('rate', 0)
                ws[f'E{row}'].number_format = '₹#,##0.00'
                ws[f'E{row}'].alignment = Alignment(horizontal='right')
                ws[f'E{row}'].border = self.thin_border
                
                # Column F: Amount (FORMULA)
                ws[f'F{row}'] = f'=D{row}*E{row}'
                ws[f'F{row}'].number_format = '₹#,##0.00'
                ws[f'F{row}'].alignment = Alignment(horizontal='right')
                ws[f'F{row}'].border = self.thin_border
                
                # Column G: CGST Rate (use calculated rate from invoice totals)
                ws[f'G{row}'] = cgst_rate
                ws[f'G{row}'].number_format = '0.0"%"'
                ws[f'G{row}'].alignment = Alignment(horizontal='right')
                ws[f'G{row}'].border = self.thin_border
                
                # Column H: CGST Amount (FORMULA)
                ws[f'H{row}'] = f'=F{row}*G{row}/100'
                ws[f'H{row}'].number_format = '₹#,##0.00'
                ws[f'H{row}'].alignment = Alignment(horizontal='right')
                ws[f'H{row}'].border = self.thin_border
                
                # Column I: SGST Rate (use calculated rate from invoice totals)
                ws[f'I{row}'] = sgst_rate
                ws[f'I{row}'].number_format = '0.0"%"'
                ws[f'I{row}'].alignment = Alignment(horizontal='right')
                ws[f'I{row}'].border = self.thin_border
                
                # Column J: SGST Amount (FORMULA)
                ws[f'J{row}'] = f'=F{row}*I{row}/100'
                ws[f'J{row}'].number_format = '₹#,##0.00'
                ws[f'J{row}'].alignment = Alignment(horizontal='right')
                ws[f'J{row}'].border = self.thin_border
                
                # Column K: IGST Rate (use calculated rate from invoice totals)
                ws[f'K{row}'] = igst_rate
                ws[f'K{row}'].number_format = '0.0"%"'
                ws[f'K{row}'].alignment = Alignment(horizontal='right')
                ws[f'K{row}'].border = self.thin_border
                
                # Column L: IGST Amount (FORMULA)
                ws[f'L{row}'] = f'=F{row}*K{row}/100'
                ws[f'L{row}'].number_format = '₹#,##0.00'
                ws[f'L{row}'].alignment = Alignment(horizontal='right')
                ws[f'L{row}'].border = self.thin_border
                
                # Column M: Line Total (FORMULA)
                ws[f'M{row}'] = f'=F{row}+H{row}+J{row}+L{row}'
                ws[f'M{row}'].number_format = '₹#,##0.00'
                ws[f'M{row}'].alignment = Alignment(horizontal='right')
                ws[f'M{row}'].border = self.thin_border
            
            # ============ TOTALS ROW (with formulas) ============
            totals_row = table_start_row + len(line_items) + 1
            
            ws[f'E{totals_row}'] = 'TOTALS:'
            ws[f'E{totals_row}'].font = self.total_font
            ws[f'E{totals_row}'].alignment = Alignment(horizontal='right')
            
            # Total Amount (FORMULA)
            ws[f'F{totals_row}'] = f'=SUM(F{table_start_row+1}:F{table_start_row+len(line_items)})'
            ws[f'F{totals_row}'].font = self.total_font
            ws[f'F{totals_row}'].number_format = '₹#,##0.00'
            ws[f'F{totals_row}'].alignment = Alignment(horizontal='right')
            ws[f'F{totals_row}'].border = self.thin_border
            
            # Total CGST (FORMULA)
            ws[f'H{totals_row}'] = f'=SUM(H{table_start_row+1}:H{table_start_row+len(line_items)})'
            ws[f'H{totals_row}'].font = self.total_font
            ws[f'H{totals_row}'].number_format = '₹#,##0.00'
            ws[f'H{totals_row}'].alignment = Alignment(horizontal='right')
            ws[f'H{totals_row}'].border = self.thin_border
            
            # Total SGST (FORMULA)
            ws[f'J{totals_row}'] = f'=SUM(J{table_start_row+1}:J{table_start_row+len(line_items)})'
            ws[f'J{totals_row}'].font = self.total_font
            ws[f'J{totals_row}'].number_format = '₹#,##0.00'
            ws[f'J{totals_row}'].alignment = Alignment(horizontal='right')
            ws[f'J{totals_row}'].border = self.thin_border
            
            # Total IGST (FORMULA)
            ws[f'L{totals_row}'] = f'=SUM(L{table_start_row+1}:L{table_start_row+len(line_items)})'
            ws[f'L{totals_row}'].font = self.total_font
            ws[f'L{totals_row}'].number_format = '₹#,##0.00'
            ws[f'L{totals_row}'].alignment = Alignment(horizontal='right')
            ws[f'L{totals_row}'].border = self.thin_border
            
            # Grand Total (FORMULA)
            ws[f'M{totals_row}'] = f'=SUM(M{table_start_row+1}:M{table_start_row+len(line_items)})'
            ws[f'M{totals_row}'].font = self.total_font
            ws[f'M{totals_row}'].number_format = '₹#,##0.00'
            ws[f'M{totals_row}'].alignment = Alignment(horizontal='right')
            ws[f'M{totals_row}'].border = self.thin_border
        
        # Auto-adjust column widths based on content (professional and smart!)
        self._auto_adjust_column_widths(ws)
    
    def _auto_adjust_column_widths(self, ws):
        """
        Automatically adjust column widths based on content length
        This ensures all content is visible and looks professional
        """
        for column in ws.columns:
            max_length = 0
            column_letter = column[0].column_letter
            
            for cell in column:
                try:
                    # Calculate length of cell value
                    if cell.value:
                        # Convert to string and get length
                        cell_value = str(cell.value)
                        
                        # Handle formulas (show result length, not formula)
                        if cell_value.startswith('='):
                            # For formulas, estimate reasonable width
                            cell_length = 12
                        else:
                            # For regular content, use actual length
                            cell_length = len(cell_value)
                        
                        # Update max length if this cell is longer
                        if cell_length > max_length:
                            max_length = cell_length
                
                except:
                    pass
            
            # Set column width with padding
            # Add 2 characters for padding, minimum width of 8
            adjusted_width = max_length + 2
            
            # Set minimum and maximum widths for usability
            if adjusted_width < 8:
                adjusted_width = 8  # Minimum width
            elif adjusted_width > 50:
                adjusted_width = 50  # Maximum width (for very long descriptions)
            
            # Apply the calculated width
            ws.column_dimensions[column_letter].width = adjusted_width
    
    def _build_summary_sheet(self, ws, data: Dict):
        """Build summary sheet with GST totals"""
        
        ws['A1'] = 'INVOICE SUMMARY'
        ws['A1'].font = Font(size=14, bold=True)
        
        # Basic info
        row = 3
        ws[f'A{row}'] = 'Invoice Number:'
        ws[f'B{row}'] = data.get('invoice_number', 'N/A')
        row += 1
        ws[f'A{row}'] = 'Invoice Date:'
        ws[f'B{row}'] = data.get('invoice_date', 'N/A')
        row += 1
        ws[f'A{row}'] = 'Vendor:'
        ws[f'B{row}'] = data.get('vendor_name', 'N/A')
        row += 2
        
        # Tax summary
        ws[f'A{row}'] = 'TAX BREAKDOWN'
        ws[f'A{row}'].font = self.total_font
        row += 1
        
        ws[f'A{row}'] = 'Subtotal (before tax):'
        ws[f'B{row}'] = float(data.get('subtotal') or 0)
        ws[f'B{row}'].number_format = '₹#,##0.00'
        row += 1
        
        ws[f'A{row}'] = 'CGST:'
        ws[f'B{row}'] = float(data.get('cgst') or 0)
        ws[f'B{row}'].number_format = '₹#,##0.00'
        row += 1
        
        ws[f'A{row}'] = 'SGST:'
        ws[f'B{row}'] = float(data.get('sgst') or 0)
        ws[f'B{row}'].number_format = '₹#,##0.00'
        row += 1
        
        ws[f'A{row}'] = 'IGST:'
        ws[f'B{row}'] = float(data.get('igst') or 0)
        ws[f'B{row}'].number_format = '₹#,##0.00'
        row += 1
        
        ws[f'A{row}'] = 'TOTAL AMOUNT:'
        ws[f'B{row}'] = float(data.get('total_amount') or 0)
        ws[f'A{row}'].font = self.total_font
        ws[f'B{row}'].font = self.total_font
        ws[f'B{row}'].number_format = '₹#,##0.00'
        
        # Auto-adjust column widths for summary sheet too
        self._auto_adjust_column_widths(ws)


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
                'amount': 30000.00,
                'cgst_rate': 9.0,
                'sgst_rate': 9.0,
                'igst_rate': 0.0
            },
            {
                'description': 'Product B - Consulting',
                'hsn_sac': '998315',
                'quantity': 1,
                'rate': 3898.31,
                'amount': 3898.31,
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
    
    exporter = AccountantExcelExporter()
    exporter.export_invoice(sample_invoice, 'Accountant_Invoice_Demo.xlsx')
    
    print("\n✅ Accountant-friendly Excel created!")
    print("Features:")
    print("  - Light grey headers (minimal styling)")
    print("  - Formulas for calculations")
    print("  - Import-ready for Tally/Zoho/QuickBooks")
    print("  - Consistent column structure")
    print("Open 'Accountant_Invoice_Demo.xlsx' to see the format")
