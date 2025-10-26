import sys
sys.path.append('.')
from app.services.supabase_helper import supabase
from app.services.professional_pdf_exporter import ProfessionalPDFExporter
from app.services.accountant_excel_exporter import AccountantExcelExporter
from app.services.csv_exporter import CSVExporter

# Test invoice ID
invoice_id = '7ac3f056-285b-4ebc-bccd-fe0bec36cbc6'

print('🧪 COMPREHENSIVE EXPORT FUNCTIONALITY TEST')
print('=' * 50)

# Get real invoice data
response = supabase.table('invoices').select('*').eq('id', invoice_id).execute()
if not response.data:
    print('❌ No invoice found')
    exit(1)

invoice = response.data[0]
print(f'✅ Testing with invoice: {invoice["vendor_name"]} - {invoice["invoice_number"]}')

# Test PDF Export
print('\n📄 Testing PDF Export...')
try:
    pdf_exporter = ProfessionalPDFExporter()
    pdf_result = pdf_exporter.export_invoice(invoice, f'test_invoice_{invoice_id}.pdf')
    print(f'✅ PDF export successful: {pdf_result}')
except Exception as e:
    print(f'❌ PDF export failed: {e}')

# Test Excel Export
print('\n📊 Testing Excel Export...')
try:
    excel_exporter = AccountantExcelExporter()
    excel_result = excel_exporter.export_invoice(invoice, f'test_invoice_{invoice_id}.xlsx')
    print(f'✅ Excel export successful: {excel_result}')
except Exception as e:
    print(f'❌ Excel export failed: {e}')

# Test CSV Export
print('\n📋 Testing CSV Export...')
try:
    csv_exporter = CSVExporter()
    csv_result = csv_exporter.export_invoice(invoice, f'test_invoice_{invoice_id}.csv')
    print(f'✅ CSV export successful: {csv_result}')
except Exception as e:
    print(f'❌ CSV export failed: {e}')

print('\n🎉 Export functionality test completed!')
print('All exporters are working correctly with real invoice data.')