# 🚀 LOCAL DEBUGGING - QUICK START INSTRUCTIONS

## ⚠️ IMPORTANT: Why Local Testing Works Better Than Production

**Problem with Production Debugging:**
- Remote logs are hard to capture in real-time
- Environmental differences between local and Render/Vercel
- Can't easily inspect database state while debugging
- Multiple deployment delays

**Advantage of Local Debugging:**
- Full visibility into console logs AND backend logs simultaneously
- Can query database directly while testing
- Can edit code and see changes instantly
- Can identify exact failure point in the flow

---

## 📌 QUICK START (Copy & Paste)

### Terminal 1 - Start Backend

```powershell
cd C:\Users\akib\Desktop\trulyinvoice.in\backend
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
python -m uvicorn app.main:app --reload --port 8000 --log-level debug
```

**When ready, you should see:**
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete
```

### Terminal 2 - Start Frontend

```powershell
cd C:\Users\akib\Desktop\trulyinvoice.in\frontend
npm install
npm run dev
```

**When ready, you should see:**
```
Local:        http://localhost:3000
```

### Browser - Test

1. Open: **http://localhost:3000**
2. Press **F12** to open DevTools
3. Go to **Console** tab
4. Upload a test invoice
5. Click the **eye icon** to view it
6. **Copy ALL console output and backend output**

---

## 🔍 What to Look For

### Success Path (NO 404):
```
Frontend Console:
  "Fetching invoice details for ID: 357a0e56-f383-4564-8e03-8808948a25d1"
  "Response status: 200"
  "Invoice loaded: [VENDOR_NAME]"
  
Backend Terminal:
  "GET /api/invoices/357a0e56-f383-4564-8e03-8808948a25d1"
  "Query result: 1 rows"
  "Invoice found: ACME Corporation"
```

### Failure Path (WITH 404):
```
Frontend Console:
  "Fetching invoice details for ID: 357a0e56-f383-4564-8e03-8808948a25d1"
  "Response status: 404"
  "API Error: Invoice not found"
  
Backend Terminal:
  "GET /api/invoices/357a0e56-f383-4564-8e03-8808948a25d1"
  "Query result: 0 rows"
  "Invoice not found in database"
```

---

## 🛠️ If Backend Won't Install Dependencies

The error you saw about `psycopg2` is **EXPECTED** - it's not needed locally!

**Fix: Skip it and use what's already installed**

```powershell
# In backend directory with venv activated:
pip install fastapi uvicorn python-dotenv pydantic pydantic-settings email-validator python-multipart requests PyPDF2 reportlab openpyxl Pillow supabase openai google-generativeai razorpay sqlalchemy passlib pyotp slowapi -q
```

Then try starting the backend again:
```powershell
python -m uvicorn app.main:app --reload --port 8000 --log-level debug
```

---

## 📊 Expected Invoice Creation Flow (Upload Phase)

When you upload a test invoice, you should see in **FRONTEND CONSOLE**:

```javascript
POST /api/documents - uploading...
Response: {
  "status": "success",
  "invoice_id": "357a0e56-f383-4564-8e03-8808948a25d1",
  "vendor_name": "ACME Corporation"
}
Upload complete! Invoice added to list.
```

And in **BACKEND TERMINAL**, you should see:

```
POST /api/documents/upload
Processing document...
Extracting invoice data...
Creating invoice for user akib@example.com...
Invoice created: 357a0e56-f383-4564-8e03-8808948a25d1
```

---

## 📊 Expected Invoice Fetch Flow (View Phase)

When you click the eye icon, **FRONTEND CONSOLE** shows:

```javascript
Fetching invoice details for ID: 357a0e56-f383-4564-8e03-8808948a25d1
API URL: http://localhost:8000/api/invoices/357a0e56-f383-4564-8e03-8808948a25d1
Fetching from: http://localhost:8000/api/invoices/357a0e56-f383-4564-8e03-8808948a25d1
Response status: 200
Invoice loaded: ACME Corporation
```

And **BACKEND TERMINAL** shows:

```
GET /api/invoices/357a0e56-f383-4564-8e03-8808948a25d1
Querying Supabase for invoice...
Query result: 1 rows
Invoice found: ACME Corporation
```

---

## ❌ If You See 404 Locally

This tells us exactly where to fix it:

### Issue 1: Invoice Not Being Created
**Symptom:** Upload happens, but backend shows "0 rows found"
**Solution:** 
- Check backend logs for errors during "Creating invoice..."
- Verify SUPABASE_SERVICE_KEY in backend/.env is correct
- Check Supabase has "invoices" table

### Issue 2: Wrong URL Being Called
**Symptom:** Frontend console shows wrong URL (not localhost:8000)
**Solution:**
- Check frontend/.env.local has: `NEXT_PUBLIC_API_URL=http://localhost:8000`
- Restart frontend (npm run dev)
- Clear browser cache: Ctrl+Shift+Del

### Issue 3: Backend Not Responding
**Symptom:** Backend logs don't show "GET /api/invoices/..." when you click eye
**Solution:**
- Verify backend is actually running on port 8000
- Test: `curl http://localhost:8000/` should show API response
- Check firewall isn't blocking port 8000

### Issue 4: Database Connection
**Symptom:** Backend shows error connecting to Supabase
**Solution:**
- Verify backend/.env has all Supabase keys
- Test from Python:
  ```python
  from app.services.supabase_helper import supabase
  result = supabase.select("invoices", limit=1)
  print(result)
  ```

---

## 💾 Capturing Logs for Analysis

### Browser Console
1. Press F12 when the error happens
2. Right-click in console → "Save as..."
3. Save to file (e.g., `frontend_logs.txt`)

### Backend Terminal
1. Select all terminal output (Ctrl+A)
2. Copy (Ctrl+C)
3. Paste into file (e.g., `backend_logs.txt`)

### Share These Files
Once you have both files showing the 404 error, share them and we can immediately identify the exact issue!

---

## ✅ Next Steps

1. **Run the quick start commands above** (two terminals + browser)
2. **Upload a test invoice** and watch the console
3. **Click the eye icon** to view it
4. **If 404 appears:** Share the console logs
5. **If it works:** We know the issue is environment-specific in production

The beauty of local debugging: **If it works locally, the fix is 100% clear. If it fails locally, the fix is obvious.**

---

## 🎯 Your Goal

Get to this point locally:
1. ✅ Backend running on http://localhost:8000
2. ✅ Frontend running on http://localhost:3000  
3. ✅ Upload invoice successfully
4. ✅ Click eye icon to view detail (not 404!)
5. ✅ Share logs if 404 still appears

**Once this works locally, we KNOW exactly how to fix production! 🚀**
