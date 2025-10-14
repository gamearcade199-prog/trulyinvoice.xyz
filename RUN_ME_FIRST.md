# 🚀 Quick Commands to Start TrulyInvoice

## ✅ Step 1: Database is Ready!
Your Supabase database schema is now fixed and ready to run.

---

## 🔧 Step 2: Start Frontend

### EASY WAY (Double-click the file):
1. Open File Explorer
2. Navigate to: `C:\Users\akib\Desktop\trulyinvoice.xyz`
3. **Double-click**: `start-frontend.bat`

### OR in Command Prompt/PowerShell:
```powershell
cd C:\Users\akib\Desktop\trulyinvoice.xyz
start-frontend.bat
```

This will:
- Clean old files
- Reinstall packages
- Start the dev server at http://localhost:3000

---

## 🖥️ Step 3: Start Backend (in a NEW window)

### EASY WAY (Double-click the file):
1. Open File Explorer
2. Navigate to: `C:\Users\akib\Desktop\trulyinvoice.xyz`
3. **Double-click**: `start-backend.bat`

### OR in Command Prompt/PowerShell:
```powershell
cd C:\Users\akib\Desktop\trulyinvoice.xyz
start-backend.bat
```

---

## 🌐 After Both Start

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

---

## ⚠️ If Frontend Still Has SWC Error

1. **Download Node.js v20 LTS**: https://nodejs.org/en/download
2. **Install it** (will replace v22)
3. **Run the frontend commands again** (above)

---

## ✅ Next: Create Storage Bucket

After servers start, go to **Supabase Dashboard**:

1. Click **Storage** in left sidebar
2. Click **Create a new bucket**
3. Name: `invoice-documents`
4. **Public bucket**: OFF (keep private)
5. Click **Create bucket**

---

## 📝 Quick Summary

**What we fixed**:
- ✅ Database schema reordered (categories before invoices)
- ✅ All backend models use UUIDs
- ✅ Connection pooling optimized
- ✅ Helper scripts created

**What you need to do**:
1. ✅ ~~Run updated SQL in Supabase~~ (DONE - tables created)
2. 🔄 Fix and start frontend (commands above)
3. 🔄 Start backend (commands above)
4. 🔄 Create storage bucket in Supabase Dashboard
5. 🔄 Test by registering a user

---

## 🆘 Having Issues?

**Frontend won't start**:
- Install Node.js v20 from https://nodejs.org
- Then repeat frontend commands

**Backend errors**:
- Check `backend/.env` has all API keys
- Make sure virtual environment is activated

**Database errors**:
- Verify all tables exist in Supabase Table Editor
- Should see: users, subscriptions, categories, documents, invoices, usage_logs

---

**YOU ARE HERE** → Next: Run the frontend fix commands above! 👆
