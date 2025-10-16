# 🔗 INTEGRATION GUIDE - Connect All 5 Fixes

Quick reference for integrating the 5 fixes into the main codebase.

---

## Fix #2: Payment Status - Already Integrated ✅

**File:** `backend/app/services/flash_lite_formatter.py`

**Status:** ✅ Code added, needs testing

**Integration:** Already done automatically in `format_text_to_json()` method

**Test it:**
```bash
python TEST_PAYMENT_STATUS_ENHANCED.py
```

**What to verify:**
- Payment status extracted with 90%+ accuracy
- Confidence scores populated
- All 10 test scenarios pass

---

## Fix #3: Image Quality - Ready to Integrate

**File:** `backend/app/services/image_quality_checker.py`

**Status:** ✅ Service ready, needs endpoint connection

**Step 1: Import in documents API**
```python
# In backend/app/api/documents.py

from app.services.image_quality_checker import ImageQualityChecker

checker = ImageQualityChecker()
```

**Step 2: Add quality check to upload endpoint**
```python
@app.post("/api/documents/upload")
async def upload_document(file: UploadFile = File(...)):
    """Upload and process invoice"""
    
    # Read file
    file_content = await file.read()
    
    # Check image quality FIRST
    quality_result = checker.check_quality(file_content)
    
    # Reject if poor quality
    if not quality_result['can_process']:
        return JSONResponse(
            status_code=400,
            content={
                "status": "rejected",
                "reason": "Image quality too low",
                "quality": quality_result['quality'],
                "score": quality_result['score'],
                "recommendations": quality_result['recommendations']
            }
        )
    
    # Continue with existing upload logic
    # Process invoice with Vision API
    # Save to database
    
    return {
        "status": "success",
        "file_id": file_id,
        "quality_check": {
            "quality": quality_result['quality'],
            "score": quality_result['score']
        }
    }
```

**Step 3: Store quality metadata**
```python
# Store in documents table
document = {
    "file_id": file_id,
    "image_quality": quality_result['quality'],  # 'good', 'fair', 'poor'
    "image_quality_score": quality_result['score'],  # 0-100
    "image_quality_details": quality_result['details'],  # JSON
    # ... other fields
}
```

---

## Fix #4: Batch Processing - Ready to Integrate

**File:** `backend/app/services/batch_processor.py`

**Status:** ✅ Service ready, needs endpoint creation

**Step 1: Import in documents API**
```python
# In backend/app/api/documents.py

from app.services.batch_processor import BatchProcessor, BatchItem
import asyncio

processor = BatchProcessor(max_concurrent=5, max_retries=2)
```

**Step 2: Create batch processing function**
```python
async def process_single_invoice(item: BatchItem) -> Dict[str, Any]:
    """Process a single invoice (called by batch processor)"""
    
    try:
        # Read file
        with open(item.file_path, 'rb') as f:
            file_content = f.read()
        
        # Check quality
        quality_result = checker.check_quality(file_content)
        if not quality_result['can_process']:
            raise Exception(f"Poor image quality: {quality_result['quality']}")
        
        # Extract text with Vision API
        text = await extract_text_with_vision_api(file_content)
        
        # Format with Gemini
        invoice_data = await format_with_gemini(text)
        
        # Save to database
        document = await save_document(item.file_id, invoice_data)
        
        return {
            "file_id": item.file_id,
            "document_id": document.id,
            "status": "success"
        }
    
    except Exception as e:
        raise Exception(f"Failed to process {item.file_id}: {str(e)}")
```

**Step 3: Create batch upload endpoint**
```python
@app.post("/api/documents/batch-upload")
async def batch_upload(files: List[UploadFile] = File(...)):
    """Upload and process multiple invoices in parallel"""
    
    try:
        # Save all files to temp directory
        items = []
        for file in files:
            content = await file.read()
            temp_path = f"/tmp/{file.filename}"
            
            with open(temp_path, 'wb') as f:
                f.write(content)
            
            items.append(BatchItem(
                id=str(uuid.uuid4()),
                file_id=file.filename,
                file_path=temp_path,
                file_size=len(content)
            ))
        
        # Process in parallel
        batch_result = await processor.process_batch(
            items,
            process_single_invoice
        )
        
        # Clean up temp files
        for item in items:
            try:
                os.remove(item.file_path)
            except:
                pass
        
        return {
            "batch_id": batch_result['batch_id'],
            "total": batch_result['total'],
            "succeeded": batch_result['succeeded'],
            "failed": batch_result['failed'],
            "success_rate": batch_result['success_rate'],
            "duration_ms": batch_result['duration_ms']
        }
    
    except Exception as e:
        return JSONResponse(
            status_code=400,
            content={"error": str(e)}
        )
```

