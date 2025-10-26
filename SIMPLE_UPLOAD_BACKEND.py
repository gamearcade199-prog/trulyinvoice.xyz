"""
SIMPLE BACKEND FOR TESTING UPLOAD
Minimal implementation to test upload functionality
"""

from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
import httpx
import asyncio
import logging
import uuid
from datetime import datetime
import json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Simple Upload Test Backend")

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
    return {"status": "healthy", "message": "Simple upload backend running"}

@app.post("/api/documents/upload")
async def upload_document(
    file: UploadFile = File(...), 
    user_id: str = Form(...)
):
    logger.info(f"📤 UPLOAD REQUEST: {file.filename} from user {user_id}")
    
    try:
        # Read file content
        content = await file.read()
        logger.info(f"📄 File size: {len(content)} bytes")
        
        # Generate document ID
        doc_id = str(uuid.uuid4())
        
        # Create document in Supabase
        async with httpx.AsyncClient(timeout=30.0) as client:
            doc_data = {
                "id": doc_id,
                "user_id": user_id,
                "file_name": file.filename,
                "file_size": len(content),
                "file_type": file.content_type or "application/octet-stream",
                "status": "uploaded",
                "upload_path": f"uploads/{user_id}/{doc_id}_{file.filename}",
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat()
            }
            
            response = await client.post(
                f"{SUPABASE_URL}/rest/v1/documents",
                headers={
                    "apikey": SUPABASE_KEY,
                    "Authorization": f"Bearer {SUPABASE_KEY}",
                    "Content-Type": "application/json",
                    "Prefer": "return=representation"
                },
                json=doc_data
            )
            
            if response.status_code in [200, 201]:
                logger.info(f"✅ Document created: {doc_id}")
                
                # Auto-trigger processing
                logger.info(f"🔄 Auto-triggering processing for {doc_id}")
                process_response = await process_document(doc_id)
                
                return {
                    "id": doc_id,
                    "message": "Upload and processing completed successfully",
                    "status": "completed",
                    "processing_result": process_response
                }
            else:
                logger.error(f"❌ Failed to create document: {response.status_code} - {response.text}")
                raise HTTPException(status_code=500, detail=f"Database error: {response.text}")
                
    except Exception as e:
        logger.error(f"❌ Upload failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")

@app.post("/api/documents/{document_id}/process")
async def process_document(document_id: str):
    logger.info(f"🚀 PROCESSING DOCUMENT: {document_id}")
    
    try:
        # Simulate AI processing
        logger.info("🧠 Running AI extraction...")
        await asyncio.sleep(2)  # Shorter delay for testing
        
        # Create invoice data
        invoice_data = {
            "document_id": document_id,
            "vendor_name": "Test Vendor Ltd",
            "invoice_number": f"INV-{document_id[:8].upper()}",
            "total_amount": 15000.00,
            "tax_amount": 2700.00,
            "invoice_date": "2025-10-12",
            "due_date": "2025-11-12",
            "payment_status": "unpaid",
            "subtotal": 12300.00,
            "cgst": 1350.00,
            "sgst": 1350.00,
            "igst": 0.00,
            "currency": "INR",
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat()
        }
        
        # Save to Supabase
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                f"{SUPABASE_URL}/rest/v1/invoices",
                headers={
                    "apikey": SUPABASE_KEY,
                    "Authorization": f"Bearer {SUPABASE_KEY}",
                    "Content-Type": "application/json",
                    "Prefer": "return=representation"
                },
                json=invoice_data
            )
            
            if response.status_code in [200, 201]:
                logger.info(f"✅ Invoice created successfully")
                
                # Update document status
                await client.patch(
                    f"{SUPABASE_URL}/rest/v1/documents",
                    headers={
                        "apikey": SUPABASE_KEY,
                        "Authorization": f"Bearer {SUPABASE_KEY}",
                        "Content-Type": "application/json"
                    },
                    params={"id": f"eq.{document_id}"},
                    json={"status": "completed", "processed_at": datetime.now().isoformat()}
                )
                
                return {"success": True, "message": "Processing completed", "invoice_data": invoice_data}
            else:
                logger.error(f"❌ Failed to create invoice: {response.status_code} - {response.text}")
                raise HTTPException(status_code=500, detail=f"Invoice creation failed: {response.text}")
                
    except Exception as e:
        logger.error(f"❌ Processing failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Processing failed: {str(e)}")

@app.get("/api/invoices/")
async def get_invoices():
    """Get all invoices for testing"""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{SUPABASE_URL}/rest/v1/invoices",
                headers={
                    "apikey": SUPABASE_KEY,
                    "Authorization": f"Bearer {SUPABASE_KEY}",
                },
                params={"select": "*", "order": "created_at.desc"}
            )
            return response.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting Simple Upload Test Backend")
    uvicorn.run(app, host="127.0.0.1", port=8000)