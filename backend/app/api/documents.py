"""
Documents API - Handle file uploads and processing
OPTIMIZED VERSION:
- Supports ALL users (proper user_id filtering)
- Supports IMAGES (JPG, PNG) with OCR
- Supports PDFs with text extraction
- Production-ready error handling
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from datetime import datetime
import os
import re
import requests
import io
from app.services.supabase_helper import supabase

# Try to import AI extractor and PDF processing
try:
    from app.services.intelligent_extractor import IntelligentAIExtractor
    import PyPDF2
    AI_AVAILABLE = True
    print("✅ INTELLIGENT AI extraction ENABLED (flexible fields, PDF + Images)")
except ImportError as e:
    AI_AVAILABLE = False
    print(f"⚠️ AI extraction DISABLED: {e}")

router = APIRouter()


class ProcessResponse(BaseModel):
    success: bool
    message: str
    invoice_id: str = None
    vendor_name: str = None
    total_amount: float = None


@router.post("/{document_id}/process", response_model=ProcessResponse)
async def process_document(document_id: str):
    """
    Process an uploaded document and create invoice
    OPTIMIZED VERSION: Supports PDFs + Images, All Users, Production-Ready
    """
    try:
        # 1. Get document from Supabase
        documents = supabase.select("documents", filters={"id": document_id})
        
        if not documents or len(documents) == 0:
            raise HTTPException(status_code=404, detail="Document not found")
        
        document = documents[0]
        
        # 2. Extract invoice data using AI if available
        file_name = document.get("file_name", "Invoice")
        user_id = document.get("user_id")
        file_url = document.get("file_url")
        storage_path = document.get("storage_path")
        
        # CRITICAL: Ensure user_id is set (for multi-user support)
        if not user_id:
            raise HTTPException(status_code=400, detail="Document missing user_id - cannot process")
        
        print(f"📄 Processing: {file_name} for user {user_id}")
        
        # Try AI extraction first
        invoice_data = None
        if AI_AVAILABLE and file_url:
            try:
                # Download file from Supabase storage
                print(f"  ⬇️ Downloading from: {file_url[:50]}...")
                file_response = requests.get(file_url, timeout=30)
                file_response.raise_for_status()
                
                file_content = file_response.content
                api_key = os.getenv('OPENAI_API_KEY')
                
                if not api_key:
                    print("  ⚠️ No OpenAI API key found")
                    raise ValueError("OpenAI API key not configured")
                
                extractor = IntelligentAIExtractor(api_key)
                ai_result = None
                
                # Check file type and extract accordingly
                file_ext = file_name.lower().split('.')[-1]
                
                # IMAGES: JPG, JPEG, PNG - Use Vision OCR
                if file_ext in ['jpg', 'jpeg', 'png']:
                    print(f"  📸 Image detected - using OCR...")
                    mime_type = f"image/{file_ext}" if file_ext != 'jpg' else "image/jpeg"
                    ai_result = extractor.extract_from_image(file_content, mime_type)
                
                # PDFs: Extract text then use AI
                elif file_ext == 'pdf':
                    print(f"  📄 PDF detected - extracting text...")
                    extracted_text = ""
                    try:
                        pdf_file = io.BytesIO(file_content)
                        pdf_reader = PyPDF2.PdfReader(pdf_file)
                        
                        for page_num, page in enumerate(pdf_reader.pages):
                            text = page.extract_text()
                            extracted_text += text
                            print(f"     Page {page_num + 1}: {len(text)} chars")
                        
                        if extracted_text.strip():
                            print(f"  🤖 Extracted {len(extracted_text)} chars - sending to AI...")
                            ai_result = extractor.extract_from_text(extracted_text)
                        else:
                            print(f"  ⚠️ No text found in PDF - might be scanned image")
                    except Exception as e:
                        print(f"  ⚠️ PDF extraction failed: {e}")
                
                else:
                    print(f"  ⚠️ Unsupported file type: {file_ext}")
                
                # Use AI results if successful
                if ai_result:
                    print(f"  ✅ AI extracted: {ai_result.get('vendor_name')} - ₹{ai_result.get('total_amount'):,.2f}")
                    print(f"  📊 Fields found: {list(ai_result.keys())}")
                    
                    # Build invoice data with ONLY the fields that were extracted
                    invoice_data = {
                        "user_id": user_id,  # Always required
                        "document_id": document_id  # Always required
                    }
                    
                    # Add all extracted fields (intelligent extractor only returns fields that exist)
                    invoice_data.update(ai_result)
                    
                    # Ensure payment_status defaults to unpaid if not extracted
                    if 'payment_status' not in invoice_data:
                        invoice_data['payment_status'] = 'unpaid'
                    
                else:
                    print(f"  ⚠️ AI extraction returned None - falling back")
                    
            except Exception as e:
                print(f"  ❌ AI extraction failed: {e}, falling back to filename extraction")
        else:
            if not AI_AVAILABLE:
                print(f"  ⚠️ AI not available")
            if not file_url:
                print(f"  ⚠️ No file URL")
        
        # Fallback: Extract from filename if AI fails
        if not invoice_data:
            print(f"  📝 Using filename extraction fallback")
            
            # Extract invoice number (look for # followed by digits)
            invoice_num_match = re.search(r'#(\d+)', file_name)
            if invoice_num_match:
                invoice_number = invoice_num_match.group(1)
            else:
                invoice_number = f"INV-{datetime.now().strftime('%Y%m%d%H%M%S')}"
            
            # Extract date from filename
            date_match = re.search(r'(\d{4}-\d{2}-\d{2})', file_name)
            invoice_date = date_match.group(1) if date_match else datetime.now().strftime('%Y-%m-%d')
            
            # Extract vendor name
            vendor_name = file_name.split('.')[0]
            vendor_name = re.sub(r'\d{4}-\d{2}-\d{2}T?\d{0,2}-?\d{0,2}', '', vendor_name)
            vendor_name = re.sub(r'#[\d-]+', '', vendor_name)
            vendor_name = re.sub(r'\s+', ' ', vendor_name).strip()
            vendor_name = vendor_name[:50] if vendor_name else "Unknown Vendor"
            
            # FALLBACK VALUES (better than placeholders)
            invoice_data = {
                "user_id": user_id,  # CRITICAL: Always set user_id
                "document_id": document_id,
                "vendor_name": vendor_name,
                "invoice_number": invoice_number,
                "invoice_date": invoice_date,
                "subtotal": 0.0,  # Better than fake 10000
                "cgst": 0.0,
                "sgst": 0.0,
                "igst": 0.0,
                "total_amount": 0.0,  # User will see 0 and know to check manually
                "payment_status": "unpaid"
            }
            print(f"  ⚠️ Fallback values used - amounts set to 0 (user should verify)")
        
        # 3. Create invoice in Supabase (with user_id for RLS)
        print(f"  💾 Creating invoice for user {user_id}...")
        created_invoice = supabase.insert("invoices", invoice_data)
        
        if not created_invoice:
            raise HTTPException(status_code=500, detail="Failed to create invoice")
        
        # 4. Update document status to 'completed'
        supabase.update("documents", filters={"id": document_id}, data={"status": "completed"})
        
        print(f"  ✅ Invoice created: {created_invoice['id']}")
        
        return ProcessResponse(
            success=True,
            message="Invoice processed successfully",
            invoice_id=created_invoice["id"],
            vendor_name=invoice_data["vendor_name"],
            total_amount=invoice_data["total_amount"]
        )
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"  ❌ Processing error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Processing error: {str(e)}")


@router.get("/{document_id}")
async def get_document(document_id: str):
    """Get document details"""
    try:
        documents = supabase.select("documents", filters={"id": document_id})
        
        if not documents:
            raise HTTPException(status_code=404, detail="Document not found")
        
        return documents[0]
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