---

## Fix #5: Invoice Edit UI - Already Created ✅

**File:** `frontend/pages/invoices/[id]/edit.tsx`

**Status:** ✅ Page ready, needs navigation integration

**Step 1: Add link in invoice list page**
```typescript
// In frontend/pages/invoices/index.tsx

import Link from 'next/link';

function InvoiceRow({ invoice }) {
    return (
        <tr>
            <td>{invoice.invoice_number}</td>
            <td>{invoice.vendor_name}</td>
            <td>₹{invoice.amount_total}</td>
            <td>
                <Link href={`/invoices/${invoice.id}`}>
                    <button>View</button>
                </Link>
                <Link href={`/invoices/${invoice.id}/edit`}>
                    <button>Edit</button>
                </Link>
            </td>
        </tr>
    );
}
```

**Step 2: Verify all fields in database schema**
```sql
-- Ensure documents table has all fields needed for edit page
SELECT column_name FROM information_schema.columns 
WHERE table_name = 'documents' 
ORDER BY column_name;

-- Should include:
-- id, user_id, file_id, file_name
-- invoice_number, invoice_date, due_date
-- vendor_name, vendor_email, vendor_phone, vendor_address, vendor_gstin
-- amount_total, tax_amount, amount_net
-- payment_status, payment_status_confidence, currency
-- extracted_data, created_at, updated_at
```

---

## 🎯 Integration Checklist

### Backend Integration

- [ ] **Image Quality (Fix #3)**
  - [ ] Import `ImageQualityChecker` in documents.py
  - [ ] Add quality check to upload endpoint
  - [ ] Reject poor quality images with recommendations
  - [ ] Store quality metadata in database

- [ ] **Batch Processing (Fix #4)**
  - [ ] Import `BatchProcessor` in documents.py
  - [ ] Create `process_single_invoice()` function
  - [ ] Create `/api/documents/batch-upload` endpoint
  - [ ] Test with 20+ files concurrently

- [ ] **Payment Status Testing (Fix #2)**
  - [ ] Run `TEST_PAYMENT_STATUS_ENHANCED.py`
  - [ ] Verify 90%+ accuracy achieved
  - [ ] Deploy enhanced formatter

### Frontend Integration

- [ ] **Navigation**
  - [ ] Add "Edit" button to invoice list
  - [ ] Link points to `/invoices/[id]/edit`
  - [ ] Verify next.js routing works

- [ ] **Edit Page**
  - [ ] Load invoice data correctly
  - [ ] Show confidence scores
  - [ ] Save changes to database
  - [ ] Delete invoice with confirmation

### Database Schema

- [ ] **Verify Columns Exist**
  ```sql
  -- Check schema
  \d documents
  
  -- Add missing columns if needed
  ALTER TABLE documents ADD COLUMN image_quality TEXT;
  ALTER TABLE documents ADD COLUMN image_quality_score INTEGER;
  ```

---

## 📊 Testing Checklist

- [ ] **Payment Status (Fix #2)**
  ```bash
  python TEST_PAYMENT_STATUS_ENHANCED.py
  # Expected: ✅ 90%+ accuracy
  ```

- [ ] **Image Quality (Fix #3)**
  - [ ] Test with good quality image → should process
  - [ ] Test with blurry image → should reject
  - [ ] Test with dark image → should reject
  - [ ] Test with bright/washed image → should warn

- [ ] **Batch Processing (Fix #4)**
  - [ ] Upload 20 files → should process in parallel
  - [ ] Verify ~5x speedup vs sequential
  - [ ] Test error handling (1 failure shouldn't crash batch)

- [ ] **Invoice Edit (Fix #5)**
  - [ ] Load invoice → displays all fields
  - [ ] Edit field → shows as modified
  - [ ] Save → database updates
  - [ ] Delete → removes from database

- [ ] **Vision API (Fix #1)**
  - [ ] Enable in Google Cloud Console
  - [ ] Verify API key works
  - [ ] Check cost savings (₹0.50 → ₹0.13)

---

## 🚀 Deployment Timeline

**Phase 1: Testing (Today - 30 min)**
1. Run payment status tests
2. Verify image quality checks
3. Test batch processing

**Phase 2: Backend (Tomorrow - 1-2 hours)**
1. Integrate image quality checker
2. Integrate batch processor
3. Deploy updated payment status
4. Enable Vision API

**Phase 3: Frontend (Day 3 - 1 hour)**
1. Deploy edit page
2. Add navigation links
3. Test end-to-end

---

**Ready for integration!** 🎉
