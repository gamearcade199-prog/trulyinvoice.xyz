# 🎯 SENTRY SETUP GUIDE

Quick guide to set up error monitoring for TrulyInvoice.

---

## 📋 STEP 1: Create Sentry Account

1. Go to https://sentry.io
2. Click **"Start Free"**
3. Sign up with:
   - GitHub account (recommended), or
   - Google account, or
   - Email

**Free Tier Includes:**
- 5,000 errors per month
- 30 days data retention
- 1 project
- Performance monitoring
- Source maps

---

## 📋 STEP 2: Create Project

1. After login, click **"Create Project"**
2. Select platform: **Python** (for backend)
3. Set project name: **trulyinvoice-backend**
4. Click **"Create Project"**

---

## 📋 STEP 3: Get Your DSN

1. After project creation, you'll see your DSN:
   ```
   https://abc123def456@o123456.ingest.sentry.io/789012
   ```

2. Copy this DSN

3. Add to your `.env` file:
   ```bash
   SENTRY_DSN=https://abc123def456@o123456.ingest.sentry.io/789012
   ```

---

## 📋 STEP 4: Install Sentry SDK

```bash
cd backend
pip install sentry-sdk[fastapi]
```

✅ **Already done!** This is already added to `requirements.txt`

---

## 📋 STEP 5: Verify Installation

1. Start your backend:
   ```bash
   cd backend
   python -m uvicorn app.main:app --reload
   ```

2. Check console output for:
   ```
   ✅ Sentry error monitoring initialized
   ```

3. If you see:
   ```
   ⚠️  SENTRY_DSN not set - Error monitoring disabled
   ```
   Then add your DSN to `.env` file

---

## 📋 STEP 6: Test Error Tracking

1. Create a test endpoint to trigger an error:
   ```python
   # In backend/app/main.py (temporary test)
   
   @app.get("/test-sentry")
   def test_sentry():
       # This will send an error to Sentry
       division_by_zero = 1 / 0
       return {"status": "ok"}
   ```

2. Visit: http://localhost:8000/test-sentry

3. Check Sentry dashboard:
   - Go to https://sentry.io
   - Click on your project
   - You should see the error!

4. **Remove the test endpoint** after verification

---

## 📋 STEP 7: Configure Sentry Dashboard

### 7.1 Set Up Alerts

1. Go to **Alerts** > **Create Alert**
2. Select: **Issues**
3. Configure:
   - **When:** An issue is first seen
   - **If:** All events
   - **Then:** Send notification to Email

4. Create another alert:
   - **When:** An issue is seen more than 10 times in 1 hour
   - **Then:** Send notification (indicates critical issue)

### 7.2 Enable Performance Monitoring

1. Go to **Performance** tab
2. Click **Set Up**
3. Already configured in code! (10% sample rate)

### 7.3 Configure Releases (Optional but Recommended)

This helps track which version introduced bugs:

```bash
# Install Sentry CLI
curl -sL https://sentry.io/get-cli/ | bash

# Authenticate
sentry-cli login

# Create release (run before each deployment)
sentry-cli releases new "backend@1.0.0"
sentry-cli releases finalize "backend@1.0.0"
```

---

## 📋 STEP 8: Team Invitations (Optional)

1. Go to **Settings** > **Members**
2. Click **Invite Member**
3. Enter email addresses
4. Set role (Admin, Member, or Billing)

---

## 📋 STEP 9: Configure Environments

1. Go to **Settings** > **Environments**
2. Add environments:
   - `development`
   - `staging`
   - `production`

These are automatically tagged based on your `ENVIRONMENT` env var!

---

## 📋 STEP 10: Verify Production Setup

Before deploying to production:

1. ✅ Sentry SDK installed
2. ✅ SENTRY_DSN in production environment variables
3. ✅ Alerts configured
4. ✅ Team members invited
5. ✅ Test error sent and received

---

## 🎯 WHAT SENTRY TRACKS

### Automatically Captured:
- ❌ **Unhandled exceptions** - All crashes
- ⚠️ **HTTP errors** - 500 errors, 404s, etc.
- 🐌 **Slow endpoints** - Performance issues
- 📊 **Request context** - URL, headers, user agent
- 🔍 **Stack traces** - Exact line that failed
- 👤 **User context** - Which user hit the error

