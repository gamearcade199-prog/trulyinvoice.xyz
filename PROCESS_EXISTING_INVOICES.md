# Process Existing Invoices - Fix ₹0 Amounts

## The Problem
Your 6 uploaded invoices show ₹0 because the AI extraction hasn't run yet. The backend endpoint uses SQLAlchemy which is currently disabled.

## Quick Solution Options

### Option 1: Re-upload (EASIEST - Recommended)
1. Make sure backend is running (`START_BACKEND.bat`)
2. Delete the existing invoices showing ₹0
3. Upload them again - the AI processing should happen automatically

### Option 2: Manually Call Backend API
For each document, call the processing endpoint:

```bash
# Get your document IDs from Supabase or frontend console
curl -X POST http://localhost:8000/documents/1/process \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

**Problem**: This endpoint is broken because it uses SQLAlchemy (which is disabled).

### Option 3: Fix Backend to Use Supabase (BEST - Permanent Fix)
The backend `/documents/{id}/process` endpoint needs to be rewritten to use Supabase client instead of SQLAlchemy.

## Recommended Action

**DELETE and RE-UPLOAD your invoices:**
1. Click the trash icon on each invoice in the Invoices page
2. Go to Upload page
3. Upload the same PDFs again
4. Backend should process them automatically (if it's running)

**Check backend is processing by:**
- Watching the backend terminal for logs when you upload
- If no logs appear, the upload page isn't calling the backend correctly

---

## Root Cause
The upload page calls `POST /documents/${docData.id}/process` but:
1. The endpoint expects SQLAlchemy database connection
2. We've disabled SQLAlchemy and use only Supabase
3. The endpoint crashes or returns error (silently caught in try-catch)

## What Needs Fixing
`backend/app/api/documents.py` line 226-360 must be rewritten to:
- Use Supabase client instead of `db.query(Document)`
- Download from storage correctly
- Call AI service
- Save to Supabase tables directly
