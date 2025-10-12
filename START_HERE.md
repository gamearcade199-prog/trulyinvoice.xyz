# 🚀 Quick Start Guide - TrulyInvoice

## ✅ What's Been Fixed

1. **Database Models** - All models now use UUIDs (compatible with Supabase)
2. **Connection Pooling** - Optimized for Supabase serverless PostgreSQL
3. **Complete SQL Schema** - Ready to execute in Supabase Dashboard
4. **Helper Scripts** - PowerShell scripts created for easy setup

---

## 📋 3-Step Setup (15 minutes total)

### STEP 1: Setup Supabase Database (5 minutes)

**Follow the detailed guide**: Open `SETUP_SUPABASE.md` and complete all steps.

**Quick Summary**:
1. Open Supabase Dashboard → SQL Editor
2. Copy entire `SUPABASE_SCHEMA.sql` → Paste → Run
3. Create storage bucket: `invoice-documents` (Private)
4. Verify 6 tables created

---

### STEP 2: Fix & Start Frontend (5 minutes)

**Option A - Automated (Recommended)**:
```powershell
# Right-click FIX_FRONTEND.ps1 → Run with PowerShell
# OR in PowerShell terminal:
.\FIX_FRONTEND.ps1
```

This script will:
- Clean node_modules and cache
- Reinstall all packages
- Start dev server

**Option B - Manual**:
```powershell
cd frontend
Remove-Item -Recurse -Force node_modules
Remove-Item -Force package-lock.json
npm install
npm run dev
```

**If SWC Error Persists**:
- Download Node.js v20 LTS: https://nodejs.org
- Install it
- Run `FIX_FRONTEND.ps1` again

---

### STEP 3: Start Backend (2 minutes)

**Automated**:
```powershell
# Right-click START_BACKEND.ps1 → Run with PowerShell
# OR in PowerShell terminal:
.\START_BACKEND.ps1
```

**Manual**:
```powershell
cd backend
.\venv\Scripts\activate
uvicorn app.main:app --reload
```

**Verify Backend**:
- Open http://localhost:8000/docs
- Should see Swagger API documentation

---

## 🧪 Test Your Setup

### 1. Register First User
1. Open http://localhost:3000
2. Click "Sign Up" or "Get Started"
3. Fill in details:
   - Email: `your@email.com`
   - Password: `password123` (min 8 chars)
   - Full Name: `Your Name`
   - Company: `Your Company`
4. Click Register

### 2. Verify Database
1. Go to Supabase Dashboard → Table Editor
2. Click `users` table → Should see your user
3. Click `categories` table → Should see 10 default categories
4. Click `subscriptions` table → Should see 1 starter subscription

### 3. Upload Test Invoice
1. Login to your account
2. Click "Upload Invoice"
3. Select a test invoice (PDF/JPG/PNG)
4. Wait for AI processing (15-30 seconds)
5. Verify extracted data appears

### 4. Check Supabase Storage
1. Supabase Dashboard → Storage → `invoice-documents`
2. Should see uploaded file in a UUID folder

---

## 🔧 Troubleshooting

### Frontend Won't Start (SWC Error)

**Symptom**: `next-swc.win32-x64-msvc.node is not a valid Win32 application`

**Solutions** (in order):
1. **Run**: `.\FIX_FRONTEND.ps1` (automated clean install)
2. **If fails**: Install Node.js v20 LTS from https://nodejs.org
3. **If still fails**: Run `npm install next@latest` (upgrade Next.js)

### Backend Database Errors

**Symptom**: `relation does not exist` or similar

**Solutions**:
1. Make sure you ran **all** of `SUPABASE_SCHEMA.sql`
2. Check `.env` file has correct `DATABASE_URL`
3. Verify Supabase project is active (not paused)

### Upload Fails

**Symptom**: File upload returns error

**Solutions**:
1. Check `invoice-documents` bucket exists in Supabase Storage
2. Verify bucket is set to **Private** (not public)
3. Make sure storage policies are created (see `SETUP_SUPABASE.md` Step 2.3)

### AI Extraction Returns Errors

**Symptom**: Processing stuck or returns errors

**Solutions**:
1. Verify `OPENAI_API_KEY` is valid in `backend/.env`
2. Verify `GOOGLE_CLOUD_VISION_API_KEY` is valid in `backend/.env`
3. Check backend logs for API errors
4. Ensure you have API credits available

---

## 📚 Important Files Reference

### Configuration Files
- `backend/.env` - Backend API keys and database URL
- `frontend/.env.local` - Frontend Supabase configuration
- `SUPABASE_SCHEMA.sql` - Complete database schema

### Documentation
- `DIAGNOSTIC_REPORT.md` - Detailed error analysis and fixes
- `SETUP_SUPABASE.md` - Step-by-step Supabase setup guide
- `README.md` - Project overview and features
- `QUICKSTART.md` - Original setup instructions

