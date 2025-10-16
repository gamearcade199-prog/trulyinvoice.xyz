# 🚀 Vercel Deployment - Environment Variables Guide

## 📋 All API Keys Required for Vercel

### **Frontend Deployment (Vercel)**

When deploying your **Next.js frontend** to Vercel, you need to add these environment variables:

#### 1. **Backend API URL** (Required)
```
NEXT_PUBLIC_API_URL=https://your-backend-url.com
```
- This is the URL where your FastAPI backend is deployed
- Example: `https://trulyinvoice-api.onrender.com` or `https://api.trulyinvoice.xyz`
- **Important**: Must start with `NEXT_PUBLIC_` to be accessible in browser

#### 2. **Supabase Configuration** (Required)
```
NEXT_PUBLIC_SUPABASE_URL=https://your-project.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=your-supabase-anon-key
```
- Get these from: [Supabase Dashboard](https://app.supabase.com) → Project Settings → API
- **Both** must start with `NEXT_PUBLIC_`

#### 3. **Optional Analytics/Monitoring**
```
NEXT_PUBLIC_GA_MEASUREMENT_ID=G-XXXXXXXXXX
```
- Google Analytics (if you want analytics)

---

### **Backend Deployment (Railway/Render/DigitalOcean)**

When deploying your **FastAPI backend**, you need these environment variables:

#### 1. **Database** (Required)
```
DATABASE_URL=postgresql://user:password@host:5432/database
```
- Your PostgreSQL database connection string
- Can use Supabase PostgreSQL or separate database
- Format: `postgresql://user:password@host:port/dbname`

#### 2. **Razorpay Payment Gateway** (Required for Payments)
```
RAZORPAY_KEY_ID=rzp_test_xxxxxxxxxxxx
RAZORPAY_KEY_SECRET=xxxxxxxxxxxxxxxxxxxxxxxx
RAZORPAY_WEBHOOK_SECRET=xxxxxxxxxxxxxxxxxxxxxxxx
```
- Get from: [Razorpay Dashboard](https://dashboard.razorpay.com) → Settings → API Keys
- **Test Mode** for testing: `rzp_test_...`
- **Live Mode** for production: `rzp_live_...`

#### 3. **Supabase** (Required)
```
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_ANON_KEY=your-supabase-anon-key
SUPABASE_SERVICE_KEY=your-supabase-service-key
```
- Get from: [Supabase Dashboard](https://app.supabase.com) → Project Settings → API
- Service key has admin privileges (keep secret!)

#### 4. **AI Services** (Required for Invoice Processing)
```
GEMINI_API_KEY=your-gemini-api-key
GOOGLE_VISION_API_KEY=your-google-vision-api-key
```
- **Gemini**: Get from [Google AI Studio](https://makersuite.google.com/app/apikey)
- **Vision API**: Get from [Google Cloud Console](https://console.cloud.google.com/apis/credentials)

#### 5. **Security** (Required)
```
SECRET_KEY=your-super-secret-key-min-32-characters-long
JWT_SECRET_KEY=your-jwt-secret-key-min-32-characters-long
```
- Generate random secure strings (32+ characters)
- Use: `openssl rand -hex 32` or Python: `python -c "import secrets; print(secrets.token_hex(32))"`

#### 6. **CORS Configuration** (Required)
```
CORS_ORIGINS=https://your-frontend.vercel.app,https://www.your-domain.com
```
- Add your Vercel frontend URL
- Add your custom domain if you have one
- Comma-separated list

#### 7. **Google OAuth** (Optional - for Google Sign-In)
```
GOOGLE_CLIENT_ID=your-client-id.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=your-google-client-secret
```
- Get from: [Google Cloud Console](https://console.cloud.google.com/apis/credentials)
- Only needed if you set up Google Sign-In OAuth

#### 8. **Environment** (Optional)
```
ENVIRONMENT=production
```
- Options: `development`, `staging`, `production`

---

## 🎯 Step-by-Step: Adding Variables to Vercel

### **For Frontend Deployment:**

1. **Go to Vercel Dashboard**
   - Visit: https://vercel.com/dashboard
   - Select your project

2. **Navigate to Settings**
   - Click on your project
   - Go to **Settings** tab
   - Click **Environment Variables** in sidebar

3. **Add Each Variable:**
   - Click **Add New**
   - **Name**: Enter variable name (e.g., `NEXT_PUBLIC_API_URL`)
   - **Value**: Enter the value
   - **Environments**: Select all (Production, Preview, Development)
   - Click **Save**

4. **Required Variables for Frontend:**
   ```
   ✅ NEXT_PUBLIC_API_URL
   ✅ NEXT_PUBLIC_SUPABASE_URL
   ✅ NEXT_PUBLIC_SUPABASE_ANON_KEY
   ```

5. **Redeploy**
   - Go to **Deployments** tab
   - Click **...** on latest deployment
   - Click **Redeploy**

---

## 📝 Complete Environment Variables Checklist

### **Frontend (Vercel)** - 3 Required:
- [ ] `NEXT_PUBLIC_API_URL`
- [ ] `NEXT_PUBLIC_SUPABASE_URL`
- [ ] `NEXT_PUBLIC_SUPABASE_ANON_KEY`

### **Backend (Railway/Render)** - 10 Required:
- [ ] `DATABASE_URL`
- [ ] `RAZORPAY_KEY_ID`
- [ ] `RAZORPAY_KEY_SECRET`
- [ ] `RAZORPAY_WEBHOOK_SECRET`
- [ ] `SUPABASE_URL`
- [ ] `SUPABASE_ANON_KEY`
- [ ] `SUPABASE_SERVICE_KEY`
- [ ] `GEMINI_API_KEY`
- [ ] `GOOGLE_VISION_API_KEY`
- [ ] `SECRET_KEY`
- [ ] `JWT_SECRET_KEY`
- [ ] `CORS_ORIGINS`

### **Optional** (Both):
- [ ] `GOOGLE_CLIENT_ID` (if using Google Sign-In)
- [ ] `GOOGLE_CLIENT_SECRET` (if using Google Sign-In)
- [ ] `NEXT_PUBLIC_GA_MEASUREMENT_ID` (if using Google Analytics)

---

## 🔐 Where to Get Each API Key

### 1. **Razorpay Keys**
- **URL**: https://dashboard.razorpay.com/app/keys
- **Steps**:
  1. Sign up/Login to Razorpay
  2. Go to Settings → API Keys
  3. Generate Test Keys (for testing)
  4. Generate Live Keys (for production)
  5. Copy Key ID and Key Secret
- **Webhook Secret**:
  1. Go to Settings → Webhooks
  2. Add webhook URL: `https://your-backend.com/api/payments/webhook`
  3. Copy webhook secret

### 2. **Supabase Keys**
- **URL**: https://app.supabase.com
- **Steps**:
  1. Select your project
  2. Go to Settings → API
  3. Copy:
     - Project URL (SUPABASE_URL)
     - anon/public key (SUPABASE_ANON_KEY)
     - service_role key (SUPABASE_SERVICE_KEY)

### 3. **Gemini API Key**
- **URL**: https://makersuite.google.com/app/apikey
- **Steps**:
  1. Sign in with Google account
  2. Click "Create API Key"
  3. Copy the key

### 4. **Google Vision API Key**
- **URL**: https://console.cloud.google.com/apis/credentials
- **Steps**:
  1. Create/Select a project
  2. Enable Vision API
  3. Go to Credentials
  4. Create API Key
  5. Copy the key

### 5. **Google OAuth** (Optional)
- **URL**: https://console.cloud.google.com/apis/credentials
- **Steps**:
  1. Create OAuth 2.0 Client ID
  2. Add authorized redirect URIs
  3. Copy Client ID and Client Secret

### 6. **Database URL**
- **Supabase PostgreSQL**:
  1. Go to Supabase → Settings → Database
  2. Copy connection string
  3. Format: `postgresql://postgres:[password]@[host]:5432/postgres`
- **Or use separate PostgreSQL** (Railway, Render, etc.)

---

## 🚀 Quick Copy-Paste Template

### **For Vercel (Frontend)**
```bash
# Copy these to Vercel → Settings → Environment Variables

NEXT_PUBLIC_API_URL=https://your-backend-url.com
NEXT_PUBLIC_SUPABASE_URL=https://xxxxx.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

### **For Backend (Railway/Render)**
```bash
# Copy these to your backend hosting platform

DATABASE_URL=postgresql://user:password@host:5432/database
RAZORPAY_KEY_ID=rzp_test_xxxxxxxxxxxx
RAZORPAY_KEY_SECRET=xxxxxxxxxxxxxxxxxxxxxxxx
RAZORPAY_WEBHOOK_SECRET=xxxxxxxxxxxxxxxxxxxxxxxx
SUPABASE_URL=https://xxxxx.supabase.co
SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
SUPABASE_SERVICE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
GEMINI_API_KEY=AIzaSy...
GOOGLE_VISION_API_KEY=AIzaSy...
SECRET_KEY=your-secret-key-here-min-32-chars
JWT_SECRET_KEY=your-jwt-secret-key-here-min-32-chars
CORS_ORIGINS=https://your-frontend.vercel.app
ENVIRONMENT=production
```

---

## ⚠️ Security Best Practices

### **DO:**
✅ Use environment variables for all secrets
✅ Use different keys for development and production
✅ Keep service keys secret (never expose in frontend)
✅ Use `NEXT_PUBLIC_` prefix only for frontend-visible vars
✅ Regenerate keys if accidentally exposed
✅ Use HTTPS for all production URLs

### **DON'T:**
❌ Commit `.env` files to Git
❌ Share API keys publicly
❌ Use test keys in production
❌ Hardcode secrets in code
❌ Use same keys across projects

---

## 🧪 Testing Your Configuration

### **Test Frontend:**
```bash
# After deploying to Vercel
curl https://your-app.vercel.app
```

### **Test Backend:**
```bash
# Test health endpoint
curl https://your-backend.com/health

# Test API
curl https://your-backend.com/api/payments/config
```

### **Test Integration:**
1. Open your Vercel app
2. Try registering a user → Should create free subscription
3. Go to pricing page → Should see all plans
4. Click upgrade → Should open Razorpay checkout
5. Complete payment → Should activate subscription

---

## 📞 Support Links

- **Vercel Docs**: https://vercel.com/docs/environment-variables
- **Razorpay Docs**: https://razorpay.com/docs/
- **Supabase Docs**: https://supabase.com/docs
- **Google Cloud**: https://console.cloud.google.com

---

## ✅ Final Checklist Before Going Live

- [ ] All environment variables added to Vercel
- [ ] All environment variables added to backend host
- [ ] Test Razorpay with test keys works
- [ ] Switch to Razorpay live keys for production
- [ ] Update CORS_ORIGINS with production URLs
- [ ] Update webhook URLs in Razorpay dashboard
- [ ] Test complete user journey (register → upgrade → payment)
- [ ] Verify database connections work
- [ ] Check all API endpoints respond
- [ ] Test payment flow end-to-end

---

**You're ready to deploy!** 🚀

Need help with any specific API key? Let me know!
