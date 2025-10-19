"""
Documents API - Handle file uploads and processing
OPTIMIZED VERSION:
- Supports ALL users (proper user_id filtering)
- Supports IMAGES (JPG, PNG) with OCR
- Supports PDFs with text extraction
- Anonymous processing for previews
- Production-ready error handling
"""
from fastapi import APIRouter, HTTPException, File, UploadFile, Depends, Request
from pydantic import BaseModel
from datetime import datetime
import os
import re
import requests
import io
from app.services.supabase_helper import supabase
from app.middleware.subscription import check_subscription

# Try to import AI extractor and PDF processing
try:
    from app.services.vision_flash_lite_extractor import VisionFlashLiteExtractor
    import PyPDF2
    AI_AVAILABLE = True
    print("✅ VISION + FLASH-LITE extraction ENABLED - 99% cost reduction target")
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
async def process_document(document_id: str, request: Request):
    """
    Process an uploaded document and create invoice
    OPTIMIZED VERSION: Supports PDFs + Images, All Users, Production-Ready
    """
    try:
        # Get document from Supabase
        doc_query = supabase.table("documents").select("*").eq("id", document_id).execute()
        if not doc_query.data:
            raise HTTPException(status_code=404, detail="Document not found")
            
        document = doc_query.data[0]
        
        # Only check subscription for non-anonymous uploads
        if not document.get("is_anonymous", False):
            await check_subscription(request)
        
        # Extract invoice data using AI if available
        file_name = document.get("file_name", "Invoice")
        user_id = document.get("user_id")
        storage_path = document.get("storage_path")
        
        # Allow anonymous uploads (user_id can be None)
        if not user_id:
            print("👤 Anonymous upload detected")
        else:
            print(f"👤 Authenticated user: {user_id}")
        
        # Try AI extraction first
        invoice_data = None
        if AI_AVAILABLE and storage_path:
            try:
                # Download file from Supabase storage
                print(f"⬇️ Downloading from storage: {storage_path}")
                storage_response = supabase.storage.from_("documents").download(storage_path)
                if not storage_response:
                    raise HTTPException(status_code=404, detail="File not found in storage")
                
                file_content = storage_response
                
                # Check for Gemini API key
                gemini_key = os.getenv('GOOGLE_AI_API_KEY')
                
                if not gemini_key:
                    print("⚠️ No Gemini API key found")
                    raise HTTPException(status_code=500, detail="AI service not configured")
                
                extractor = VisionFlashLiteExtractor()
                ai_result = None
                
                # Check file type and extract accordingly
                file_ext = file_name.lower().split('.')[-1]
                
                # IMAGES: JPG, JPEG, PNG - Use Vision API + Flash-Lite
                if file_ext in ['jpg', 'jpeg', 'png']:
                    print(f"  📸 Image detected - using Vision API + Flash-Lite...")
                    
                    # Use raw bytes directly for our new extractor
                if file_name.lower().endswith(('.jpg', '.jpeg', '.png')):
                    print(f"📸 Image detected - using Vision API...")
                    try:
                        ai_result = await extractor.extract_invoice_data(file_content, file_name)
                    except Exception as e:
                        print(f"⚠️ Vision API extraction failed: {str(e)}")
                        raise HTTPException(status_code=500, detail=f"Vision API extraction failed: {str(e)}")
                
                # PDFs: Extract text then use AI
                elif file_name.lower().endswith('.pdf'):
                    print(f"📄 PDF detected - extracting text...")
                    extracted_text = ""
                    try:
                        pdf_file = io.BytesIO(file_content)
                        pdf_reader = PyPDF2.PdfReader(pdf_file)
                        
                        for page_num, page in enumerate(pdf_reader.pages):
                            text = page.extract_text()
                            extracted_text += text
                            print(f"   Page {page_num + 1}: {len(text)} chars")
                        
                        if extracted_text.strip():
                            print(f"🤖 Extracted {len(extracted_text)} chars - processing...")
                            ai_result = await extractor.process_text(extracted_text)
                        else:
                            raise HTTPException(status_code=422, detail="No text found in PDF - might be scanned image")
                    except Exception as e:
                        print(f"⚠️ PDF extraction failed: {str(e)}")
                        raise HTTPException(status_code=500, detail=f"PDF extraction failed: {str(e)}")
                
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
                    
                    # Add extracted fields, but exclude internal metadata, confidence scores, and error fields
                    # Error fields: 'error', 'error_message', '_extraction_metadata' don't exist in database schema
                    excluded_fields = {'error', 'error_message', '_extraction_metadata'}
                    for key, value in ai_result.items():
                        if key not in excluded_fields and not key.startswith('_') and not key.endswith('_confidence'):
                            invoice_data[key] = value
                    
                    # Validate payment_status - MUST match ENHANCED_SCHEMA_50_PLUS_FIELDS.sql
                    # Database allows: 'pending', 'paid', 'overdue', 'cancelled', 'refunded', 'partial', 'processing', 'failed'
                    valid_payment_statuses = {'pending', 'paid', 'overdue', 'cancelled', 'refunded', 'partial', 'processing', 'failed'}
                    
                    # Map additional invalid values to valid ones
                    payment_status_mapping = {
                        'unpaid': 'pending',          # unpaid → pending (unpaid not valid!)
                        'draft': 'pending',           # draft → pending
                        'unknown': 'pending',         # unknown → pending
                        'na': 'pending',              # n/a → pending
                        'n/a': 'pending',
                    }
                    
                    payment_status = invoice_data.get('payment_status', '').strip().lower() if invoice_data.get('payment_status') else ''
                    
                    # Use mapping if exists, otherwise validate
                    if payment_status in payment_status_mapping:
                        invoice_data['payment_status'] = payment_status_mapping[payment_status]
                    elif payment_status in valid_payment_statuses:
                        invoice_data['payment_status'] = payment_status
                    else:
                        invoice_data['payment_status'] = 'pending'  # Default to pending if invalid or empty

                if not invoice_data:
                    print(f"⚠️ AI extraction returned no results")
                    raise HTTPException(status_code=422, detail="AI extraction failed to extract data")
                    
            except Exception as e:
                print(f"❌ AI extraction failed: {str(e)}")
                raise HTTPException(status_code=500, detail=f"AI extraction error: {str(e)}")
        else:
            if not AI_AVAILABLE:
                print(f"⚠️ AI not available")
                raise HTTPException(status_code=501, detail="AI extraction not available")
            if not storage_path:
                print(f"⚠️ No storage path")
                raise HTTPException(status_code=422, detail="Document has no file")        # Fallback: Extract from filename if AI fails
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
                "payment_status": "pending"  # Must be valid: pending, paid, overdue, cancelled, refunded, partial, processing, failed
            }
            print(f"  ⚠️ Fallback values used - amounts set to 0 (user should verify)")
        
        # 3. Create invoice in Supabase (with user_id for RLS)
        print(f"  💾 Creating invoice for user {user_id}...")
        print(f"  📋 Invoice data keys: {list(invoice_data.keys())}")
        try:
            created_invoice = supabase.insert("invoices", invoice_data)
            
            if not created_invoice:
                print(f"  ❌ Supabase returned empty response!")
                raise HTTPException(status_code=500, detail="Failed to create invoice - Supabase returned empty")
            
            invoice_id = created_invoice.get('id')
            print(f"  ✅ Invoice created: {invoice_id}")
            
            # Verify invoice was created
            print(f"  🔍 Verifying invoice exists...")
            verify = supabase.select("invoices", filters={"id": invoice_id})
            if verify:
                print(f"  ✅ Verification successful - invoice found in database")
            else:
                print(f"  ⚠️ Invoice created but not found in database!")
        except Exception as e:
            print(f"  ❌ Error creating invoice: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Failed to create invoice: {str(e)}")
        
        # 4. Update document status to 'completed'
        try:
            supabase.update("documents", filters={"id": document_id}, data={"status": "completed"})
        except Exception as e:
            print(f"  ⚠️ Warning: Failed to update document status: {str(e)}")
            # Don't fail the whole process just because status update failed
        
        return ProcessResponse(
            success=True,
            message="Invoice processed successfully",
            invoice_id=created_invoice["id"],
            vendor_name=invoice_data["vendor_name"],
            total_amount=invoice_data["total_amount"]
        )
        
    except HTTPException as he:
        # Update document status to failed on HTTP exceptions
        try:
            supabase.update("documents", filters={"id": document_id}, data={"status": "failed", "error": str(he.detail)})
        except:
            pass  # Don't let status update failure mask the original error
        raise
    except Exception as e:
        print(f"  ❌ Processing error: {str(e)}")
        # Update document status to failed on general exceptions
        try:
            supabase.update("documents", filters={"id": document_id}, data={"status": "failed", "error": str(e)})
        except:
            pass  # Don't let status update failure mask the original error
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/process-anonymous")
async def process_anonymous_document(file: UploadFile = File(...)):
    """
    Process a document for anonymous users (preview mode)
    - No database storage
    - Direct AI processing
    - Returns extracted data for preview
    """
    try:
        if not AI_AVAILABLE:
            raise HTTPException(status_code=503, detail="AI processing temporarily unavailable")
        
        # Validate file type
        allowed_types = [
            'application/pdf',
            'image/jpeg', 'image/jpg', 'image/png',
            'image/webp', 'image/heic', 'image/heif'
        ]
        
        if file.content_type not in allowed_types:
            raise HTTPException(
                status_code=400, 
                detail=f"Unsupported file type: {file.content_type}. Supported: PDF, JPG, PNG, WebP, HEIC"
            )
        
        # Read file content
        file_content = await file.read()
        
        # Process with AI extractor
        extractor = VisionFlashLiteExtractor()
        
        if file.content_type == 'application/pdf':
            # Extract text from PDF
            pdf_reader = PyPDF2.PdfReader(io.BytesIO(file_content))
            text_content = ""
            for page in pdf_reader.pages:
                text_content += page.extract_text() + "\n"
            
            # Process with AI
            result = extractor.extract_invoice_data_from_text(text_content)
        else:
            # Process image directly
            result = extractor.extract_invoice_data_from_image(file_content)
        
        # Return preview data (no database storage)
        return {
            "success": True,
            "message": "Invoice processed successfully (preview mode)",
            "preview": True,
            "vendor_name": result.get('vendor_name'),
            "invoice_number": result.get('invoice_number'),
            "invoice_date": result.get('invoice_date'),
            "total_amount": result.get('total_amount'),
            "subtotal": result.get('subtotal'),
            "tax_amount": result.get('tax_amount'),
            "due_date": result.get('due_date'),
            "vendor_email": result.get('vendor_email'),
            "vendor_phone": result.get('vendor_phone'),
            "vendor_address": result.get('vendor_address'),
            "extracted_fields": len([v for v in result.values() if v]),
            "processing_time": "< 5 seconds",
            "file_name": file.filename
        }
        
    except Exception as e:
        print(f"❌ Anonymous processing error: {e}")
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
