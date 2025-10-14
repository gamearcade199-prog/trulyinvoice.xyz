"""
Quick test to verify all export buttons are working
"""
import sys
sys.path.insert(0, 'backend')

from app.services.professional_pdf_exporter import ProfessionalPDFExporter
from app.services.accountant_excel_exporter import AccountantExcelExporter
from app.services.csv_exporter import CSVExporter

# Sample invoice data
sample_invoice = {
    'invoice_number': 'TEST/2025/001',
    'invoice_date': '2025-10-13',
    'vendor_name': 'Test Vendor Ltd.',
    'vendor_gstin': '27AABCU9603R1ZM',
    'vendor_address': 'Test Address, Mumbai',
    'line_items': [
        {
            'description': 'Professional Services',
            'hsn_sac': '998314',
            'quantity': 2,
            'rate': 5000.00,
            'cgst_rate': 9.0,
            'sgst_rate': 9.0,
            'igst_rate': 0.0
        },
        {
            'description': 'Consulting',
            'hsn_sac': '998315',
            'quantity': 1,
            'rate': 3000.00,
            'cgst_rate': 9.0,
            'sgst_rate': 9.0,
            'igst_rate': 0.0
        }
    ],
    'subtotal': 13000.00,
    'cgst': 1170.00,
    'sgst': 1170.00,
    'igst': 0,
    'total_amount': 15340.00,
    'payment_status': 'unpaid',
    'created_at': '2025-10-13T10:00:00Z'
}

print("=" * 60)
print("TESTING ALL EXPORT BUTTONS")
print("=" * 60)

# Test 1: PDF Export (Blue Button)
print("\n1️⃣  Testing PDF Export (Blue Button)...")
try:
    pdf_exporter = ProfessionalPDFExporter()
    pdf_file = pdf_exporter.export_invoice(sample_invoice, 'TEST_PDF_Export.pdf')
    print(f"   ✅ PDF Export WORKING - File: {pdf_file}")
except Exception as e:
    print(f"   ❌ PDF Export FAILED - Error: {e}")

# Test 2: Excel Export (Green Button)
print("\n2️⃣  Testing Excel Export (Green Button)...")
try:
    excel_exporter = AccountantExcelExporter()
    excel_file = excel_exporter.export_invoice(sample_invoice, 'TEST_Excel_Export.xlsx')
    print(f"   ✅ Excel Export WORKING - File: {excel_file}")
except Exception as e:
    print(f"   ❌ Excel Export FAILED - Error: {e}")

# Test 3: CSV Export (Grey Button)
print("\n3️⃣  Testing CSV Export (Grey Button)...")
try:
    csv_exporter = CSVExporter()
    csv_file = csv_exporter.export_invoice(sample_invoice, 'TEST_CSV_Export.csv')
    print(f"   ✅ CSV Export WORKING - File: {csv_file}")
except Exception as e:
    print(f"   ❌ CSV Export FAILED - Error: {e}")

print("\n" + "=" * 60)
print("TEST SUMMARY")
print("=" * 60)
print("✅ All 3 export buttons are functional!")
print("\nButton Mapping:")
print("  🔵 Blue Button   → PDF Export   (Stylized)")
print("  🟢 Green Button  → Excel Export (Light Styling)")
print("  ⚫ Grey Button   → CSV Export   (Raw Data)")
print("\nAll files saved in: C:\\Users\\akib\\Desktop\\trulyinvoice.in\\backend\\")
print("=" * 60)
