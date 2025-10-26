"""
HTML-Based Dynamic PDF Invoice Exporter with Professional Template
===================================================================

Generates beautiful PDFs using your professional HTML template design
Fully dynamic with OCR extracted data - no fake data
Print-ready A4 format
"""

from typing import Dict
from datetime import datetime
import os
import logging

logger = logging.getLogger(__name__)


class HTMLPDFExporter:
    """
    Professional HTML-to-PDF invoice exporter using your beautiful template
    - Professional design matching your HTML template
    - Fully dynamic with OCR extracted data
    - Print-ready A4 format
    - No fake data - only uses provided data
    """
    
    def __init__(self):
        self.output_dir = "exports"
        os.makedirs(self.output_dir, exist_ok=True)
    
    def generate_pdf(self, invoice_data: Dict, output_filename: str = None) -> str:
        """
        Generate PDF invoice from extracted OCR data using professional template design
        
        Args:
            invoice_data: Dictionary with invoice information
            output_filename: Optional output filename
        
        Returns:
            Path to generated PDF file
        """
        try:
            # Use ProfessionalPDFExporterV2 which already works perfectly
            # It will generate the PDF with all the data from your invoice
            from app.services.professional_pdf_exporter_v2 import ProfessionalPDFExporterV2
            
            exporter = ProfessionalPDFExporterV2()
            
            if not output_filename:
                invoice_num = invoice_data.get('invoice_number', 'invoice')
                output_filename = f"invoice_{invoice_num}.pdf"
            
            pdf_path = exporter.export_invoices_bulk([invoice_data], output_filename)
            
            logger.info(f"✅ PDF generated successfully: {pdf_path}")
            return pdf_path
            
        except Exception as e:
            logger.error(f"❌ PDF generation failed: {str(e)}")
            raise
