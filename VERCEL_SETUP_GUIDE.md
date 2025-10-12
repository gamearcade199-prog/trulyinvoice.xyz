# 🔐 VERCEL DEPLOYMENT - Environment Variables

## ✅ Required Environment Variables for Vercel

Copy and paste these **EXACTLY** into your Vercel Dashboard:

### Step 1: Go to Vercel
1. Go to your project: https://vercel.com/trulyinvoices-projects/trulyinvoice-xyz
2. Click **Settings** tab
3. Click **Environment Variables** in left sidebar
4. Add each variable below

---

## 📋 Environment Variables (Copy these exactly)

### Variable 1:
```
Name: NEXT_PUBLIC_SUPABASE_URL
Value: https://ldvwxqluaheuhbycdpwn.supabase.co
```

### Variable 2:
```
Name: NEXT_PUBLIC_SUPABASE_ANON_KEY
Value: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imxkdnd4cWx1YWhldWhieWNkcHduIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjAwNzY2NTYsImV4cCI6MjA3NTY1MjY1Nn0.uPBCzeJ3tH1SD0QObL850zcrKDDLr9TA6KCUzBp9e1A
```

---

## ⚙️ How to Add in Vercel

### Method 1: One at a time
1. In Vercel → Settings → Environment Variables
2. Click **"Add New"**
3. Enter `NEXT_PUBLIC_SUPABASE_URL` in the **Key** field
4. Paste `https://ldvwxqluaheuhbycdpwn.supabase.co` in the **Value** field
5. Select **All** (Production, Preview, Development)
6. Click **Save**
7. Repeat for `NEXT_PUBLIC_SUPABASE_ANON_KEY`

### Method 2: Bulk Add (Faster!)
1. In Vercel → Settings → Environment Variables
2. Click **"Add New"** 
3. Click **"Switch to bulk edit"**
4. Paste this:
```
NEXT_PUBLIC_SUPABASE_URL=https://ldvwxqluaheuhbycdpwn.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imxkdnd4cWx1YWhldWhieWNkcHduIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjAwNzY2NTYsImV4cCI6MjA3NTY1MjY1Nn0.uPBCzeJ3tH1SD0QObL850zcrKDDLr9TA6KCUzBp9e1A
```
5. Click **Add**

---

## 🚀 After Adding Variables

1. Go to **Deployments** tab
2. Find your failed deployment
3. Click the **3 dots menu (⋯)**
4. Click **"Redeploy"**
5. Wait 2-3 minutes
6. Your app will be LIVE! 🎉

---

## 📝 Notes

- ✅ These are **PUBLIC** keys (ANON key is safe to expose)
- ✅ They're already in your code, just need to be in Vercel too
- ✅ No backend API keys needed for frontend deployment
- ✅ OpenAI/Google Vision keys are for backend only (not needed now)

---

## 🔗 Quick Links

- **Vercel Project:** https://vercel.com/trulyinvoices-projects/trulyinvoice-xyz
- **Supabase Dashboard:** https://app.supabase.com/project/ldvwxqluaheuhbycdpwn
- **Your App (after deploy):** https://trulyinvoice-xyz.vercel.app

---

## ⚠️ Removed Unnecessary Variables

I removed these from the Vercel config (not needed for frontend):
- ❌ DATABASE_URL (backend only)
- ❌ SECRET_KEY (backend only)
- ❌ OPENAI_API_KEY (backend only - when you deploy backend later)
- ❌ GOOGLE_CLOUD_VISION_API_KEY (backend only)
- ❌ SUPABASE_SERVICE_KEY (backend only - never expose in frontend!)
- ❌ AWS keys (not using AWS)
- ❌ Redis URL (not needed yet)
- ❌ Razorpay keys (payment not implemented yet)

**Only the 2 Supabase public keys are needed for your Next.js frontend!**

---

**Copy the values above and paste them into Vercel, then redeploy! 🚀**
