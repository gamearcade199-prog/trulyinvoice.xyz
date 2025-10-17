# 🚀 QUICK START - TEST NOW

## Systems Running

✅ Backend: http://localhost:8000
✅ Frontend: http://localhost:3000

## 3 Quick Tests

### 1️⃣ Backend Health (5 seconds)
```
http://localhost:8000/health
```
Should show: `{"status":"ok"}`

### 2️⃣ Upload Invoice (1 minute)
```
http://localhost:3000/dashboard
→ Click Upload
→ Select invoice image
→ Wait for processing
```

### 3️⃣ Click Eye Button (10 seconds)
```
→ Find invoice in list
→ Click 👁️ icon
→ Should see invoice details (NO 404!)
```

---

## Why It Says "No API Keys"

**Before:** Backend started without environment variables → API key not loaded

**Now:** Backend starts with API keys exported in PowerShell first

```powershell
$env:GOOGLE_AI_API_KEY="AIzaSyBEnD60M9_JkSzUz_ZiBolN9pe5fDodPSE"
python -m uvicorn app.main:app --reload --port 8000
```

---

## How to Start Backend (Recommended)

Instead of manual setup, use:
```powershell
cd backend
.\START_BACKEND_WITH_API_KEYS.ps1
```

This script sets API keys automatically before starting Python.

---

## If Eye Button Shows 404

✅ Upload a NEW invoice (ones from before the fix might not work)
✅ Check backend logs for extraction messages
✅ Verify backend is running (check terminal)

---

## Expected: Eye Button Works! ✅

```
Upload invoice → Backend extracts with Gemini ✅
Invoice saved with amount (NOT ₹0.00) ✅
Click eye button → See all details ✅
NO 404 error ✅
```

**Go test at:** http://localhost:3000/dashboard
