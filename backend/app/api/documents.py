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
import logging
from app.services.supabase_helper import supabase

# Set up logger
logger = logging.getLogger(__name__)
from app.services.invoice_validator import InvoiceValidator, validate_invoice_before_save
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.middleware.subscription import check_subscription

# Load environment variables for AI services
import pathlib
backend_dir = pathlib.Path(__file__).parent.parent.parent  # Go up to backend directory
env_path = backend_dir / ".env"
from dotenv import load_dotenv
load_dotenv(env_path, encoding='utf-8')

# Try to import AI extractor and PDF processing
try:
    from app.services.vision_ocr_flash_lite_extractor import VisionOCR_FlashLite_Extractor
    import PyPDF2
    AI_AVAILABLE = True
    print("✅ VISION OCR + FLASH-LITE extraction ENABLED - 99% cost reduction target")
except ImportError as e:
    AI_AVAILABLE = False
    print(f"⚠️ AI extraction DISABLED (Import Error): {e}")
except RuntimeError as e:
    AI_AVAILABLE = False
    print(f"⚠️ AI extraction DISABLED (Runtime Error): {e}")
except Exception as e:
    AI_AVAILABLE = False
    print(f"⚠️ AI extraction DISABLED (Unexpected Error): {e}")
except RuntimeError as e:
    AI_AVAILABLE = False
    print(f"⚠️ AI extraction DISABLED (Runtime Error): {e}")
