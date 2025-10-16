# 🔔 How to Get Razorpay Webhook Secret - Step by Step

## 🎯 What is a Webhook?

A webhook is a way for Razorpay to automatically notify your backend when a payment event happens (like payment success or failure). The webhook secret is used to verify that the notification really came from Razorpay.

---

## 📋 Step-by-Step Guide

### **Step 1: Login to Razorpay Dashboard**
1. Go to: https://dashboard.razorpay.com
2. Login with your credentials
3. Make sure you're in the correct mode (Test/Live)

---

### **Step 2: Navigate to Webhooks**

#### Option A: Through Settings Menu
1. Click on **Settings** (gear icon) in the left sidebar
2. Click on **Webhooks** in the dropdown

#### Option B: Direct Link
- Test Mode: https://dashboard.razorpay.com/app/webhooks
- Live Mode: Switch to live mode first, then go to webhooks

---

### **Step 3: Add New Webhook**

1. Click the **"+ Add New Webhook"** button (blue button on the right)

2. **Webhook Setup Form** will appear with:
   - Webhook URL
   - Alert Email
   - Events to listen
   - Active/Inactive toggle

---

### **Step 4: Configure Webhook URL**

#### **Enter Your Backend URL:**

**Development/Testing:**
```
http://localhost:8000/api/payments/webhook
```
⚠️ This won't work in production - it's local only

**Production:**
```
https://your-backend-domain.com/api/payments/webhook
```

Examples:
- Railway: `https://your-app.railway.app/api/payments/webhook`
- Render: `https://your-app.onrender.com/api/payments/webhook`
- DigitalOcean: `https://your-api.example.com/api/payments/webhook`

---

### **Step 5: Select Events to Listen**

**Select these important events:**

✅ **payment.authorized** - Payment authorized by bank
✅ **payment.captured** - Payment successfully captured (MOST IMPORTANT)
✅ **payment.failed** - Payment failed

**Other useful events (optional):**
- payment.pending
- refund.created
- refund.processed
- order.paid

**Recommendation:** Select all payment-related events for better tracking.

---

### **Step 6: Configure Alert Email**

1. Enter your email address
2. You'll receive notifications when webhook fails
3. Example: `admin@yourdomain.com`

---

### **Step 7: Save and Get Secret**

1. Click **"Create Webhook"** button at the bottom

2. **Webhook will be created** and you'll see it in the list

3. **Click on the webhook** you just created

4. You'll see webhook details:
   ```
   Webhook URL: https://your-backend.com/api/payments/webhook
   Status: Active
   Secret: [Hidden by default]
   ```

5. **Click "Show Secret"** button

6. **Copy the Webhook Secret**
   - It looks like: `whsec_aBcDeFgHiJkLmNoPqRsTuVwXyZ123456`
   - Or: `WhSec1234AbCd5678EfGh9012IjKl3456`
   - Length: ~32-40 characters
   - Alphanumeric string

---

## 📸 Visual Guide

### **Dashboard View:**
```
┌─────────────────────────────────────────────┐
│ Razorpay Dashboard - Webhooks              │
├─────────────────────────────────────────────┤
│                                             │
│  [+ Add New Webhook]                        │
│                                             │
│  Active Webhooks:                           │
│  ┌───────────────────────────────────────┐ │
│  │ https://your-api.com/api/payments/... │ │
│  │ Status: Active                        │ │
│  │ Events: 3 selected                    │ │
│  │ [Edit] [Delete] [View Details]        │ │
│  └───────────────────────────────────────┘ │
│                                             │
└─────────────────────────────────────────────┘
```

### **Webhook Details View:**
```
┌─────────────────────────────────────────────┐
│ Webhook Details                             │
├─────────────────────────────────────────────┤
│ URL: https://your-api.com/api/payments/... │
│ Status: Active ●                            │
│                                             │
│ Events Selected:                            │
│ ✓ payment.authorized                        │
│ ✓ payment.captured                          │
│ ✓ payment.failed                            │
│                                             │
│ Secret:                                     │
│ ••••••••••••••••••••••• [Show Secret]       │
│                                             │
│ After clicking "Show Secret":               │
│ whsec_aBcDeFgHiJkLmNoPqRsTuVwXyZ123456    │
│ [Copy]                                      │
└─────────────────────────────────────────────┘
```

---

## 🔑 What You'll Get

After following these steps, you'll have:

```bash
RAZORPAY_WEBHOOK_SECRET=whsec_aBcDeFgHiJkLmNoPqRsTuVwXyZ123456
```

---

## 📝 Add to Your Environment Variables

### **Backend .env file:**
```bash
# Razorpay Webhook
RAZORPAY_WEBHOOK_SECRET=whsec_aBcDeFgHiJkLmNoPqRsTuVwXyZ123456
```

### **Railway/Render/DigitalOcean:**
1. Go to your backend deployment settings
2. Add environment variable:
   - **Name**: `RAZORPAY_WEBHOOK_SECRET`
   - **Value**: `whsec_aBcDeFgHiJkLmNoPqRsTuVwXyZ123456`
3. Redeploy

---

## 🧪 Testing Your Webhook

### **Method 1: Using Razorpay Dashboard**

1. Go to Webhooks page
2. Click on your webhook
3. Click **"Send Test Webhook"**
4. Select event type (e.g., payment.captured)
5. Click **"Send"**
6. Check your backend logs to see if it received the webhook

### **Method 2: Make a Test Payment**

