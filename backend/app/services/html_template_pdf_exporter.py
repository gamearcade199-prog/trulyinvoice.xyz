"""
HTML Template-Based PDF Exporter - Professional Invoice Design
==============================================================

Converts beautiful HTML invoice templates to PDF
Matches the exact visual design from your HTML template
"""

from xhtml2pdf import pisa
from io import BytesIO
import os
from datetime import datetime
from typing import Dict
import logging

logger = logging.getLogger(__name__)


class HTMLTemplatePDFExporter:
    """
    Professional HTML-to-PDF invoice exporter
    Uses your exact HTML template design
    """
    
    def __init__(self):
        self.output_dir = "exports"
        os.makedirs(self.output_dir, exist_ok=True)
    
    def _generate_html(self, invoice: Dict) -> str:
        """Generate HTML from invoice data using your template"""
        
        # Extract invoice data
        invoice_number = invoice.get('invoice_number', 'INV-000000')
        invoice_date = invoice.get('invoice_date', 'N/A')
        due_date = invoice.get('due_date', 'N/A')
        status = invoice.get('payment_status', 'Pending')
        
        # Vendor info
        vendor_name = invoice.get('vendor_name', 'Company Name')
        vendor_address = invoice.get('vendor_address', 'Address')
        vendor_phone = invoice.get('vendor_phone', 'N/A')
        vendor_email = invoice.get('vendor_email', 'N/A')
        vendor_gstin = invoice.get('vendor_gstin', 'N/A')
        
        # Customer info
        customer_name = invoice.get('customer_name', 'Customer Name')
        customer_address = invoice.get('customer_address', 'Address')
        customer_phone = invoice.get('customer_phone', 'N/A')
        customer_email = invoice.get('customer_email', 'N/A')
        customer_gstin = invoice.get('customer_gstin', 'N/A')
        
        # Line items
        line_items_html = ""
        line_items = invoice.get('line_items', [])
        if isinstance(line_items, list):
            for idx, item in enumerate(line_items, 1):
                desc = item.get('description', 'Item')
                detail = item.get('detail', '')
                qty = item.get('quantity', 1) or 1
                rate_val = item.get('rate') or item.get('unit_price') or 0
                rate = float(rate_val) if rate_val is not None else 0.0
                amount_val = item.get('amount') or (rate * qty)
                amount = float(amount_val) if amount_val is not None else 0.0
                
                line_items_html += f"""
                <tr>
                    <td>{idx}</td>
                    <td>
                        <div class="item-desc">{desc}</div>
                        <div class="item-detail">{detail}</div>
                    </td>
                    <td class="text-center">{qty}</td>
                    <td class="text-right">₹{rate:,.2f}</td>
                    <td class="text-right"><strong>₹{amount:,.2f}</strong></td>
                </tr>
                """
        
        # Totals - Handle None values safely
        subtotal = float(invoice.get('subtotal') or 0)
        discount = float(invoice.get('discount') or 0)
        cgst = float(invoice.get('cgst') or 0)
        sgst = float(invoice.get('sgst') or 0)
        igst = float(invoice.get('igst') or 0)
        total = float(invoice.get('total_amount') or invoice.get('total') or subtotal)
        
        # Tax rows - formatted for new structure
        tax_rows_html = ""
        if cgst > 0:
            tax_rows_html += f'<div class="total-line"><span class="total-label">CGST (9%)</span><span class="total-value">₹{cgst:,.2f}</span></div>'
        if sgst > 0:
            tax_rows_html += f'<div class="total-line"><span class="total-label">SGST (9%)</span><span class="total-value">₹{sgst:,.2f}</span></div>'
        if igst > 0:
            tax_rows_html += f'<div class="total-line"><span class="total-label">IGST (18%)</span><span class="total-value">₹{igst:,.2f}</span></div>'
        
        # Bank details
        bank_name = invoice.get('bank_name', 'N/A')
        account_number = invoice.get('bank_account', 'N/A')
        ifsc_code = invoice.get('ifsc_code', 'N/A')
        upi_id = invoice.get('upi_id', 'N/A')
        
        # Amount in words (simple version)
        amount_words = self._number_to_words(total)
        
        html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Invoice {invoice_number}</title>
    <style>
        @page {{
            size: A4;
            margin: 0;
        }}
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            font-size: 11pt;
            color: #2d3748;
            line-height: 1.6;
        }}
        
        /* Header with blue background */
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px 50px 30px 50px;
        }}
        .header-content {{
            display: table;
            width: 100%;
        }}
        .company-section {{
            display: table-cell;
            width: 60%;
            vertical-align: top;
        }}
        .company-name {{
            font-size: 28px;
            font-weight: 700;
            margin-bottom: 8px;
            letter-spacing: -0.5px;
        }}
        .company-details {{
            font-size: 11px;
            opacity: 0.95;
            line-height: 1.7;
        }}
        .invoice-section {{
            display: table-cell;
            width: 40%;
            text-align: right;
            vertical-align: top;
        }}
        .invoice-title {{
            font-size: 42px;
            font-weight: 700;
            margin-bottom: 5px;
            letter-spacing: 1px;
        }}
        .invoice-number {{
            font-size: 14px;
            opacity: 0.9;
            font-weight: 500;
        }}
        
        /* Main content container */
        .content {{
            padding: 0 50px 50px 50px;
        }}
        
        /* Invoice meta info section */
        .meta-section {{
            margin: 30px 0;
            background: #f7fafc;
            border: 1px solid #e2e8f0;
            border-radius: 8px;
            padding: 20px 25px;
        }}
        .meta-grid {{
            display: table;
            width: 100%;
        }}
        .meta-item {{
            display: table-cell;
            width: 25%;
            padding-right: 15px;
        }}
        .meta-label {{
            font-size: 9px;
            color: #718096;
            text-transform: uppercase;
            font-weight: 600;
            letter-spacing: 0.5px;
            margin-bottom: 5px;
        }}
        .meta-value {{
            font-size: 13px;
            color: #2d3748;
            font-weight: 600;
        }}
        .status-badge {{
            background: #48bb78;
            color: white;
            padding: 5px 12px;
            border-radius: 4px;
            font-size: 10px;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}
        .status-pending {{
            background: #ed8936;
        }}
        
        /* Bill To and Payment Details */
        .parties-section {{
            margin: 30px 0;
            display: table;
            width: 100%;
        }}
        .party-box {{
            display: table-cell;
            width: 48%;
            background: white;
            border: 2px solid #e2e8f0;
            border-radius: 8px;
            padding: 20px;
        }}
        .party-box:first-child {{
            margin-right: 4%;
        }}
        .party-title {{
            font-size: 10px;
            color: #667eea;
            text-transform: uppercase;
            font-weight: 700;
            letter-spacing: 1px;
            margin-bottom: 12px;
            border-bottom: 2px solid #667eea;
            padding-bottom: 8px;
        }}
        .party-name {{
            font-size: 14px;
            font-weight: 700;
            color: #2d3748;
            margin-bottom: 8px;
        }}
        .party-details {{
            font-size: 11px;
            color: #4a5568;
            line-height: 1.8;
        }}
        
        /* Items Table - Modern Design */
        .items-section {{
            margin: 30px 0;
        }}
        .items-table {{
            width: 100%;
            border-collapse: separate;
            border-spacing: 0;
            border: 2px solid #e2e8f0;
            border-radius: 8px;
            overflow: hidden;
        }}
        .items-table thead {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }}
        .items-table th {{
            padding: 15px 12px;
            text-align: left;
            font-size: 10px;
            text-transform: uppercase;
            font-weight: 700;
            letter-spacing: 0.8px;
        }}
        .items-table th:last-child,
        .items-table td:last-child {{
            text-align: right;
        }}
        .items-table tbody tr {{
            background: white;
            transition: background 0.2s;
        }}
        .items-table tbody tr:nth-child(even) {{
            background: #f7fafc;
        }}
        .items-table td {{
            padding: 16px 12px;
            border-bottom: 1px solid #e2e8f0;
            font-size: 11px;
            color: #4a5568;
        }}
        .items-table tbody tr:last-child td {{
            border-bottom: none;
        }}
        .item-desc {{
            color: #2d3748;
            font-weight: 600;
            margin-bottom: 4px;
            font-size: 12px;
        }}
        .item-detail {{
            color: #718096;
            font-size: 10px;
            font-style: italic;
        }}
        .text-right {{ text-align: right; }}
        .text-center {{ text-align: center; }}
        
        /* Totals Section - Right Aligned */
        .totals-section {{
            width: 45%;
            margin-left: auto;
            margin-top: 20px;
            background: #f7fafc;
            border: 2px solid #e2e8f0;
            border-radius: 8px;
            padding: 20px;
        }}
        .total-line {{
            display: table;
            width: 100%;
            padding: 10px 0;
            border-bottom: 1px solid #e2e8f0;
            font-size: 12px;
        }}
        .total-line:last-of-type {{
            border-bottom: none;
        }}
        .total-label {{
            display: table-cell;
            color: #4a5568;
            font-weight: 500;
        }}
        .total-value {{
            display: table-cell;
            text-align: right;
            color: #2d3748;
            font-weight: 600;
        }}
        .total-final {{
            margin-top: 15px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 18px 20px;
            border-radius: 6px;
            font-size: 16px;
            font-weight: 700;
        }}
        .total-final .total-label {{
            color: white;
            font-size: 14px;
        }}
        .total-final .total-value {{
            color: white;
            font-size: 20px;
        }}
        .amount-words {{
            text-align: right;
            color: #718096;
            font-size: 10px;
            margin-top: 8px;
            font-style: italic;
        }}
        
        /* Payment Details Box */
        .payment-section {{
            margin-top: 30px;
            background: #edf2f7;
            border: 2px solid #cbd5e0;
            border-radius: 8px;
            padding: 20px;
        }}
        .payment-title {{
            font-size: 11px;
            color: #667eea;
            text-transform: uppercase;
            font-weight: 700;
            letter-spacing: 0.8px;
            margin-bottom: 15px;
        }}
        .payment-grid {{
            display: table;
            width: 100%;
        }}
        .payment-row {{
            display: table-row;
        }}
        .payment-label {{
            display: table-cell;
            font-size: 11px;
            color: #718096;
            padding: 6px 0;
            font-weight: 500;
        }}
        .payment-value {{
            display: table-cell;
            font-size: 11px;
            color: #2d3748;
            font-weight: 600;
            text-align: right;
            padding: 6px 0;
        }}
        
        /* Terms & Notes */
        .notes-terms-section {{
            margin-top: 30px;
        }}
        .terms-box {{
            background: #fff6e5;
            border-left: 4px solid #f6ad55;
            padding: 20px;
            border-radius: 6px;
            margin-bottom: 15px;
        }}
        .terms-title {{
            font-size: 11px;
            color: #dd6b20;
            text-transform: uppercase;
            font-weight: 700;
            letter-spacing: 0.8px;
            margin-bottom: 10px;
        }}
        .terms-content {{
            color: #744210;
            font-size: 10px;
            line-height: 1.7;
        }}
        .notes-box {{
            background: #e6fffa;
            border-left: 4px solid #38b2ac;
            padding: 20px;
            border-radius: 6px;
        }}
        .notes-title {{
            font-size: 11px;
            color: #047857;
            text-transform: uppercase;
            font-weight: 700;
            letter-spacing: 0.8px;
            margin-bottom: 10px;
        }}
        .notes-content {{
            color: #065f46;
            font-size: 10px;
            line-height: 1.7;
        }}
        
        /* Footer */
        .footer {{
            margin-top: 40px;
            padding: 25px 50px;
            background: #f7fafc;
            text-align: center;
            border-top: 3px solid #e2e8f0;
        }}
        .footer-title {{
            font-size: 16px;
            color: #667eea;
            font-weight: 700;
            margin-bottom: 8px;
        }}
        .footer-text {{
            color: #718096;
            font-size: 10px;
            line-height: 1.6;
        }}
        .footer-note {{
            margin-top: 10px;
            font-size: 9px;
            color: #999;
        }}
    </style>
