import os
from dotenv import load_dotenv
load_dotenv()
from app.services.supabase_helper import supabase

print('Checking document status after processing...')
doc_id = '4378bba9-dd9d-406a-9020-a5b17c56a51d'
try:
    response = supabase.table('documents').select('*').eq('id', doc_id).execute()
    doc = response.data[0] if response.data else None
    if doc:
        print(f'Document ID: {doc.get("id")}')
        print(f'Status: {doc.get("status")}')
        print(f'File: {doc.get("file_name")}')
        print(f'User: {doc.get("user_id")}')
    else:
        print('Document not found')
except Exception as e:
    print(f'Error: {e}')