# 🔐 VERCEL ENVIRONMENT VARIABLES - COMPLETE GUIDE

## 📋 What You Need to Add to Vercel

Go to: **Vercel Dashboard → Your Project → Settings → Environment Variables**

---

## ✅ REQUIRED (Must Add):

### 1. **Supabase Configuration**
```
NEXT_PUBLIC_SUPABASE_URL
Value: https://ldvwxqluaheuhbycdpwn.supabase.co
```

```
NEXT_PUBLIC_SUPABASE_ANON_KEY
Value: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imxkdnd4cWx1YWhldWhieWNkcHduIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjAwNzY2NTYsImV4cCI6MjA3NTY1MjY1Nn0.uPBCzeJ3tH1SD0QObL850zcrKDDLr9TA6KCUzBp9e1A
```

### 2. **Backend API URL** ⚠️ CRITICAL FOR UPLOADS
```
NEXT_PUBLIC_API_URL
Value: https://your-backend.railway.app
```
**⚠️ IMPORTANT:** Replace with your actual Railway/Render URL after deployment!
- **Before backend deployment:** Leave it as `http://localhost:8000` (won't work in prod)
- **After backend deployment:** Update to your Railway URL

---

## 🎯 OPTIONAL (But Recommended):

### 3. **App Name**
```
NEXT_PUBLIC_APP_NAME
Value: TrulyInvoice
```

### 4. **Razorpay** (If you enable payments)
```
NEXT_PUBLIC_RAZORPAY_KEY
Value: rzp_test_xxxxx
```
(Update with real key when ready for payments)

---

## 🚫 DO NOT ADD TO VERCEL:

These are backend-only (add to Railway/Render instead):
- ❌ `SUPABASE_SERVICE_KEY` (security risk!)
- ❌ `OPENAI_API_KEY` (backend only)
- ❌ `GOOGLE_CLOUD_VISION_API_KEY` (backend only)
- ❌ `RAZORPAY_KEY_SECRET` (security risk!)
- ❌ `SECRET_KEY` (backend only)

**Why?** These secrets would be exposed to the browser! Only `NEXT_PUBLIC_*` vars go to Vercel.

---

## 📝 Step-by-Step Instructions:

### Step 1: Go to Vercel
1. Visit: https://vercel.com/dashboard
2. Click on your `trulyinvoice` project
3. Click **Settings** (top menu)
4. Click **Environment Variables** (left sidebar)

### Step 2: Add Variables
For each variable:
1. Click **"Add New"**
2. **Key**: Enter the name (e.g., `NEXT_PUBLIC_SUPABASE_URL`)
3. **Value**: Paste the value
4. **Environment**: Select **Production**, **Preview**, and **Development** (all 3)
5. Click **"Save"**

### Step 3: Redeploy
After adding all variables:
1. Go to **Deployments** tab
2. Click **•••** (three dots) on latest deployment
3. Click **"Redeploy"**
4. Check **"Use existing Build Cache"** is OFF
5. Click **"Redeploy"**

---

## 🎬 Current Status Check:

### Already in Vercel? ✅
If you've deployed before, you might already have:
- ✅ `NEXT_PUBLIC_SUPABASE_URL`
- ✅ `NEXT_PUBLIC_SUPABASE_ANON_KEY`

### Missing (Need to Add): ⚠️
- ⚠️ `NEXT_PUBLIC_API_URL` - **THIS IS CRITICAL!**

---

## 🔍 How to Verify:

### Check in Vercel Dashboard:
1. Settings → Environment Variables
2. You should see:
   - `NEXT_PUBLIC_SUPABASE_URL` ✅
   - `NEXT_PUBLIC_SUPABASE_ANON_KEY` ✅
   - `NEXT_PUBLIC_API_URL` ✅

### Test After Deployment:
1. Open browser console on your site
2. Type: `console.log(process.env.NEXT_PUBLIC_API_URL)`
3. Should show your backend URL (not localhost!)

---

## 🚨 COMMON MISTAKES:

### ❌ Mistake 1: Forgot `NEXT_PUBLIC_` prefix
```
API_URL=https://backend.railway.app  ❌ WRONG
NEXT_PUBLIC_API_URL=https://backend.railway.app  ✅ CORRECT
```
**Why?** Next.js only exposes vars with `NEXT_PUBLIC_` prefix to the browser.

### ❌ Mistake 2: Added backend secrets to Vercel
```
OPENAI_API_KEY=sk-proj-xxxxx  ❌ SECURITY RISK!
```
**Why?** This would expose your API key in the browser source code!

### ❌ Mistake 3: Didn't redeploy after adding vars
**Fix:** Always redeploy after adding environment variables!

---

## 🎯 Priority Order:

### 1️⃣ **Must Add Now** (or uploads won't work):
- `NEXT_PUBLIC_API_URL` (after you deploy backend)

### 2️⃣ **Should Already Exist** (check if present):
- `NEXT_PUBLIC_SUPABASE_URL`
- `NEXT_PUBLIC_SUPABASE_ANON_KEY`

### 3️⃣ **Optional** (add later):
- `NEXT_PUBLIC_RAZORPAY_KEY` (when you enable payments)
- `NEXT_PUBLIC_APP_NAME` (nice to have)

---

## 📊 Full Environment Variables Table:

| Variable | Required? | Where? | Purpose |
|----------|-----------|---------|----------|
| `NEXT_PUBLIC_SUPABASE_URL` | ✅ Yes | Vercel | Database connection |
| `NEXT_PUBLIC_SUPABASE_ANON_KEY` | ✅ Yes | Vercel | Database auth |
| `NEXT_PUBLIC_API_URL` | ✅ Yes | Vercel | Backend API calls |
| `NEXT_PUBLIC_RAZORPAY_KEY` | ❌ No | Vercel | Payment gateway |
| `NEXT_PUBLIC_APP_NAME` | ❌ No | Vercel | App branding |
| `SUPABASE_SERVICE_KEY` | ✅ Yes | Railway | Backend database |
| `OPENAI_API_KEY` | ✅ Yes | Railway | AI processing |
| `GOOGLE_CLOUD_VISION_API_KEY` | ✅ Yes | Railway | OCR processing |

---

## ⚡ Quick Copy-Paste (For Vercel):

### Variable 1:
```
Key: NEXT_PUBLIC_SUPABASE_URL
Value: https://ldvwxqluaheuhbycdpwn.supabase.co
Environments: Production, Preview, Development
```

### Variable 2:
```
Key: NEXT_PUBLIC_SUPABASE_ANON_KEY
Value: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imxkdnd4cWx1YWhldWhieWNkcHduIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjAwNzY2NTYsImV4cCI6MjA3NTY1MjY1Nn0.uPBCzeJ3tH1SD0QObL850zcrKDDLr9TA6KCUzBp9e1A
Environments: Production, Preview, Development
```

### Variable 3 (ADD AFTER BACKEND DEPLOYMENT):
```
Key: NEXT_PUBLIC_API_URL
Value: [YOUR_RAILWAY_URL_HERE]
Environments: Production, Preview, Development
```

---

## 🔄 Workflow:

1. ✅ Add Supabase vars to Vercel (if not already there)
2. 🚀 Deploy backend to Railway
3. 📋 Copy Railway URL
4. ✅ Add `NEXT_PUBLIC_API_URL` to Vercel with Railway URL
5. 🔄 Redeploy frontend
6. 🎉 Uploads work!

---

## 🆘 Troubleshooting:

### "Environment variable not found"
- Did you add `NEXT_PUBLIC_` prefix?
- Did you redeploy after adding?
- Wait 1-2 minutes for deployment to complete

### "Upload still fails"
- Check if `NEXT_PUBLIC_API_URL` is correct
- Test backend health: `https://your-backend.railway.app/health`
- Check browser console for actual URL being called

### "Backend returns 404"
- Backend might not be deployed yet
- Check Railway deployment status
- Verify backend is running

---

## ✅ Final Checklist:

- [ ] Supabase URL added to Vercel
- [ ] Supabase Anon Key added to Vercel
- [ ] Backend deployed to Railway
- [ ] Backend URL added to Vercel as `NEXT_PUBLIC_API_URL`
- [ ] Redeployed frontend on Vercel
- [ ] Tested upload functionality
- [ ] No localhost URLs in production

---

**Need Help?** 
Check Vercel logs: Dashboard → Deployments → Click deployment → View Function Logs