</head>
<body>
    <!-- Header with gradient background -->
    <div class="header">
        <div class="header-content">
            <div class="company-section">
                <div class="company-name">{vendor_name}</div>
                <div class="company-details">
                    {vendor_address}<br>
                    📞 {vendor_phone} | ✉ {vendor_email}<br>
                    GSTIN: {vendor_gstin}
                </div>
            </div>
            <div class="invoice-section">
                <div class="invoice-title">INVOICE</div>
                <div class="invoice-number">{invoice_number}</div>
            </div>
        </div>
    </div>
    
    <!-- Main Content -->
    <div class="content">
        <!-- Invoice Meta Information -->
        <div class="meta-section">
            <div class="meta-grid">
                <div class="meta-item">
                    <div class="meta-label">Invoice Date</div>
                    <div class="meta-value">{invoice_date}</div>
                </div>
                <div class="meta-item">
                    <div class="meta-label">Due Date</div>
                    <div class="meta-value">{due_date}</div>
                </div>
                <div class="meta-item">
                    <div class="meta-label">Status</div>
                    <div class="meta-value"><span class="status-badge {'status-pending' if status.lower() == 'pending' else ''}">{status.upper()}</span></div>
                </div>
                <div class="meta-item">
                    <div class="meta-label">Customer GSTIN</div>
                    <div class="meta-value">{customer_gstin}</div>
                </div>
            </div>
        </div>
        
        <!-- Bill To and Payment Details -->
        <div class="parties-section">
            <div class="party-box">
                <div class="party-title">Bill To</div>
                <div class="party-name">{customer_name}</div>
                <div class="party-details">
                    📍 {customer_address}<br>
                    📞 {customer_phone}<br>
                    ✉ {customer_email}
                </div>
            </div>
            <div class="party-box">
                <div class="party-title">Payment Details</div>
                <div class="party-details">
                    <strong>Bank Name:</strong> {bank_name}<br>
                    <strong>Account No:</strong> {account_number}<br>
                    <strong>IFSC Code:</strong> {ifsc_code}<br>
                    <strong>UPI ID:</strong> {upi_id}
                </div>
            </div>
        </div>
        
        <!-- Items Table -->
        <div class="items-section">
            <table class="items-table">
                <thead>
                    <tr>
                        <th style="width: 40px;">#</th>
                        <th>Item Description</th>
                        <th class="text-center" style="width: 70px;">Quantity</th>
                        <th style="width: 100px;">Rate</th>
                        <th style="width: 120px;">Amount</th>
                    </tr>
                </thead>
                <tbody>
                    {line_items_html}
                </tbody>
            </table>
        </div>
        
        <!-- Totals Section -->
        <div class="totals-section">
            <div class="total-line">
                <span class="total-label">Subtotal</span>
                <span class="total-value">₹{subtotal:,.2f}</span>
            </div>
            {tax_rows_html}
            <div class="total-line">
                <span class="total-label">Discount</span>
                <span class="total-value">- ₹{discount:,.2f}</span>
            </div>
            <div class="total-final">
                <span class="total-label">TOTAL AMOUNT</span>
                <span class="total-value">₹{total:,.2f}</span>
            </div>
            <div class="amount-words">Amount in words: {amount_words}</div>
        </div>
        
        <!-- Payment Details Section -->
        <div class="payment-section">
            <div class="payment-title">Bank Transfer Details</div>
            <div class="payment-grid">
                <div class="payment-row">
                    <span class="payment-label">Bank Name</span>
                    <span class="payment-value">{bank_name}</span>
                </div>
                <div class="payment-row">
                    <span class="payment-label">Account Number</span>
                    <span class="payment-value">{account_number}</span>
                </div>
                <div class="payment-row">
                    <span class="payment-label">IFSC Code</span>
                    <span class="payment-value">{ifsc_code}</span>
                </div>
                <div class="payment-row">
                    <span class="payment-label">UPI ID</span>
                    <span class="payment-value">{upi_id}</span>
                </div>
            </div>
        </div>
        
        <!-- Terms and Notes -->
        <div class="notes-terms-section">
            <div class="terms-box">
                <div class="terms-title">⚠ Terms & Conditions</div>
                <div class="terms-content">
                    Payment is due within 15 days from invoice date. Please include the invoice number in your payment reference. Late payments may incur interest charges as per company policy.
                </div>
            </div>
            <div class="notes-box">
                <div class="notes-title">📝 Notes</div>
                <div class="notes-content">
                    Thank you for your business! For any queries regarding this invoice, please contact us at {vendor_email} or {vendor_phone}.
                </div>
            </div>
        </div>
    </div>
    
    <!-- Footer -->
    <div class="footer">
        <div class="footer-title">Thank You For Your Business!</div>
        <div class="footer-text">
            This is a computer-generated invoice and does not require a physical signature<br>
            {vendor_name} | {vendor_email} | {vendor_phone}
        </div>
    </div>