### Example Error Report:
```
ZeroDivisionError: division by zero
  File "app/api/invoices.py", line 42, in process_invoice
    result = total / count  ← Error occurred here

User: user@example.com
URL: /api/invoices/process
Browser: Chrome 119
Time: 2025-10-26 14:32:01 UTC
```

---

## 🔧 ADVANCED CONFIGURATION

### Custom Error Capture

```python
import sentry_sdk

# Manually capture exception
try:
    risky_operation()
except Exception as e:
    sentry_sdk.capture_exception(e)

# Add custom context
with sentry_sdk.push_scope() as scope:
    scope.set_context("invoice", {
        "id": invoice_id,
        "amount": invoice_amount
    })
    scope.set_tag("payment_method", "razorpay")
    sentry_sdk.capture_exception(exception)

# Add breadcrumbs (track user actions)
sentry_sdk.add_breadcrumb(
    category='action',
    message='User uploaded invoice',
    level='info'
)
```

### Filter Sensitive Data

```python
# Already configured in main.py:
sentry_sdk.init(
    dsn=sentry_dsn,
    send_default_pii=False,  # Don't send personal info
    before_send=scrub_sensitive_data,  # Custom filter
)

def scrub_sensitive_data(event, hint):
    # Remove sensitive fields
    if 'request' in event:
        if 'headers' in event['request']:
            event['request']['headers'].pop('Authorization', None)
            event['request']['headers'].pop('Cookie', None)
    return event
```

---

## 💰 PRICING

### Free Tier (Current)
- ✅ 5,000 errors/month
- ✅ 10,000 performance transactions/month
- ✅ 30 days data retention
- ✅ 1 project
- **Cost: $0/month**

### Team Tier (If Needed)
- 50,000 errors/month
- 100,000 performance transactions
- 90 days retention
- Unlimited projects
- Priority support
- **Cost: $26/month**

**Recommendation:** Start with free tier. Upgrade if you exceed limits.

---

## 📊 MONITORING BEST PRACTICES

### 1. Check Sentry Daily
Review errors every morning:
- Any new errors?
- Any spike in error count?
- Any critical issues?

### 2. Set Up Slack/Discord Integration
Get real-time alerts:
1. Go to **Settings** > **Integrations**
2. Enable **Slack** or **Discord**
3. Choose channel for notifications

### 3. Create Dashboards
Monitor key metrics:
- Error rate
- Response times
- Most common errors
- Affected users

### 4. Weekly Review
Every week:
- Review top 10 errors
- Fix or mark as resolved
- Track error trends

---

## ✅ VERIFICATION CHECKLIST

Before marking this as complete:

- [ ] Sentry account created
- [ ] Project created (trulyinvoice-backend)
- [ ] DSN added to `.env`
- [ ] SDK installed (`pip install sentry-sdk[fastapi]`)
- [ ] Backend restarted
- [ ] Test error sent
- [ ] Error appeared in dashboard
- [ ] Alerts configured
- [ ] Production DSN added to Render environment variables
- [ ] Team members invited (if applicable)

---

## 🆘 TROUBLESHOOTING

### Issue: Not seeing errors in Sentry

**Check:**
1. Is SENTRY_DSN set correctly?
   ```bash
   echo $SENTRY_DSN
   ```

2. Is Sentry initialized?
   Check console output for: `✅ Sentry error monitoring initialized`

3. Is the error actually happening?
   Check server logs

4. Is sample rate too low?
   In `main.py`, temporarily set:
   ```python
   traces_sample_rate=1.0,  # 100% for testing
   ```

### Issue: Too many errors

**Solution:**
1. Filter out expected errors:
   ```python
   def before_send(event, hint):
       if 'exc_info' in hint:
           exc_type, exc_value, tb = hint['exc_info']
           if isinstance(exc_value, ExpectedError):
               return None  # Don't send
       return event
   ```

2. Adjust sample rate:
   ```python
   traces_sample_rate=0.01,  # 1% instead of 10%
   ```

---

## 📞 SUPPORT

- **Sentry Docs:** https://docs.sentry.io/platforms/python/guides/fastapi/
- **Sentry Support:** support@sentry.io
- **Community:** https://discord.gg/sentry

---

**Setup Time: ~15 minutes**  
**Difficulty: Easy ⭐**

Once set up, Sentry runs automatically and catches all errors! 🎉
