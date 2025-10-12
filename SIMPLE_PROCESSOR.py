from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import httpx
import asyncio
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Simple Invoice Processor")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Supabase config
SUPABASE_URL = "https://ldvwxqluaheuhbycdpwn.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imxkdnd4cWx1YWhldWhieWNkcHduIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjAwNzY2NTYsImV4cCI6MjA3NTY1MjY1Nn0.uPBCzeJ3tH1SD0QObL850zcrKDDLr9TA6KCUzBp9e1A"

@app.get("/health")
async def health():
    return {"status": "healthy", "message": "Simple processor running"}

@app.post("/api/documents/{document_id}/process")
async def process_document(document_id: str):
    logger.info(f"🚀 PROCESSING DOCUMENT: {document_id}")
    
    try:
        # Simulate AI processing
        await asyncio.sleep(2)
        
        # Update database with dummy data
        async with httpx.AsyncClient() as client:
            # Update via Supabase REST API with only basic fields
            invoice_data = {
                "vendor_name": "ABC Technologies Pvt Ltd",
                "invoice_number": f"INV-{document_id[:8]}",
                "total_amount": 15750.00,
                "tax_amount": 2835.00,
                "invoice_date": "2025-09-15",
                "due_date": "2025-10-15",
                "payment_status": "unpaid",
                "updated_at": "now()"
            }
            
            # Update via Supabase REST API
            response = await client.patch(
                f"{SUPABASE_URL}/rest/v1/invoices",
                headers={
                    "apikey": SUPABASE_KEY,
                    "Authorization": f"Bearer {SUPABASE_KEY}",
                    "Content-Type": "application/json",
                    "Prefer": "return=minimal"
                },
                params={"document_id": f"eq.{document_id}"},
                json=invoice_data
            )
            
            if response.status_code not in [200, 204]:
                logger.error(f"Failed to update invoice: {response.text}")
                raise HTTPException(status_code=500, detail="Failed to update invoice")
        
        logger.info(f"✅ PROCESSING COMPLETE: {document_id}")
        return {
            "success": True,
            "message": "Processing complete",
            "document_id": document_id,
            "data": invoice_data
        }
        
    except Exception as e:
        logger.error(f"❌ PROCESSING FAILED: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)