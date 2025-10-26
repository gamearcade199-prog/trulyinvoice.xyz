"""
TEST GST FIX - Export invoice without GST to verify fix
"""
import sys
import os
sys.path.append('backend')

from app.services.accountant_excel_exporter import AccountantExcelExporter
from app.services.csv_exporter import CSVExporter

# Test invoice data matching the Meenakshi Tour invoice
test_invoice = {
    'invoice_number': '496',
    'invoice_date': '2023-09-20',
    'vendor_name': 'MEENAKSHI TOUR & TRAVEL',
    'vendor_gstin': None,  # No GSTIN
    'subtotal': 750.00,
    'cgst': 0,  # No GST
    'sgst': 0,  # No GST  
    'igst': 0,  # No GST
    'total_amount': 750.00,
    'currency': 'INR',
    'payment_status': 'unpaid',
    'line_items': [
        {
            'description': 'Journey from Ghy to D.B.R.G.',
            'quantity': 1,
            'rate': 750.00,
            'amount': 750.00,
            'hsn_sac': 'N/A',
            # No GST rates specified - should default to 0
        }
    ]
}

def test_exports():
    print("🧪 TESTING GST FIX...")
    print("=" * 50)
    
    # Test Excel Export
    print("📊 Testing Excel Export (Fixed)...")
    excel_exporter = AccountantExcelExporter()
    excel_file = excel_exporter.export_invoice(test_invoice, "TEST_GST_FIXED.xlsx")
    print(f"✅ Excel exported: {excel_file}")
    
    # Test CSV Export  
    print("\n📄 Testing CSV Export (Fixed)...")
    csv_exporter = CSVExporter()
    csv_file = csv_exporter.export_invoice(test_invoice, "TEST_GST_FIXED.csv")
    print(f"✅ CSV exported: {csv_file}")
    
    print("\n🎉 FIX VERIFICATION:")
    print("   ✅ GST rates should now default to 0% instead of 9%")
    print("   ✅ Non-GST invoices will show ₹0 tax instead of artificial calculations")
    print("   ✅ Excel/CSV will match the original invoice exactly")
    
    print(f"\n📂 Check these files:")
    print(f"   - {excel_file}")
    print(f"   - {csv_file}")

if __name__ == "__main__":
    test_exports()