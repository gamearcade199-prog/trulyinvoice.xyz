import httpx
import asyncio

async def check_invoices():
    async with httpx.AsyncClient() as client:
        response = await client.get(
            "https://ldvwxqluaheuhbycdpwn.supabase.co/rest/v1/invoices",
            headers={
                "apikey": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imxkdnd4cWx1YWhldWhieWNkcHduIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjAwNzY2NTYsImV4cCI6MjA3NTY1MjY1Nn0.uPBCzeJ3tH1SD0QObL850zcrKDDLr9TA6KCUzBp9e1A",
                "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imxkdnd4cWx1YWhldWhieWNkcHduIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjAwNzY2NTYsImV4cCI6MjA3NTY1MjY1Nn0.uPBCzeJ3tH1SD0QObL850zcrKDDLr9TA6KCUzBp9e1A"
            },
            params={"select": "*", "order": "created_at.desc", "limit": "3"}
        )
        
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            invoices = response.json()
            print(f"Found {len(invoices)} invoices:")
            for invoice in invoices:
                print(f"  - {invoice.get('vendor_name')} | ₹{invoice.get('total_amount')} | {invoice.get('invoice_number')}")
        else:
            print(f"Error: {response.text}")

if __name__ == "__main__":
    asyncio.run(check_invoices())