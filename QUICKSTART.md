# 🚀 Quick Start Guide - TrulyInvoice

Get TrulyInvoice running in 10 minutes!

## Prerequisites Check

- [ ] Node.js 18+ installed (`node --version`)
- [ ] Python 3.11+ installed (`python --version`)
- [ ] PostgreSQL OR Supabase account
- [ ] Google Cloud Vision API key
- [ ] Anthropic API key

---

## Step 1: Clone & Setup (2 min)

```powershell
# Navigate to project
cd c:\Users\akib\Desktop\trulyinvoice.in
```

---

## Step 2: Backend Setup (3 min)

```powershell
# Go to backend
cd backend

# Create virtual environment
python -m venv venv
.\venv\Scripts\activate

# Install dependencies (this may take 2-3 minutes)
pip install -r requirements.txt

# Copy environment file
copy .env.example .env

# Edit .env with your actual API keys
notepad .env
```

**Required in .env**:
```
DATABASE_URL=postgresql://user:pass@localhost:5432/trulyinvoice
SECRET_KEY=change-this-to-random-string
GOOGLE_CLOUD_VISION_API_KEY=your_key
ANTHROPIC_API_KEY=sk-ant-your-key
SUPABASE_URL=https://xxx.supabase.co
SUPABASE_KEY=your_key
```

**Important**: Set Google credentials
```powershell
$env:GOOGLE_APPLICATION_CREDENTIALS="C:\path\to\service-account.json"
```

---

## Step 3: Start Backend (1 min)

```powershell
# Still in backend directory with venv activated
uvicorn app.main:app --reload
```

✅ Backend running at: http://localhost:8000  
✅ API docs at: http://localhost:8000/docs

---

## Step 4: Frontend Setup (3 min)

**Open a NEW terminal window**

```powershell
# Navigate to frontend
cd c:\Users\akib\Desktop\trulyinvoice.in\frontend

# Install dependencies (2-3 minutes)
npm install

# Copy environment file
copy .env.example .env.local

# Edit if needed
notepad .env.local
```

---

## Step 5: Start Frontend (1 min)

```powershell
# Still in frontend directory
npm run dev
```

✅ Frontend running at: http://localhost:3000

---

## Step 6: Test It! (2 min)

### Open Browser

Visit: http://localhost:3000

You should see the beautiful landing page!

### Test API

Visit: http://localhost:8000/docs

Try the `/health` endpoint - you should get:
```json
{"status": "healthy"}
```

### Register a User

1. Click "Start Free Trial" on the landing page, OR
2. Use the API docs at http://localhost:8000/docs
3. POST to `/api/auth/register` with:
   ```json
   {
     "email": "test@example.com",
     "password": "password123",
     "full_name": "Test User"
   }
   ```

---

## Common Issues

### ❌ "Module not found" (Backend)
```powershell
# Ensure venv is activated
.\venv\Scripts\activate
pip install -r requirements.txt
```

### ❌ "Database connection error"
- Check your `DATABASE_URL` in `.env`
- Ensure PostgreSQL is running OR Supabase credentials are correct

### ❌ "Google Cloud Vision error"
- Verify `GOOGLE_APPLICATION_CREDENTIALS` is set
- Check the JSON file path is correct
- Ensure Cloud Vision API is enabled in Google Cloud Console

### ❌ Port already in use
```powershell
# Use different ports
uvicorn app.main:app --reload --port 8001
npm run dev -- -p 3001
```

---

## Next Steps

1. **Build the Dashboard** (frontend/src/app/dashboard)
2. **Add API client** (frontend/src/lib/api.ts)
3. **Create upload component**
4. **Implement invoice table**

See `PROJECT_STATUS.md` for detailed roadmap!

---

## File Structure

```
trulyinvoice.in/
├── backend/          ← FastAPI application
├── frontend/         ← Next.js application
├── README.md         ← Project overview
├── SETUP.md          ← Detailed setup guide
├── PROJECT_STATUS.md ← Current status
└── QUICKSTART.md     ← This file!
```

---

## Help & Resources

- **Backend API Docs**: http://localhost:8000/docs
- **Full Setup Guide**: See `SETUP.md`
- **Project Status**: See `PROJECT_STATUS.md`

---

**Happy coding! 🎉**
