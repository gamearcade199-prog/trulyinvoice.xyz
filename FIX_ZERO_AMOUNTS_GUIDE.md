# 🔧 FIXING ₹0 AMOUNTS & VIEW BUTTON - Quick Guide

## ✅ What I Just Fixed

### 1. View Button (FIXED ✅)
- **Issue**: "File path not found" error
- **Fix**: Added `storage_path` to invoice queries
- **Status**: Should work now after page refresh

### 2. Amount Showing ₹0 (NEEDS ACTION ⚠️)
- **Issue**: Backend hasn't processed uploaded invoices yet
- **Why**: You uploaded before backend was fully configured
- **Solution**: 2 options below

---

## 🚀 OPTION 1: Re-Upload (EASIEST - Recommended)

**This is the simplest solution:**

1. **Delete existing invoice** (the one showing ₹0)
   - Click the trash icon on the invoice row
   - Confirm deletion

2. **Re-upload the same PDF**
   - Go to Upload page
   - Drag & drop your invoice PDF
   - Click "Process Invoice"

3. **Watch it process**
   - Backend will automatically extract data
   - You'll see real amounts (not ₹0)
   - Takes ~5-10 seconds

**Why this works:**
- Backend is NOW running with AI extraction
- Upload page calls `/documents/{id}/process` automatically
- AI extracts: vendor, amount, GST, date, etc.

---

## 🔧 OPTION 2: Process Existing Invoice via API

**If you want to keep the existing upload:**

### Method A: Using Browser Console

1. Open your invoices page: http://localhost:3000/invoices
2. Press F12 to open Developer Tools
3. Go to **Console** tab
4. Run this command to get your access token:
   ```javascript
   (await supabase.auth.getSession()).data.session.access_token
   ```
5. Copy the token (long string)
6. Run this to process document ID 1 (replace TOKEN and ID):
   ```javascript
   fetch('http://localhost:8000/api/documents/1/process', {
     method: 'POST',
     headers: {
       'Authorization': 'Bearer YOUR_TOKEN_HERE',
       'Content-Type': 'application/json'
     }
   }).then(r => r.json()).then(console.log)
   ```

### Method B: Using Python Script

1. Get your access token (see Method A, step 4)
2. Edit `process_invoice.py` in your project folder
3. Update these lines:
   ```python
   DOCUMENT_ID = 1  # Your document ID from database
   ACCESS_TOKEN = "paste_token_here"
   ```
4. Run:
   ```bash
   python process_invoice.py
   ```

### Method C: Using Postman/Thunder Client

1. GET your access token (see Method A, step 4)
2. Create a POST request:
   - URL: `http://localhost:8000/api/documents/1/process`
   - Headers:
     - `Authorization: Bearer YOUR_TOKEN`
     - `Content-Type: application/json`
3. Send request
4. Check response for extracted data

---

## ✅ TESTING THE FIX

### Test View Button (Should work now!)

1. **Refresh your invoices page**: http://localhost:3000/invoices
2. **Click the eye icon** (👁️) on any invoice
3. **Expected**: PDF opens in new tab
4. **If it still fails**: 
   - Check browser console (F12 → Console)
   - Look for error message
   - Check that storage_path exists in database

### Test AI Extraction

**After re-uploading or processing:**

1. Invoice should show:
   - ✅ Actual vendor name (not "Processing...")
   - ✅ Real invoice number
   - ✅ Actual total amount (not ₹0)
   - ✅ Tax amount (GST)
   - ✅ Invoice date
   - ✅ Status: "Unpaid" (not "Processing")

2. Check backend logs for:
   ```
   INFO - Starting processing for document X
   INFO - Extracting data from [temp file path]
   INFO - Extraction successful. Confidence: 0.XX
   INFO - Created new invoice for document X
   ```

---

## 🐛 TROUBLESHOOTING

### View Button Still Shows "File path not found"

**Check in Browser Console:**
```javascript
// See what data you have
const { data } = await supabase.from('documents').select('*')
console.log(data)
```

**Look for:**
- Does `storage_path` column exist?
- Does it have a value like `user_id/filename.pdf`?

**If empty**, re-upload the file.

### AI Extraction Not Working

**Check Backend Logs:**
Look for errors in the backend terminal. Common issues:

1. **"No module named..."** → Missing Python package
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

2. **"API key not found"** → Missing environment variables
   - Check `backend/.env` has:
     - `OPENAI_API_KEY=sk-...`
     - `GOOGLE_CLOUD_VISION_API_KEY=...`
     - `SUPABASE_URL=...`
     - `SUPABASE_SERVICE_KEY=...`

3. **"Document not found"** → Wrong document ID
   - Check database for correct ID
   - Use the ID from your invoices page

### Amount Still Shows ₹0 After Processing

**Possible causes:**

1. **Processing failed** → Check backend logs for errors

2. **Invoice not created** → Check database:
   ```sql
   SELECT * FROM invoices WHERE document_id = 1;
   ```

3. **Frontend not refreshing** → Hard refresh (Ctrl+Shift+R)

4. **Data extraction failed** → AI couldn't read the PDF
   - Check PDF quality
   - Try a different invoice
   - Check backend logs for confidence score

---

## 📊 EXPECTED FLOW

### New Upload (After Fixes)
```
1. User uploads PDF → Frontend
   ↓
2. File saved to Supabase Storage
   ↓
3. Record created in documents table
   ↓
4. Frontend calls: POST /api/documents/{id}/process
   ↓
5. Backend downloads file from storage
   ↓
6. AI extracts: vendor, amount, GST, dates
   ↓
7. Backend saves to invoices table
   ↓
8. Frontend shows: ✅ Real data (not ₹0)
```

### View Button Flow
```
1. User clicks eye icon
   ↓
2. Frontend gets storage_path from invoice
   ↓
3. Creates signed URL (valid 1 hour)
   ↓
4. Opens PDF in new tab: ✅
```

---

## 🎯 QUICK CHECKLIST

Before reporting issues, verify:

- [ ] Backend is running (http://localhost:8000/health should return OK)
- [ ] Frontend is running (http://localhost:3000 loads)
- [ ] User is logged in (check top-right corner)
- [ ] Database migration ran successfully (SUPABASE_FIX_ALL.sql)
- [ ] Browser console shows no errors (F12 → Console)
- [ ] Backend terminal shows no errors

---

## 💡 RECOMMENDED ACTION

**Just re-upload the invoice!** It's the fastest way:

1. Delete the ₹0 invoice ❌
2. Upload the same PDF again 📤
3. Wait 5-10 seconds ⏳
4. See real data! ✅

The backend is now properly configured with enterprise-grade AI extraction. It will work!

---

## 📞 STILL STUCK?

If nothing works:

1. **Check backend terminal** for errors
2. **Check browser console** (F12) for errors
3. **Share error messages** - I'll help debug
4. **Try a different PDF** - ensure it's a valid invoice

---

**Everything should work now! Try re-uploading and let me know how it goes! 🚀**
