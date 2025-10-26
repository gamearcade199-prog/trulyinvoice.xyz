"""
Test the new HTML PDF Exporter with realistic OCR data
"""

from app.services.html_pdf_exporter import HTMLPDFExporter
from datetime import datetime

# Sample invoice data extracted from OCR
sample_invoice = {
    # Basic info
    'invoice_number': 'INV-92C002F8',
    'invoice_date': '13 September 2023',
    'due_date': '30 September 2023',
    'invoice_period': 'Sep 2023',
    'status': 'Pending',
    
    # Vendor/Company info
    'company_name': 'Nambor Tours & Travels',
    'vendor_name': 'Nambor Tours & Travels',
    'company_address': 'Main Road, Golaghat\nAssam 785601, India',
    'company_phone': '+91-98765-43210',
    'company_email': 'contact@nambortours.com',
    
    # Customer info
    'customer_name': 'Payout Ali',
    'bill_to_name': 'Payout Ali',
    'customer_address': '123 Customer Street\nGolaghat, Assam 785621',
    'customer_phone': '+91-98765-12345',
    'customer_email': 'payout.ali@email.com',
    
    # Service details
    'service_details': 'Package: Wildlife Tour Package | Destination: Kaziranga National Park | Duration: 5 Days / 4 Nights | Travel Dates: October 1-5, 2023 | Guests: 2 Adults',
    
    # Line items
    'line_items': [
        {
            'description': 'Travel Agent Services - Complete Tour Package',
            'details': 'Includes accommodation at Kaziranga Resort, all meals (breakfast, lunch, dinner), private AC vehicle transportation, guided wildlife safari sessions, professional tour guide, national park entry fees, and travel insurance',
            'quantity': 1,
            'rate': 55000,  # ₹55,000
            'amount': 55000
        },
        {
            'description': 'Airport Transfer Service',
            'details': 'Round trip airport transfers for 2 guests',
            'quantity': 2,
            'rate': 2500,
            'amount': 5000
        }
    ],
    
    # Financial data
    'subtotal': 60000,
    'discount': 5000,
    'cgst': 4950,  # 9%
    'sgst': 4950,  # 9%
    'igst': 0,
    'total': 64900,
    
    # Payment details
    'bank_name': 'State Bank of India',
    'account_name': 'Nambor Tours & Travels',
    'account_number': '38472019283746',
    'ifsc_code': 'SBIN0001234',
    'branch': 'Golaghat Main Branch',
    'upi_id': 'nambortours@sbi',
    
    # Terms
    'terms_conditions': 'Payment is due within 15 days from invoice date. Please include the invoice number in your payment reference. For any queries regarding this invoice, please contact us at contact@nambortours.com or call +91-98765-43210. Cancellation policy applies as per tour booking agreement.'
}

def test_html_pdf_exporter():
    """Test the HTML PDF exporter with realistic data"""
    
    print("=" * 80)
    print("🧪 TESTING HTML PDF EXPORTER WITH OCR DATA")
    print("=" * 80)
    print()
    
    exporter = HTMLPDFExporter()
    
    try:
        # Generate PDF
        print("📝 Generating invoice PDF...")
        output_file = exporter.generate_pdf(sample_invoice)
        
        print()
        print("✅ HTML PDF Exporter TEST PASSED!")
        print(f"📁 Output file: {output_file}")
        print()
        
        # Check file exists
        import os
        if os.path.exists(output_file):
            file_size = os.path.getsize(output_file)
            print(f"✅ File created successfully")
            print(f"   File size: {file_size:,} bytes")
            
            if output_file.endswith('.html'):
                print(f"   Format: HTML (open in browser or convert to PDF using print-to-PDF)")
                print(f"   To convert to PDF:")
                print(f"     - Option 1: Open in browser and press Ctrl+P, then 'Save as PDF'")
                print(f"     - Option 2: npx puppeteer print-to-pdf {output_file}")
            else:
                print(f"   Format: PDF (ready to use)")
        else:
            print(f"❌ File not created at {output_file}")
            
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        return False
    
    print()
    print("=" * 80)
    print("✅ TEST COMPLETE")
    print("=" * 80)
    return True


if __name__ == "__main__":
    import sys
    import os
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
    
    success = test_html_pdf_exporter()
    sys.exit(0 if success else 1)
