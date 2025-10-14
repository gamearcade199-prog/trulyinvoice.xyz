# 🎨 DEPLOY BACKEND TO RENDER - COMPLETE GUIDE

## 🚀 Get Your Backend URL in 10 Minutes!

Render.com is the **best free option** after Railway removed their free tier.

---

## ✅ **Why Render?**

- ✅ **Truly free forever** (no credit card needed)
- ✅ **750 hours/month free** (enough for 24/7 uptime)
- ✅ **Simple web-based deployment** (no CLI)
- ✅ **Auto-deploys from GitHub** (push code → auto update)
- ✅ **Python-optimized** (perfect for FastAPI)
- ✅ **Free SSL certificates** (automatic HTTPS)
- ⚠️ **Only tradeoff:** Sleeps after 15 min inactivity

---

## 📋 **STEP-BY-STEP DEPLOYMENT**

### **Step 1: Sign Up for Render (2 minutes)**

1. Go to: **https://render.com**
2. Click **"Get Started"** or **"Sign Up"**
3. Click **"Sign in with GitHub"**
4. Authorize Render to access your repositories
5. ✅ You're in!

---

### **Step 2: Create New Web Service (1 minute)**

1. From Render Dashboard, click **"New +"** (top right)
2. Select **"Web Service"**
3. You'll see "Create a new Web Service" page

---

### **Step 3: Connect Your Repository (1 minute)**

1. Look for your repo: **`gamearcade199-prog/trulyinvoice.xyz`**
   - If you don't see it, click **"Configure account"** to grant access
2. Click **"Connect"** next to your repository
3. Render will redirect you to configuration page

---

### **Step 4: Configure Web Service (3 minutes)**

Fill in these settings:

#### **Basic Info:**
```
Name: trulyinvoice-backend
Region: Singapore (or closest to you)
Branch: main
Root Directory: backend
```

