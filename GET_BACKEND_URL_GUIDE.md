# 🎯 GET YOUR BACKEND URL - VISUAL GUIDE

## 🚀 FASTEST METHOD: Railway.app (Recommended)

---

## ⚡ **3 SIMPLE STEPS** (10 minutes total)

### Step 1️⃣: Sign Up & Deploy (5 min)

```
1. Visit: https://railway.app
2. Click "Login with GitHub"
3. Click "New Project"
4. Select "Deploy from GitHub repo"
5. Choose: gamearcade199-prog/trulyinvoice.xyz
6. Wait for automatic deployment
```

✅ **Railway will auto-detect Python and deploy!**

---

### Step 2️⃣: Add Environment Variables (3 min)

Click **"Variables"** tab and add these:

| Variable Name | Value |
|--------------|--------|
| `SUPABASE_URL` | `https://ldvwxqluaheuhbycdpwn.supabase.co` |
| `SUPABASE_KEY` | `eyJhbGciOiJI...` (your anon key) |
| `SUPABASE_SERVICE_KEY` | `eyJhbGciOiJI...` (your service key) |
| `OPENAI_API_KEY` | `sk-proj-QV11...` (your OpenAI key) |
| `GOOGLE_CLOUD_VISION_API_KEY` | `AIzaSyBQ...` (your Vision key) |
| `STORAGE_TYPE` | `supabase` |
| `ENVIRONMENT` | `production` |

📋 Copy from your `.env` file!

---

### Step 3️⃣: Get Your URL (2 min)

```
1. In Railway dashboard, click "Settings"
2. Scroll to "Domains" section
3. Click "Generate Domain"
4. Copy your URL (looks like):
   https://trulyinvoice-backend-production.up.railway.app
```

🎉 **That's your backend URL!**

---

## 🎯 What to Do With Your URL

### ✅ Add to Vercel:

1. Go to **Vercel Dashboard**
2. Open your project → **Settings** → **Environment Variables**
3. Add:
   ```
   NEXT_PUBLIC_API_URL
   https://your-railway-url.up.railway.app
   ```
4. **Redeploy** your frontend

### ✅ Test Your Backend:

Visit these URLs in browser:

```
✅ Docs: https://your-railway-url.up.railway.app/docs
✅ Health: https://your-railway-url.up.railway.app/health
✅ API: https://your-railway-url.up.railway.app/api/invoices
```

If you see responses → Backend is working! 🎉

---

## 🆓 Cost Comparison

| Platform | Free Tier | Speed | Best For |
|----------|-----------|-------|----------|
| **Railway** ⭐ | $5/month credit | Fast, no sleep | Small projects |
| **Render** | Unlimited | Slow (sleeps) | Testing only |
| **Vercel** | Backend ❌ | N/A | Frontend only |
| **Heroku** | None ❌ | N/A | Paid only now |

**Winner: Railway** 🏆

---

## 📱 Railway Dashboard Tour

```
┌─────────────────────────────────────────┐
│  Railway Dashboard                       │
├─────────────────────────────────────────┤
│                                          │
│  [trulyinvoice-backend]  ✅ Active      │
│                                          │
│  Tabs:                                   │
│  ├─ Overview  ← See deployment status   │
│  ├─ Variables ← Add your API keys       │
│  ├─ Settings  ← Generate domain here    │
│  └─ Logs      ← Check for errors        │
│                                          │
└─────────────────────────────────────────┘
```

---

## ✅ Verification Checklist

After deployment, check:

- [ ] Railway deployment shows "Active" ✅
- [ ] `/docs` endpoint loads (Swagger UI)
- [ ] `/health` returns `{"status": "healthy"}`
- [ ] No errors in Railway logs
- [ ] URL added to Vercel as `NEXT_PUBLIC_API_URL`
- [ ] Frontend redeployed on Vercel
- [ ] Upload works on your site!

---

## 🆘 Troubleshooting

### ❌ "Build failed"
- Check if `requirements.txt` exists in `/backend` folder
- Look at Railway logs for specific error
- Make sure `railway.toml` file exists in project root

### ❌ "Application error"
- Check environment variables are added
- Make sure all 7 variables are present
- Redeploy after adding variables

### ❌ "Cannot generate domain"
- Make sure service is deployed first (green checkmark)
- Try refreshing the page
- Contact Railway support on Discord

---

## 💡 Pro Tips

1. **Auto-Deploy:** Every time you push to GitHub, Railway auto-deploys! 🚀

2. **View Logs:** Click "Deployments" → Click latest → See real-time logs

3. **Free Usage:** Monitor your usage in Railway dashboard to stay within free tier

4. **Custom Domain:** After testing, you can add custom domain like `api.trulyinvoice.xyz`

---

## 🎯 Your Final Architecture

```
┌─────────────┐
│   Browser   │
└──────┬──────┘
       │
       ↓
┌─────────────┐
│   Vercel    │  ← Frontend (trulyinvoice.xyz)
│  (Frontend) │
└──────┬──────┘
       │ calls NEXT_PUBLIC_API_URL
       ↓
┌─────────────┐
│   Railway   │  ← Backend API (your-backend.railway.app)
│  (Backend)  │
└──────┬──────┘
       │
       ↓
┌─────────────┐
│  Supabase   │  ← Database & Storage
└──────┬──────┘
       │
       ↓
┌─────────────┐
│  OpenAI API │  ← AI Processing
└─────────────┘
```

---

## 📞 Need More Help?

**Railway:**
- Website: https://railway.app
- Docs: https://docs.railway.app
- Discord: https://discord.gg/railway

**Your Project:**
- I've already created `railway.toml` for you ✅
- I've updated CORS settings in backend ✅
- Everything is ready to deploy! ✅

---

## ⚡ TL;DR

1. **Go to Railway.app** → Login with GitHub
2. **Deploy your repo** → Auto-detects everything
3. **Add 7 environment variables** → Copy from .env
4. **Generate domain** → Get your URL
5. **Add to Vercel** → `NEXT_PUBLIC_API_URL`
6. **Redeploy** → Done! 🎉

**Time:** 10 minutes
**Cost:** Free ($5 credit/month)
**Result:** Working upload system! ✅
