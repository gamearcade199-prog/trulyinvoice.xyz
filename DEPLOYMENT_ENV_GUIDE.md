# 🚀 Production Environment Variables Guide

## Required Environment Variables for Render Backend

### 1. Generate Strong Secrets (Run Locally)

```bash
# Generate SECRET_KEY
python -c "import secrets; print('SECRET_KEY=' + secrets.token_urlsafe(32))"

# Generate JWT_SECRET_KEY
python -c "import secrets; print('JWT_SECRET_KEY=' + secrets.token_urlsafe(32))"
```

Copy the output and save it.

---

### 2. Get Razorpay Secrets

1. Go to: https://dashboard.razorpay.com/
2. Login to your account
3. **Get Key Secret:**
   - Settings → API Keys
   - Click "Show" on Key Secret
   - Copy the secret (starts with something like `AaBbCc123...`)
4. **Get Webhook Secret:**
   - Settings → Webhooks
   - Find your webhook endpoint
   - Copy the "Signing Secret"

---

### 3. Add to Render Backend

Go to Render Dashboard → `trulyinvoice-backend` service → Environment

**Add these variables:**

```bash
# Environment
ENVIRONMENT=production
DEBUG=false

# Security (use generated values from step 1)
SECRET_KEY=<paste_your_generated_SECRET_KEY>
JWT_SECRET_KEY=<paste_your_generated_JWT_SECRET_KEY>

# Razorpay (use values from step 2)
RAZORPAY_KEY_ID=rzp_live_RUCxZnVyqol9Nv
RAZORPAY_KEY_SECRET=<paste_your_actual_key_secret>
RAZORPAY_WEBHOOK_SECRET=<paste_your_actual_webhook_secret>

# Redis (already set)
REDIS_URL=redis://default:CtqaJntbmNO0YIoujIQCILUSqAlANElg@redis-11022.c13.us-east-1-3.ec2.redns.redis-cloud.com:11022

# Supabase (get from Supabase dashboard)
SUPABASE_URL=https://ldvwxqluaheuhbycdpwn.supabase.co
SUPABASE_KEY=<your_supabase_anon_key>
SUPABASE_SERVICE_KEY=<your_supabase_service_key>

# Database (get from Supabase → Settings → Database → Connection String)
DATABASE_URL=postgresql://postgres:[YOUR-PASSWORD]@db.ldvwxqluaheuhbycdpwn.supabase.co:5432/postgres

# AI Keys (if using)
GEMINI_API_KEY=<your_gemini_key>
GOOGLE_AI_API_KEY=<your_google_ai_key>
VISION_API_ENABLED=true

# Optional: Sentry for error tracking
SENTRY_DSN=<your_sentry_dsn>

# Optional: Email (if using password reset)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=<your_email@gmail.com>
SMTP_PASSWORD=<your_app_password>
SENDER_EMAIL=noreply@trulyinvoice.xyz
```

Click **"Save Changes"** - Render will auto-redeploy.

---

### 4. Verify Vercel Frontend Variables

Go to Vercel Dashboard → `trulyinvoice-xyz` project → Settings → Environment Variables

**✅ VERIFY THESE ARE SET:**

```bash
NEXT_PUBLIC_SUPABASE_URL=https://ldvwxqluaheuhbycdpwn.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=<your_anon_key>
NEXT_PUBLIC_API_URL=https://trulyinvoice-backend.onrender.com
NEXT_PUBLIC_RAZORPAY_KEY_ID=rzp_live_RUCxZnVyqol9Nv
```

**❌ CRITICAL: VERIFY THESE ARE SERVER-ONLY (NO NEXT_PUBLIC_ PREFIX):**

```bash
RAZORPAY_KEY_SECRET=<your_secret>  # ✅ Server-side only
```

**⚠️ If you see `NEXT_PUBLIC_RAZORPAY_KEY_SECRET`:**
- **DELETE IT IMMEDIATELY** (this would expose your secret to browsers!)
- Re-add as `RAZORPAY_KEY_SECRET` (without NEXT_PUBLIC_)

---

## 5. Test After Deployment

