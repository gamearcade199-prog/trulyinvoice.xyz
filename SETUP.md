# TrulyInvoice - Development Setup Guide

## Prerequisites

Before you begin, ensure you have the following installed:

### Required Software
- **Node.js** 18+ and npm (for frontend)
- **Python** 3.11+ (for backend)
- **PostgreSQL** 14+ (or use Supabase)
- **Git** (for version control)

### API Keys Required
1. **Google Cloud Vision API**
   - Go to https://console.cloud.google.com/
   - Create a new project or select existing
   - Enable Cloud Vision API
   - Create service account and download credentials JSON
   - Set `GOOGLE_APPLICATION_CREDENTIALS` environment variable

2. **Anthropic API**
   - Sign up at https://console.anthropic.com/
   - Generate API key
   - Add to backend `.env` file

3. **Supabase** (recommended) or AWS S3
   - Create project at https://supabase.com/
   - Get URL and anon key from project settings
   - Alternatively, use AWS S3 with access keys

4. **Razorpay** (for Phase 2)
   - Sign up at https://razorpay.com/
   - Get test keys from dashboard

---

## Part 1: Backend Setup

### Step 1: Navigate to Backend Directory

```powershell
cd backend
```

### Step 2: Create Virtual Environment

```powershell
python -m venv venv
.\venv\Scripts\activate
```

### Step 3: Install Dependencies

```powershell
pip install -r requirements.txt
```

### Step 4: Configure Environment Variables

```powershell
copy .env.example .env
```

Edit `.env` file with your actual credentials:

```env
# Database - Use Supabase or local PostgreSQL
DATABASE_URL=postgresql://postgres:password@localhost:5432/trulyinvoice

# Security - Generate a secure key
SECRET_KEY=your-very-secure-secret-key-here

# Google Cloud Vision
# First, download service account JSON from Google Cloud Console
# Then set the environment variable (PowerShell):
$env:GOOGLE_APPLICATION_CREDENTIALS="C:\path\to\service-account.json"

# Anthropic
ANTHROPIC_API_KEY=sk-ant-your-key-here

# Supabase
SUPABASE_URL=https://xxxxxxxxxxxxx.supabase.co
SUPABASE_KEY=your-anon-key
SUPABASE_SERVICE_KEY=your-service-role-key

# Razorpay (optional for Phase 1)
RAZORPAY_KEY_ID=rzp_test_xxxxx
RAZORPAY_KEY_SECRET=your_secret
```

### Step 5: Set Up Database

If using **Supabase** (recommended):
1. Create a new project at https://supabase.com
2. Get your connection string from Settings > Database
3. The tables will be auto-created when you run the backend

If using **local PostgreSQL**:
```powershell
# Create database
psql -U postgres
CREATE DATABASE trulyinvoice;
\q
```

### Step 6: Run the Backend

```powershell
uvicorn app.main:app --reload
```

The API will be available at: http://localhost:8000

Test it: Open http://localhost:8000/docs for interactive API documentation

---

## Part 2: Frontend Setup

### Step 1: Open New Terminal and Navigate to Frontend

```powershell
cd frontend
```

### Step 2: Install Dependencies

```powershell
npm install
```

### Step 3: Configure Environment

```powershell
copy .env.example .env.local
```

Edit `.env.local`:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_APP_NAME=TrulyInvoice
NEXT_PUBLIC_RAZORPAY_KEY=rzp_test_xxxxx
```

### Step 4: Run the Frontend

```powershell
npm run dev
```

The app will be available at: http://localhost:3000

---

## Part 3: Testing the Complete Flow

### 1. Register a User

Go to http://localhost:3000 and click "Start Free Trial" or use the API:

```bash
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "password123",
    "full_name": "Test User"
  }'
```

### 2. Login

```bash
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "password123"
  }'
```

Save the `access_token` from the response.

### 3. Upload an Invoice

```bash
curl -X POST http://localhost:8000/api/documents/upload \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -F "file=@/path/to/invoice.pdf"
```

### 4. Check Usage Limits

```bash
curl http://localhost:8000/api/subscriptions/usage \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

---

## Part 4: Database Schema

The following tables will be auto-created:

- `users` - User accounts
- `subscriptions` - Subscription plans and usage
- `documents` - Uploaded files metadata
- `invoices` - Extracted invoice data
- `categories` - Expense categories
- `usage_logs` - API usage tracking

---

## Part 5: Project Structure Overview

```
trulyinvoice.xyz/
├── backend/
│   ├── app/
│   │   ├── api/              # API endpoints
│   │   │   ├── auth.py       # Authentication
│   │   │   ├── documents.py  # Document upload
│   │   │   ├── invoices.py   # Invoice CRUD
│   │   │   ├── categories.py # Categories
│   │   │   └── subscriptions.py
│   │   ├── core/             # Core configuration
│   │   │   ├── config.py     # Settings
│   │   │   ├── database.py   # DB connection
│   │   │   └── security.py   # Auth helpers
│   │   ├── models/           # Data models
│   │   │   ├── models.py     # SQLAlchemy models
│   │   │   └── schemas.py    # Pydantic schemas
│   │   ├── services/         # Business logic
│   │   │   ├── ai_service.py # AI extraction
│   │   │   └── subscription_service.py
│   │   └── main.py          # FastAPI app
│   └── requirements.txt
│
└── frontend/
    ├── src/
    │   ├── app/             # Next.js pages
    │   │   ├── layout.tsx
    │   │   └── page.tsx     # Landing page
    │   ├── components/      # React components (to add)
    │   └── lib/             # Utilities (to add)
    └── package.json
```

---

## Part 6: Common Issues & Solutions

### Issue: Google Cloud Vision Error

**Solution**: Ensure `GOOGLE_APPLICATION_CREDENTIALS` is set:

```powershell
$env:GOOGLE_APPLICATION_CREDENTIALS="C:\path\to\your\service-account.json"
```

### Issue: Database Connection Error

**Solution**: Check your `DATABASE_URL` is correct and PostgreSQL is running.

### Issue: Module Not Found

**Solution**: Ensure virtual environment is activated and all dependencies are installed:

```powershell
.\venv\Scripts\activate
pip install -r requirements.txt
```

### Issue: Port Already in Use

**Solution**: Change the port or kill the process:

```powershell
# Backend
uvicorn app.main:app --reload --port 8001

# Frontend
npm run dev -- -p 3001
```

---

## Part 7: Next Steps

### Phase 1 (Current - MVP):
- ✅ Document upload
- ✅ AI extraction with fallback
- ✅ Dashboard structure
- 🔲 Build frontend dashboard
- 🔲 Add Excel export functionality
- 🔲 User testing

### Phase 2 (Monetization):
- 🔲 Razorpay integration
- 🔲 Google Sheets sync
- 🔲 Payment webhook handling

### Phase 3 (Business Features):
- 🔲 Multi-user accounts
- 🔲 Tally export
- 🔲 QuickBooks export

---

## Part 8: Deployment

### Backend Deployment (Railway/Render)

1. Create account on Railway.app or Render.com
2. Connect your Git repository
3. Set environment variables
4. Deploy

### Frontend Deployment (Vercel)

1. Install Vercel CLI: `npm i -g vercel`
2. Run: `vercel deploy`
3. Set environment variables in Vercel dashboard

---

## Support & Resources

- **FastAPI Docs**: https://fastapi.tiangolo.com/
- **Next.js Docs**: https://nextjs.org/docs
- **Anthropic API**: https://docs.anthropic.com/
- **Google Vision**: https://cloud.google.com/vision/docs

---

**Happy Building! 🚀**
