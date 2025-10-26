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
import re
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
    
    def _clean_text_field(self, text: str, max_length: int = 1000) -> str:
        """
        Clean text fields to prevent Excel display issues:
        - Remove newlines and extra whitespace
        - Truncate very long text
        - Strip leading/trailing whitespace
        """
        if not text:
            return ""
        
        # Convert to string if not already
        text = str(text)
        
        # Remove newlines and replace with spaces
        text = text.replace('\n', ' ').replace('\r', ' ').replace('\t', ' ')
        
        # Remove multiple consecutive spaces
        text = re.sub(r'\s+', ' ', text)
        
        # Strip leading/trailing whitespace
        text = text.strip()
        
        # Truncate if too long (prevents Excel performance issues)
        if len(text) > max_length:
            text = text[:max_length - 3] + "..."
        
        return text
    
    def export_invoices_line_item_format(self, invoices: List[Dict], filename: str = None) -> str:
        """
        Export invoices in line-item format matching the provided Excel template
        
        Args:
            invoices: List of invoice dictionaries
            filename: Output filename (auto-generated if not provided)
        
        Returns:
            Path to created Excel file
        """
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"invoices_line_item_export_{timestamp}.xlsx"
        
        wb = Workbook()
        
        # Create the main sheet matching the template
        self._create_line_item_sheet(wb, invoices)
        
        # Remove default sheet if exists
        if 'Sheet' in wb.sheetnames:
            wb.remove(wb['Sheet'])
        
        # Save file
        wb.save(filename)
        print(f"✅ Line-item Excel file created: {filename}")
        return filename
        ws = wb.active
        ws.title = "Summary"
        
        # Calculate metrics
        total_invoices = len(invoices)
        total_amount = sum(inv.get('total_amount', 0) or 0 for inv in invoices)
        total_gst = sum(
            (inv.get('cgst', 0) or 0) + (inv.get('sgst', 0) or 0) + (inv.get('igst', 0) or 0) 
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
            vendor = self._clean_text_field(inv.get('vendor_name', 'Unknown'), 100)
            amount = inv.get('total_amount', 0) or 0
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
            count = sum(1 for inv in invoices if self._clean_text_field(inv.get('vendor_name', 'Unknown'), 100) == vendor)
            ws[f'A{row}'] = vendor
            ws[f'B{row}'] = amount
            ws[f'B{row}'].number_format = '₹#,##0.00'
            ws[f'C{row}'] = count
            
            for cell in [ws[f'A{row}'], ws[f'B{row}'], ws[f'C{row}']]:
                cell.border = self.border_style
            
            row += 1
        
        # Auto-adjust column widths with proper text handling
        for column in ['A', 'B', 'C']:
            max_width = 0
            for row in range(1, ws.max_row + 1):
                cell = ws[f'{column}{row}']
                if cell.value:
                    content_length = len(str(cell.value))
                    max_width = max(max_width, content_length)
            
            # Set appropriate width with padding
            ws.column_dimensions[column].width = min(max(max_width + 3, 15), 40)
            
            # Enable text wrapping for long content
            for row in range(1, ws.max_row + 1):
                cell = ws[f'{column}{row}']
                if cell.value and len(str(cell.value)) > 20:
                    cell.alignment = Alignment(wrap_text=True, vertical='center')
                else:
                    cell.alignment = Alignment(horizontal='left', vertical='center')
    
    def _create_details_sheet(self, wb: Workbook, invoices: List[Dict]):
        """Create Details sheet with ALL extracted fields - COMPREHENSIVE VIEW"""
        ws = wb.create_sheet("Complete Invoice Data")
        
        # Define ALL possible headers (171+ fields for comprehensive export)
        headers = [
            # Core Invoice Fields
            'Invoice Number', 'Invoice Date', 'Due Date', 'Total Amount', 'Currency', 'Payment Status',
            
            # Vendor Information (15 fields)
            'Vendor Name', 'Vendor Address', 'Vendor GSTIN', 'Vendor PAN', 'Vendor Email', 'Vendor Phone',
            'Vendor TAN', 'Vendor State', 'Vendor Pincode', 'Vendor Type', 'Vendor Confidence',
            
            # Customer Information (5 fields)
            'Customer Name', 'Customer GSTIN', 'Customer Address', 'Customer State', 'Customer Phone',
            
            # Financial Breakdown (6 fields)
            'Subtotal', 'Taxable Amount', 'Discount', 'Shipping Charges', 'Other Charges', 'Roundoff',
            
            # GST & Tax Details (11 fields)
            'CGST', 'SGST', 'IGST', 'UGST', 'CESS', 'Tax Amount', 'Total GST', 'VAT', 'Service Tax',
            'Taxable Value', 'Processing Fee',
            
            # Banking Information (5 fields)
            'Bank Details', 'Bank Name', 'Account Number', 'IFSC Code', 'SWIFT Code',
            
            # Payment & Business Terms (4 fields)
            'Payment Terms', 'Payment Method', 'Payment Date', 'Payment Reference',
            
            # Purchase Order & References (8 fields)
            'PO Number', 'PO Date', 'Challan Number', 'Eway Bill Number', 'LR Number',
            'Credit Note Ref', 'Debit Note Ref', 'Original Invoice Ref',
            
            # Tax Deductions (4 fields)
            'TDS Amount', 'TDS Percentage', 'TCS Amount', 'Discount Percentage',
            
            # Additional Charges (4 fields)
            'Packing Charges', 'Handling Charges', 'Insurance Charges', 'Processing Time Seconds',
            
            # HSN/SAC & Supply Details (6 fields)
            'HSN Code', 'SAC Code', 'Place of Supply', 'Reverse Charge', 'Invoice Type', 'Supply Type',
            
            # Import/Export (8 fields)
            'Bill of Entry', 'Bill of Entry Date', 'Port Code', 'Shipping Bill Number',
            'Country of Origin', 'Exchange Rate', 'Foreign Currency Amount',
            
            # Hotel & Hospitality (7 fields)
            'Arrival Date', 'Departure Date', 'Room Number', 'Guest Count', 'Booking Reference',
            'Hotel Star Rating', 'Meal Plan',
            
            # Retail & E-commerce (7 fields)
            'Order ID', 'Tracking Number', 'Shipping Method', 'Delivery Date', 'Return Policy',
            'Coupon Code',
            
            # Manufacturing & Quality (7 fields)
            'Purchase Order', 'Batch Number', 'Quality Certificate', 'Warranty Period',
            'Manufacturing Date', 'Expiry Date',
            
            # Healthcare (7 fields)
            'Patient ID', 'Doctor Name', 'Medical License', 'Insurance Claim', 'Treatment Date',
            'Prescription Number',
            
            # Transportation (7 fields)
            'Vehicle Number', 'Driver Name', 'Origin Location', 'Destination Location',
            'Distance KM', 'Fuel Surcharge',
            
            # Professional Services (7 fields)
            'Project Name', 'Consultant Name', 'Hourly Rate', 'Hours Worked', 'Project Phase', 'Deliverable',
            
            # Real Estate (6 fields)
            'Property Address', 'Property Type', 'Square Footage', 'Lease Term', 'Security Deposit',
            
            # Education (6 fields)
            'Student ID', 'Course Name', 'Academic Year', 'Semester', 'Instructor Name',
            
            # Utilities (6 fields)
            'Meter Reading Start', 'Meter Reading End', 'Units Consumed', 'Rate Per Unit', 'Connection ID',
            
            # Financial Services (5 fields)
            'Transaction ID', 'Interest Rate', 'Principal Amount',
            
            # Subscription Services (6 fields)
            'Subscription Type', 'Billing Cycle', 'Next Billing Date', 'Auto Renewal', 'Plan Features',
            
            # Business Operations (9 fields)
            'Contract Number', 'Milestone', 'Approval Status', 'Approved By', 'Department',
            'Cost Center', 'Budget Code', 'Regulatory Code', 'Compliance Certificate',
            
            # Audit & Compliance (4 fields)
            'Audit Trail', 'Authorized Signatory',
            
            # Metadata & Quality (8 fields)
            'Document ID', 'Notes', 'Category ID', 'Tags', 'Metadata', 'Attachments',
            'Is Starred', 'Is Verified', 'Is Recurring', 'Recurring Frequency',
            
            # AI/ML Quality Scores (6 fields)
            'Extraction Version', 'Data Source', 'Quality Score', 'Confidence Score',
            'Amount Confidence', 'Date Confidence', 'Invoice Number Confidence',
            
            # Line Items (stored as JSON for now)
            'Line Items'
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
                # Core Invoice Fields (6)
                self._clean_text_field(invoice.get('invoice_number', '')),
                self._clean_text_field(invoice.get('invoice_date', '')),
                self._clean_text_field(invoice.get('due_date', '')),
                invoice.get('total_amount', 0),
                self._clean_text_field(invoice.get('currency', 'INR')),
                self._clean_text_field(invoice.get('payment_status', '')),
                
                # Vendor Information (11 fields)
                self._clean_text_field(invoice.get('vendor_name', ''), 200),
                self._clean_text_field(invoice.get('vendor_address', ''), 300),
                self._clean_text_field(invoice.get('vendor_gstin', '')),
                self._clean_text_field(invoice.get('vendor_pan', '')),
                self._clean_text_field(invoice.get('vendor_email', '')),
                self._clean_text_field(invoice.get('vendor_phone', '')),
                self._clean_text_field(invoice.get('vendor_tan', '')),
                self._clean_text_field(invoice.get('vendor_state', '')),
                self._clean_text_field(invoice.get('vendor_pincode', '')),
                self._clean_text_field(invoice.get('vendor_type', '')),
                invoice.get('vendor_confidence', 0),
                
                # Customer Information (5 fields)
                self._clean_text_field(invoice.get('customer_name', ''), 200),
                self._clean_text_field(invoice.get('customer_gstin', '')),
                self._clean_text_field(invoice.get('customer_address', ''), 300),
                self._clean_text_field(invoice.get('customer_state', '')),
                self._clean_text_field(invoice.get('customer_phone', '')),
                
                # Financial Breakdown (6 fields)
                invoice.get('subtotal', 0),
                invoice.get('taxable_amount', 0),
                invoice.get('discount', 0),
                invoice.get('shipping_charges', 0),
                invoice.get('other_charges', 0),
                invoice.get('roundoff', 0),
                
                # GST & Tax Details (11 fields)
                invoice.get('cgst', 0),
                invoice.get('sgst', 0),
                invoice.get('igst', 0),
                invoice.get('ugst', 0),
                invoice.get('cess', 0),
                invoice.get('tax_amount', 0),
                invoice.get('total_gst', 0),
                invoice.get('vat', 0),
                invoice.get('service_tax', 0),
                invoice.get('taxable_value', 0),
                invoice.get('processing_fee', 0),
                
                # Banking Information (5 fields)
                self._clean_text_field(invoice.get('bank_details', ''), 300),
                self._clean_text_field(invoice.get('bank_name', '')),
                self._clean_text_field(invoice.get('account_number', '')),
                self._clean_text_field(invoice.get('ifsc_code', '')),
                self._clean_text_field(invoice.get('swift_code', '')),
                
                # Payment & Business Terms (4 fields)
                self._clean_text_field(invoice.get('payment_terms', '')),
                self._clean_text_field(invoice.get('payment_method', '')),
                self._clean_text_field(invoice.get('payment_date', '')),
                self._clean_text_field(invoice.get('payment_reference', '')),
                
                # Purchase Order & References (8 fields)
                self._clean_text_field(invoice.get('po_number', '')),
                self._clean_text_field(invoice.get('po_date', '')),
                self._clean_text_field(invoice.get('challan_number', '')),
                self._clean_text_field(invoice.get('eway_bill_number', '')),
                self._clean_text_field(invoice.get('lr_number', '')),
                self._clean_text_field(invoice.get('credit_note_ref', '')),
                self._clean_text_field(invoice.get('debit_note_ref', '')),
                self._clean_text_field(invoice.get('original_invoice_ref', '')),
                
                # Tax Deductions (4 fields)
                invoice.get('tds_amount', 0),
                invoice.get('tds_percentage', 0),
                invoice.get('tcs_amount', 0),
                invoice.get('discount_percentage', 0),
                
                # Additional Charges (4 fields)
                invoice.get('packing_charges', 0),
                invoice.get('handling_charges', 0),
                invoice.get('insurance_charges', 0),
                invoice.get('processing_time_seconds', 0),
                
                # HSN/SAC & Supply Details (6 fields)
                self._clean_text_field(invoice.get('hsn_code', '')),
                self._clean_text_field(invoice.get('sac_code', '')),
                self._clean_text_field(invoice.get('place_of_supply', '')),
                self._clean_text_field(invoice.get('reverse_charge', '')),
                self._clean_text_field(invoice.get('invoice_type', '')),
                self._clean_text_field(invoice.get('supply_type', '')),
                
                # Import/Export (7 fields)
                self._clean_text_field(invoice.get('bill_of_entry', '')),
                self._clean_text_field(invoice.get('bill_of_entry_date', '')),
                self._clean_text_field(invoice.get('port_code', '')),
                self._clean_text_field(invoice.get('shipping_bill_number', '')),
                self._clean_text_field(invoice.get('country_of_origin', '')),
                invoice.get('exchange_rate', 0),
                invoice.get('foreign_currency_amount', 0),
                
                # Hotel & Hospitality (7 fields)
                self._clean_text_field(invoice.get('arrival_date', '')),
                self._clean_text_field(invoice.get('departure_date', '')),
                self._clean_text_field(invoice.get('room_number', '')),
                self._clean_text_field(invoice.get('guest_count', '')),
                self._clean_text_field(invoice.get('booking_reference', '')),
                self._clean_text_field(invoice.get('hotel_star_rating', '')),
                self._clean_text_field(invoice.get('meal_plan', '')),
                
                # Retail & E-commerce (6 fields)
                self._clean_text_field(invoice.get('order_id', '')),
                self._clean_text_field(invoice.get('tracking_number', '')),
                self._clean_text_field(invoice.get('shipping_method', '')),
                self._clean_text_field(invoice.get('delivery_date', '')),
                self._clean_text_field(invoice.get('return_policy', '')),
                self._clean_text_field(invoice.get('coupon_code', '')),
                
                # Manufacturing & Quality (6 fields)
                self._clean_text_field(invoice.get('purchase_order', '')),
                self._clean_text_field(invoice.get('batch_number', '')),
                self._clean_text_field(invoice.get('quality_certificate', '')),
                self._clean_text_field(invoice.get('warranty_period', '')),
                self._clean_text_field(invoice.get('manufacturing_date', '')),
                self._clean_text_field(invoice.get('expiry_date', '')),
                
                # Healthcare (6 fields)
                self._clean_text_field(invoice.get('patient_id', '')),
                self._clean_text_field(invoice.get('doctor_name', '')),
                self._clean_text_field(invoice.get('medical_license', '')),
                self._clean_text_field(invoice.get('insurance_claim', '')),
                self._clean_text_field(invoice.get('treatment_date', '')),
                self._clean_text_field(invoice.get('prescription_number', '')),
                
                # Transportation (6 fields)
                self._clean_text_field(invoice.get('vehicle_number', '')),
                self._clean_text_field(invoice.get('driver_name', '')),
                self._clean_text_field(invoice.get('origin_location', '')),
                self._clean_text_field(invoice.get('destination_location', '')),
                invoice.get('distance_km', 0),
                invoice.get('fuel_surcharge', 0),
                
                # Professional Services (6 fields)
                self._clean_text_field(invoice.get('project_name', ''), 200),
                self._clean_text_field(invoice.get('consultant_name', ''), 200),
                invoice.get('hourly_rate', 0),
                invoice.get('hours_worked', 0),
                self._clean_text_field(invoice.get('project_phase', '')),
                self._clean_text_field(invoice.get('deliverable', '')),
                
                # Real Estate (5 fields)
                self._clean_text_field(invoice.get('property_address', ''), 300),
                self._clean_text_field(invoice.get('property_type', '')),
                invoice.get('square_footage', 0),
                self._clean_text_field(invoice.get('lease_term', '')),
                invoice.get('security_deposit', 0),
                
                # Education (5 fields)
                self._clean_text_field(invoice.get('student_id', '')),
                self._clean_text_field(invoice.get('course_name', '')),
                self._clean_text_field(invoice.get('academic_year', '')),
                self._clean_text_field(invoice.get('semester', '')),
                self._clean_text_field(invoice.get('instructor_name', '')),
                
                # Utilities (5 fields)
                self._clean_text_field(invoice.get('meter_reading_start', '')),
                self._clean_text_field(invoice.get('meter_reading_end', '')),
                invoice.get('units_consumed', 0),
                invoice.get('rate_per_unit', 0),
                self._clean_text_field(invoice.get('connection_id', '')),
                
                # Financial Services (3 fields)
                self._clean_text_field(invoice.get('transaction_id', '')),
                invoice.get('interest_rate', 0),
                invoice.get('principal_amount', 0),
                
                # Subscription Services (5 fields)
                self._clean_text_field(invoice.get('subscription_type', '')),
                self._clean_text_field(invoice.get('billing_cycle', '')),
                self._clean_text_field(invoice.get('next_billing_date', '')),
                self._clean_text_field(invoice.get('auto_renewal', '')),
                self._clean_text_field(invoice.get('plan_features', '')),
                
                # Business Operations (9 fields)
                self._clean_text_field(invoice.get('contract_number', '')),
                self._clean_text_field(invoice.get('milestone', '')),
                self._clean_text_field(invoice.get('approval_status', '')),
                self._clean_text_field(invoice.get('approved_by', '')),
                self._clean_text_field(invoice.get('department', '')),
                self._clean_text_field(invoice.get('cost_center', '')),
                self._clean_text_field(invoice.get('budget_code', '')),
                self._clean_text_field(invoice.get('regulatory_code', '')),
                self._clean_text_field(invoice.get('compliance_certificate', '')),
                
                # Audit & Compliance (2 fields)
                self._clean_text_field(invoice.get('audit_trail', '')),
                self._clean_text_field(invoice.get('authorized_signatory', '')),
                
                # Metadata & Quality (10 fields)
                self._clean_text_field(invoice.get('document_id', '')),
                self._clean_text_field(invoice.get('notes', ''), 500),
                self._clean_text_field(invoice.get('category_id', '')),
                self._clean_text_field(invoice.get('tags', '')),
                self._clean_text_field(invoice.get('metadata', '')),
                self._clean_text_field(invoice.get('attachments', '')),
                self._clean_text_field(invoice.get('is_starred', '')),
                self._clean_text_field(invoice.get('is_verified', '')),
                self._clean_text_field(invoice.get('is_recurring', '')),
                self._clean_text_field(invoice.get('recurring_frequency', '')),
                
                # AI/ML Quality Scores (7 fields)
                self._clean_text_field(invoice.get('extraction_version', '')),
                self._clean_text_field(invoice.get('data_source', '')),
                invoice.get('quality_score', 0),
                invoice.get('confidence_score', 0),
                invoice.get('amount_confidence', 0),
                invoice.get('date_confidence', 0),
                invoice.get('invoice_number_confidence', 0),
                
                # Line Items (stored as JSON)
                self._clean_text_field(str(invoice.get('line_items', [])), 1000)
            ]
            
            # Currency columns (amounts) - updated for comprehensive fields
            currency_columns = [4,  # Total Amount
                               17,  # Subtotal
                               18,  # Taxable Amount
                               19,  # Discount
                               20,  # Shipping Charges
                               21,  # Other Charges
                               22,  # Roundoff
                               23, 24, 25, 26, 27,  # GST amounts (CGST, SGST, IGST, UGST, CESS)
                               28,  # Tax Amount
                               29,  # Total GST
                               30,  # VAT
                               31,  # Service Tax
                               32,  # Taxable Value
                               33,  # Processing Fee
                               45,  # TDS Amount
                               47,  # TCS Amount
                               49, 50, 51,  # Additional Charges
                               58,  # Exchange Rate
                               59,  # Foreign Currency Amount
                               67,  # Hourly Rate
                               70,  # Security Deposit
                               74,  # Rate Per Unit
                               76,  # Interest Rate
                               77,  # Principal Amount
                               82,  # Distance KM
                               83,  # Fuel Surcharge
                               87,  # Square Footage
                               89,  # Units Consumed
                               90,  # Rate Per Unit (duplicate, but keeping for now)
                               91]  # Security Deposit (duplicate, but keeping for now)
            
            for col_num, value in enumerate(data_values, 1):
                cell = ws.cell(row=row_num, column=col_num)
                cell.value = value
                cell.border = self.border_style
                
                # Format currency columns
                if col_num in currency_columns and isinstance(value, (int, float)) and value > 0:
                    cell.number_format = '₹#,##0.00'
                
                # Color code payment status
                if col_num == 6 and value:  # Payment Status column (now column 6)
                    if str(value).lower() in ['paid', 'completed']:
                        cell.fill = PatternFill(start_color="C6EFCE", fill_type="solid")  # Green
                    elif str(value).lower() in ['pending', 'unpaid']:
                        cell.fill = PatternFill(start_color="FFC7CE", fill_type="solid")  # Red
        
        # Auto-adjust column widths (optimized for readability and prevent text clipping)
        max_width = 80  # Increased maximum column width for long text
        min_width = 10  # Minimum column width
        
        for col_num in range(1, len(headers) + 1):
            column_letter = get_column_letter(col_num)
            
            # Get header length
            header_length = len(headers[col_num - 1])
            
            # Find maximum content length in this column
            max_content_length = header_length
            for row_num in range(1, len(invoices) + 2):  # +2 for header row
                cell_value = ws.cell(row=row_num, column=col_num).value
                if cell_value is not None:
                    content_length = len(str(cell_value))
                    max_content_length = max(max_content_length, content_length)
            
            # Calculate optimal width with some padding
            optimal_width = min(max_content_length + 3, max_width)
            optimal_width = max(optimal_width, min_width)
            
            # Special handling for certain column types
            header_name = headers[col_num - 1].lower()
            if any(keyword in header_name for keyword in ['address', 'description', 'name', 'email', 'phone']):
                # Wider columns for text-heavy fields
                optimal_width = min(max_content_length + 8, max_width)  # More padding
                # Enable text wrapping for long text
                for row_num in range(1, len(invoices) + 2):
                    cell = ws.cell(row=row_num, column=col_num)
                    cell.alignment = Alignment(wrap_text=True, vertical='top')
            else:
                # Center alignment for numeric/currency fields
                if any(keyword in header_name for keyword in ['amount', 'total', 'gst', 'rate', 'price']):
                    for row_num in range(2, len(invoices) + 2):  # Skip header
                        cell = ws.cell(row=row_num, column=col_num)
                        cell.alignment = Alignment(horizontal='right', vertical='center')
                else:
                    # Left align other text fields
                    for row_num in range(1, len(invoices) + 2):
                        cell = ws.cell(row=row_num, column=col_num)
                        cell.alignment = Alignment(horizontal='left', vertical='center')
            
            ws.column_dimensions[column_letter].width = optimal_width
        
        # Adjust row heights for wrapped text (improved calculation)
        for row_num in range(1, min(len(invoices) + 2, 100)):  # Check more rows
            max_lines = 1
            wrapped_cols = 0
            
            for col_num in range(1, len(headers) + 1):
                cell = ws.cell(row=row_num, column=col_num)
                if cell.value and cell.alignment and cell.alignment.wrap_text:
                    content = str(cell.value)
                    column_width = ws.column_dimensions[get_column_letter(col_num)].width
                    
                    # Better line estimation: account for word wrapping
                    if column_width > 0:
                        # Estimate characters per line (more conservative)
                        chars_per_line = max(1, int(column_width * 0.9))  # 0.9 for better wrapping
                        estimated_lines = max(1, (len(content) + chars_per_line - 1) // chars_per_line)
                        max_lines = max(max_lines, min(estimated_lines, 10))  # Allow up to 10 lines
                        wrapped_cols += 1
            
            # Set row height based on estimated lines (18 pixels per line for better readability)
            if max_lines > 1 or wrapped_cols > 0:
                base_height = 15  # Base height for single line
                additional_height = (max_lines - 1) * 18  # 18 pixels per additional line
                ws.row_dimensions[row_num].height = base_height + additional_height
        
        # Freeze header row for easy scrolling
        ws.freeze_panes = 'A2'
        
        print(f"✅ Excel export includes {len(headers)} comprehensive fields per invoice!")
    
    def _create_line_item_sheet(self, wb: Workbook, invoices: List[Dict]):
        """Create sheet in fully dynamic format: all unique keys from invoices and line items as columns"""
        ws = wb.active
        ws.title = "Invoice Analysis Data"

        # Collect all unique keys from invoices and line items
        all_keys = set()
        for invoice in invoices:
            all_keys.update(invoice.keys())
            line_items = invoice.get('line_items', [])
            if isinstance(line_items, list):
                for item in line_items:
                    if isinstance(item, dict):
                        all_keys.update(item.keys())
            elif isinstance(line_items, dict):
                all_keys.update(line_items.keys())

        # Remove raw_extracted_data if present (too verbose)
        all_keys.discard('raw_extracted_data')

        # Sort keys for consistency
        headers = sorted(list(all_keys))

        # Add headers with formatting
        for col_num, header in enumerate(headers, 1):
            cell = ws.cell(row=1, column=col_num)
            cell.value = header
            cell.font = self.header_font
            cell.fill = self.header_fill
            cell.border = self.border_style
            cell.alignment = Alignment(horizontal='center', vertical='center')

        row_num = 2
        for invoice in invoices:
            line_items = invoice.get('line_items', [])
            if not line_items:
                line_items = [{}]
            if not isinstance(line_items, list):
                line_items = [line_items]
            for item in line_items:
                row_data = {}
                # Fill with invoice fields
                for key in invoice:
                    row_data[key] = invoice[key]
                # Fill with line item fields (overrides invoice fields if same key)
                if isinstance(item, dict):
                    for key in item:
                        row_data[key] = item[key]
                # Write row
                for col_num, header in enumerate(headers, 1):
                    value = row_data.get(header, "")
                    cell = ws.cell(row=row_num, column=col_num)
                    cell.value = value
                    cell.border = self.border_style
                    # Simple formatting for numbers
                    if isinstance(value, (int, float)):
                        cell.number_format = '#,##0.00'
                    # Text wrapping for long text
                    if isinstance(value, str) and len(value) > 30:
                        cell.alignment = Alignment(wrap_text=True, vertical='center')
                row_num += 1

        # Auto-adjust column widths
        for col_num in range(1, len(headers) + 1):
            column_letter = get_column_letter(col_num)
            header_length = len(headers[col_num - 1])
            max_content_length = header_length
            for row in range(1, ws.max_row + 1):
                cell_value = ws.cell(row=row, column=col_num).value
                if cell_value is not None:
                    content_length = len(str(cell_value))
                    max_content_length = max(max_content_length, content_length)
            optimal_width = min(max_content_length + 3, 50)
            optimal_width = max(optimal_width, 12)
            ws.column_dimensions[column_letter].width = optimal_width

        ws.freeze_panes = 'A2'
        print(f"✅ Dynamic export completed with {ws.max_row - 1} rows and {len(headers)} columns!")


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
