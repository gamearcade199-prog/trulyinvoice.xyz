import httpx
import asyncio

async def check_document():
    async with httpx.AsyncClient() as client:
        response = await client.get(
            'https://ldvwxqluaheuhbycdpwn.supabase.co/rest/v1/documents',
            headers={
                'apikey': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imxkdnd4cWx1YWhldWhieWNkcHduIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjAwNzY2NTYsImV4cCI6MjA3NTY1MjY1Nn0.uPBCzeJ3tH1SD0QObL850zcrKDDLr9TA6KCUzBp9e1A',
                'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imxkdnd4cWx1YWhldWhieWNkcHduIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjAwNzY2NTYsImV4cCI6MjA3NTY1MjY1Nn0.uPBCzeJ3tH1SD0QObL850zcrKDDLr9TA6KCUzBp9e1A'
            },
            params={'id': 'eq.d05d36e4-ff37-487b-9e68-64dcc3c75c6c', 'select': '*'}
        )
        
        if response.status_code == 200:
            docs = response.json()
            if docs:
                doc = docs[0]
                print(f"Document ID: {doc.get('id')}")
                print(f"File Name: {doc.get('file_name')}")
                print(f"File Path: {doc.get('file_path')}")
                print(f"Status: {doc.get('status')}")
                print(f"Upload Date: {doc.get('created_at')}")
            else:
                print('No document found')
        else:
            print(f'Error: {response.status_code} - {response.text}')

if __name__ == "__main__":
    asyncio.run(check_document())