#### **Build & Deploy:**
```
Runtime: Python 3
Build Command: pip install -r requirements.txt
Start Command: uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

#### **Plan:**
```
Instance Type: Free
```
⚠️ **Important:** Make sure you select **"Free"** plan!

---

### **Step 5: Add Environment Variables (5 minutes)**

Scroll down to **"Environment Variables"** section.

Click **"Add Environment Variable"** for each:

#### **Variable 1:**
```
Key: SUPABASE_URL
Value: https://ldvwxqluaheuhbycdpwn.supabase.co
```

#### **Variable 2:**
```
Key: SUPABASE_KEY
Value: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imxkdnd4cWx1YWhldWhieWNkcHduIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjAwNzY2NTYsImV4cCI6MjA3NTY1MjY1Nn0.uPBCzeJ3tH1SD0QObL850zcrKDDLr9TA6KCUzBp9e1A
```

#### **Variable 3:**
```
Key: SUPABASE_SERVICE_KEY
Value: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imxkdnd4cWx1YWhldWhieWNkcHduIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2MDA3NjY1NiwiZXhwIjoyMDc1NjUyNjU2fQ.939ySYuwA9ByCprCiI9GL5xEmvkhONYEWdtuHVLweWM
```

#### **Variable 4:**
```
Key: OPENAI_API_KEY
Value: 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
```

#### **Variable 5:**
```
Key: GOOGLE_CLOUD_VISION_API_KEY
Value: AIzaSyBQP5BaQeLE07wJj5WgneYJJA_QKAwiUh0
```

#### **Variable 6:**
```
Key: STORAGE_TYPE
Value: supabase
```

#### **Variable 7:**
```
Key: ENVIRONMENT
Value: production
```

#### **Variable 8:**
```
Key: PYTHON_VERSION
Value: 3.11.0
```

---

### **Step 6: Deploy! (5-10 minutes)**

1. Scroll to bottom and click **"Create Web Service"**
2. Render will start building your app
3. Watch the logs in real-time (you'll see):
   ```
   ==> Cloning from GitHub...
   ==> Installing dependencies...
   ==> Starting application...
   ==> Your service is live 🎉
   ```
4. Wait for: **"Your service is live"** message
5. Build takes **5-10 minutes** (be patient!)

---

### **Step 7: Get Your Backend URL 🎉**

Once deployment is complete:

1. You'll see your service dashboard
2. At the top, you'll see your URL:
   ```
   https://trulyinvoice-backend.onrender.com
   ```
3. **Copy this URL!** This is your `NEXT_PUBLIC_API_URL`

---

### **Step 8: Test Your Backend (1 minute)**

Open your browser and visit:

#### **Test 1: API Documentation**
```
https://trulyinvoice-backend.onrender.com/docs
```
✅ You should see FastAPI Swagger UI!

#### **Test 2: Health Check**
```
https://trulyinvoice-backend.onrender.com/health
```
✅ Should return:
```json
{
  "status": "healthy",
  "service": "trulyinvoice-api",
  "timestamp": "..."
}
```

#### **Test 3: Root Endpoint**
```
https://trulyinvoice-backend.onrender.com/
```
✅ Should return:
```json
{
  "message": "TrulyInvoice API v2.0 - Clean Architecture",
  "status": "operational",
  "docs": "/docs"
}
```

If all 3 work → **Backend is deployed successfully!** 🎉

---

## 🔧 **Step 9: Update Vercel (3 minutes)**

Now connect your backend to frontend:

1. Go to **Vercel Dashboard**: https://vercel.com/dashboard
2. Open your **trulyinvoice** project
3. Click **"Settings"** (top menu)
4. Click **"Environment Variables"** (left sidebar)
5. Click **"Add New"**
6. Enter:
   ```
   Key: NEXT_PUBLIC_API_URL
   Value: https://trulyinvoice-backend.onrender.com
   ```
7. Select: **Production**, **Preview**, and **Development** (all 3)
8. Click **"Save"**

---

## 🔄 **Step 10: Redeploy Frontend**

1. Stay in Vercel Dashboard
2. Click **"Deployments"** tab
3. Find latest deployment
4. Click **"•••"** (three dots menu)
5. Click **"Redeploy"**
6. ⚠️ **Uncheck** "Use existing Build Cache"
7. Click **"Redeploy"**
8. Wait 2-3 minutes for build

---

## 🗄️ **Step 11: Fix Database Permissions (2 minutes)**

1. Go to **Supabase Dashboard**: https://supabase.com/dashboard
2. Open your project
3. Click **"SQL Editor"** (left sidebar)
4. Click **"New Query"**
5. Paste the contents of: `FIX_ANONYMOUS_UPLOAD_RLS.sql`
6. Click **"Run"** (or Ctrl+Enter)
7. ✅ You should see "Success" message

---

## ✅ **Step 12: Test Upload!**

1. Go to your site: **https://trulyinvoice.xyz**
2. Click **"Upload"** or go to upload page
3. Try uploading an invoice (PDF, PNG, or JPG)
4. Watch it process!

**Expected behavior:**
- First upload might take 30-60 seconds (cold start)
- After that, uploads are fast!
- Invoice data extracted and displayed

✅ **If it works → You're DONE!** 🎉

---

## ⚠️ **Understanding Cold Starts**

### **What is a Cold Start?**
After **15 minutes of inactivity**, Render puts your free app to "sleep" to save resources.

### **What Happens:**
- ⏰ First request after sleep: **30-60 seconds** (waking up)
- ⚡ All requests after: **Fast** (2-5 seconds)
- 😴 Sleeps again after 15 min idle

### **Solutions:**

#### **Option 1: Accept It** (Recommended for MVP)
- It's free!
- First upload is slow, rest are fast
- Most users won't notice

#### **Option 2: Keep-Alive Service** (Free)
Use a free service to ping your backend every 10 minutes:

1. **UptimeRobot**: https://uptimerobot.com
   - Free monitoring
   - Pings your URL every 5 minutes
   - Keeps app awake!

2. **Cron-job.org**: https://cron-job.org
   - Free cron jobs
   - Set to hit `/health` every 10 min

#### **Option 3: Upgrade to Paid** ($7/month)
- Render Starter plan
- No cold starts
- Always fast

---

## 🔧 **Troubleshooting**

### ❌ **Build Failed: "requirements.txt not found"**

**Solution:**
- Make sure "Root Directory" is set to `backend`
- Check that `requirements.txt` exists in `/backend` folder

### ❌ **Build Failed: "Python version error"**

**Solution:**
- I already created `backend/runtime.txt` with Python 3.11 ✅
- If still fails, try changing to `3.10.0` in runtime.txt

### ❌ **"Application Error" After Deploy**

**Solution:**
1. Check all 8 environment variables are set
2. Click "Manual Deploy" → "Clear build cache & deploy"
3. Check logs for specific error

### ❌ **Upload Still Not Working**

**Checklist:**
- [ ] Backend URL is accessible (test `/docs`)
- [ ] `NEXT_PUBLIC_API_URL` added to Vercel
- [ ] Frontend redeployed after adding variable
- [ ] SQL script run in Supabase
- [ ] Check browser console for errors

### ❌ **CORS Error**

**Solution:**
- I already updated CORS settings in `backend/app/main.py` ✅
- Should include your domain already
- If not working, check the logs

---

## 📊 **Monitoring Your App**

### **Check Deployment Status:**
1. Render Dashboard → Your Service
2. See: "Live" (green) or "Deploy failed" (red)

### **View Logs:**
1. Click "Logs" tab (left sidebar)
2. See real-time application logs
3. Look for errors here

### **Check Usage:**
1. Click "Metrics" tab
2. See CPU, Memory, Bandwidth usage
3. Monitor to stay within free tier

---

## 💰 **Free Tier Limits**

Render Free Tier includes:
- ✅ **750 hours/month** (enough for 24/7!)
- ✅ **100 GB bandwidth/month**
- ✅ **512 MB RAM**
- ✅ **0.1 CPU**
- ⚠️ **Sleeps after 15 min inactivity**

**Perfect for:**
- MVPs and demos
- Low-traffic apps
- Testing and development
- Your invoice processing app!

---

## 🎯 **What You've Accomplished:**

```
✅ Backend deployed to Render
✅ Backend URL obtained
✅ Vercel updated with backend URL
✅ Database permissions fixed
✅ CORS configured
✅ Uploads working for all users!
```

---

## 🚀 **Your Final Architecture:**

```
┌─────────────────┐
│   User Browser  │
└────────┬────────┘
         │
         ↓
