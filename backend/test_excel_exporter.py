"""
Quick Test - Excel Exporter Functionality
Tests if the Excel exporter is working correctly
"""

from app.services.excel_exporter_v2 import ProfessionalExcelExporterV2
from datetime import datetime
import os

# Sample test data
test_invoices = [
    {
        'id': 'test-001',
        'invoice_number': 'INV-2025-001',
        'invoice_date': '2025-10-28',
        'due_date': '2025-11-28',
        'vendor_name': 'Test Vendor Ltd',
        'vendor_gstin': '27AABCU9603R1ZX',
        'vendor_address': '123 Test Street, Mumbai',
        'customer_name': 'Test Customer',
        'customer_gstin': '29AABCU9603R1ZY',
        'subtotal': 10000.00,
        'discount': 0,
        'cgst': 900.00,
        'sgst': 900.00,
        'igst': 0,
        'total_amount': 11800.00,
        'paid_amount': 0,
        'payment_status': 'pending',
        'line_items': [
            {
                'description': 'Professional Services',
                'quantity': 10,
                'unit': 'hours',
                'rate': 1000.00,
                'amount': 10000.00,
                'tax_rate': 18,
                'tax_amount': 1800.00
            }
        ]
    },
    {
        'id': 'test-002',
        'invoice_number': 'INV-2025-002',
        'invoice_date': '2025-10-27',
        'due_date': '2025-11-27',
        'vendor_name': 'Another Vendor Pvt Ltd',
        'vendor_gstin': '27AABCU9603R1ZZ',
        'vendor_address': '456 Test Road, Delhi',
        'customer_name': 'Another Customer',
        'customer_gstin': '07AABCU9603R1ZA',
        'subtotal': 25000.00,
        'discount': 500,
        'cgst': 0,
        'sgst': 0,
        'igst': 4410.00,
        'total_amount': 28910.00,
        'paid_amount': 28910.00,
        'payment_status': 'paid',
        'line_items': [
            {
                'description': 'Product A',
                'quantity': 5,
                'unit': 'units',
                'rate': 3000.00,
                'amount': 15000.00,
                'tax_rate': 18,
                'tax_amount': 2700.00
            },
            {
                'description': 'Product B',
                'quantity': 10,
                'unit': 'units',
                'rate': 1000.00,
                'amount': 10000.00,
                'tax_rate': 18,
                'tax_amount': 1800.00
            }
        ]
    }
]

def test_excel_export():
    """Test Excel export functionality"""
    print("=" * 60)
    print("🧪 TESTING EXCEL EXPORTER")
    print("=" * 60)
    
    try:
        # Test 1: Import check
        print("\n✅ Test 1: Import successful")
        
        # Test 2: Create exporter instance
        exporter = ProfessionalExcelExporterV2()
        print("✅ Test 2: Exporter instance created")
        
        # Test 3: Export invoices
        print("\n📊 Test 3: Exporting test invoices...")
        filename = exporter.export_invoices_bulk(test_invoices)
        print(f"✅ Test 3: Export successful - {filename}")
        
        # Test 4: Verify file exists
        if os.path.exists(filename):
            file_size = os.path.getsize(filename)
            print(f"✅ Test 4: File exists - Size: {file_size:,} bytes")
        else:
            print("❌ Test 4: File not found!")
            return False
        
        # Test 5: Check file extension
        if filename.endswith('.xlsx'):
            print("✅ Test 5: Correct file extension (.xlsx)")
        else:
            print(f"❌ Test 5: Wrong file extension - {filename}")
            return False
        
        print("\n" + "=" * 60)
        print("✅ ALL TESTS PASSED - Excel Exporter is WORKING!")
        print("=" * 60)
        print(f"\n📁 Test file created: {filename}")
        print("💡 Open this file in Excel to verify the formatting")
        
        return True
        
    except ImportError as e:
        print(f"\n❌ Import Error: {e}")
        print("💡 Make sure openpyxl is installed: pip install openpyxl")
        return False
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_excel_export()
