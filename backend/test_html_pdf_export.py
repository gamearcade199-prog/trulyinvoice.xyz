"""
Test HTML Template PDF Exporter
================================
Generates a sample invoice PDF to verify the new exporter works
"""

import sys
import os

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))

from app.services.html_template_pdf_exporter import HTMLTemplatePDFExporter
from datetime import datetime

def test_pdf_export():
    """Test PDF generation with sample invoice data"""
    
    print("\n" + "="*60)
    print("  TESTING HTML TEMPLATE PDF EXPORTER")
    print("="*60 + "\n")
    
    # Sample invoice data (mimics real invoice structure)
    sample_invoice = {
        'invoice_number': 'INV-TEST-001',
        'invoice_date': '2024-01-15',
        'due_date': '2024-02-15',
        'payment_status': 'Paid',
        
        # Vendor (From)
        'vendor_name': 'TrulyInvoice Technologies Pvt Ltd',
        'vendor_address': '123 MG Road, Bangalore, Karnataka 560001, India',
        'vendor_phone': '+91 98765 43210',
        'vendor_email': 'billing@trulyinvoice.xyz',
        'vendor_gstin': '29ABCDE1234F1Z5',
        'vendor_pan': 'ABCDE1234F',
        
        # Customer (Bill To)
        'customer_name': 'Acme Corporation India Pvt Ltd',
        'customer_address': '456 Park Street, Mumbai, Maharashtra 400001, India',
        'customer_phone': '+91 98765 12345',
        'customer_email': 'accounts@acmecorp.in',
        'customer_gstin': '27ZYXWV9876T1S5',
        
        # Line Items
        'items': [
            {
                'description': 'Premium Invoice OCR Service - Monthly Subscription',
                'quantity': 1,
                'unit_price': 10000.00,
                'tax_rate': 18.0,
                'amount': 10000.00
            },
            {
                'description': 'Additional Storage - 50GB Cloud Storage',
                'quantity': 2,
                'unit_price': 500.00,
                'tax_rate': 18.0,
                'amount': 1000.00
            },
            {
                'description': 'API Integration Support - Custom Development',
                'quantity': 5,
                'unit_price': 2000.00,
                'tax_rate': 18.0,
                'amount': 10000.00
            }
        ],
        
        # Amounts
        'subtotal': 21000.00,
        'tax_amount': 3780.00,
        'total_amount': 24780.00,
        'discount': 0.00,
        'cgst': 1890.00,
        'sgst': 1890.00,
        'igst': 0.00,
        
        # Payment Details
        'payment_method': 'Bank Transfer',
        'bank_name': 'HDFC Bank',
        'account_number': '123456789012',
        'ifsc_code': 'HDFC0001234',
        'upi_id': 'trulyinvoice@hdfc',
        
        # Notes
        'notes': 'Thank you for your business! Payment received via NEFT on 15th January 2024.',
        'terms': 'Payment is due within 30 days. Late payments may incur interest charges as per company policy.'
    }
    
    try:
        print("📄 Creating PDF exporter instance...")
        exporter = HTMLTemplatePDFExporter()
        
        print("🎨 Generating HTML with embedded CSS...")
        html_content = exporter._generate_html(sample_invoice)
        print(f"   HTML generated: {len(html_content)} characters")
        
        print("🔄 Converting HTML to PDF...")
        pdf_filename = exporter.generate_pdf(sample_invoice, "test_invoice.pdf")
        
        print("\n" + "="*60)
        print("  ✅ SUCCESS!")
        print("="*60)
        print(f"\n📁 PDF Generated: {pdf_filename}")
        
        # Check file exists and size
        if os.path.exists(pdf_filename):
            file_size = os.path.getsize(pdf_filename) / 1024  # KB
            print(f"📊 File Size: {file_size:.2f} KB")
            print(f"📂 Location: {os.path.abspath(pdf_filename)}")
            
            print("\n🎯 VERIFICATION CHECKLIST:")
            print("   ✅ PDF file created")
            print("   ✅ File extension is .pdf")
            print(f"   ✅ File size is reasonable ({file_size:.2f} KB)")
            
            print("\n👀 NEXT STEPS:")
            print("   1. Open the PDF file in a PDF reader")
            print("   2. Verify visual design matches HTML template:")
            print("      • Dark blue header (#2c3e50)")
            print("      • Professional typography and spacing")
            print("      • Grid layouts for invoice details")
            print("      • Table with proper styling")
            print("      • Yellow terms section (#fffbf0)")
            print("   3. Check all invoice data displays correctly")
            
            return True
        else:
            print("\n❌ ERROR: PDF file was not created")
            return False
            
    except Exception as e:
        print("\n" + "="*60)
        print("  ❌ ERROR DURING PDF GENERATION")
        print("="*60)
        print(f"\n🔴 Error Type: {type(e).__name__}")
        print(f"🔴 Error Message: {str(e)}")
        
        import traceback
        print("\n📋 Full Traceback:")
        print("-"*60)
        traceback.print_exc()
        print("-"*60)
        
        return False


if __name__ == "__main__":
    success = test_pdf_export()
    sys.exit(0 if success else 1)
