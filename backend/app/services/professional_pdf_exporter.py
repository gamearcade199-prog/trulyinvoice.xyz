"""
🏆 PROFESSIONAL PDF EXPORTER - Industry Standard
=================================================

Creates beautifully formatted PDF invoices with:
- Company branding header
- Proper sections (Vendor, Invoice Details, Line Items, Tax Summary)
- Color coding and professional styling
- Print-ready format
- ANTI-OVERLAP FORMATTING: Optimized spacing, padding, and text truncation
  to prevent text overlapping in all sections
"""

from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image, PageBreak
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
            invoice_num = invoice_data.get('invoice_number') or 'INVOICE'
            invoice_num = str(invoice_num).replace('/', '_')
            filename = f"Invoice_{invoice_num}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        
        # Create PDF with improved margins to prevent text crowding
        pdf = SimpleDocTemplate(
            filename,
            pagesize=A4,
            rightMargin=50,  # Increased from 40
            leftMargin=50,   # Increased from 40
            topMargin=50,    # Increased from 40
            bottomMargin=50  # Increased from 40
        )
        
        # Container for PDF elements
        story = []
        
        # Build PDF content with improved spacing
        story.extend(self._build_header())
        story.append(Spacer(1, 0.25 * inch))  # Increased spacing
        
        story.extend(self._build_vendor_section(invoice_data))
        story.append(Spacer(1, 0.2 * inch))   # Increased spacing
        
        story.extend(self._build_invoice_details(invoice_data))
        story.append(Spacer(1, 0.2 * inch))   # Increased spacing
        
        if invoice_data.get('line_items'):
            story.extend(self._build_line_items_table(invoice_data))
            story.append(Spacer(1, 0.2 * inch))   # Increased spacing
        
        story.extend(self._build_tax_summary(invoice_data))
        
        # Build PDF
        pdf.build(story)
        
        print(f"✅ Professional PDF invoice exported: {filename}")
        return filename
    
    def _build_invoice_info(self, invoice: Dict) -> List:
        """Build basic invoice information for bulk export"""
        elements = []
        
        # Basic info
        info_data = [
            ['Invoice:', invoice.get('invoice_number', 'N/A'), 'Date:', invoice.get('invoice_date', 'N/A')],
            ['Vendor:', invoice.get('vendor_name', 'N/A'), 'Amount:', f"₹{invoice.get('total_amount', 0):,.2f}"]
        ]
        
        info_table = Table(info_data, colWidths=[1*inch, 2*inch, 1*inch, 2*inch])
        info_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (2, 0), (2, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
        ]))
        
        elements.append(info_table)
        elements.append(Spacer(1, 0.1 * inch))
        return elements
    
    def _build_line_items(self, invoice: Dict) -> List:
        """Build line items for bulk export"""
        elements = []
        
        if not invoice.get('line_items'):
            return elements
            
        # Simple line items table
        table_data = [['Item', 'Qty', 'Rate', 'Amount']]
        for item in invoice.get('line_items', []):
            table_data.append([
                str(item.get('description', 'N/A'))[:30],
                str(item.get('quantity', 1)),
                f"₹{float(item.get('rate', 0)):,.0f}",
                f"₹{float(item.get('amount', 0)):,.0f}"
            ])
        
        items_table = Table(table_data, colWidths=[3*inch, 0.8*inch, 1.2*inch, 1.2*inch])
        items_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        
        elements.append(items_table)
        return elements
    
    def export_invoices_bulk(self, invoices: List[Dict], filename: str = None) -> str:
        """Export multiple invoices to a single PDF file"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"bulk_invoices_professional_{timestamp}.pdf"
        
        # Create PDF with multiple invoices with improved margins
        pdf = SimpleDocTemplate(
            filename,
            pagesize=A4,
            rightMargin=50,  # Increased from 40
            leftMargin=50,   # Increased from 40
            topMargin=50,    # Increased from 40
            bottomMargin=50  # Increased from 40
        )
        
        story = []
        
        # Title page
        title_data = [['BULK INVOICE EXPORT']]
        title_table = Table(title_data, colWidths=[7 * inch])
        title_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.darkblue),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 24),
            ('TOPPADDING', (0, 0), (-1, -1), 20),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 20),
        ]))
        
        story.append(title_table)
        story.append(Spacer(1, 0.5 * inch))
        
        # Summary table
        summary_data = [['Invoice #', 'Date', 'Vendor', 'Amount', 'Status']]
        for invoice in invoices:
            summary_data.append([
                invoice.get('invoice_number', 'N/A'),
                invoice.get('invoice_date', 'N/A'),
                invoice.get('vendor_name', 'N/A')[:20],
                f"₹{invoice.get('total_amount', 0):,.2f}",
                invoice.get('payment_status', 'N/A')
            ])
        
        summary_table = Table(summary_data, colWidths=[1.2*inch, 1*inch, 2*inch, 1.2*inch, 1*inch])
        summary_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey])
        ]))
        
        story.append(summary_table)
        story.append(PageBreak())
        
        # Individual invoices (first 5 only to prevent huge files)
        for i, invoice in enumerate(invoices):
            if i > 0:
                story.append(PageBreak())
            
            # Add invoice header
            story.append(Paragraph(f"Invoice {i+1}/{len(invoices)}", 
                                 getSampleStyleSheet()['Heading2']))
            story.append(Spacer(1, 0.2 * inch))
            
            # Add basic invoice details
            story.extend(self._build_invoice_info(invoice))
            story.extend(self._build_line_items(invoice))
            story.extend(self._build_tax_summary(invoice))
        
        pdf.build(story)
        print(f"✅ Bulk PDF exported: {filename} ({len(invoices)} invoices)")
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
        """Build comprehensive vendor and customer information section"""
        elements = []
        
        # VENDOR INFORMATION Section
        vendor_header_data = [['VENDOR INFORMATION']]
        vendor_header_table = Table(vendor_header_data, colWidths=[7 * inch])
        vendor_header_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), self.colors['subheader']),
            ('TEXTCOLOR', (0, 0), (-1, -1), self.colors['white']),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 12),
            ('LEFTPADDING', (0, 0), (-1, -1), 12),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ]))
        elements.append(vendor_header_table)
        elements.append(Spacer(1, 0.1 * inch))
        
        # Comprehensive vendor details with better text handling
        vendor_data = [
            ['Vendor Name:', str(data.get('vendor_name', 'N/A'))[:25], 'GSTIN:', str(data.get('vendor_gstin', 'N/A'))[:18]],
            ['PAN:', str(data.get('vendor_pan', 'N/A'))[:12], 'Email:', str(data.get('vendor_email', 'N/A'))[:25]],
            ['Phone:', str(data.get('vendor_phone', 'N/A'))[:15], 'State:', str(data.get('vendor_state', 'N/A'))[:20]],
            ['Address:', str(data.get('vendor_address', 'N/A'))[:35], 'Pincode:', str(data.get('vendor_pincode', 'N/A'))[:10]],
        ]
        
        vendor_table = Table(vendor_data, colWidths=[1.4 * inch, 2.1 * inch, 1.4 * inch, 2.1 * inch])
        vendor_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (2, 0), (2, -1), 'Helvetica-Bold'),
            ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
            ('FONTNAME', (3, 0), (3, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),  # Slightly smaller font
            ('LEFTPADDING', (0, 0), (-1, -1), 14),  # Increased padding
            ('RIGHTPADDING', (0, 0), (-1, -1), 14),
            ('TOPPADDING', (0, 0), (-1, -1), 5),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ]))
        elements.append(vendor_table)
        elements.append(Spacer(1, 0.2 * inch))
        
        # CUSTOMER INFORMATION Section
        customer_header_data = [['CUSTOMER INFORMATION']]
        customer_header_table = Table(customer_header_data, colWidths=[7 * inch])
        customer_header_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), self.colors['subheader']),
            ('TEXTCOLOR', (0, 0), (-1, -1), self.colors['white']),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 12),
            ('LEFTPADDING', (0, 0), (-1, -1), 12),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ]))
        elements.append(customer_header_table)
        elements.append(Spacer(1, 0.1 * inch))
        
        # Customer details with better text handling
        customer_data = [
            ['Customer Name:', str(data.get('customer_name', 'N/A'))[:25], 'GSTIN:', str(data.get('customer_gstin', 'N/A'))[:18]],
            ['Phone:', str(data.get('customer_phone', 'N/A'))[:15], 'State:', str(data.get('customer_state', 'N/A'))[:20]],
            ['Address:', str(data.get('customer_address', 'N/A'))[:35], '', ''],
        ]
        
        customer_table = Table(customer_data, colWidths=[1.4 * inch, 2.1 * inch, 1.4 * inch, 2.1 * inch])
        customer_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (2, 0), (2, -1), 'Helvetica-Bold'),
            ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
            ('FONTNAME', (3, 0), (3, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),  # Slightly smaller font
            ('LEFTPADDING', (0, 0), (-1, -1), 14),  # Increased padding
            ('RIGHTPADDING', (0, 0), (-1, -1), 14),
            ('TOPPADDING', (0, 0), (-1, -1), 5),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ]))
        elements.append(customer_table)
        
        # Banking Information (if available)
        if data.get('bank_name') or data.get('account_number') or data.get('ifsc_code'):
            elements.append(Spacer(1, 0.2 * inch))
            
            bank_header_data = [['BANKING INFORMATION']]
            bank_header_table = Table(bank_header_data, colWidths=[7 * inch])
            bank_header_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, -1), self.colors['subheader']),
                ('TEXTCOLOR', (0, 0), (-1, -1), self.colors['white']),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 12),
                ('LEFTPADDING', (0, 0), (-1, -1), 12),
                ('TOPPADDING', (0, 0), (-1, -1), 8),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ]))
            elements.append(bank_header_table)
            elements.append(Spacer(1, 0.1 * inch))
            
            bank_data = [
                ['Bank Name:', str(data.get('bank_name', 'N/A'))[:25], 'Account Number:', str(data.get('account_number', 'N/A'))[:18]],
                ['IFSC Code:', str(data.get('ifsc_code', 'N/A'))[:12], 'SWIFT Code:', str(data.get('swift_code', 'N/A'))[:12]],
            ]
            
            bank_table = Table(bank_data, colWidths=[1.4 * inch, 2.1 * inch, 1.4 * inch, 2.1 * inch])
            bank_table.setStyle(TableStyle([
                ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
                ('FONTNAME', (2, 0), (2, -1), 'Helvetica-Bold'),
                ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
                ('FONTNAME', (3, 0), (3, -1), 'Helvetica'),
                ('FONTSIZE', (0, 0), (-1, -1), 9),  # Slightly smaller font
                ('LEFTPADDING', (0, 0), (-1, -1), 14),  # Increased padding
                ('RIGHTPADDING', (0, 0), (-1, -1), 14),
                ('TOPPADDING', (0, 0), (-1, -1), 5),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
            ]))
            elements.append(bank_table)

        return elements
    
    def _build_invoice_details(self, data: Dict) -> List:
        """Build comprehensive invoice details section"""
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
        
        # Core invoice details (enhanced) with better text handling
        details_data = [
            ['Invoice Number:', str(data.get('invoice_number', 'N/A'))[:20], 'Payment Status:', payment_status],
            ['Invoice Date:', str(data.get('invoice_date', 'N/A'))[:12], 'Due Date:', str(data.get('due_date', 'N/A'))[:12]],
            ['Currency:', str(data.get('currency', 'INR'))[:5], 'Invoice Type:', str(data.get('invoice_type', 'Standard'))[:15]],
            ['Payment Method:', str(data.get('payment_method', 'N/A'))[:18], 'Payment Terms:', str(data.get('payment_terms', 'N/A'))[:20]],
        ]
        
        # Add PO information if available
        if data.get('po_number') or data.get('po_date'):
            details_data.extend([
                ['PO Number:', str(data.get('po_number', 'N/A'))[:15], 'PO Date:', str(data.get('po_date', 'N/A'))[:12]],
            ])
        
        # Add GST information
        if data.get('place_of_supply') or data.get('hsn_code') or data.get('sac_code'):
            details_data.extend([
                ['Place of Supply:', str(data.get('place_of_supply', 'N/A'))[:18], 'Supply Type:', str(data.get('supply_type', 'N/A'))[:15]],
                ['HSN Code:', str(data.get('hsn_code', 'N/A'))[:12], 'SAC Code:', str(data.get('sac_code', 'N/A'))[:12]],
            ])
        
        details_table = Table(details_data, colWidths=[1.5 * inch, 1.8 * inch, 1.5 * inch, 2.2 * inch])
        
        style_list = [
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (2, 0), (2, -1), 'Helvetica-Bold'),
            ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
            ('FONTNAME', (3, 0), (3, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),  # Slightly smaller font
            ('LEFTPADDING', (0, 0), (-1, -1), 14),  # Increased padding
            ('RIGHTPADDING', (0, 0), (-1, -1), 14),
            ('TOPPADDING', (0, 0), (-1, -1), 5),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ]
        
        # Highlight payment status
        for i, row in enumerate(details_data):
            if 'Payment Status:' in row:
                style_list.append(('BACKGROUND', (3, i), (3, i), status_color))
                style_list.append(('FONTNAME', (3, i), (3, i), 'Helvetica-Bold'))
        
        details_table.setStyle(TableStyle(style_list))
        elements.append(details_table)
        
        # Industry-specific information section
        industry_data = []
        
        # Hotel & Hospitality
        if data.get('arrival_date') or data.get('room_number') or data.get('booking_reference'):
            industry_data.extend([
                ['=== HOSPITALITY DETAILS ===', '', '', ''],
                ['Arrival Date:', data.get('arrival_date', 'N/A'), 'Departure Date:', data.get('departure_date', 'N/A')],
                ['Room Number:', data.get('room_number', 'N/A'), 'Guest Count:', data.get('guest_count', 'N/A')],
                ['Booking Reference:', data.get('booking_reference', 'N/A'), '', ''],
            ])
        
        # E-commerce & Retail
        if data.get('order_id') or data.get('tracking_number'):
            industry_data.extend([
                ['=== E-COMMERCE DETAILS ===', '', '', ''],
                ['Order ID:', data.get('order_id', 'N/A'), 'Tracking Number:', data.get('tracking_number', 'N/A')],
                ['Shipping Method:', data.get('shipping_method', 'N/A'), 'Delivery Date:', data.get('delivery_date', 'N/A')],
            ])
        
        # Manufacturing
        if data.get('batch_number') or data.get('quality_certificate'):
            industry_data.extend([
                ['=== MANUFACTURING DETAILS ===', '', '', ''],
                ['Batch Number:', data.get('batch_number', 'N/A'), 'Quality Certificate:', data.get('quality_certificate', 'N/A')],
                ['Warranty Period:', data.get('warranty_period', 'N/A'), '', ''],
            ])
        
        # Professional Services
        if data.get('project_name') or data.get('consultant_name'):
            industry_data.extend([
                ['=== PROFESSIONAL SERVICES ===', '', '', ''],
                ['Project Name:', data.get('project_name', 'N/A'), 'Consultant Name:', data.get('consultant_name', 'N/A')],
                ['Hourly Rate:', f"₹{data.get('hourly_rate', 0):.2f}" if data.get('hourly_rate') else 'N/A', 
                 'Hours Worked:', f"{data.get('hours_worked', 0):.1f}" if data.get('hours_worked') else 'N/A'],
            ])
        
        # Add industry-specific section if data exists
        if industry_data:
            elements.append(Spacer(1, 0.15 * inch))
            
            industry_table = Table(industry_data, colWidths=[1.5 * inch, 1.8 * inch, 1.5 * inch, 2.2 * inch])
            industry_style = [
                ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
                ('FONTNAME', (2, 0), (2, -1), 'Helvetica-Bold'),
                ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
                ('FONTNAME', (3, 0), (3, -1), 'Helvetica'),
                ('FONTSIZE', (0, 0), (-1, -1), 8),  # Smaller font for industry details
                ('LEFTPADDING', (0, 0), (-1, -1), 14),  # Increased padding
                ('RIGHTPADDING', (0, 0), (-1, -1), 14),
                ('TOPPADDING', (0, 0), (-1, -1), 4),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
            ]
            
            # Style section headers
            for i, row in enumerate(industry_data):
                if '===' in str(row[0]):
                    industry_style.extend([
                        ('SPAN', (0, i), (3, i)),
                        ('BACKGROUND', (0, i), (3, i), colors.lightgrey),
                        ('FONTNAME', (0, i), (3, i), 'Helvetica-Bold'),
                        ('ALIGN', (0, i), (3, i), 'CENTER'),
                    ])
            
            industry_table.setStyle(TableStyle(industry_style))
            elements.append(industry_table)
        
        details_table.setStyle(TableStyle(style_list))
        elements.append(details_table)
        
        return elements
    
    def _build_line_items_table(self, data: Dict) -> List:
        """Build line items table with improved spacing to prevent text overlap"""
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
        elements.append(Spacer(1, 0.15 * inch))  # Increased spacing
        
        # Table header
        table_data = [['#', 'Description', 'HSN/SAC', 'Qty', 'Rate', 'Amount']]
        
        # Add line items with better text handling
        for idx, item in enumerate(data.get('line_items', []), start=1):
            # Truncate description more conservatively and handle long text better
            description = str(item.get('description', 'N/A'))
            if len(description) > 35:  # Reduced from 40
                description = description[:32] + "..."  # Better truncation
            
            table_data.append([
                str(idx),
                description,
                str(item.get('hsn_sac', item.get('hsn', 'N/A'))),
                str(item.get('quantity', 1)),
                f"₹{float(item.get('rate', 0)):,.2f}",
                f"₹{float(item.get('amount', 0)):,.2f}"
            ])
        
        # Create table with better column widths and spacing
        items_table = Table(table_data, colWidths=[0.5 * inch, 2.2 * inch, 1.0 * inch, 0.7 * inch, 1.4 * inch, 1.4 * inch])
        
        # Table styling with increased padding to prevent overlap
        style_list = [
            # Header row
            ('BACKGROUND', (0, 0), (-1, 0), self.colors['total_bg']),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 9),  # Slightly smaller font
            ('TOPPADDING', (0, 0), (-1, 0), 10),  # Increased padding
            ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
            
            # Data rows
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 8),  # Smaller font for data
            ('ALIGN', (0, 1), (0, -1), 'CENTER'),  # # column
            ('ALIGN', (1, 1), (1, -1), 'LEFT'),    # Description
            ('ALIGN', (2, 1), (2, -1), 'CENTER'),  # HSN
            ('ALIGN', (3, 1), (3, -1), 'CENTER'),  # Qty
            ('ALIGN', (4, 1), (-1, -1), 'RIGHT'),  # Rate, Amount
            
            # Borders
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('BOX', (0, 0), (-1, -1), 1, colors.black),
            
            # Increased padding to prevent text overlap
            ('LEFTPADDING', (0, 0), (-1, -1), 8),
            ('RIGHTPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 1), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
        ]
        
        items_table.setStyle(TableStyle(style_list))
        elements.append(items_table)
        
        return elements
    
    def _build_tax_summary(self, data: Dict) -> List:
        """Build comprehensive tax summary and totals section"""
        elements = []
        
        # Section header
        header_data = [['COMPREHENSIVE TAX SUMMARY & FINANCIAL BREAKDOWN']]
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
        
        # Build comprehensive financial summary
        summary_data = []
        
        # Handle None values properly for all financial fields
        subtotal = float(data.get('subtotal') or 0)
        taxable_amount = float(data.get('taxable_amount') or 0)
        discount = float(data.get('discount') or 0)
        shipping_charges = float(data.get('shipping_charges') or 0)
        other_charges = float(data.get('other_charges') or 0)
        roundoff = float(data.get('roundoff') or 0)
        
        # GST & Tax amounts
        cgst = float(data.get('cgst') or 0)
        sgst = float(data.get('sgst') or 0)
        igst = float(data.get('igst') or 0)
        ugst = float(data.get('ugst') or 0)
        cess = float(data.get('cess') or 0)
        total_gst = float(data.get('total_gst') or 0)
        
        # Additional taxes
        vat = float(data.get('vat') or 0)
        service_tax = float(data.get('service_tax') or 0)
        tds_amount = float(data.get('tds_amount') or 0)
        tcs_amount = float(data.get('tcs_amount') or 0)
        
        total_amount = float(data.get('total_amount') or 0)
        
        # Financial Breakdown Section
        if subtotal > 0 or taxable_amount > 0:
            summary_data.append(['', 'AMOUNT BREAKDOWN', ''])
            if subtotal > 0:
                summary_data.append(['', 'Subtotal:', f"₹{subtotal:,.2f}"])
            if taxable_amount > 0 and taxable_amount != subtotal:
                summary_data.append(['', 'Taxable Amount:', f"₹{taxable_amount:,.2f}"])
            if discount > 0:
                summary_data.append(['', 'Discount:', f"-₹{discount:,.2f}"])
            if shipping_charges > 0:
                summary_data.append(['', 'Shipping Charges:', f"₹{shipping_charges:,.2f}"])
            if other_charges > 0:
                summary_data.append(['', 'Other Charges:', f"₹{other_charges:,.2f}"])
            if roundoff != 0:
                summary_data.append(['', 'Round Off:', f"₹{roundoff:,.2f}"])
            summary_data.append(['', '', ''])  # Separator
        
        # GST Section
        gst_total = cgst + sgst + igst + ugst + cess
        if gst_total > 0:
            summary_data.append(['', 'GST BREAKDOWN', ''])
            if cgst > 0:
                summary_data.append(['', 'CGST:', f"₹{cgst:,.2f}"])
            if sgst > 0:
                summary_data.append(['', 'SGST:', f"₹{sgst:,.2f}"])
            if igst > 0:
                summary_data.append(['', 'IGST:', f"₹{igst:,.2f}"])
            if ugst > 0:
                summary_data.append(['', 'UGST:', f"₹{ugst:,.2f}"])
            if cess > 0:
                summary_data.append(['', 'CESS:', f"₹{cess:,.2f}"])
            if total_gst > 0:
                summary_data.append(['', 'Total GST:', f"₹{total_gst:,.2f}"])
            summary_data.append(['', '', ''])  # Separator
        
        # Additional Taxes Section
        other_tax_total = vat + service_tax
        if other_tax_total > 0:
            summary_data.append(['', 'OTHER TAXES', ''])
            if vat > 0:
                summary_data.append(['', 'VAT:', f"₹{vat:,.2f}"])
            if service_tax > 0:
                summary_data.append(['', 'Service Tax:', f"₹{service_tax:,.2f}"])
            summary_data.append(['', '', ''])  # Separator
        
        # TDS/TCS Section
        if tds_amount > 0 or tcs_amount > 0:
            summary_data.append(['', 'TAX DEDUCTIONS', ''])
            if tds_amount > 0:
                summary_data.append(['', 'TDS Amount:', f"-₹{tds_amount:,.2f}"])
            if tcs_amount > 0:
                summary_data.append(['', 'TCS Amount:', f"₹{tcs_amount:,.2f}"])
            summary_data.append(['', '', ''])  # Separator
        
        # Final Total (highlighted)
        summary_data.append(['', 'FINAL TOTAL AMOUNT:', f"₹{total_amount:,.2f}"])
        
        # Create table
        summary_table = Table(summary_data, colWidths=[2.5 * inch, 2.5 * inch, 2 * inch])
        
        # Styling with better spacing
        style_list = [
            ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
            ('FONTNAME', (2, 0), (2, -1), 'Helvetica'),
            ('FONTSIZE', (1, 0), (2, -1), 9),  # Slightly smaller font
            ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
            ('ALIGN', (2, 0), (2, -1), 'RIGHT'),
            
            # Increased padding to prevent text overlap
            ('TOPPADDING', (1, 0), (2, -1), 5),
            ('BOTTOMPADDING', (1, 0), (2, -1), 5),
            ('RIGHTPADDING', (2, 0), (2, -1), 15),  # More right padding
            ('LEFTPADDING', (1, 0), (1, -1), 10),
        ]
        
        # Style section headers and final total
        for i, row in enumerate(summary_data):
            if len(row) >= 2:
                # Section headers (BREAKDOWN, GST BREAKDOWN, etc.)
                if 'BREAKDOWN' in str(row[1]) or 'TAXES' in str(row[1]) or 'DEDUCTIONS' in str(row[1]) or 'QUALITY' in str(row[1]):
                    style_list.extend([
                        ('SPAN', (1, i), (2, i)),
                        ('FONTNAME', (1, i), (2, i), 'Helvetica-Bold'),
                        ('FONTSIZE', (1, i), (2, i), 11),
                        ('BACKGROUND', (1, i), (2, i), colors.lightgrey),
                        ('ALIGN', (1, i), (2, i), 'CENTER'),
                    ])
                
                # Final total row
                elif 'FINAL TOTAL' in str(row[1]):
                    style_list.extend([
                        ('FONTNAME', (1, i), (2, i), 'Helvetica-Bold'),
                        ('FONTSIZE', (1, i), (2, i), 12),
                        ('BACKGROUND', (1, i), (2, i), self.colors['total_bg']),
                        ('LINEABOVE', (1, i), (2, i), 2, colors.black),
                        ('LINEBELOW', (1, i), (2, i), 2, colors.black),
                    ])
        
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
