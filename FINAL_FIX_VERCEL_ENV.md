# ✅ FINAL FIX - Set Backend URL in Vercel

## The Real Problem

The 404 error happens because Vercel doesn't know where your backend is. The page builds with `process.env.NEXT_PUBLIC_API_URL = undefined`, so it tries to fetch from an invalid URL.

## Solution - 2 Minutes to Fix

### Step 1: Go to Vercel Dashboard

1. Open: https://vercel.com/dashboard
2. Click on your project: **trulyinvoice**
3. Click on **Settings** (top navigation)
4. Click on **Environment Variables** (left sidebar)

### Step 2: Add Environment Variable

Click **Add New** and fill in:

| Field | Value |
|-------|-------|
| **Name** | `NEXT_PUBLIC_API_URL` |
| **Value** | `https://trulyinvoice-backend.onrender.com` |
| **Environment** | Select all three: Production, Preview, Development |

Then click **Save**

### Step 3: Redeploy

Back on main dashboard:
1. Find your deployment
2. Click the **...** (three dots) menu
3. Click **Redeploy**

Wait 2-3 minutes for deployment to complete.

### Step 4: Test

1. Go to: https://trulyinvoice.xyz/invoices
2. Click **eye icon** on any invoice
3. Should now load invoice details ✅

---

## Why This Works

**Before (broken)**:
- Frontend builds with `API_URL = undefined`
- Click eye icon → tries `undefined/api/invoices/{id}` → 404 ❌

**After (fixed)**:
- Frontend builds with `API_URL = https://trulyinvoice-backend.onrender.com`
- Click eye icon → tries `https://trulyinvoice-backend.onrender.com/api/invoices/{id}` → 200 ✅

---

## Verification Checklist

After redeploy, check these:

- [ ] Vercel shows "Production" deployment completed
- [ ] Browser console (F12) shows the correct API URL
- [ ] Eye icon click loads invoice details (no 404)
- [ ] Works on multiple invoices

---

## If Still Not Working

1. **Hard refresh**: Ctrl+Shift+R (clears Next.js cache)
2. **Check deployment**: Vercel dashboard → your project → Deployments
3. **Check Vercel logs**: Click on the deployment → Logs
4. **Check Render logs**: render.com dashboard → Backend service → Logs

---

## Important Notes

- ⚠️ DO NOT commit `.env.production` to git (it's in .gitignore)
- ✅ Set environment variables in Vercel dashboard instead
- ✅ Use HTTPS URLs only (http won't work from browser to cloud)
- ✅ The backend URL format: `https://trulyinvoice-backend.onrender.com` (no trailing slash)
