"""
Ultra-minimal FastAPI server for testing upload functionality
"""
from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import asyncio

app = FastAPI()

# Simple CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/api/documents/process-anonymous")
async def process_anonymous(file: UploadFile = File(...)):
    # Add delay to simulate processing
    await asyncio.sleep(2)
    
    return {
        "success": True,
        "vendor_name": "Acme Technologies Pvt Ltd",
        "invoice_number": "INV-2025-789",
        "invoice_date": "2025-01-20",
        "total_amount": "₹15,750.00",
        "subtotal": "₹13,347.46",
        "tax_amount": "₹2,402.54",
        "due_date": "2025-02-20",
        "vendor_email": "accounts@acmetech.com",
        "vendor_phone": "+91-9876543210",
        "vendor_address": "Phase-II, Sector 18, Gurgaon-122015",
        "file_name": file.filename
    }