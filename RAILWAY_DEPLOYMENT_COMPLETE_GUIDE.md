# 🚂 DEPLOY BACKEND TO RAILWAY - STEP BY STEP

## 🎯 Get Your Backend URL in 10 Minutes!

---

## ⚡ QUICK START

### Step 1: Sign Up for Railway
1. Go to: **https://railway.app**
2. Click **"Login"** (top right)
3. Click **"Login with GitHub"**
4. Authorize Railway to access your repos
5. ✅ You're in!

---

### Step 2: Create New Project

1. Click **"New Project"** (purple button)
2. Select **"Deploy from GitHub repo"**
3. Find and select: **`gamearcade199-prog/trulyinvoice.xyz`**
4. Railway will ask which directory to deploy from

⚠️ **IMPORTANT:** You need to tell Railway to deploy from the `/backend` folder!

---

### Step 3: Configure Root Directory

**Option A: Use railway.toml (Recommended)**

Create this file in your project root:

`railway.toml`:
```toml
[build]
builder = "nixpacks"

[deploy]
startCommand = "cd backend && pip install -r requirements.txt && uvicorn main:app --host 0.0.0.0 --port $PORT"
```

**Option B: Manual Configuration**

1. After selecting repo, click **"Settings"** (left sidebar)
2. Find **"Root Directory"**
3. Change from `/` to `/backend`
4. Click **"Update"**

---

### Step 4: Add Environment Variables

1. In Railway dashboard, click **"Variables"** tab (left sidebar)
2. Click **"+ New Variable"**
3. Add these **one by one**:

```bash
SUPABASE_URL
https://ldvwxqluaheuhbycdpwn.supabase.co

SUPABASE_KEY
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imxkdnd4cWx1YWhldWhieWNkcHduIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjAwNzY2NTYsImV4cCI6MjA3NTY1MjY1Nn0.uPBCzeJ3tH1SD0QObL850zcrKDDLr9TA6KCUzBp9e1A

SUPABASE_SERVICE_KEY
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imxkdnd4cWx1YWhldWhieWNkcHduIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2MDA3NjY1NiwiZXhwIjoyMDc1NjUyNjU2fQ.939ySYuwA9ByCprCiI9GL5xEmvkhONYEWdtuHVLweWM

OPENAI_API_KEY
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

GOOGLE_CLOUD_VISION_API_KEY
AIzaSyBQP5BaQeLE07wJj5WgneYJJA_QKAwiUh0

STORAGE_TYPE
supabase

ENVIRONMENT
production

PORT
$PORT
```

**Note:** Railway automatically provides `$PORT` variable, just type it as is.

---

### Step 5: Deploy!

1. Railway will **auto-deploy** after you add variables
2. Watch the deployment logs (bottom of screen)
3. Wait 2-5 minutes for build to complete
4. Look for: ✅ **"Build successful"**

---

### Step 6: Get Your Backend URL 🎉

1. In Railway dashboard, look at the top section
2. You'll see your service/deployment
3. Click **"Settings"** tab
4. Scroll down to **"Domains"** section
5. Click **"Generate Domain"**
6. Railway will create a URL like:
   ```
   https://trulyinvoice-backend-production.up.railway.app
   ```
7. **Copy this URL!** This is your `NEXT_PUBLIC_API_URL`

---

### Step 7: Test Your Backend

Open your browser and go to:
```
https://your-railway-url.up.railway.app/docs
```

You should see the **FastAPI Swagger documentation** page! ✅

Also test the health endpoint:
```
https://your-railway-url.up.railway.app/health
```

Should return:
```json
{"status": "healthy", "timestamp": "..."}
```

---

### Step 8: Update Vercel

Now that you have your backend URL:

1. Go to **Vercel Dashboard**
2. Open your project
3. **Settings** → **Environment Variables**
4. Add new variable:
   - **Key:** `NEXT_PUBLIC_API_URL`
   - **Value:** `https://your-railway-url.up.railway.app`
   - **Environments:** Select all (Production, Preview, Development)
