#!/usr/bin/env python
"""Test invoice export functionality"""

from app.services.supabase_helper import supabase
from app.services.accountant_excel_exporter import AccountantExcelExporter
from app.services.csv_exporter import CSVExporter
from app.services.professional_pdf_exporter import ProfessionalPDFExporter
import json

print("=" * 60)
print("TESTING INVOICE EXPORT FUNCTIONALITY")
print("=" * 60)

# Get the most recent invoice
result = supabase.table('invoices').select('*').order('created_at', desc=True).limit(1).execute()

if not result.data:
    print("❌ No invoices found")
    exit(1)

invoice = result.data[0]
print(f"\n✅ Found invoice: {invoice.get('vendor_name')}")
print(f"   ID: {invoice.get('id')}")
print(f"   Invoice #: {invoice.get('invoice_number')}")
print(f"   Total: {invoice.get('total_amount')}")
print(f"   Line items type: {type(invoice.get('line_items')).__name__}")

# Parse line_items if string
if isinstance(invoice.get('line_items'), str):
    try:
        invoice['line_items'] = json.loads(invoice['line_items'])
        print("   ✅ Parsed line_items from JSON string")
    except:
        invoice['line_items'] = []
        print("   ⚠️  Failed to parse line_items, set to empty")

# Test 1: Excel Export
print("\n" + "-" * 60)
print("Testing Excel Export...")
try:
    exporter = AccountantExcelExporter()
    excel_file = exporter.export_invoices_bulk([invoice])
    print(f"✅ Excel Export SUCCESS: {excel_file}")
except Exception as e:
    print(f"❌ Excel Export FAILED: {e}")

# Test 2: CSV Export
print("\n" + "-" * 60)
print("Testing CSV Export...")
try:
    exporter = CSVExporter()
    csv_file = exporter.export_invoice(invoice)
    print(f"✅ CSV Export SUCCESS: {csv_file}")
except Exception as e:
    print(f"❌ CSV Export FAILED: {e}")

# Test 3: PDF Export
print("\n" + "-" * 60)
print("Testing PDF Export...")
try:
    exporter = ProfessionalPDFExporter()
    pdf_file = exporter.export_invoice(invoice)
    print(f"✅ PDF Export SUCCESS: {pdf_file}")
except Exception as e:
    print(f"❌ PDF Export FAILED: {e}")

print("\n" + "=" * 60)
print("Export testing complete!")
print("=" * 60)