</body>
</html>
        """
        return html
    
    def _number_to_words(self, amount: float) -> str:
        """Convert amount to words (simplified)"""
        try:
            amount_int = int(amount)
            return f"{amount_int} Rupees Only"
        except:
            return "Amount in Rupees"
    
    def generate_pdf(self, invoice: Dict, output_filename: str = None) -> str:
        """Generate PDF from HTML template"""
        try:
            if not output_filename:
                invoice_num = invoice.get('invoice_number', 'invoice').replace('/', '-')
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                output_filename = f"invoice_{invoice_num}_{timestamp}.pdf"
            
            output_path = os.path.join(self.output_dir, output_filename)
            
            # Generate HTML
            html_content = self._generate_html(invoice)
            
            # Convert to PDF
            with open(output_path, "wb") as pdf_file:
                pisa_status = pisa.CreatePDF(
                    html_content,
                    dest=pdf_file
                )
            
            if pisa_status.err:
                logger.error(f"PDF generation error: {pisa_status.err}")
                raise Exception("PDF generation failed")
            
            logger.info(f"✅ PDF generated successfully: {output_path}")
            return output_path
            
        except Exception as e:
            logger.error(f"❌ PDF generation failed: {str(e)}")
            raise
    
    def export_invoices_bulk(self, invoices: list, filename: str = None) -> str:
        """Export multiple invoices - generates first invoice"""
        if not invoices:
            raise ValueError("No invoices provided")
        
        # For now, just generate the first invoice
        # You can extend this to create multi-page PDFs
        return self.generate_pdf(invoices[0], filename)