5. Click **"Save"**
6. Go to **"Deployments"** tab
7. Click **"Redeploy"** on latest deployment

---

## 🔧 Troubleshooting Railway Deployment

### ❌ Build Failed: "requirements.txt not found"

**Solution:** Make sure Railway is looking at the `/backend` folder:

1. Settings → Root Directory → Change to `backend`
2. Or create `railway.toml` file (see Step 3)

### ❌ Build Failed: "Python version error"

**Solution:** Create `runtime.txt` in `/backend` folder:

```
python-3.11
```

### ❌ Application crashed after deploy

**Solution:** Check if `main.py` has the correct app name:

```python
app = FastAPI()

# At the end of file, this should NOT be there for Railway:
# if __name__ == "__main__":
#     uvicorn.run(app, host="0.0.0.0", port=8000)
```

Railway runs uvicorn separately, so remove the `if __name__` block.

### ❌ Environment variables not working

**Solution:** 
1. Double-check variable names (no typos)
2. Make sure you clicked "Add" after each one
3. Redeploy after adding variables

---

## 💰 Railway Free Tier Limits

- **$5 credit per month** (resets monthly)
- **500 execution hours free** 
- After free credit: **$0.000463 per GB-hour**
- Estimate: ~200-300 invoice processes per month free
- No sleep/cold starts!

**Comparison:**
- **Railway Free:** $5 credit, no sleep, fast
- **Render Free:** Unlimited but sleeps after 15 min (slow!)
- **Heroku:** No longer has free tier ❌

---

## 🎯 Alternative: Render.com (If Railway doesn't work)

### Quick Render Setup:

1. Go to: **https://render.com**
2. Sign in with GitHub
3. **New** → **Web Service**
4. Select repo: `trulyinvoice.xyz`
5. Configure:
   - **Name:** `trulyinvoice-backend`
   - **Root Directory:** `backend`
   - **Runtime:** `Python 3`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn main:app --host 0.0.0.0 --port $PORT`
6. Add same environment variables
7. Click **"Create Web Service"**
8. Get URL: `https://trulyinvoice-backend.onrender.com`

⚠️ **Render Free Tier:** App sleeps after 15 min of inactivity (first request will be slow!)

---

## 📋 Quick Checklist

- [ ] Sign up for Railway with GitHub
- [ ] Create new project from your repo
- [ ] Set root directory to `/backend`
- [ ] Add all environment variables
- [ ] Wait for deployment to complete
- [ ] Generate domain in Railway
- [ ] Copy backend URL
- [ ] Test `/docs` endpoint
- [ ] Add `NEXT_PUBLIC_API_URL` to Vercel
- [ ] Redeploy frontend on Vercel
- [ ] Test upload on your site
- [ ] 🎉 Done!

---

## 🚀 After Deployment

Your architecture will be:

```
User Browser
    ↓
Vercel (Frontend) - trulyinvoice.xyz
    ↓
Railway (Backend) - your-backend.railway.app
    ↓
Supabase (Database) - ldvwxqluaheuhbycdpwn.supabase.co
    ↓
OpenAI API (AI Processing)
```

All connected! ✅

---

## 📞 Need Help?

**Railway Support:**
- Docs: https://docs.railway.app
- Discord: https://discord.gg/railway

**Check Logs:**
- Railway Dashboard → Your Service → "Deployments" → Click on deployment → View logs

**Common Issues:**
- Port binding: Railway provides `$PORT`, make sure your app uses it
- Build errors: Check if `requirements.txt` has all dependencies
- Runtime errors: Check environment variables are set correctly

---

## ⚡ TL;DR

1. **Railway.app** → Login with GitHub
2. New Project → Select your repo → Set root to `/backend`
3. Add environment variables
4. Generate domain → Copy URL
5. Add URL to Vercel as `NEXT_PUBLIC_API_URL`
6. Redeploy both
7. **Done!** 🎉
