#!/usr/bin/env python3
"""
CLEANUP PHANTOM INVOICES
Removes invoices that have no corresponding documents (causing stuck "Processing..." state)
"""

import httpx
import asyncio

# Supabase config
SUPABASE_URL = "https://ldvwxqluaheuhbycdpwn.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imxkdnd4cWx1YWhldWhieWNkcHduIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjAwNzY2NTYsImV4cCI6MjA3NTY1MjY1Nn0.uPBCzeJ3tH1SD0QObL850zcrKDDLr9TA6KCUzBp9e1A"

async def cleanup_phantom_invoices():
    """Remove invoices without corresponding documents"""
    
    print("🧹 CLEANING UP PHANTOM INVOICES")
    print("=" * 50)
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        
        # Step 1: Get all invoices
        print("📋 Fetching all invoices...")
        invoices_response = await client.get(
            f"{SUPABASE_URL}/rest/v1/invoices",
            headers={
                "apikey": SUPABASE_KEY,
                "Authorization": f"Bearer {SUPABASE_KEY}",
            },
            params={"select": "id,document_id,vendor_name,total_amount"}
        )
        
        if invoices_response.status_code != 200:
            print(f"❌ Failed to fetch invoices: {invoices_response.status_code}")
            return
            
        invoices = invoices_response.json()
        print(f"📊 Found {len(invoices)} invoices")
        
        # Step 2: Get all documents
        print("📋 Fetching all documents...")
        docs_response = await client.get(
            f"{SUPABASE_URL}/rest/v1/documents",
            headers={
                "apikey": SUPABASE_KEY,
                "Authorization": f"Bearer {SUPABASE_KEY}",
            },
            params={"select": "id,file_name,status"}
        )
        
        if docs_response.status_code != 200:
            print(f"❌ Failed to fetch documents: {docs_response.status_code}")
            return
            
        documents = docs_response.json()
        print(f"📊 Found {len(documents)} documents")
        
        # Step 3: Find phantom invoices
        document_ids = {doc['id'] for doc in documents}
        phantom_invoices = []
        
        for invoice in invoices:
            if invoice['document_id'] not in document_ids:
                phantom_invoices.append(invoice)
                
        print(f"👻 Found {len(phantom_invoices)} phantom invoices")
        
        # Step 4: Delete phantom invoices
        if phantom_invoices:
            print("\n🗑️ Deleting phantom invoices:")
            
            for invoice in phantom_invoices:
                print(f"   Deleting: {invoice['vendor_name']} (ID: {invoice['id']})")
                
                delete_response = await client.delete(
                    f"{SUPABASE_URL}/rest/v1/invoices",
                    headers={
                        "apikey": SUPABASE_KEY,
                        "Authorization": f"Bearer {SUPABASE_KEY}",
                    },
                    params={"id": f"eq.{invoice['id']}"}
                )
                
                if delete_response.status_code == 204:
                    print(f"   ✅ Deleted invoice {invoice['id']}")
                else:
                    print(f"   ❌ Failed to delete invoice {invoice['id']}: {delete_response.status_code}")
        
        print("\n✅ CLEANUP COMPLETE!")
        print("🔄 Refresh your browser to see the clean invoices page")

if __name__ == "__main__":
    print("🚀 Starting phantom invoice cleanup...")
    asyncio.run(cleanup_phantom_invoices())