# ✅ VERCEL ENVIRONMENT VARIABLES - QUICK CHECKLIST

## 🎯 ADD THESE TO VERCEL:

### ✅ REQUIRED VARIABLES (3 total):

#### 1. Supabase URL
```
NEXT_PUBLIC_SUPABASE_URL=https://ldvwxqluaheuhbycdpwn.supabase.co
```
**Status:** Probably already added ✅

#### 2. Supabase Anon Key
```
NEXT_PUBLIC_SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imxkdnd4cWx1YWhldWhieWNkcHduIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjAwNzY2NTYsImV4cCI6MjA3NTY1MjY1Nn0.uPBCzeJ3tH1SD0QObL850zcrKDDLr9TA6KCUzBp9e1A
```
**Status:** Probably already added ✅

#### 3. Backend API URL ⚠️ **CRITICAL - THIS IS MISSING!**
```
NEXT_PUBLIC_API_URL=https://your-backend.railway.app
```
**Status:** ⚠️ **YOU NEED TO ADD THIS!**

---

## 🚫 DO NOT ADD THESE:
(These go to Railway backend, not Vercel frontend)

- ❌ OPENAI_API_KEY
- ❌ GOOGLE_CLOUD_VISION_API_KEY  
- ❌ SUPABASE_SERVICE_KEY
- ❌ RAZORPAY_KEY_SECRET

**Why?** They would be exposed in browser = security risk!

---

## 📋 ACTION STEPS:

### Step 1: Check What's Already There
1. Go to: https://vercel.com/dashboard
2. Open your project
3. Settings → Environment Variables
4. Check if you already have:
   - [ ] `NEXT_PUBLIC_SUPABASE_URL`
   - [ ] `NEXT_PUBLIC_SUPABASE_ANON_KEY`

### Step 2: Add the Missing One
**After you deploy backend to Railway:**
1. Copy your Railway backend URL
2. Add to Vercel:
   - Key: `NEXT_PUBLIC_API_URL`
   - Value: `https://your-backend.railway.app`
   - Select: Production + Preview + Development

### Step 3: Redeploy
1. Go to Deployments tab
2. Redeploy latest deployment
3. Wait for build to complete

---

## ⚡ TL;DR:

**You only need to add 1 new variable:**

```
NEXT_PUBLIC_API_URL = [Your Railway Backend URL]
```

**But only AFTER you deploy the backend first!**

---

## 🔄 Correct Order:

1. ✅ Deploy backend to Railway
2. ✅ Get Railway URL (e.g., `https://trulyinvoice-backend-production.up.railway.app`)
3. ✅ Add `NEXT_PUBLIC_API_URL` to Vercel with that URL
4. ✅ Redeploy Vercel
5. 🎉 Done!

---

**See `VERCEL_ENV_VARIABLES_GUIDE.md` for detailed instructions.**
