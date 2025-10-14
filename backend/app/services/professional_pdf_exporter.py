"""
🏆 PROFESSIONAL PDF EXPORTER - Industry Standard
=================================================

Creates beautifully formatted PDF invoices with:
- Company branding header
- Proper sections (Vendor, Invoice Details, Line Items, Tax Summary)
- Color coding and professional styling
- Print-ready format
"""

from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_RIGHT, TA_LEFT
from reportlab.pdfgen import canvas
from datetime import datetime
from typing import Dict, List, Any
import os


class ProfessionalPDFExporter:
    """
    Creates professional PDF invoices matching industry standards
    """
    
    def __init__(self):
        # Color scheme (professional blue/grey)
        self.colors = {
            'header': colors.HexColor('#1F4E78'),      # Dark blue
            'subheader': colors.HexColor('#5B9BD5'),   # Light blue
            'total_bg': colors.HexColor('#F2F2F2'),    # Light grey
            'warning': colors.HexColor('#FFC7CE'),     # Light red (unpaid)
            'success': colors.HexColor('#C6EFCE'),     # Light green (paid)
            'text': colors.HexColor('#000000'),        # Black
            'white': colors.white
        }
        
        # Styles
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()
    
    def _setup_custom_styles(self):
        """Setup custom paragraph styles"""
        
        # Title style
        self.styles.add(ParagraphStyle(
            name='InvoiceTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            textColor=self.colors['white'],
            alignment=TA_CENTER,
            spaceAfter=12,
            fontName='Helvetica-Bold'
        ))
        
        # Section header style
        self.styles.add(ParagraphStyle(
            name='SectionHeader',
            parent=self.styles['Heading2'],
            fontSize=12,
            textColor=self.colors['white'],
            alignment=TA_LEFT,
            spaceAfter=6,
            spaceBefore=12,
            fontName='Helvetica-Bold',
            backColor=self.colors['subheader']
        ))
        
        # Company info style
        self.styles.add(ParagraphStyle(
            name='CompanyInfo',
            parent=self.styles['Normal'],
            fontSize=10,
            textColor=colors.grey,
            alignment=TA_CENTER,
            spaceAfter=12,
            fontName='Helvetica-Oblique'
        ))
        
        # Field label style
        self.styles.add(ParagraphStyle(
            name='FieldLabel',
            parent=self.styles['Normal'],
            fontSize=10,
            textColor=colors.black,
            fontName='Helvetica-Bold'
        ))
    
    def export_invoice(self, invoice_data: Dict, filename: str = None) -> str:
        """
        Export invoice to professional PDF format
        
        Args:
            invoice_data: Invoice data dictionary
            filename: Optional custom filename
            
        Returns:
            Path to created PDF file
        """
        
        if not filename:
            invoice_num = invoice_data.get('invoice_number', 'INVOICE').replace('/', '_')
            filename = f"Invoice_{invoice_num}_{datetime.now().strftime('%Y%m%d')}.pdf"
        
        # Create PDF
        pdf = SimpleDocTemplate(
            filename,
            pagesize=A4,
            rightMargin=40,
            leftMargin=40,
            topMargin=40,
            bottomMargin=40
        )
        
        # Container for PDF elements
        story = []
        
        # Build PDF content
        story.extend(self._build_header())
        story.append(Spacer(1, 0.2 * inch))
        
        story.extend(self._build_vendor_section(invoice_data))
        story.append(Spacer(1, 0.15 * inch))
        
        story.extend(self._build_invoice_details(invoice_data))
        story.append(Spacer(1, 0.15 * inch))
        
        if invoice_data.get('line_items'):
            story.extend(self._build_line_items_table(invoice_data))
            story.append(Spacer(1, 0.15 * inch))
        
        story.extend(self._build_tax_summary(invoice_data))
        
        # Build PDF
        pdf.build(story)
        
        print(f"✅ Professional PDF invoice exported: {filename}")
        return filename
    
    def _build_header(self) -> List:
        """Build PDF header with branding"""
        elements = []
        
        # Title with background
        title_data = [['INVOICE']]
        title_table = Table(title_data, colWidths=[7 * inch])
        title_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), self.colors['header']),
            ('TEXTCOLOR', (0, 0), (-1, -1), self.colors['white']),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 24),
            ('TOPPADDING', (0, 0), (-1, -1), 15),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 15),
        ]))
        elements.append(title_table)
        
        # Company info
        company_info = Paragraph(
            "TrulyInvoice.in - Professional Invoice Management",
            self.styles['CompanyInfo']
        )
        elements.append(company_info)
        
        return elements
    
    def _build_vendor_section(self, data: Dict) -> List:
        """Build vendor information section"""
        elements = []
        
        # Section header
        header_data = [['VENDOR INFORMATION']]
        header_table = Table(header_data, colWidths=[7 * inch])
        header_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), self.colors['subheader']),
            ('TEXTCOLOR', (0, 0), (-1, -1), self.colors['white']),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 12),
            ('LEFTPADDING', (0, 0), (-1, -1), 12),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ]))
        elements.append(header_table)
        elements.append(Spacer(1, 0.1 * inch))
        
        # Vendor details
        vendor_data = [
            ['Vendor Name:', data.get('vendor_name', 'N/A')],
            ['GSTIN:', data.get('vendor_gstin', 'N/A')],
            ['Address:', data.get('vendor_address', 'N/A')],
        ]
        
        vendor_table = Table(vendor_data, colWidths=[1.5 * inch, 5.5 * inch])
        vendor_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('LEFTPADDING', (0, 0), (-1, -1), 12),
            ('RIGHTPADDING', (0, 0), (-1, -1), 12),
            ('TOPPADDING', (0, 0), (-1, -1), 4),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ]))
        elements.append(vendor_table)
        
        return elements
    
    def _build_invoice_details(self, data: Dict) -> List:
        """Build invoice details section"""
        elements = []
        
        # Section header
        header_data = [['INVOICE DETAILS']]
        header_table = Table(header_data, colWidths=[7 * inch])
        header_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), self.colors['subheader']),
            ('TEXTCOLOR', (0, 0), (-1, -1), self.colors['white']),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 12),
            ('LEFTPADDING', (0, 0), (-1, -1), 12),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ]))
        elements.append(header_table)
        elements.append(Spacer(1, 0.1 * inch))
        
        # Payment status styling
        payment_status = data.get('payment_status', 'unpaid').upper()
        status_color = self.colors['success'] if 'PAID' in payment_status else self.colors['warning']
        
        # Invoice details (two columns)
        details_data = [
            ['Invoice Number:', data.get('invoice_number', 'N/A'), 'Payment Status:', payment_status],
            ['Invoice Date:', data.get('invoice_date', 'N/A'), 'Currency:', data.get('currency', 'INR')],
            ['Due Date:', data.get('due_date', 'N/A'), 'Created At:', data.get('created_at', 'N/A')[:10] if data.get('created_at') else 'N/A'],
        ]
        
        details_table = Table(details_data, colWidths=[1.3 * inch, 2 * inch, 1.3 * inch, 2.4 * inch])
        
        style_list = [
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (2, 0), (2, -1), 'Helvetica-Bold'),
            ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
            ('FONTNAME', (3, 0), (3, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('LEFTPADDING', (0, 0), (-1, -1), 12),
            ('RIGHTPADDING', (0, 0), (-1, -1), 12),
            ('TOPPADDING', (0, 0), (-1, -1), 4),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
            ('BACKGROUND', (3, 0), (3, 0), status_color),  # Payment status background
        ]
        
        details_table.setStyle(TableStyle(style_list))
        elements.append(details_table)
        
        return elements
    
    def _build_line_items_table(self, data: Dict) -> List:
        """Build line items table"""
        elements = []
        
        # Section header
        header_data = [['LINE ITEMS']]
        header_table = Table(header_data, colWidths=[7 * inch])
        header_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), self.colors['subheader']),
            ('TEXTCOLOR', (0, 0), (-1, -1), self.colors['white']),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 12),
            ('LEFTPADDING', (0, 0), (-1, -1), 12),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ]))
        elements.append(header_table)
        elements.append(Spacer(1, 0.1 * inch))
        
        # Table header
        table_data = [['#', 'Description', 'HSN/SAC', 'Qty', 'Rate', 'Amount']]
        
        # Add line items
        for idx, item in enumerate(data.get('line_items', []), start=1):
            table_data.append([
                str(idx),
                str(item.get('description', 'N/A'))[:40],  # Truncate long descriptions
                str(item.get('hsn_sac', item.get('hsn', 'N/A'))),
                str(item.get('quantity', 1)),
                f"₹{float(item.get('rate', 0)):,.2f}",
                f"₹{float(item.get('amount', 0)):,.2f}"
            ])
        
        # Create table
        items_table = Table(table_data, colWidths=[0.4 * inch, 2.5 * inch, 0.9 * inch, 0.6 * inch, 1.3 * inch, 1.3 * inch])
        
        # Table styling
        style_list = [
            # Header row
            ('BACKGROUND', (0, 0), (-1, 0), self.colors['total_bg']),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('TOPPADDING', (0, 0), (-1, 0), 8),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
            
            # Data rows
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 9),
            ('ALIGN', (0, 1), (0, -1), 'CENTER'),  # # column
            ('ALIGN', (1, 1), (1, -1), 'LEFT'),    # Description
            ('ALIGN', (2, 1), (2, -1), 'CENTER'),  # HSN
            ('ALIGN', (3, 1), (3, -1), 'CENTER'),  # Qty
            ('ALIGN', (4, 1), (-1, -1), 'RIGHT'),  # Rate, Amount
            
            # Borders
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('BOX', (0, 0), (-1, -1), 1, colors.black),
            
            # Padding
            ('LEFTPADDING', (0, 0), (-1, -1), 6),
            ('RIGHTPADDING', (0, 0), (-1, -1), 6),
            ('TOPPADDING', (0, 1), (-1, -1), 5),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 5),
        ]
        
        items_table.setStyle(TableStyle(style_list))
        elements.append(items_table)
        
        return elements
    
    def _build_tax_summary(self, data: Dict) -> List:
        """Build tax summary and totals section"""
        elements = []
        
        # Section header
        header_data = [['TAX SUMMARY & TOTALS']]
        header_table = Table(header_data, colWidths=[7 * inch])
        header_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), self.colors['subheader']),
            ('TEXTCOLOR', (0, 0), (-1, -1), self.colors['white']),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 12),
            ('LEFTPADDING', (0, 0), (-1, -1), 12),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ]))
        elements.append(header_table)
        elements.append(Spacer(1, 0.1 * inch))
        
        # Build summary data (right-aligned)
        summary_data = []
        
        # Add amounts (handle None values properly)
        subtotal = data.get('subtotal') or 0
        cgst = data.get('cgst') or 0
        sgst = data.get('sgst') or 0
        igst = data.get('igst') or 0
        total_amount = data.get('total_amount') or 0
        
        if float(subtotal) > 0:
            summary_data.append(['', 'Subtotal:', f"₹{float(subtotal):,.2f}"])
        
        if float(cgst) > 0:
            summary_data.append(['', 'CGST:', f"₹{float(cgst):,.2f}"])
        
        if float(sgst) > 0:
            summary_data.append(['', 'SGST:', f"₹{float(sgst):,.2f}"])
        
        if float(igst) > 0:
            summary_data.append(['', 'IGST:', f"₹{float(igst):,.2f}"])
        
        # Total (highlighted)
        summary_data.append(['', 'TOTAL AMOUNT:', f"₹{float(total_amount):,.2f}"])
        
        # Create table
        summary_table = Table(summary_data, colWidths=[3.5 * inch, 2 * inch, 1.5 * inch])
        
        # Styling
        style_list = [
            ('FONTNAME', (1, 0), (1, -2), 'Helvetica'),
            ('FONTNAME', (2, 0), (2, -2), 'Helvetica'),
            ('FONTSIZE', (1, 0), (2, -2), 10),
            ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
            ('ALIGN', (2, 0), (2, -1), 'RIGHT'),
            
            # Total row (last row)
            ('FONTNAME', (1, -1), (2, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (1, -1), (2, -1), 11),
            ('BACKGROUND', (1, -1), (2, -1), self.colors['total_bg']),
            ('LINEABOVE', (1, -1), (2, -1), 2, colors.black),
            ('LINEBELOW', (1, -1), (2, -1), 2, colors.black),
            
            # Padding
            ('TOPPADDING', (1, 0), (2, -1), 5),
            ('BOTTOMPADDING', (1, 0), (2, -1), 5),
            ('RIGHTPADDING', (2, 0), (2, -1), 12),
        ]
        
        summary_table.setStyle(TableStyle(style_list))
        elements.append(summary_table)
        
        return elements


# ============ USAGE EXAMPLE ============
if __name__ == "__main__":
    # Sample invoice data
    sample_invoice = {
        'invoice_number': 'IN67/2025-26',
        'invoice_date': '2025-06-04',
        'due_date': 'N/A',
        'vendor_name': 'INNOVATION',
        'vendor_gstin': '18AABCI4851C1ZB',
        'vendor_address': 'Pattan Bazar, Guwahati, Assam',
        'currency': 'INR',
        'line_items': [
            {
                'description': 'Product A - Professional Services',
                'hsn_sac': '998314',
                'quantity': 2,
                'rate': 15000.00,
                'amount': 30000.00
            },
            {
                'description': 'Product B - Consulting',
                'hsn_sac': '998315',
                'quantity': 1,
                'rate': 10000.00,
                'amount': 10000.00
            }
        ],
        'subtotal': 33898.31,
        'cgst': 3050.85,
        'sgst': 3050.85,
        'igst': 0,
        'total_amount': 40000.00,
        'payment_status': 'unpaid',
        'created_at': '2025-10-13T10:30:00Z'
    }
    
    exporter = ProfessionalPDFExporter()
    exporter.export_invoice(sample_invoice, 'Professional_Invoice_Demo.pdf')
    
    print("\n✅ Professional PDF invoice created!")
    print("Open 'Professional_Invoice_Demo.pdf' to see the professional format")