### Test 1: Health Check
```bash
curl https://trulyinvoice-backend.onrender.com/api/health
# Expected: {"status": "healthy", ...}
```

### Test 2: Debug Endpoint (Should Fail in Production)
```bash
curl https://trulyinvoice-backend.onrender.com/api/debug/auth-header
# Expected: 404 Not Found (debug endpoints disabled)
```

### Test 3: Payment Order Creation
```bash
curl -X POST https://trulyinvoice-backend.onrender.com/api/payments/create-order \
  -H "Authorization: Bearer <your_token>" \
  -H "Content-Type: application/json" \
  -d '{"tier":"pro","billing_cycle":"monthly","amount":100,"currency":"INR"}'

# Expected: {"order_id": "order_...", "amount_paise": 100, ...}
```

### Test 4: Admin Endpoints (Should Fail)
```bash
curl -X POST https://trulyinvoice-backend.onrender.com/api/storage/cleanup/all
# Expected: 404 Not Found (admin endpoints removed)
```

---

## 6. Security Checklist

- [ ] `ENVIRONMENT=production` set in Render
- [ ] `DEBUG=false` set in Render
- [ ] Strong `SECRET_KEY` generated and set
- [ ] Strong `JWT_SECRET_KEY` generated and set
- [ ] Real `RAZORPAY_KEY_SECRET` set (not xxxxxxx)
- [ ] Real `RAZORPAY_WEBHOOK_SECRET` set (not xxxxxxx)
- [ ] No `NEXT_PUBLIC_RAZORPAY_KEY_SECRET` in Vercel
- [ ] Debug endpoints return 404 in production
- [ ] Admin cleanup endpoints return 404

---

## 7. What Changed in Code

### Security Fixes Applied:

1. ✅ **Removed unprotected admin endpoints** (`/api/storage/cleanup/all`, `/api/storage/cleanup/anonymous`)
2. ✅ **Debug endpoint disabled in production** (only loads if `ENVIRONMENT != production`)
3. ✅ **Added rate limiting to user cleanup** (5 requests/hour)
4. ✅ **Restricted CORS methods** (only GET, POST, PUT, DELETE, OPTIONS, PATCH)
5. ✅ **Replaced password logging** (print → logger with sanitized output)
6. ✅ **Updated .env with production instructions**

### Files Modified:

- `backend/app/api/storage.py` - Removed admin endpoints, added rate limiting
- `backend/app/main.py` - Disabled debug in production, restricted CORS
- `backend/app/api/auth.py` - Replaced print() with logger
- `.env` - Added production deployment instructions

---

## 8. Common Issues & Solutions

### Issue: "Payment secret not configured"
**Solution:** Verify `RAZORPAY_KEY_SECRET` is set in Render (not xxxxxxx)

### Issue: "Webhook signature invalid"
**Solution:** Verify `RAZORPAY_WEBHOOK_SECRET` matches Razorpay dashboard

### Issue: "Database connection failed"
**Solution:** Get correct `DATABASE_URL` from Supabase dashboard

### Issue: "CORS error from frontend"
**Solution:** Verify `NEXT_PUBLIC_API_URL` points to Render backend

### Issue: "Rate limit exceeded immediately"
**Solution:** Redis might not be connected - check `REDIS_URL` in Render

---

## 9. Post-Deployment Monitoring

1. **Check Render Logs:**
   - Go to Render Dashboard → trulyinvoice-backend → Logs
   - Look for startup messages
   - Verify no errors about missing secrets

2. **Test Payment Flow:**
   - Create a test order for ₹1
   - Complete payment in Razorpay test mode
   - Verify webhook received in Render logs
   - Check subscription activated in database

3. **Monitor Sentry (if configured):**
   - Check for error reports
   - Set up alerts for critical issues

---

## 10. Emergency Rollback

If something breaks after deployment:

1. **Render:** Click "Manual Deploy" → Select previous working commit
2. **Vercel:** Deployments → Find previous deployment → Promote to Production

---

**Questions?** Check `COMPREHENSIVE_SECURITY_AUDIT_REPORT.md` for detailed security findings.
