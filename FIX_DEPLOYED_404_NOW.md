# 🚨 CRITICAL - Fix 404 Error on Deployed Site

## THE ACTUAL PROBLEM

Your `frontend/.env.local` has:
```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

This works **locally** (your laptop) but fails on **deployed site** (trulyinvoice.xyz on Vercel) because:
- Vercel cannot reach `http://localhost:8000` on your machine
- It tries to connect to localhost, gets 404
- Frontend falls back to Supabase client which has RLS issues

## THE FIX - Set Backend URL in Vercel

You need to tell Vercel where your deployed backend is:

### Step 1: Find Your Backend URL

Go to: https://dashboard.render.com

Look for your service name (trulyinvoice-backend or similar):
- Click on it
- Copy the URL shown (looks like: `https://trulyinvoice-backend-xxxxx.onrender.com`)

### Step 2: Set Environment Variable in Vercel

1. Go to: https://vercel.com/dashboard
2. Click on your project: **trulyinvoice**
3. Click **Settings** → **Environment Variables**
4. Click **Add New**
5. Fill in:
   - **Name**: `NEXT_PUBLIC_API_URL`
   - **Value**: `https://trulyinvoice-backend-xxxxx.onrender.com` (your Render URL)
   - **Environment**: Select "Production"
6. Click **Save**
7. Click **Redeploy** on the main dashboard to apply changes

### Step 3: Update Your Local .env.local (for local testing)

Keep your local setup working:
```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

(This stays the same - only Vercel environment variable changes)

---

## After Setting Environment Variable

Vercel will redeploy automatically. Then:

1. Click eye icon on https://trulyinvoice.xyz/invoices
2. Should now load invoice details ✅
3. No more 404 error ✅

---

## Quick Reference: What Was Wrong

| Where | API_URL | Works? |
|-------|---------|--------|
| Local laptop | http://localhost:8000 | ✅ YES |
| Vercel (deployed) | http://localhost:8000 | ❌ NO (can't reach your laptop!) |
| Vercel (deployed) | https://yourrender.onrender.com | ✅ YES |

---

## Still Getting 404 After This?

1. Hard refresh: Ctrl+Shift+R (clears cache)
2. Check Vercel deployment status at vercel.com
3. Check Render logs at render.com for any API errors
4. Check browser console (F12) for exact error message
