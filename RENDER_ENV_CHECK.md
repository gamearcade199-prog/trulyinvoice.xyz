# ⚠️ CRITICAL: Check Your Render Environment Variables

## 🚨 Issue Found in Logs

Your deployment failed with this error:
```
Port could not be cast to integer value as '11022RAZORPAY_KEY_SECRET=<get_from_dashboard>'
```

This means your `REDIS_URL` environment variable in Render is **corrupted** or **merged with another variable**.

---

## ✅ How to Fix (5 minutes)

### Step 1: Go to Render Dashboard

1. Open: https://dashboard.render.com/
2. Click your **trulyinvoice-backend** service
3. Click **Environment** tab

---

### Step 2: Check REDIS_URL Format

Your `REDIS_URL` should look like this (ONE LINE):

```
redis://default:CtqaJntbmNO0YIoujIQCILUSqAlANElg@redis-11022.c13.us-east-1-3.ec2.redns.redis-cloud.com:11022
```

**❌ WRONG (what you might have):**
```
redis://default:CtqaJntbmNO0YIoujIQCILUSqAlANElg@redis-11022.c13.us-east-1-3.ec2.redns.redis-cloud.com:11022RAZORPAY_KEY_SECRET=<get_from_dashboard>
```

**If it looks corrupted:**
1. Delete the `REDIS_URL` variable
2. Add it again with the correct value (see below)

---

### Step 3: Set ALL Environment Variables Correctly

**Copy and paste these EXACTLY (one per line):**

```bash
# Environment
ENVIRONMENT=production
DEBUG=false

# Redis (use YOUR actual Redis URL)
REDIS_URL=redis://default:CtqaJntbmNO0YIoujIQCILUSqAlANElg@redis-11022.c13.us-east-1-3.ec2.redns.redis-cloud.com:11022

# Security Keys (generate these - see below)
SECRET_KEY=your-generated-secret-key-here
JWT_SECRET_KEY=your-generated-jwt-secret-here

# Razorpay (get from dashboard)
RAZORPAY_KEY_ID=rzp_live_RUCxZnVyqol9Nv
RAZORPAY_KEY_SECRET=your-actual-razorpay-secret
RAZORPAY_WEBHOOK_SECRET=your-actual-webhook-secret

# Supabase (get from Supabase dashboard)
SUPABASE_URL=https://ldvwxqluaheuhbycdpwn.supabase.co
SUPABASE_KEY=your-supabase-anon-key
SUPABASE_SERVICE_KEY=your-supabase-service-key

# Database (get from Supabase)
DATABASE_URL=postgresql://postgres:your-password@db.ldvwxqluaheuhbycdpwn.supabase.co:5432/postgres

# AI Keys (if using)
GEMINI_API_KEY=your-gemini-key
GOOGLE_AI_API_KEY=your-google-ai-key
VISION_API_ENABLED=true
```

---

### Step 4: Generate Secret Keys

Run these commands **locally**:

```bash
# Generate SECRET_KEY
python -c "import secrets; print(secrets.token_urlsafe(32))"

# Generate JWT_SECRET_KEY
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

Copy the output and paste into Render.

---

### Step 5: Get Razorpay Secrets

1. Go to: https://dashboard.razorpay.com/
2. **Settings → API Keys**
   - Click "Show" on Key Secret → Copy
3. **Settings → Webhooks**
   - Copy the "Signing Secret"

---

### Step 6: Save and Redeploy

1. Click **"Save Changes"** in Render
2. Render will auto-redeploy (~2-3 minutes)
3. Watch the logs for success

---

## 🧪 After Deployment - Test These

```bash
# 1. Health check
curl https://trulyinvoice-backend.onrender.com/api/health

# 2. Debug endpoint (should be 404)
curl https://trulyinvoice-backend.onrender.com/api/debug/auth-header

# 3. Check logs for these messages:
✅ Configuration loaded for production environment
✅ Security middleware added
Application startup complete
```

---

## ⚠️ Common Mistakes to Avoid

1. **❌ Don't put multiple variables on one line**
   ```
   WRONG: REDIS_URL=redis://...RAZORPAY_KEY=xxx
   RIGHT: Each variable on its own line in Render UI
   ```

2. **❌ Don't copy/paste the entire .env file**
   - Render needs each variable separately
   - Use the "Add Environment Variable" button for each one

3. **❌ Don't include quotes around values**
   ```
   WRONG: SECRET_KEY="abc123"
   RIGHT: SECRET_KEY=abc123
   ```

4. **❌ Don't include comments**
   ```
   WRONG: ENVIRONMENT=production  # this is production
   RIGHT: ENVIRONMENT=production
   ```

---

## 📋 Checklist

- [ ] `REDIS_URL` is on one line (no extra text)
- [ ] `ENVIRONMENT=production` is set
- [ ] `DEBUG=false` is set
- [ ] `SECRET_KEY` generated and set
- [ ] `RAZORPAY_KEY_SECRET` from dashboard
- [ ] `RAZORPAY_WEBHOOK_SECRET` from dashboard
- [ ] Each variable is separate (not merged)
- [ ] No quotes around values
- [ ] No comments in values
- [ ] Clicked "Save Changes"

---

## 🎯 Expected Result

After fixing, your deployment logs should show:

```
✅ Configuration loaded for production environment
✅ Security middleware added
✅ Security headers middleware initialized
✅ VISION OCR + FLASH-LITE extraction ENABLED
Application startup complete
Uvicorn running on http://0.0.0.0:10000
```

---

## 🆘 Still Getting Errors?

Check the exact error in Render logs:

1. Go to Render Dashboard
2. Click your service
3. Click **Logs** tab
4. Look for the last error message
5. Share it if you need help

---

**This should fix the deployment!** The code is working fine (tested locally). The issue is just the environment variable format in Render.