┌─────────────────┐
│  Vercel (Frontend)  │  ← trulyinvoice.xyz
└────────┬────────┘
         │ calls NEXT_PUBLIC_API_URL
         ↓
┌─────────────────┐
│  Render (Backend)   │  ← trulyinvoice-backend.onrender.com
└────────┬────────┘
         │
         ↓
┌─────────────────┐
│  Supabase (DB)     │  ← Database + Storage
└────────┬────────┘
         │
         ↓
┌─────────────────┐
│  OpenAI API        │  ← AI Processing
└─────────────────┘
```

---

## 📚 **Files Created For You:**

1. ✅ `render.yaml` - Render configuration (optional)
2. ✅ `backend/runtime.txt` - Python version specification
3. ✅ Updated `backend/app/main.py` - CORS settings
4. ✅ `FIX_ANONYMOUS_UPLOAD_RLS.sql` - Database permissions

Everything is ready! Just follow the steps above! 🎉

---

## 📞 **Need Help?**

**Render Support:**
- Docs: https://render.com/docs
- Community: https://community.render.com
- Status: https://status.render.com

**Check Deployment Logs:**
- Render Dashboard → Your Service → "Logs" tab
- See real-time errors and warnings

---

## ⏱️ **Total Time Estimate:**

- Step 1-3: Sign up & connect (3 min)
- Step 4: Configure (3 min)
- Step 5: Environment variables (5 min)
- Step 6: Deploy & build (5-10 min)
- Step 7-12: Test & connect (5 min)

**Total: 20-25 minutes** to fully working system!

---

## 🎉 **You're Ready to Deploy!**

Everything is configured and ready. Just follow the steps above and you'll have your backend live in 20 minutes!

**Let's go!** 🚀
