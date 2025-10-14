# 🚀 DEPLOY BACKEND TO FIX UPLOAD ISSUES

## 🔴 CURRENT PROBLEM
Your frontend is deployed on Vercel, but your backend is only running locally (`localhost:8000`).
When users try to upload invoices, they get errors because:
1. The backend API is not accessible from the internet
2. `localhost:8000` only works on your computer

## ✅ SOLUTION: Deploy Backend to Cloud

You have **3 options** to deploy your backend:

---

## 🚄 OPTION 1: Railway.app (RECOMMENDED - EASIEST)

### Why Railway?
- ✅ Free tier available
- ✅ Auto-deploys from GitHub
- ✅ Built-in PostgreSQL if needed
- ✅ Easy environment variables
- ✅ Automatic HTTPS

### Steps:

1. **Go to Railway.app**
   ```
   https://railway.app
   ```

2. **Sign in with GitHub**

3. **New Project > Deploy from GitHub repo**
   - Select: `gamearcade199-prog/trulyinvoice.xyz`
   - Root directory: `/backend`

4. **Configure Environment Variables**
   Add these in Railway dashboard:
   ```
   SUPABASE_URL=https://ldvwxqluaheuhbycdpwn.supabase.co
   SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imxkdnd4cWx1YWhldWhieWNkcHduIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjAwNzY2NTYsImV4cCI6MjA3NTY1MjY1Nn0.uPBCzeJ3tH1SD0QObL850zcrKDDLr9TA6KCUzBp9e1A
   SUPABASE_SERVICE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imxkdnd4cWx1YWhldWhieWNkcHduIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2MDA3NjY1NiwiZXhwIjoyMDc1NjUyNjU2fQ.939ySYuwA9ByCprCiI9GL5xEmvkhONYEWdtuHVLweWM
   OPENAI_API_KEY=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
   GOOGLE_CLOUD_VISION_API_KEY=AIzaSyBQP5BaQeLE07wJj5WgneYJJA_QKAwiUh0
   STORAGE_TYPE=supabase
   ENVIRONMENT=production
   ```

5. **Get Your Backend URL**
   - Railway will give you a URL like: `https://trulyinvoice-backend.railway.app`
   - Copy this URL

6. **Update Frontend Environment**
   - Go to Vercel Dashboard
   - Open your `trulyinvoice` project
   - Settings > Environment Variables
   - Add:
     ```
     NEXT_PUBLIC_API_URL=https://trulyinvoice-backend.railway.app
     ```
   - Redeploy frontend

---

## 🎨 OPTION 2: Render.com

### Why Render?
- ✅ Free tier available
- ✅ Simple deployment
- ✅ Automatic HTTPS
- ⚠️ Free tier sleeps after inactivity (slower first load)

### Steps:

1. **Go to Render.com**
   ```
   https://render.com
   ```

2. **Sign in with GitHub**

3. **New > Web Service**
   - Connect repo: `gamearcade199-prog/trulyinvoice.xyz`
   - Name: `trulyinvoice-backend`
   - Root Directory: `backend`
   - Runtime: `Python 3`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn main:app --host 0.0.0.0 --port $PORT`

4. **Add Environment Variables**
   Same as Railway option above

5. **Deploy**
   - Click "Create Web Service"
   - Wait for deployment
   - Get URL: `https://trulyinvoice-backend.onrender.com`

6. **Update Vercel**
   ```
   NEXT_PUBLIC_API_URL=https://trulyinvoice-backend.onrender.com
   ```

---

## 🐳 OPTION 3: Docker + Any Cloud Provider

If you prefer Docker:

### Create Dockerfile in `/backend`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Deploy to:
- **Google Cloud Run**
- **AWS ECS/Fargate**
- **Azure Container Apps**
- **DigitalOcean App Platform**

---

## 🔧 AFTER DEPLOYMENT

### 1. Update Frontend Environment

**Local development** (`.env.local`):
```bash
NEXT_PUBLIC_API_URL=https://your-backend-url.railway.app
```

**Vercel production**:
1. Vercel Dashboard > Project > Settings > Environment Variables
2. Add: `NEXT_PUBLIC_API_URL` = `https://your-backend-url.railway.app`
3. Redeploy

### 2. Test Backend

Visit: `https://your-backend-url.railway.app/docs`

You should see the FastAPI Swagger documentation.

### 3. Test Upload

1. Go to your deployed site: `https://trulyinvoice.xyz`
2. Try uploading an invoice
3. Check browser console for errors
4. Should now work! ✅

---

## 📝 QUICK DEPLOYMENT CHECKLIST

- [ ] Choose deployment platform (Railway recommended)
- [ ] Sign up and connect GitHub
- [ ] Configure `/backend` as root directory
- [ ] Add all environment variables
- [ ] Wait for deployment to complete
- [ ] Copy backend URL
- [ ] Update `NEXT_PUBLIC_API_URL` in Vercel
- [ ] Redeploy frontend on Vercel
- [ ] Test upload functionality
- [ ] Run SQL script: `FIX_ANONYMOUS_UPLOAD_RLS.sql` in Supabase

---

## 🚨 IMPORTANT: Security

After deployment:

1. **Add CORS Origins** in backend `main.py`:
   ```python
   allow_origins=[
       "https://trulyinvoice.xyz",
       "https://trulyinvoice-xyz.vercel.app"
   ]
   ```

2. **Enable Rate Limiting** to prevent abuse

3. **Monitor API Usage** (OpenAI costs money!)

4. **Add API Key Authentication** for production

---

## 💡 ESTIMATED COSTS

### Free Tier Options:
- **Railway**: $5/month (500 hours free)
- **Render**: Free (with sleep)
- **Vercel**: Free (frontend already deployed)
- **Supabase**: Free (up to 500MB database)

### Paid Services:
- **OpenAI API**: ~$0.002 per invoice (pay-as-you-go)
- **Google Vision**: Free up to 1000 requests/month

**Total estimated cost**: $5-10/month for small scale

---

## 🆘 TROUBLESHOOTING

### Upload still failing?
1. Check backend health: `https://your-backend-url/health`
2. Check browser console for errors
3. Verify environment variable in Vercel
4. Run RLS fix SQL script in Supabase

### Backend not deploying?
1. Check `requirements.txt` exists in `/backend`
2. Verify Python version (3.11 recommended)
3. Check deployment logs for errors

### API calls timing out?
1. Increase timeout in Railway/Render settings
2. Check OpenAI API key is valid
3. Verify Supabase connection

---

## ✅ NEXT STEPS

1. **Deploy backend now** (Railway is fastest)
2. **Update NEXT_PUBLIC_API_URL** in Vercel
3. **Run SQL fix** in Supabase
4. **Test upload** on production site
5. **Celebrate!** 🎉

Need help? Check the logs:
- Railway: Dashboard > Deployments > Logs
- Render: Dashboard > Logs
- Vercel: Dashboard > Deployments > Function Logs
