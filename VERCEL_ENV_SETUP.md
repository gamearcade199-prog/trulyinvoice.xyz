# 🚨 CRITICAL: Vercel Environment Variables Setup

## Required for Production Deployment

Add these environment variables to Vercel Dashboard:

### 1. Go to: https://vercel.com/dashboard
### 2. Select your project → Settings → Environment Variables
### 3. Add these exact variables:

```bash
# Backend API Connection (CRITICAL)
NEXT_PUBLIC_API_URL = https://trulyinvoice-backend.onrender.com

# Database Connection
NEXT_PUBLIC_SUPABASE_URL = https://ldvwxqluaheuhbycdpwn.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY = eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imxkdnd4cWx1YWhldWhieWNkcHduIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjAwNzY2NTYsImV4cCI6MjA3NTY1MjY1Nn0.uPBCzeJ3tH1SD0QObL850zcrKDDLr9TA6KCUzBp9e1A

# Payment Gateway (Optional)
NEXT_PUBLIC_RAZORPAY_KEY = rzp_test_xxxxxxxxxxxxxxxx
```

## Environment Settings:
- **Environment:** Production, Preview, Development (select all)

## After Adding:
1. Click "Redeploy" on latest deployment
2. Frontend will connect to production backend
3. API requests will show in Render logs

---
**Created:** October 17, 2025  
**Status:** URGENT - Required for production functionality