1. Use Razorpay test mode
2. Make a test payment with test card: `4111 1111 1111 1111`
3. Complete payment
4. Razorpay will automatically send webhook to your URL
5. Check backend logs to verify webhook received

### **Method 3: Check Webhook Logs in Dashboard**

1. Go to Webhooks page
2. Click on your webhook
3. Click **"Logs"** or **"Recent Deliveries"**
4. See all webhook attempts:
   - ✅ Success (200 OK)
   - ❌ Failed (4xx, 5xx errors)
5. Click on individual log to see request/response

---

## ⚠️ Common Issues & Solutions

### **Issue 1: Webhook URL Not Accessible**
**Problem:** Razorpay can't reach your webhook URL

**Solutions:**
- ✅ Make sure backend is deployed and running
- ✅ URL must be public (not localhost for production)
- ✅ Use HTTPS in production (not HTTP)
- ✅ Check firewall settings
- ✅ Verify URL is correct: `/api/payments/webhook`

### **Issue 2: Webhook Secret Invalid**
**Problem:** Signature verification fails

**Solutions:**
- ✅ Copy the FULL webhook secret (all characters)
- ✅ No extra spaces or quotes
- ✅ Make sure environment variable is loaded
- ✅ Restart backend after adding variable

### **Issue 3: Webhook Receives but Fails**
**Problem:** Webhook receives but returns error

**Solutions:**
- ✅ Check backend logs for errors
- ✅ Verify signature verification code is correct
- ✅ Make sure database connection is working
- ✅ Test locally first with test webhooks

### **Issue 4: Can't Find Webhook Secret**
**Problem:** Don't see webhook secret in dashboard

**Solutions:**
- ✅ Make sure webhook is created first
- ✅ Click on the webhook to see details
- ✅ Click "Show Secret" button
- ✅ If still not visible, delete and recreate webhook

---

## 🔄 For Development (Local Testing)

### **Option 1: Use ngrok (Recommended)**

1. **Install ngrok:**
   ```bash
   # Download from https://ngrok.com/download
   # Or use package manager
   choco install ngrok  # Windows
   brew install ngrok   # Mac
   ```

2. **Start your backend:**
   ```bash
   cd backend
   python -m uvicorn app.main:app --reload --port 8000
   ```

3. **Start ngrok:**
   ```bash
   ngrok http 8000
   ```

4. **Copy the ngrok URL:**
   ```
   Forwarding: https://abc123.ngrok.io -> http://localhost:8000
   ```

5. **Use in Razorpay Webhook:**
   ```
   https://abc123.ngrok.io/api/payments/webhook
   ```

### **Option 2: Use Localtunnel**

```bash
# Install
npm install -g localtunnel

# Start backend
cd backend
python -m uvicorn app.main:app --reload --port 8000

# Create tunnel
lt --port 8000

# Use the URL in webhook
https://random-name.loca.lt/api/payments/webhook
```

---

## 📋 Complete Setup Checklist

- [ ] Login to Razorpay Dashboard
- [ ] Navigate to Settings → Webhooks
- [ ] Click "Add New Webhook"
- [ ] Enter webhook URL (your backend URL + `/api/payments/webhook`)
- [ ] Select events: payment.captured, payment.failed
- [ ] Add alert email
- [ ] Click "Create Webhook"
- [ ] Click on webhook to view details
- [ ] Click "Show Secret" button
- [ ] Copy webhook secret
- [ ] Add to backend environment variables as `RAZORPAY_WEBHOOK_SECRET`
- [ ] Restart/redeploy backend
- [ ] Test webhook with "Send Test Webhook" button
- [ ] Verify webhook logs show successful delivery

---

## 🎯 Quick Reference

| Step | Action | What You Get |
|------|--------|--------------|
| 1 | Login to Razorpay | Access to dashboard |
| 2 | Go to Settings → Webhooks | Webhooks page |
| 3 | Click "Add New Webhook" | Webhook form |
| 4 | Enter backend URL + `/api/payments/webhook` | Webhook endpoint |
| 5 | Select payment events | Event subscriptions |
| 6 | Click "Create Webhook" | Webhook created |
| 7 | Click webhook → "Show Secret" | **Webhook Secret!** ✅ |
| 8 | Copy and add to `.env` | Ready to use! 🚀 |

---

## 🔗 Quick Links

- **Razorpay Webhooks**: https://dashboard.razorpay.com/app/webhooks
- **Webhook Documentation**: https://razorpay.com/docs/webhooks/
- **Webhook Events**: https://razorpay.com/docs/webhooks/payloads/
- **ngrok**: https://ngrok.com/
- **Localtunnel**: https://localtunnel.github.io/www/

---

## 💡 Pro Tips

1. **Use Different Webhooks for Test and Live**
   - Test mode webhook for development
   - Live mode webhook for production

2. **Monitor Webhook Logs**
   - Check logs regularly in Razorpay dashboard
   - Set up alerts for failed webhooks

3. **Handle Webhook Retries**
   - Razorpay retries failed webhooks
   - Make your webhook endpoint idempotent

4. **Secure Your Webhook**
   - Always verify webhook signature
   - Don't trust webhook data without verification

5. **Test Thoroughly**
   - Test with all payment scenarios
   - Test failed payments too
   - Test with real cards in test mode

---

**Now you know how to get your webhook secret!** 🎉

Need more help? Check the full webhook implementation in your `backend/app/api/payments.py` file!
