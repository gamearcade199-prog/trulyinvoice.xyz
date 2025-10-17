# COPY-PASTE READY COMMANDS

## ⚡ Fast Path - Copy & Paste These Commands

### TERMINAL 1 - Start Backend (Copy everything below, paste into PowerShell)

```powershell
cd C:\Users\akib\Desktop\trulyinvoice.in\backend; python -m venv venv; .\venv\Scripts\Activate.ps1; pip install fastapi uvicorn python-dotenv pydantic pydantic-settings email-validator python-multipart requests PyPDF2 reportlab openpyxl Pillow supabase openai google-generativeai razorpay sqlalchemy passlib pyotp slowapi -q; python -m uvicorn app.main:app --reload --port 8000 --log-level debug
```

**Expected Result:**
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete
```

---

### TERMINAL 2 - Start Frontend (Open NEW PowerShell, copy & paste)

```powershell
cd C:\Users\akib\Desktop\trulyinvoice.in\frontend; npm install -q; npm run dev
```

**Expected Result:**
```
Local:        http://localhost:3000
```

---

### BROWSER

1. Open: **http://localhost:3000**
2. Press **F12** → Click **Console** tab
3. **Upload a test invoice**
4. **Click the eye icon**
5. **Copy ALL text in console**
6. **Paste in your next message**

---

## 🎯 Signs It's Working

### Backend Terminal Should Show (After Step 1):
```
INFO:     Started server process [12345]
INFO:     Waiting for application startup.
INFO:     Application startup complete
INFO:     Uvicorn running on http://127.0.0.1:8000
```

### Frontend Terminal Should Show (After Step 2):
```
  ▲ Next.js 14.1.0
  Local:        http://localhost:3000
```

### Browser Should Show:
```
Page loads with "Upload Invoice" button
```

---

## ❌ If Something Breaks

### Backend fails to install
Use this instead (bare minimum):
```powershell
cd C:\Users\akib\Desktop\trulyinvoice.in\backend
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install fastapi uvicorn -q
python -m uvicorn app.main:app --reload --port 8000 --log-level debug
```

### Frontend won't start
Make sure backend is running first, then:
```powershell
cd C:\Users\akib\Desktop\trulyinvoice.in\frontend
npm run dev
```

### Port already in use
```powershell
# Check what's using port 8000
netstat -ano | findstr :8000

# Kill it (replace PID with number from above)
taskkill /PID PID_HERE /F
```

---

## 📊 When Upload Completes

You should see in **browser console**:
```
Upload completed
Invoice ID: 357a0e56-f383-4564-8e03-8808948a25d1
Invoice appears in list
```

Then in **backend terminal**, look for:
```
POST /api/documents/
Processing document...
Creating invoice...
Invoice created: 357a0e56-f383-4564-8e03-8808948a25d1
```

---

## 📊 When You Click Eye Icon

### FRONTEND CONSOLE should show:
```
Fetching invoice details for ID: 357a0e56-f383-4564-8e03-8808948a25d1
API URL: http://localhost:8000/api/invoices/357a0e56-f383-4564-8e03-8808948a25d1
Fetching from: http://localhost:8000/api/invoices/357a0e56-f383-4564-8e03-8808948a25d1
Response status: 200 OR 404
```

### BACKEND TERMINAL should show:
```
GET /api/invoices/357a0e56-f383-4564-8e03-8808948a25d1
Querying Supabase for invoice...
Query result: 1 rows OR 0 rows
Invoice found: VENDOR_NAME OR Invoice not found in database
```

---

## 🎯 What to Do Next

1. **Run Terminal 1 command** (backend)
2. **Wait 30 seconds** for backend to start
3. **Run Terminal 2 command** (frontend)
4. **Wait 10 seconds** for frontend to start
5. **Open browser** to http://localhost:3000
6. **Upload invoice** and watch console
7. **Click eye icon** and watch for 404
8. **Copy all console output**
9. **Reply with the output**

That's it! We'll identify the issue from the logs.

---

## 🚨 IMPORTANT

- **Do NOT close Terminal 1** - Backend must stay running
- **Do NOT close Terminal 2** - Frontend must stay running
- **Press F12 BEFORE uploading** - To capture all logs
- **Copy EVERYTHING** in console - Don't leave anything out
- **Include backend logs too** - Show me the terminal window output

Once I see both frontend console + backend terminal output, I'll know exactly what's wrong!

🚀 Ready? Paste the Terminal 1 command now!
