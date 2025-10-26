"""
📄 RAW CSV EXPORTER - Machine-Readable
======================================

Plain text, no formatting, for automation and ERP integration

Target Users: Developers, ERP/CRM Systems, Automation Scripts

FIXED: UTF-8 BOM encoding for Excel compatibility (₹ symbols display correctly)
"""

import csv
import io
import re
from datetime import datetime
from typing import Dict, List


class CSVExporter:
    """
    CSV exporter for machine-readable data
    - No formatting whatsoever
    - Plain text, comma-separated
    - Consistent column order (same as Excel)
    - UTF-8 encoding for ₹ symbols
    - Prevents column overlap and line wrapping
    """
    
    def _clean_text_field(self, text: str, max_length: int = 1000) -> str:
        """
        Clean text fields to prevent CSV issues:
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
        
        # Truncate if too long (prevents column overflow)
        if len(text) > max_length:
            text = text[:max_length - 3] + "..."
        
        return text
    
    def _format_numeric_field(self, value, decimals: int = 2) -> str:
        """
        Format numeric fields consistently to prevent alignment issues
        """
        try:
            if value is None or value == "":
                return "0.00"
            numeric_value = float(value)
            return f"{numeric_value:.{decimals}f}"
        except (ValueError, TypeError):
            return "0.00"
    
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
            invoice_num = invoice_data.get('invoice_number') or 'INVOICE'
            invoice_num = str(invoice_num).replace('/', '_')
            filename = f"Invoice_{invoice_num}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        
        # Create comprehensive CSV content with ALL fields
        with open(filename, 'w', newline='', encoding='utf-8-sig') as csvfile:  # utf-8-sig for Excel compatibility
            writer = csv.writer(csvfile, quoting=csv.QUOTE_ALL)  # Quote all fields to prevent issues
            
            # ============ COMPLETE INVOICE DATA ============
            # Core Invoice Information
            writer.writerow(['Invoice Number', self._clean_text_field(invoice_data.get('invoice_number', ''))])
            writer.writerow(['Invoice Date', self._clean_text_field(invoice_data.get('invoice_date', ''))])
            writer.writerow(['Due Date', self._clean_text_field(invoice_data.get('due_date', ''))])
            writer.writerow(['Total Amount', self._format_numeric_field(invoice_data.get('total_amount', 0))])
            writer.writerow(['Currency', self._clean_text_field(invoice_data.get('currency', 'INR'))])
            
            # Vendor Information
            writer.writerow(['Vendor Name', self._clean_text_field(invoice_data.get('vendor_name', ''), 200)])
            writer.writerow(['Vendor GSTIN', self._clean_text_field(invoice_data.get('vendor_gstin', ''))])
            writer.writerow(['Vendor PAN', self._clean_text_field(invoice_data.get('vendor_pan', ''))])
            writer.writerow(['Vendor Email', self._clean_text_field(invoice_data.get('vendor_email', ''))])
            writer.writerow(['Vendor Phone', self._clean_text_field(invoice_data.get('vendor_phone', ''))])
            writer.writerow(['Vendor Address', self._clean_text_field(invoice_data.get('vendor_address', ''), 300)])
            writer.writerow(['Vendor State', self._clean_text_field(invoice_data.get('vendor_state', ''))])
            writer.writerow(['Vendor Pincode', self._clean_text_field(invoice_data.get('vendor_pincode', ''))])
            
            # Customer Information
            writer.writerow(['Customer Name', self._clean_text_field(invoice_data.get('customer_name', ''), 200)])
            writer.writerow(['Customer GSTIN', self._clean_text_field(invoice_data.get('customer_gstin', ''))])
            writer.writerow(['Customer Address', self._clean_text_field(invoice_data.get('customer_address', ''), 300)])
            writer.writerow(['Customer State', self._clean_text_field(invoice_data.get('customer_state', ''))])
            writer.writerow(['Customer Phone', self._clean_text_field(invoice_data.get('customer_phone', ''))])
            
            # Financial Breakdown
            writer.writerow(['Subtotal', self._format_numeric_field(invoice_data.get('subtotal', 0))])
            writer.writerow(['Taxable Amount', self._format_numeric_field(invoice_data.get('taxable_amount', 0))])
            writer.writerow(['Discount', self._format_numeric_field(invoice_data.get('discount', 0))])
            writer.writerow(['Shipping Charges', self._format_numeric_field(invoice_data.get('shipping_charges', 0))])
            writer.writerow(['Other Charges', self._format_numeric_field(invoice_data.get('other_charges', 0))])
            writer.writerow(['Roundoff', self._format_numeric_field(invoice_data.get('roundoff', 0))])
            
            # GST & Tax Details
            writer.writerow(['CGST', self._format_numeric_field(invoice_data.get('cgst', 0))])
            writer.writerow(['SGST', self._format_numeric_field(invoice_data.get('sgst', 0))])
            writer.writerow(['IGST', self._format_numeric_field(invoice_data.get('igst', 0))])
            writer.writerow(['UGST', self._format_numeric_field(invoice_data.get('ugst', 0))])
            writer.writerow(['CESS', self._format_numeric_field(invoice_data.get('cess', 0))])
            writer.writerow(['Total GST', self._format_numeric_field(invoice_data.get('total_gst', 0))])
            writer.writerow(['HSN Code', self._clean_text_field(invoice_data.get('hsn_code', ''))])
            writer.writerow(['SAC Code', self._clean_text_field(invoice_data.get('sac_code', ''))])
            writer.writerow(['Place of Supply', self._clean_text_field(invoice_data.get('place_of_supply', ''))])
            
            # Banking Information
            writer.writerow(['Bank Name', self._clean_text_field(invoice_data.get('bank_name', ''))])
            writer.writerow(['Account Number', self._clean_text_field(invoice_data.get('account_number', ''))])
            writer.writerow(['IFSC Code', self._clean_text_field(invoice_data.get('ifsc_code', ''))])
            writer.writerow(['SWIFT Code', self._clean_text_field(invoice_data.get('swift_code', ''))])
            
            # Payment & Business Terms
            writer.writerow(['Payment Status', self._clean_text_field(invoice_data.get('payment_status', 'pending'))])
            writer.writerow(['Payment Method', self._clean_text_field(invoice_data.get('payment_method', ''))])
            writer.writerow(['Payment Terms', self._clean_text_field(invoice_data.get('payment_terms', ''))])
            
            # Purchase Order Details
            writer.writerow(['PO Number', self._clean_text_field(invoice_data.get('po_number', ''))])
            writer.writerow(['PO Date', self._clean_text_field(invoice_data.get('po_date', ''))])
            writer.writerow(['Invoice Type', self._clean_text_field(invoice_data.get('invoice_type', ''))])
            writer.writerow(['Supply Type', self._clean_text_field(invoice_data.get('supply_type', ''))])
            writer.writerow(['Reverse Charge', self._clean_text_field(invoice_data.get('reverse_charge', ''))])
            
            # Additional Taxes
            writer.writerow(['VAT', self._format_numeric_field(invoice_data.get('vat', 0))])
            writer.writerow(['Service Tax', self._format_numeric_field(invoice_data.get('service_tax', 0))])
            writer.writerow(['TDS Amount', self._format_numeric_field(invoice_data.get('tds_amount', 0))])
            writer.writerow(['TCS Amount', self._format_numeric_field(invoice_data.get('tcs_amount', 0))])
            
            # Import/Export Fields
            writer.writerow(['Bill of Entry', self._clean_text_field(invoice_data.get('bill_of_entry', ''))])
            writer.writerow(['Port Code', self._clean_text_field(invoice_data.get('port_code', ''))])
            
            # Industry-Specific Fields
            # Hotel & Hospitality
            if invoice_data.get('arrival_date') or invoice_data.get('room_number'):
                writer.writerow(['=== HOTEL & HOSPITALITY ===', ''])
                writer.writerow(['Arrival Date', self._clean_text_field(invoice_data.get('arrival_date', ''))])
                writer.writerow(['Departure Date', self._clean_text_field(invoice_data.get('departure_date', ''))])
                writer.writerow(['Room Number', self._clean_text_field(invoice_data.get('room_number', ''))])
                writer.writerow(['Guest Count', self._clean_text_field(invoice_data.get('guest_count', ''))])
                writer.writerow(['Booking Reference', self._clean_text_field(invoice_data.get('booking_reference', ''))])
            
            # Retail & E-commerce
            if invoice_data.get('order_id') or invoice_data.get('tracking_number'):
                writer.writerow(['=== RETAIL & E-COMMERCE ===', ''])
                writer.writerow(['Order ID', self._clean_text_field(invoice_data.get('order_id', ''))])
                writer.writerow(['Tracking Number', self._clean_text_field(invoice_data.get('tracking_number', ''))])
                writer.writerow(['Shipping Method', self._clean_text_field(invoice_data.get('shipping_method', ''))])
                writer.writerow(['Delivery Date', self._clean_text_field(invoice_data.get('delivery_date', ''))])
            
            # Manufacturing
            if invoice_data.get('purchase_order') or invoice_data.get('batch_number'):
                writer.writerow(['=== MANUFACTURING ===', ''])
                writer.writerow(['Purchase Order', self._clean_text_field(invoice_data.get('purchase_order', ''))])
                writer.writerow(['Batch Number', self._clean_text_field(invoice_data.get('batch_number', ''))])
                writer.writerow(['Quality Certificate', self._clean_text_field(invoice_data.get('quality_certificate', ''))])
                writer.writerow(['Warranty Period', self._clean_text_field(invoice_data.get('warranty_period', ''))])
            
            # Professional Services
            if invoice_data.get('project_name') or invoice_data.get('consultant_name'):
                writer.writerow(['=== PROFESSIONAL SERVICES ===', ''])
                writer.writerow(['Project Name', self._clean_text_field(invoice_data.get('project_name', ''), 200)])
                writer.writerow(['Consultant Name', self._clean_text_field(invoice_data.get('consultant_name', ''), 200)])
                writer.writerow(['Hourly Rate', self._format_numeric_field(invoice_data.get('hourly_rate', 0))])
                writer.writerow(['Hours Worked', self._format_numeric_field(invoice_data.get('hours_worked', 0))])
            
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
                    self._clean_text_field(item.get('description', 'N/A'), 500),  # Limit description length
                    self._clean_text_field(item.get('hsn_sac', item.get('hsn', 'N/A'))),
                    self._format_numeric_field(qty, 2),
                    self._format_numeric_field(rate, 2),
                    self._format_numeric_field(amount, 2),
                    self._format_numeric_field(cgst_rate, 1),
                    self._format_numeric_field(cgst_amount, 2),
                    self._format_numeric_field(sgst_rate, 1),
                    self._format_numeric_field(sgst_amount, 2),
                    self._format_numeric_field(igst_rate, 1),
                    self._format_numeric_field(igst_amount, 2),
                    self._format_numeric_field(line_total, 2)
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
                self._format_numeric_field(subtotal, 2),
                '',
                self._format_numeric_field(cgst, 2),
                '',
                self._format_numeric_field(sgst, 2),
                '',
                self._format_numeric_field(igst, 2),
                self._format_numeric_field(total_amount, 2)
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
        
        with open(filename, 'w', newline='', encoding='utf-8-sig') as csvfile:  # utf-8-sig for Excel compatibility
            writer = csv.writer(csvfile, quoting=csv.QUOTE_ALL)  # Quote all fields
            
            # Comprehensive headers for bulk export (ALL 171+ fields)
            headers = [
                # Core Invoice Fields (6)
                'Invoice Number', 'Invoice Date', 'Due Date', 'Total Amount', 'Currency', 'Payment Status',
                
                # Vendor Information (11 fields)
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
                
                # Import/Export (7 fields)
                'Bill of Entry', 'Bill of Entry Date', 'Port Code', 'Shipping Bill Number',
                'Country of Origin', 'Exchange Rate', 'Foreign Currency Amount',
                
                # Hotel & Hospitality (7 fields)
                'Arrival Date', 'Departure Date', 'Room Number', 'Guest Count', 'Booking Reference',
                'Hotel Star Rating', 'Meal Plan',
                
                # Retail & E-commerce (6 fields)
                'Order ID', 'Tracking Number', 'Shipping Method', 'Delivery Date', 'Return Policy',
                'Coupon Code',
                
                # Manufacturing & Quality (6 fields)
                'Purchase Order', 'Batch Number', 'Quality Certificate', 'Warranty Period',
                'Manufacturing Date', 'Expiry Date',
                
                # Healthcare (6 fields)
                'Patient ID', 'Doctor Name', 'Medical License', 'Insurance Claim', 'Treatment Date',
                'Prescription Number',
                
                # Transportation (6 fields)
                'Vehicle Number', 'Driver Name', 'Origin Location', 'Destination Location',
                'Distance KM', 'Fuel Surcharge',
                
                # Professional Services (6 fields)
                'Project Name', 'Consultant Name', 'Hourly Rate', 'Hours Worked', 'Project Phase', 'Deliverable',
                
                # Real Estate (5 fields)
                'Property Address', 'Property Type', 'Square Footage', 'Lease Term', 'Security Deposit',
                
                # Education (5 fields)
                'Student ID', 'Course Name', 'Academic Year', 'Semester', 'Instructor Name',
                
                # Utilities (5 fields)
                'Meter Reading Start', 'Meter Reading End', 'Units Consumed', 'Rate Per Unit', 'Connection ID',
                
                # Financial Services (3 fields)
                'Transaction ID', 'Interest Rate', 'Principal Amount',
                
                # Subscription Services (5 fields)
                'Subscription Type', 'Billing Cycle', 'Next Billing Date', 'Auto Renewal', 'Plan Features',
                
                # Business Operations (9 fields)
                'Contract Number', 'Milestone', 'Approval Status', 'Approved By', 'Department',
                'Cost Center', 'Budget Code', 'Regulatory Code', 'Compliance Certificate',
                
                # Audit & Compliance (2 fields)
                'Audit Trail', 'Authorized Signatory',
                
                # Metadata & Quality (10 fields)
                'Document ID', 'Notes', 'Category ID', 'Tags', 'Metadata', 'Attachments',
                'Is Starred', 'Is Verified', 'Is Recurring', 'Recurring Frequency',
                
                # AI/ML Quality Scores (7 fields)
                'Extraction Version', 'Data Source', 'Quality Score', 'Confidence Score',
                'Amount Confidence', 'Date Confidence', 'Invoice Number Confidence',
                
                # Line Items (stored as JSON)
                'Line Items'
            ]
            writer.writerow(headers)
            
            # Write each invoice as a row with ALL fields
            for invoice in invoices:
                # Handle None values properly and create comprehensive row with ALL 171+ fields
                row = [
                    # Core Invoice Fields (6)
                    self._clean_text_field(invoice.get('invoice_number', '')),
                    self._clean_text_field(invoice.get('invoice_date', '')),
                    self._clean_text_field(invoice.get('due_date', '')),
                    self._format_numeric_field(invoice.get('total_amount', 0)),
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
                    self._format_numeric_field(invoice.get('vendor_confidence', 0)),
                    
                    # Customer Information (5 fields)
                    self._clean_text_field(invoice.get('customer_name', ''), 200),
                    self._clean_text_field(invoice.get('customer_gstin', '')),
                    self._clean_text_field(invoice.get('customer_address', ''), 300),
                    self._clean_text_field(invoice.get('customer_state', '')),
                    self._clean_text_field(invoice.get('customer_phone', '')),
                    
                    # Financial Breakdown (6 fields)
                    self._format_numeric_field(invoice.get('subtotal', 0)),
                    self._format_numeric_field(invoice.get('taxable_amount', 0)),
                    self._format_numeric_field(invoice.get('discount', 0)),
                    self._format_numeric_field(invoice.get('shipping_charges', 0)),
                    self._format_numeric_field(invoice.get('other_charges', 0)),
                    self._format_numeric_field(invoice.get('roundoff', 0)),
                    
                    # GST & Tax Details (11 fields)
                    self._format_numeric_field(invoice.get('cgst', 0)),
                    self._format_numeric_field(invoice.get('sgst', 0)),
                    self._format_numeric_field(invoice.get('igst', 0)),
                    self._format_numeric_field(invoice.get('ugst', 0)),
                    self._format_numeric_field(invoice.get('cess', 0)),
                    self._format_numeric_field(invoice.get('tax_amount', 0)),
                    self._format_numeric_field(invoice.get('total_gst', 0)),
                    self._format_numeric_field(invoice.get('vat', 0)),
                    self._format_numeric_field(invoice.get('service_tax', 0)),
                    self._format_numeric_field(invoice.get('taxable_value', 0)),
                    self._format_numeric_field(invoice.get('processing_fee', 0)),
                    
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
                    self._format_numeric_field(invoice.get('tds_amount', 0)),
                    self._format_numeric_field(invoice.get('tds_percentage', 0)),
                    self._format_numeric_field(invoice.get('tcs_amount', 0)),
                    self._format_numeric_field(invoice.get('discount_percentage', 0)),
                    
                    # Additional Charges (4 fields)
                    self._format_numeric_field(invoice.get('packing_charges', 0)),
                    self._format_numeric_field(invoice.get('handling_charges', 0)),
                    self._format_numeric_field(invoice.get('insurance_charges', 0)),
                    self._format_numeric_field(invoice.get('processing_time_seconds', 0)),
                    
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
                    self._format_numeric_field(invoice.get('exchange_rate', 0)),
                    self._format_numeric_field(invoice.get('foreign_currency_amount', 0)),
                    
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
                    self._format_numeric_field(invoice.get('distance_km', 0)),
                    self._format_numeric_field(invoice.get('fuel_surcharge', 0)),
                    
                    # Professional Services (6 fields)
                    self._clean_text_field(invoice.get('project_name', ''), 200),
                    self._clean_text_field(invoice.get('consultant_name', ''), 200),
                    self._format_numeric_field(invoice.get('hourly_rate', 0)),
                    self._format_numeric_field(invoice.get('hours_worked', 0)),
                    self._clean_text_field(invoice.get('project_phase', '')),
                    self._clean_text_field(invoice.get('deliverable', '')),
                    
                    # Real Estate (5 fields)
                    self._clean_text_field(invoice.get('property_address', ''), 300),
                    self._clean_text_field(invoice.get('property_type', '')),
                    self._format_numeric_field(invoice.get('square_footage', 0)),
                    self._clean_text_field(invoice.get('lease_term', '')),
                    self._format_numeric_field(invoice.get('security_deposit', 0)),
                    
                    # Education (5 fields)
                    self._clean_text_field(invoice.get('student_id', '')),
                    self._clean_text_field(invoice.get('course_name', '')),
                    self._clean_text_field(invoice.get('academic_year', '')),
                    self._clean_text_field(invoice.get('semester', '')),
                    self._clean_text_field(invoice.get('instructor_name', '')),
                    
                    # Utilities (5 fields)
                    self._clean_text_field(invoice.get('meter_reading_start', '')),
                    self._clean_text_field(invoice.get('meter_reading_end', '')),
                    self._format_numeric_field(invoice.get('units_consumed', 0)),
                    self._format_numeric_field(invoice.get('rate_per_unit', 0)),
                    self._clean_text_field(invoice.get('connection_id', '')),
                    
                    # Financial Services (3 fields)
                    self._clean_text_field(invoice.get('transaction_id', '')),
                    self._format_numeric_field(invoice.get('interest_rate', 0)),
                    self._format_numeric_field(invoice.get('principal_amount', 0)),
                    
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
                    self._format_numeric_field(invoice.get('quality_score', 0)),
                    self._format_numeric_field(invoice.get('confidence_score', 0)),
                    self._format_numeric_field(invoice.get('amount_confidence', 0)),
                    self._format_numeric_field(invoice.get('date_confidence', 0)),
                    self._format_numeric_field(invoice.get('invoice_number_confidence', 0)),
                    
                    # Line Items (stored as JSON)
                    self._clean_text_field(str(invoice.get('line_items', [])), 1000)
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
