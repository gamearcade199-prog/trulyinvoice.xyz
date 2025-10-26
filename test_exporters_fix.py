"""Quick test to verify PDF and CSV exporters work with fixed None handling"""

import sys
sys.path.insert(0, r'c:\Users\akib\Desktop\trulyinvoice.xyz\backend')

from app.services.professional_pdf_exporter_v2 import ProfessionalPDFExporterV2
from app.services.csv_exporter_v2 import ProfessionalCSVExporterV2

# Test data with None values and long descriptions
test_invoice = {
    'invoice_number': 'INV-92C002',
    'invoice_date': '13-09-2023',
    'due_date': '20-09-2023',
    'payment_status': 'pending',
    'vendor_name': 'Nambor Tours & Travels',
    'vendor_address': '123 Main Street, Mumbai',
    'vendor_gstin': '27AAFCU5055K1Z0',
    'vendor_pan': 'AAFCU5055K',
    'customer_name': 'ABC Company Ltd',
    'customer_address': '456 Park Avenue, Delhi',
    'customer_gstin': '07AACCT1234H1Z1',
    'customer_pan': 'AACCT1234H',
    'line_items': [
        {
            'description': 'Professional Tour Package - Complete Holiday Experience with Accommodation, Meals, and Guided Tours (Very Long Description)',
            'quantity': 2,
            'unit': 'pcs',
            'rate': 5000,
            'amount': 10000,
            'tax_rate': 18,
            'tax_amount': 1800,
        },
        {
            'description': 'Transport Services',
            'quantity': 1,
            'unit': 'days',
            'rate': None,  # This is None - should not crash!
            'amount': None,  # This is None - should not crash!
            'tax_rate': 18,
            'tax_amount': 0,
        }
    ],
    'subtotal': 10000,
    'cgst': None,  # None value
    'sgst': None,  # None value
    'igst': 1800,
    'discount': 0,
    'total_amount': 11800,
}

print("=" * 80)
print("🧪 TESTING PDF EXPORTER WITH NONE VALUES AND LONG TEXT")
print("=" * 80)

try:
    pdf_exporter = ProfessionalPDFExporterV2()
    pdf_file = pdf_exporter.export_invoices_bulk([test_invoice])
    print(f"✅ PDF EXPORTER: SUCCESS! Created {pdf_file}")
except Exception as e:
    print(f"❌ PDF EXPORTER: FAILED! {type(e).__name__}: {e}")

print("\n" + "=" * 80)
print("🧪 TESTING CSV EXPORTER WITH NONE VALUES AND LONG TEXT")
print("=" * 80)

try:
    csv_exporter = ProfessionalCSVExporterV2()
    csv_file = csv_exporter.export_invoices_bulk([test_invoice])
    print(f"✅ CSV EXPORTER: SUCCESS! Created {csv_file}")
    
    # Show first 50 lines of CSV
    print("\n📄 CSV Output (first 50 lines):")
    print("-" * 80)
    with open(csv_file, 'r', encoding='utf-8-sig') as f:
        lines = f.readlines()[:50]
        for line in lines:
            print(line.rstrip())
    
except Exception as e:
    print(f"❌ CSV EXPORTER: FAILED! {type(e).__name__}: {e}")

print("\n" + "=" * 80)
print("✅ TESTING COMPLETE!")
print("=" * 80)
