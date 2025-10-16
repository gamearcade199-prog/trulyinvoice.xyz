# 🚀 Quick Reference: Vercel Environment Variables

## Frontend (Vercel) - 3 Variables

Add these in **Vercel Dashboard → Settings → Environment Variables**:

```
NEXT_PUBLIC_API_URL=https://your-backend-url.com
NEXT_PUBLIC_SUPABASE_URL=https://xxxxx.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

---

## Where to Get Each Key

### 1. `NEXT_PUBLIC_API_URL`
- Your backend URL (Railway, Render, DigitalOcean, etc.)
- Example: `https://trulyinvoice-api.onrender.com`

### 2. `NEXT_PUBLIC_SUPABASE_URL`
- Supabase Dashboard → Settings → API → Project URL
- Format: `https://xxxxx.supabase.co`

### 3. `NEXT_PUBLIC_SUPABASE_ANON_KEY`
- Supabase Dashboard → Settings → API → anon public key
- Starts with: `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...`

---

## Backend Variables (Railway/Render) - 10+ Variables

```
DATABASE_URL=postgresql://user:password@host:5432/database
RAZORPAY_KEY_ID=rzp_test_xxxxxxxxxxxx
RAZORPAY_KEY_SECRET=xxxxxxxxxxxxxxxxxxxxxxxx
RAZORPAY_WEBHOOK_SECRET=xxxxxxxxxxxxxxxxxxxxxxxx
SUPABASE_URL=https://xxxxx.supabase.co
SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
SUPABASE_SERVICE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
GEMINI_API_KEY=AIzaSy...
GOOGLE_VISION_API_KEY=AIzaSy...
SECRET_KEY=your-secret-key-min-32-chars
JWT_SECRET_KEY=your-jwt-secret-key-min-32-chars
CORS_ORIGINS=https://your-app.vercel.app
```

---

## 🔗 Quick Links

- **Razorpay Keys**: https://dashboard.razorpay.com/app/keys
- **Supabase Keys**: https://app.supabase.com (Settings → API)
- **Gemini API**: https://makersuite.google.com/app/apikey
- **Vision API**: https://console.cloud.google.com/apis/credentials
- **Vercel Dashboard**: https://vercel.com/dashboard

---

## ⚡ Quick Steps

1. **Deploy Backend First** (Railway/Render)
   - Add all 10+ backend variables
   - Get the deployed backend URL

2. **Deploy Frontend to Vercel**
   - Add 3 frontend variables
   - Use backend URL in `NEXT_PUBLIC_API_URL`
   - Deploy!

3. **Test Everything**
   - Register a user → Gets free plan ✅
   - Try payment → Razorpay opens ✅
   - Complete payment → Subscription activates ✅

---

**That's it!** See `VERCEL_DEPLOYMENT_GUIDE.md` for detailed instructions.
