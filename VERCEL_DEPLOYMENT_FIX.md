# 🚀 VERCEL DEPLOYMENT - QUICK FIX

## ❌ Current Error:
```
Environment Variable "NEXT_PUBLIC_SUPABASE_URL" references Secret "supabase-url", which does not exist.
```

## ✅ Solution: Add Environment Variables to Vercel

### Step 1: Go to Your Vercel Project
1. Open: https://vercel.com/trulyinvoices-projects/trulyinvoice-xyz
2. Click **Settings** (top navigation)
3. Click **Environment Variables** (left sidebar)

### Step 2: Add Variables (Use Bulk Edit - FASTER!)
1. Click **"Add New"** button
2. Click **"Switch to bulk edit"** (top right)
3. **Paste these 2 lines:**

```
NEXT_PUBLIC_SUPABASE_URL=https://ldvwxqluaheuhbycdpwn.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imxkdnd4cWx1YWhldWhieWNkcHduIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjAwNzY2NTYsImV4cCI6MjA3NTY1MjY1Nn0.uPBCzeJ3tH1SD0QObL850zcrKDDLr9TA6KCUzBp9e1A
```

4. Click **"Add"** button

### Step 3: Redeploy
1. Go to **Deployments** tab (top navigation)
2. Find the **FAILED** deployment
3. Click the **⋯** (three dots) menu
4. Click **"Redeploy"**
5. Wait 2-3 minutes ⏳

### Step 4: Check Your Live Site
Your app will be live at: **https://trulyinvoice-xyz.vercel.app** 🎉

---

## 📝 Important Notes:

- ✅ Only these 2 variables are needed for frontend
- ❌ DO NOT add backend keys (OPENAI_API_KEY, GOOGLE_CLOUD_VISION_API_KEY, SUPABASE_SERVICE_KEY)
- 🔐 Backend keys stay in your local `.env` file only
- 🌐 `NEXT_PUBLIC_` prefix makes variables accessible in browser (safe for public keys only)

---

## 🆘 If You Still See Errors:

1. Make sure you clicked **"Add"** after pasting
2. Check that both variables appear in the list
3. Try **hard refresh** on deployment page (Ctrl + F5)
4. Redeploy again from scratch

---

**Done! Your invoice scanner will be live! 🚀**
