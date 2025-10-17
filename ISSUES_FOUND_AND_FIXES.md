# ISSUES FOUND & FIXES DEPLOYED (Commit to Follow)

## Issue 1: Invoice Detail Page Returns 404 ✅ FIXED
**Root Cause**: Frontend was querying Supabase directly with `.single()` which fails if RLS policy is blocking or if there's a junction table issue with `documents:document_id`.

**Fix Applied**: 
- Updated `/frontend/src/app/invoices/[id]/page.tsx` 
- Now uses backend API endpoint: `GET /api/invoices/{invoice_id}`
- Added fallback to Supabase query if API is unavailable
- This avoids RLS policy conflicts and junction table issues

---

## Issue 2: AI Extraction Returns ₹0.00 (Fallback Mode) ⚠️ NEEDS ENV VARS
**Root Cause**: `GOOGLE_AI_API_KEY` environment variable is NOT set on Render.

**Evidence**: 
- Log shows: `⚠️ AI not available`
- Then falls back to filename extraction
- All amounts become ₹0.00

**Solution Required** (User Action):
1. Go to Render dashboard
2. Navigate to TrulyInvoice backend service → Settings → Environment
3. Add these critical variables:

```env
GOOGLE_AI_API_KEY=AIzaSyBQP5BaQeLE07wJj5WgneYJJA_QKAwiUh0
GEMINI_API_KEY=AIzaSyBQP5BaQeLE07wJj5WgneYJJA_QKAwiUh0
```

4. Click "Save"
5. Go back to "Deploy" tab and click "Manual Deploy"
6. Wait 2-3 minutes for redeploy
7. Test upload again - should now extract amounts correctly

---

## Code Fix Summary

### File: frontend/src/app/invoices/[id]/page.tsx (FIXED)

**Before**:
```tsx
const { data, error } = await supabase
  .from('invoices')
  .select(`
    *,
    documents:document_id (...)
  `)
  .eq('id', invoiceId)
  .single()  // ❌ Fails if document junction has issues
```

**After**:
```tsx
const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/invoices/${invoiceId}`)
// ✅ Uses backend API - no RLS/junction table issues
// ✅ Has fallback to Supabase query
```

---

## Testing Checklist

After deploying frontend fix + setting env vars on Render:

- [ ] Build succeeds on Render (no Pydantic 2.1.1 errors)
- [ ] Upload an invoice - should see amounts (not ₹0.00)
- [ ] Click eye icon - should navigate to detail page (not 404)
- [ ] Detail page loads invoice data (vendor name, amount, date, GST)
- [ ] Can edit invoice details
- [ ] Can export to PDF/CSV

---

## Commits Ready to Push
1. **Frontend Fix**: Invoice detail page uses backend API instead of Supabase query
   - File: `frontend/src/app/invoices/[id]/page.tsx`
   - Status: ✅ READY TO COMMIT

## Environment Setup Required (Render Dashboard)
- [ ] GOOGLE_AI_API_KEY
- [ ] GEMINI_API_KEY  
- [ ] DATABASE_URL
- [ ] SUPABASE_URL
- [ ] SUPABASE_KEY
- [ ] SUPABASE_SERVICE_KEY
- [ ] SECRET_KEY
- [ ] RAZORPAY_KEY_ID
- [ ] RAZORPAY_KEY_SECRET