### Helper Scripts
- `FIX_FRONTEND.ps1` - Automated frontend fix and start
- `START_BACKEND.ps1` - Automated backend start

---

## 🌐 URLs After Setup

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs (Swagger)**: http://localhost:8000/docs
- **Supabase Dashboard**: https://app.supabase.com

---

## 🔑 Environment Variables Checklist

### Backend (.env)
- [x] `DATABASE_URL` - Supabase PostgreSQL connection string
- [x] `SUPABASE_URL` - Your Supabase project URL
- [x] `SUPABASE_SERVICE_ROLE_KEY` - Service role key from Supabase
- [x] `OPENAI_API_KEY` - Your OpenAI API key
- [x] `GOOGLE_CLOUD_VISION_API_KEY` - Your Google Cloud Vision API key
- [x] `SECRET_KEY` - JWT secret (auto-generated)

### Frontend (.env.local)
- [x] `NEXT_PUBLIC_SUPABASE_URL` - Same as backend SUPABASE_URL
- [x] `NEXT_PUBLIC_SUPABASE_ANON_KEY` - Anon/public key from Supabase
- [x] `NEXT_PUBLIC_API_URL` - Should be http://localhost:8000

---

## 📊 Architecture Overview

```
┌─────────────────┐
│   Frontend      │  Next.js 14 + React 18
│  (Port 3000)    │  Tailwind CSS
└────────┬────────┘
         │
         │ HTTP/REST
         ↓
┌─────────────────┐
│   Backend       │  FastAPI + Python 3.14
│  (Port 8000)    │  JWT Auth
└────────┬────────┘
         │
         ├─────────→ Google Cloud Vision API (OCR)
         │
         ├─────────→ OpenAI GPT-4o-mini (Extraction)
         │
         └─────────→ Supabase PostgreSQL
                     (Database + Storage)
```

---

## 🎯 Feature Checklist

### Implemented ✅
- [x] User registration and login (JWT)
- [x] Document upload (PDF/JPG/PNG)
- [x] OCR with Google Cloud Vision API
- [x] AI extraction with OpenAI GPT-4o-mini
- [x] Fallback to GPT-4o for low confidence
- [x] Automatic categorization (10 Indian business categories)
- [x] Subscription tiers (Starter/Pro/Business)
- [x] Usage tracking and limits
- [x] Invoice CRUD operations
- [x] GST field extraction (CGST/SGST/IGST)
- [x] Landing page UI
- [x] Supabase integration

### To Be Implemented 🔜
- [ ] Razorpay payment integration
- [ ] Export to CSV/Excel/Google Sheets
- [ ] Advanced search and filters
- [ ] Dashboard analytics
- [ ] Email notifications
- [ ] Mobile responsive design improvements

---

## 💰 Subscription Tiers

| Feature | Starter (Free) | Pro (₹499/mo) | Business (₹999/mo) |
|---------|----------------|---------------|-------------------|
| Scans/month | 30 | 200 | 750 |
| Data retention | 30 days | 90 days | Unlimited |
| Bulk upload | ❌ | ✅ | ✅ |
| Export | ❌ | ✅ CSV/Excel | ✅ All formats |
| API access | ❌ | ❌ | ✅ |
| Priority support | ❌ | ❌ | ✅ |

---

## 📞 Need More Help?

1. **Check Diagnostic Report**: Open `DIAGNOSTIC_REPORT.md` for detailed error analysis
2. **Review Supabase Setup**: Open `SETUP_SUPABASE.md` for database setup
3. **Check Logs**:
   - Backend: Look at terminal running `START_BACKEND.ps1`
   - Frontend: Look at terminal running `npm run dev`
   - Browser: Open DevTools → Console tab

---

## ✨ Quick Command Reference

### Start Everything
```powershell
# Terminal 1 - Backend
.\START_BACKEND.ps1

# Terminal 2 - Frontend
.\FIX_FRONTEND.ps1
```

### Stop Everything
- Press `Ctrl+C` in both terminals

### Reset Frontend
```powershell
cd frontend
Remove-Item -Recurse -Force node_modules, .next, package-lock.json
npm install
```

### Check Logs
```powershell
# Backend logs
cd backend
.\venv\Scripts\activate
uvicorn app.main:app --reload

# Frontend logs
cd frontend
npm run dev
```

---

## 🎉 You're All Set!

Your TrulyInvoice application should now be running successfully. 

**Next**: 
1. Register your first account
2. Upload a test invoice
3. See the AI magic happen! ✨

**Remember**: 
- Supabase schema must be executed first
- Both frontend and backend need to be running
- API keys must be valid and have credits

---

**Created**: System setup completed
**Status**: Ready for testing
**Estimated Setup Time**: 15 minutes
