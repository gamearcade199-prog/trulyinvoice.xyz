# 🎯 LOCAL DEBUGGING STRATEGY - Why & How

## The Problem We're Solving

**Current Situation:**
- ❌ Invoices appear in list (created successfully)
- ❌ Clicking eye icon returns 404 error
- ❌ This happens on PRODUCTION (Vercel + Render)
- ✅ You said "this error didn't show up when testing locally"

**Why Remote Debugging is Hard:**
1. We deployed logging but can't see real-time output
2. Hard to know which step fails without being in control
3. Environment variables might be different
4. Multiple "redeploy cycles" waste time

**Why Local Debugging Solves It:**
1. **FULL CONTROL:** You run both frontend and backend
2. **INSTANT FEEDBACK:** See console logs immediately
3. **EXACT ERROR:** Know exactly where the 404 originates
4. **FAST FIX:** Once identified, fix is instant

---

## 🚀 What You Need to Do (Simple 3-Step Process)

### Step 1: Start Backend (Terminal 1)
```
Navigate to: C:\Users\akib\Desktop\trulyinvoice.in\backend

Option A (Batch file - Easiest):
  Double-click: START_BACKEND.bat

Option B (PowerShell):
  powershell.exe -ExecutionPolicy Bypass -File START_BACKEND_LOCAL.ps1

Option C (Manual):
  python -m venv venv
  .\venv\Scripts\Activate.ps1
  pip install -r requirements.txt
  python -m uvicorn app.main:app --reload --port 8000 --log-level debug
```

**When it's ready, you'll see:**
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete
```

### Step 2: Start Frontend (Terminal 2)
```
Navigate to: C:\Users\akib\Desktop\trulyinvoice.in\frontend

Option A (Batch file - Easiest):
  Double-click: START_FRONTEND.bat

Option B (Manual):
  npm install (if first time)
  npm run dev
```

**When it's ready, you'll see:**
```
  ▲ Next.js 14.1.0
  Local:        http://localhost:3000
