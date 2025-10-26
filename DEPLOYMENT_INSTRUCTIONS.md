# 🚀 DEPLOYMENT INSTRUCTIONS
**Status**: All systems ready for production deployment  
**Date**: October 22, 2025  

---

## ✅ PRE-DEPLOYMENT CHECKLIST

### Frontend (Vercel)
- [x] Build passes locally (`npm run build`)
- [x] All dependencies installed
- [x] No breaking errors
- [x] Pages optimized
- [ ] GitHub repository pushed with latest code

### Backend (Render)
- [x] Python imports work
- [x] FastAPI app initializes
- [x] All dependencies installed
- [x] Import errors fixed
- [ ] GitHub repository pushed with latest code

### Shared Resources
- [x] Supabase project configured
- [x] Database schema created
- [x] RLS policies configured
- [ ] Environment variables documented

---

## 🔧 STEP 1: PREPARE GITHUB REPOSITORY

### 1.1 Commit and Push Latest Code
```bash
# Navigate to project root
cd C:\Users\akib\Desktop\trulyinvoice.in

# Stage all changes
git add .

# Commit with message
git commit -m "Production build ready - frontend and backend builds pass"

# Push to main branch
git push origin main
```

### 1.2 Verify Push Success
```bash
git log -1 --oneline
# Should show your latest commit
```

---

## 🌐 STEP 2: DEPLOY FRONTEND TO VERCEL

