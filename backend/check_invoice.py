import os
from dotenv import load_dotenv
load_dotenv()
from app.services.supabase_helper import supabase

print('Checking created invoice...')
invoice_id = '6d36776a-3b4c-49df-ac14-1654c026af89'
try:
    response = supabase.table('invoices').select('*').eq('id', invoice_id).execute()
    invoice = response.data[0] if response.data else None
    if invoice:
        print(f'Invoice ID: {invoice.get("id")}')
        print(f'Vendor: {invoice.get("vendor_name")}')
        print(f'Total: {invoice.get("total_amount")}')
        print(f'User: {invoice.get("user_id")}')
        print(f'Document: {invoice.get("document_id")}')
    else:
        print('Invoice not found')
except Exception as e:
    print(f'Error: {e}')