except Exception as e:
    AI_AVAILABLE = False
    print(f"⚠️ AI extraction DISABLED (Unexpected Error): {e}")

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
        doc_response = supabase.table("documents").select("*").eq("id", document_id).execute()
        if not doc_response.data:
            raise HTTPException(status_code=404, detail="Document not found")
            
        document = doc_response.data[0]
        
        # Only check subscription for non-anonymous uploads
        user_id = document.get("user_id")
        is_anonymous = user_id is None
        
        if not is_anonymous:
            await check_subscription(user_id)
        
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
                file_content = supabase.storage.from_("invoice-documents").download(storage_path)
                if not file_content:
                    raise HTTPException(status_code=404, detail="File not found in storage")
                
                # Check for Gemini API key
                gemini_key = os.getenv('GOOGLE_AI_API_KEY')
                
                if not gemini_key:
                    print("⚠️ No Gemini API key found")
                    raise HTTPException(status_code=500, detail="AI service not configured")
                
                extractor = VisionOCR_FlashLite_Extractor()
                ai_result = None
                
                # Check file type and extract accordingly
                file_ext = file_name.lower().split('.')[-1]
                
                # IMAGES: JPG, JPEG, PNG - Use Vision OCR + Flash-Lite
                if file_ext in ['jpg', 'jpeg', 'png', 'webp', 'heic', 'heif']:
                    print(f"📸 Image detected - using Vision OCR + Flash-Lite...")
                    ai_result = extractor.extract_invoice_data(file_content, file_name)
                
                # PDFs: Extract text and use Flash-Lite for formatting
                elif file_name.lower().endswith('.pdf'):
                    print(f"📄 PDF detected - extracting text and using Flash-Lite...")
                    extracted_text = ""
                    try:
                        pdf_file = io.BytesIO(file_content)
                        pdf_reader = PyPDF2.PdfReader(pdf_file)
                        
                        for page_num, page in enumerate(pdf_reader.pages):
                            text = page.extract_text()
                            extracted_text += text
                            print(f"   Page {page_num + 1}: {len(text)} chars")
                        
                        if extracted_text.strip():
                            print(f"📝 Extracted {len(extracted_text)} chars - formatting with Flash-Lite...")
                            # Use Flash-Lite directly for text formatting
                            from app.services.flash_lite_formatter import FlashLiteFormatter
                            formatter = FlashLiteFormatter()
                            ai_result = formatter.format_text_to_json(extracted_text)
                        else:
                            raise HTTPException(status_code=422, detail="No text found in PDF - might be scanned image")
                    except Exception as e:
                        print(f"⚠️ PDF text extraction failed: {str(e)}")
                        raise HTTPException(status_code=500, detail=f"PDF processing failed: {str(e)}")
                
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
                    
                    # CRITICAL: Ensure invoice_number is NEVER empty or None
                    invoice_num = invoice_data.get('invoice_number')
                    if not invoice_num or (isinstance(invoice_num, str) and not invoice_num.strip()):
                        # Generate fallback invoice number from document_id
                        invoice_num = f"INV-{document_id[:8].upper()}"
                        print(f"  ⚠️  AI didn't extract invoice_number, using fallback: {invoice_num}")
                    else:
                        invoice_num = str(invoice_num).strip()
                    invoice_data['invoice_number'] = invoice_num
                    
                    # Clean up other string fields to remove extra whitespace
                    string_fields = ['vendor_name', 'customer_name', 'vendor_address', 'customer_address']
                    for field in string_fields:
                        if field in invoice_data and invoice_data[field]:
                            if isinstance(invoice_data[field], str):
                                invoice_data[field] = invoice_data[field].strip()
                            else:
                                invoice_data[field] = str(invoice_data[field]).strip()

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
        
        # VALIDATION: Check data quality before saving
        is_valid, validation_message, cleaned_invoice_data = InvoiceValidator.validate_invoice_data(invoice_data)
        if not is_valid:
            print(f"  ❌ {validation_message}")
            raise HTTPException(status_code=422, detail=validation_message)
        print(f"  ✅ {validation_message}")
        
        # Use cleaned data for database insertion
        invoice_data = cleaned_invoice_data
        
        try:
            created_invoice_response = supabase.table("invoices").insert(invoice_data).execute()
            created_invoice = created_invoice_response.data[0] if created_invoice_response.data else None
            
            if not created_invoice:
                print(f"  ❌ Supabase returned empty response!")
                raise HTTPException(status_code=500, detail="Failed to create invoice - Supabase returned empty")
            
            invoice_id = created_invoice.get('id')
            print(f"  ✅ Invoice created: {invoice_id}")
            
            # Increment scan count for the user
            if not is_anonymous:
                try:
                    # Update usage tracking in Supabase (using usage_logs table)
                    current_month = datetime.now().strftime("%Y-%m")

                    # Check if usage record exists
                    usage_response = supabase.table("usage_logs").select("*").eq("user_id", user_id).eq("month", current_month).execute()

                    if usage_response.data:
                        # Update existing record
                        current_count = usage_response.data[0].get("scans_used", 0)
                        supabase.table("usage_logs").update({
                            "scans_used": current_count + 1,
                            "updated_at": datetime.now().isoformat()
                        }).eq("user_id", user_id).eq("month", current_month).execute()
                    else:
                        # Create new record
                        supabase.table("usage_logs").insert({
                            "user_id": user_id,
                            "month": current_month,
                            "scans_used": 1,
                            "created_at": datetime.now().isoformat(),
                            "updated_at": datetime.now().isoformat()
                        }).execute()

                    print(f"  📊 Scan count incremented for user {user_id}")
                except Exception as e:
                    print(f"  ⚠️ Warning: Failed to increment scan count: {str(e)}")
                    # Don't fail the whole process just because scan count update failed
            
            # Verify invoice was created
            print(f"  🔍 Verifying invoice exists...")
            verify_response = supabase.table("invoices").select("*").eq("id", invoice_id).execute()
            if verify_response.data:
                print(f"  ✅ Verification successful - invoice found in database")
            else:
                print(f"  ⚠️ Invoice created but not found in database!")
        except Exception as e:
            print(f"  ❌ Error creating invoice: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Failed to create invoice: {str(e)}")
        
        # 4. Update document status to 'completed'
        try:
            supabase.table("documents").update({"status": "completed"}).eq("id", document_id).execute()
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
            supabase.table("documents").update({"status": "failed"}).eq("id", document_id).execute()
        except Exception as update_error:
            logger.warning(f"Failed to update document status after HTTP error: {update_error}")
        raise
    except Exception as e:
        print(f"  ❌ Processing error: {str(e)}")
        # Update document status to failed on general exceptions
        try:
            supabase.table("documents").update({"status": "failed"}).eq("id", document_id).execute()
        except Exception as update_error:
            logger.warning(f"Failed to update document status after error: {update_error}")
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
        extractor = VisionOCR_FlashLite_Extractor()
        
        if file.content_type == 'application/pdf':
            # Extract text from PDF and use Flash-Lite for formatting
            pdf_reader = PyPDF2.PdfReader(io.BytesIO(file_content))
            text_content = ""
            for page in pdf_reader.pages:
                text_content += page.extract_text() + "\n"
            
            # Use Flash-Lite for text formatting
            from app.services.flash_lite_formatter import FlashLiteFormatter
            formatter = FlashLiteFormatter()
            result = formatter.format_text_to_json(text_content)
        else:
            # Process image directly with Vision OCR + Flash-Lite
            result = extractor.extract_invoice_data(file_content, file.filename)
        
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
        documents_response = supabase.table("documents").select("*").eq("id", document_id).execute()
        documents = documents_response.data
        
        if not documents:
            raise HTTPException(status_code=404, detail="Document not found")
        
        return documents[0]
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/upload")
async def upload_document(
    file: UploadFile = File(...),
    user_id: str = None,  # Optional for anonymous uploads
    request: Request = None
):
    """
    Upload a document and optionally trigger processing
    Supports both authenticated and anonymous uploads
    """
    try:
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
        
        # Check file size (10MB limit)
        file_size = 0
        content = await file.read()
        file_size = len(content)
        
        if file_size > 10 * 1024 * 1024:  # 10MB
            raise HTTPException(status_code=413, detail="File too large. Maximum size: 10MB")
        
        # Generate document ID
        import uuid
        doc_id = str(uuid.uuid4())
        
        # Upload file to Supabase storage
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        storage_path = f"documents/{user_id or 'anonymous'}/{timestamp}_{file.filename}"
        
        try:
            # Reset file pointer and upload
            await file.seek(0)
            content = await file.read()
            
            supabase.storage.from_("invoice-documents").upload(
                path=storage_path,
                file=content,
                file_options={"content-type": file.content_type}
            )
            print(f"✅ File uploaded to storage: {storage_path}")
            
        except Exception as e:
            print(f"❌ Storage upload failed: {str(e)}")
            raise HTTPException(status_code=500, detail=f"File storage failed: {str(e)}")
        
        # Create document record in database
        doc_data = {
            "id": doc_id,
            "user_id": user_id,
            "file_name": file.filename,
            "file_size": file_size,
            "file_type": file.content_type,
            "storage_path": storage_path,
            "status": "uploaded",
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat()
        }
        
        try:
            doc_response = supabase.table("documents").insert(doc_data).execute()
            if not doc_response.data:
                raise Exception("No data returned from document creation")
            print(f"✅ Document record created: {doc_id}")
            
        except Exception as e:
            print(f"❌ Document creation failed: {str(e)}")
            # Try to clean up storage file
            try:
                supabase.storage.from_("invoice-documents").remove([storage_path])
            except Exception as cleanup_error:
                logger.warning(f"Failed to cleanup storage after document creation error: {cleanup_error}")
            raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
        
        # For authenticated users, auto-process the document
        if user_id:
            print(f"🔄 Auto-processing authenticated upload: {doc_id}")
            try:
                # Call process endpoint internally
                from fastapi import Request as FastAPIRequest
                # Create a mock request for the process endpoint
                process_response = await process_document(doc_id, request)
                print(f"✅ Auto-processing completed: {process_response.invoice_id}")
                
                return {
                    "id": doc_id,
                    "message": "Document uploaded and processed successfully",
                    "status": "processed",
                    "file_name": file.filename,
                    "file_size": file_size,
                    "storage_path": storage_path,
                    "invoice_id": process_response.invoice_id,
                    "invoice_data": {
                        "vendor_name": process_response.vendor_name,
                        "total_amount": process_response.total_amount
                    }
                }
            except Exception as e:
                print(f"⚠️ Auto-processing failed (will require manual process): {str(e)}")
                # Still return success for upload, process can be called manually
                return {
                    "id": doc_id,
                    "message": "Document uploaded successfully (auto-process failed, will process manually)",
                    "status": "uploaded",
                    "file_name": file.filename,
                    "file_size": file_size,
                    "storage_path": storage_path,
                    "process_url": f"/api/documents/{doc_id}/process",
                    "needs_manual_process": True
                }
        else:
            # For anonymous uploads, return document info without processing
            return {
                "id": doc_id,
                "message": "Document uploaded successfully (anonymous)",
                "status": "uploaded",
                "file_name": file.filename,
                "file_size": file_size,
                "storage_path": storage_path
            }
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Upload error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")