### 2.1 Connect to Vercel (First Time Only)
1. Go to [vercel.com](https://vercel.com)
2. Sign in or create account
3. Click "New Project"
4. Select your GitHub repository (gamearcade199-prog/trulyinvoice.xyz)
5. Select `frontend` as the root directory

### 2.2 Set Environment Variables in Vercel
In Vercel Dashboard → Settings → Environment Variables, add:

```
NEXT_PUBLIC_SUPABASE_URL=https://ldvwxqluaheuhbycdpwn.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imxkdnd4cWx1YWhldWhieWNkcHduIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjAwNzY2NTYsImV4cCI6MjA3NTY1MjY1Nn0.uPBCzeJ3tH1SD0QObL850zcrKDDLr9TA6KCUzBp9e1A
NEXT_PUBLIC_API_URL=https://your-render-backend-url.onrender.com
NEXT_PUBLIC_RAZORPAY_KEY=rzp_live_xxxxx  (Replace with your live key)
```

### 2.3 Deploy
1. Click "Deploy"
2. Wait for build to complete (2-3 minutes)
3. Vercel will show your frontend URL (https://trulyinvoice-xyz.vercel.app)
4. Visit URL to verify it's working

---

## 🖥️ STEP 3: DEPLOY BACKEND TO RENDER

### 3.1 Connect to Render (First Time Only)
1. Go to [render.com](https://render.com)
2. Sign in or create account
3. Click "New +"
4. Select "Web Service"
5. Connect GitHub repository (gamearcade199-prog/trulyinvoice.xyz)
6. Select `backend` as the root directory

### 3.2 Configure Web Service
- **Name**: `trulyinvoice-backend`
- **Runtime**: `Python`
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port 8000`

### 3.3 Set Environment Variables in Render
Go to Settings → Environment → Add the following:

```
SUPABASE_URL=https://ldvwxqluaheuhbycdpwn.supabase.co
SUPABASE_SERVICE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imxkdnd4cWx1YWhldWhieWNkcHduIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2MDA3NjY1NiwiZXhwIjoyMDc1NjUyNjU2fQ.939ySYuwA9ByCprCiI9GL5xEmvkhONYEWdtuHVLweWM

NEXT_PUBLIC_SUPABASE_URL=https://ldvwxqluaheuhbycdpwn.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imxkdnd4cWx1YWhldWhieWNkcHduIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjAwNzY2NTYsImV4cCI6MjA3NTY1MjY1Nn0.uPBCzeJ3tH1SD0QObL850zcrKDDLr9TA6KCUzBp9e1A

OPENAI_API_KEY=YOUR_NEW_OPENAI_API_KEY_HERE

GOOGLE_CLOUD_VISION_API_KEY=YOUR_NEW_GOOGLE_VISION_API_KEY_HERE

RAZORPAY_KEY_ID=rzp_live_xxxxx
RAZORPAY_KEY_SECRET=your_razorpay_live_secret_here

RAZORPAY_KEY_ID=rzp_live_xxxxx
RAZORPAY_KEY_SECRET=your_razorpay_live_secret_here

SECRET_KEY=96AC26418E865B266E4556ADB93AB
ACCESS_TOKEN_EXPIRE_MINUTES=30

ENVIRONMENT=production
DEBUG=False
```

### 3.4 Deploy
1. Click "Deploy"
2. Wait for build to complete (3-5 minutes)
3. Render will show your backend URL (https://trulyinvoice-backend.onrender.com)
4. Test the API: https://trulyinvoice-backend.onrender.com/docs

---

## 🔑 STEP 4: UPDATE RAZORPAY KEYS (LIVE)

### 4.1 Get Your Razorpay Live Keys
1. Go to [Razorpay Dashboard](https://dashboard.razorpay.com)
2. Navigate to Settings → API Keys
3. Copy your **Live Key ID** and **Live Secret**
4. Copy your **Live Key ID** (different format for frontend)

### 4.2 Update Vercel Environment
1. Go to Vercel Dashboard
2. Project Settings → Environment Variables
3. Update `NEXT_PUBLIC_RAZORPAY_KEY` with your live key

### 4.3 Update Render Environment
1. Go to Render Dashboard
2. Service Settings → Environment
3. Update `RAZORPAY_KEY_ID` with your live key ID
4. Update `RAZORPAY_KEY_SECRET` with your live secret

### 4.4 Redeploy Both Services
- Vercel: Click "Redeploy" (auto happens on env change)
- Render: Click "Redeploy"

---

## ✅ STEP 5: VERIFY DEPLOYMENT

### 5.1 Test Frontend
1. Visit your Vercel URL
2. Check that pages load correctly
3. Verify Supabase connection works
4. Test login/signup flow
5. Verify environment variables are loaded

### 5.2 Test Backend
1. Visit `https://your-render-url.onrender.com/docs`
2. Check API documentation loads
3. Test health endpoint: `GET /health`
4. Verify Razorpay config loaded

### 5.3 Test Payment Flow
1. Go to pricing page
2. Click "Upgrade to Plan"
3. Razorpay checkout should open
4. Complete test payment
5. Verify subscription activated in database

### 5.4 Test Invoice Upload
1. Go to Dashboard → Upload
2. Upload a test invoice
3. Verify it processes correctly
4. Check invoice appears in list

---

## 🔗 STEP 6: UPDATE FRONTEND API URL

### 6.1 Add Render Backend URL to Vercel
In Vercel Dashboard → Environment Variables, make sure:
```
NEXT_PUBLIC_API_URL=https://your-render-backend-url.onrender.com
```

### 6.2 Redeploy Frontend
Click "Redeploy" to apply the change

---

## 🎯 POST-DEPLOYMENT CHECKLIST

### Monitoring
- [ ] Set up error tracking (Sentry)
- [ ] Enable performance monitoring
- [ ] Configure email alerts for errors
- [ ] Monitor payment success rate

### Security
- [ ] Verify HTTPS is enforced
- [ ] Check security headers
- [ ] Enable CORS validation
- [ ] Review rate limiting settings

### Functionality
- [ ] Test complete user flow (signup → payment → invoice upload)
- [ ] Verify email notifications work
- [ ] Test password reset flow
- [ ] Confirm subscription limits enforced
- [ ] Test all export formats (Excel, CSV, PDF)

### Performance
- [ ] Check backend response times
- [ ] Verify frontend load times
- [ ] Monitor database query performance
- [ ] Check for any N+1 query issues

---

## 🚨 TROUBLESHOOTING

### Frontend Build Fails on Vercel
**Solution**: 
1. Check environment variables are set
2. Clear Vercel cache and redeploy
3. Ensure package.json has all dependencies

### Backend Build Fails on Render
**Solution**:
1. Check requirements.txt is complete
2. Verify Python version matches (3.11+)
3. Check for import errors in logs

### Payment Not Working
**Solution**:
1. Verify Razorpay keys are correct
2. Check webhook URL in Razorpay dashboard
3. Enable Razorpay test mode for testing

### Database Connection Fails
**Solution**:
1. Verify Supabase URL and keys
2. Check RLS policies are correct
3. Ensure database tables exist

---

## 📞 DEPLOYMENT SUPPORT

### Vercel Support
- Docs: https://vercel.com/docs
- Dashboard: https://vercel.com/dashboard

### Render Support
- Docs: https://render.com/docs
- Dashboard: https://dashboard.render.com

### Supabase Support
- Docs: https://supabase.com/docs
- Dashboard: https://app.supabase.com

### Razorpay Support
- Docs: https://razorpay.com/docs
- Dashboard: https://dashboard.razorpay.com

---

## ✅ DEPLOYMENT COMPLETE

Once all steps are done:
1. ✅ Frontend deployed on Vercel
2. ✅ Backend deployed on Render
3. ✅ Database configured on Supabase
4. ✅ Payments configured with Razorpay
5. ✅ All systems connected and working

**Your TrulyInvoice platform is now live!** 🎉

---

**Deployment Date**: October 22, 2025  
**Status**: ✅ Ready to Deploy  
**Estimated Time**: 20-30 minutes total