```

### Step 3: Test in Browser
```
1. Open: http://localhost:3000
2. Press F12 to open DevTools → Console tab
3. Upload a test invoice image
4. Click the eye icon to view it
5. COPY ALL CONSOLE OUTPUT
```

---

## 📊 What Happens If It WORKS Locally

### Success: No 404

**Frontend Console shows:**
```
Fetching invoice details for ID: [ID]
Response status: 200
Invoice loaded: VENDOR_NAME
[Shows invoice details normally]
```

**Backend Terminal shows:**
```
GET /api/invoices/[ID]
Query result: 1 rows
Invoice found: VENDOR_NAME
```

**Next Action:**
- The issue is ENVIRONMENT-SPECIFIC in production
- We check Render environment variables
- We check Vercel environment variables
- We compare with your working local setup

---

## 📊 What Happens If It FAILS Locally (404 Error)

### Failure: 404 Appears

**Frontend Console shows:**
```
Fetching invoice details for ID: [ID]
Response status: 404
API Error: Invoice not found
```

**Backend Terminal shows:**
```
GET /api/invoices/[ID]
Query result: 0 rows
Invoice not found in database
```

**Next Action - We Know Exactly Where It Fails:**

1. **Invoice Creation Failed** (most likely)
   - Check backend logs during upload for errors
   - Verify SUPABASE_SERVICE_KEY is correct
   - Check Supabase has "invoices" table with columns
   
2. **Invoice Created But Deleted** (unlikely)
   - Query database: SELECT * FROM invoices LIMIT 1
   - Check if any invoices exist at all
   
3. **Invoice Created But Query Returns Wrong ID** (possible)
   - Compare invoice ID in URL with database ID
   - Verify no truncation or ID mismatch

4. **URL or API Connection Issue** (rare)
   - Frontend is calling correct URL
   - Backend is receiving request
   - Response is 404 (not 500 error)

---

## 🎯 The Real Advantage

**Local debugging gives you:**

✅ Complete visibility into the entire flow  
✅ Ability to add more logging in real-time  
✅ Database access while testing  
✅ Instant code changes with auto-reload  
✅ Clear understanding of what's failing  

**Instead of:**

❌ Guessing based on symptoms  
❌ Waiting for deployments  
❌ Hoping logs capture the right moment  
❌ Multiple redeploy cycles  

---

## 📋 Step-by-Step Test Checklist

After following the 3 steps above:

### Upload Phase
- [ ] Frontend shows upload in progress
- [ ] Backend terminal shows processing logs
- [ ] Upload completes without error
- [ ] Invoice appears in the list

### View Phase (The Critical Test)
- [ ] Click eye icon on the invoice
- [ ] Check frontend console for logs
- [ ] Check backend terminal for GET request logs
- [ ] Either:
  - ✅ Invoice detail page loads (no 404) - SUCCESS!
  - ❌ 404 error appears - FAILURE, BUT WE KNOW WHERE

### Data Verification
- [ ] Open Supabase dashboard
- [ ] Check "invoices" table
- [ ] Verify new invoice is there

---

## 🔍 Debugging Zones

```
┌─────────────────────────────────────────────────────────┐
│ ZONE 1: Frontend → Backend Connection                  │
├─────────────────────────────────────────────────────────┤
│ Frontend Console shows:                                 │
│  - "API URL: http://localhost:8000/api/invoices/[ID]"  │
│ Backend Terminal shows:                                 │
│  - "GET /api/invoices/[ID]"                            │
│                                                        │
│ If ZONE 1 fails:                                        │
│  - CORS error in browser console                       │
│  - Backend doesn't see the request                     │
│  - Solution: Check localhost:3000 → localhost:8000     │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│ ZONE 2: Backend → Database Query                        │
├─────────────────────────────────────────────────────────┤
│ Backend Terminal shows:                                 │
│  - "Querying Supabase for invoice..."                   │
│  - "Query result: 1 rows" (or "0 rows")                │
│                                                        │
│ If ZONE 2 fails:                                        │
│  - Query returns 0 rows but invoice was created        │
│  - Database connection issue                           │
│  - Solution: Verify Supabase credentials               │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│ ZONE 3: Upload → Invoice Creation                       │
├─────────────────────────────────────────────────────────┤
│ Backend Terminal shows during upload:                   │
│  - "Creating invoice for user..."                       │
│  - "Invoice created: [ID]"                              │
│                                                        │
│ If ZONE 3 fails:                                        │
│  - Upload completes but no invoice in database         │
│  - Gemini extraction failed                            │
│  - Supabase insert failed                              │
│  - Solution: Check backend error logs during upload     │
└─────────────────────────────────────────────────────────┘
```

---

## 🛠️ Common Issues & Quick Fixes

### "Backend won't start - Port 8000 in use"
```
Solution: Kill the process or use different port
netstat -ano | findstr :8000
taskkill /PID [PID] /F

Or start on different port:
python -m uvicorn app.main:app --reload --port 8001 --log-level debug
```

### "Frontend won't start - Port 3000 in use"
```
Solution: Kill the process or use different port
netstat -ano | findstr :3000
taskkill /PID [PID] /F
```

### "Backend won't install dependencies"
```
Solution: Install core packages only
pip install fastapi uvicorn python-dotenv pydantic supabase openai google-generativeai -q
```

### "Backend starts but no API response"
```
Solution: Test connectivity
curl http://localhost:8000/health
(Should return JSON response)
```

---

## 📝 When You Find the Issue

Once you identify where the 404 occurs, come back with:

1. **Complete frontend console output** (F12, Console tab)
2. **Complete backend terminal output** (entire terminal window)
3. **Screenshot of the 404 error page**
4. **Which zone failed** (1, 2, or 3 from above)

Then we can:
- Make a targeted fix
- Test it locally first
- Deploy confidently

---

## ⏱️ Estimated Time

- Backend setup & start: **5 minutes**
- Frontend setup & start: **3 minutes**
- Upload test invoice: **1 minute**
- Click eye icon & capture logs: **1 minute**

**Total: ~10 minutes to identify the exact issue**

---

## 🚀 Ready?

Start with **Step 1: Start Backend** using one of the methods above. Come back once you've captured the logs showing the 404 error (or success!).

**Files you have:**
- `LOCAL_DEBUGGING_START_HERE.md` - This guide
- `LOCAL_DEBUG_GUIDE.md` - Detailed technical guide
- `backend/START_BACKEND.bat` - Quick start script
- `frontend/START_FRONTEND.bat` - Quick start script

**Next Message:** Share your console logs + backend logs showing the upload and 404 error. That's all we need!
