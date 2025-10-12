import httpx
import asyncio

async def check_storage():
    async with httpx.AsyncClient() as client:
        # List files in storage bucket
        response = await client.get(
            'https://ldvwxqluaheuhbycdpwn.supabase.co/storage/v1/object/list/invoice-documents',
            headers={
                'apikey': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imxkdnd4cWx1YWhldWhieWNkcHduIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjAwNzY2NTYsImV4cCI6MjA3NTY1MjY1Nn0.uPBCzeJ3tH1SD0QObL850zcrKDDLr9TA6KCUzBp9e1A',
                'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imxkdnd4cWx1YWhldWhieWNkcHduIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjAwNzY2NTYsImV4cCI6MjA3NTY1MjY1Nn0.uPBCzeJ3tH1SD0QObL850zcrKDDLr9TA6KCUzBp9e1A'
            }
        )
        
        if response.status_code == 200:
            files = response.json()
            print(f'Found {len(files)} files in storage:')
            for file in files:
                name = file.get('name', 'unknown')
                size = file.get('metadata', {}).get('size', 'unknown')
                print(f'  - {name} (size: {size} bytes)')
                
                # If this looks like our PDF, try to download and process it
                if 'tax invoice' in name.lower() or '24347159344967481' in name:
                    print(f'  🎯 This looks like your PDF: {name}')
        else:
            print(f'Error: {response.status_code} - {response.text}')

if __name__ == "__main__":
    asyncio.run(check_storage())