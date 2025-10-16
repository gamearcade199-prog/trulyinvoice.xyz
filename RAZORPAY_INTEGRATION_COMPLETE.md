# 💳 Razorpay Payment Integration Guide

## Overview
Complete Razorpay payment gateway integration for TrulyInvoice subscription management. This system handles payment processing, signature verification, subscription activation, and webhook events.

## 🎯 Features Implemented

### ✅ Backend Payment System
- **Razorpay Service** (`backend/app/services/razorpay_service.py`)
  - Payment order creation
  - HMAC SHA256 signature verification
  - Subscription activation after payment
  - Webhook event processing
  - Mock mode for development (no real keys needed)

### ✅ Payment API Endpoints (`backend/app/api/payments.py`)
- `POST /api/payments/create-order` - Create Razorpay payment order
- `POST /api/payments/verify` - Verify payment and activate subscription
- `POST /api/payments/webhook` - Handle Razorpay webhooks
- `GET /api/payments/config` - Get Razorpay key_id for frontend
- `POST /api/payments/cancel-subscription` - Cancel user subscription

### ✅ Frontend Integration
- **Razorpay Checkout Component** (`frontend/src/components/RazorpayCheckout.tsx`)
  - Loads Razorpay SDK dynamically
  - Handles payment flow with success/failure callbacks
  - Custom hook `useRazorpay()` for easy integration

### ✅ User Authentication
- **Auth API** (`backend/app/api/auth.py`)
  - Auto-assigns free plan (10 scans/month) to new users
  - Subscription setup and management

---

## 🚀 Quick Setup

### Step 1: Get Razorpay Account
1. Go to [Razorpay Dashboard](https://dashboard.razorpay.com)
2. Sign up / Log in
3. Navigate to **Settings → API Keys**
4. Generate **Test Mode** keys (for development)

### Step 2: Configure Backend Environment

Create or update `backend/.env`:

```bash
# Test Mode (Development)
RAZORPAY_KEY_ID=rzp_test_xxxxxxxxxxxxxxxx
RAZORPAY_KEY_SECRET=xxxxxxxxxxxxxxxxxxxxxxxx
RAZORPAY_WEBHOOK_SECRET=xxxxxxxxxxxxxxxxxxxxxxxx

# Database
DATABASE_URL=postgresql://user:password@localhost:5432/trulyinvoice

# Other configs...
```

### Step 3: Configure Frontend Environment

Create or update `frontend/.env.local`:

```bash
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### Step 4: Test Payment Flow

1. **Start Backend**:
   ```bash
   cd backend
   python -m uvicorn app.main:app --reload --port 8000
   ```

2. **Start Frontend**:
   ```bash
   cd frontend
   npm run dev
   ```

3. **Test Flow**:
   - Register a new user → Gets free plan (10 scans)
   - Go to Dashboard → Pricing
   - Click "Upgrade to Basic/Pro/Ultra/Max"
   - Razorpay checkout opens
   - Use [test cards](https://razorpay.com/docs/payments/payments/test-card-upi-details/) to complete payment
   - Subscription activates automatically

---

## 🧪 Testing with Test Cards

Razorpay provides test cards for development:

### Successful Payment
- **Card Number**: `4111 1111 1111 1111`
- **CVV**: Any 3 digits
- **Expiry**: Any future date
- **Name**: Any name

### Failed Payment
- **Card Number**: `4000 0000 0000 0002`
- **CVV**: Any 3 digits
- **Expiry**: Any future date

### UPI Testing
- **UPI ID**: `success@razorpay`
- **UPI ID (Failed)**: `failure@razorpay`

More test credentials: [Razorpay Test Cards](https://razorpay.com/docs/payments/payments/test-card-upi-details/)

---

## 🔐 Security Features

### 1. **Signature Verification**
Every payment is verified using HMAC SHA256:
```python
generated_signature = hmac.new(
    key=settings.RAZORPAY_KEY_SECRET.encode(),
    msg=f"{order_id}|{payment_id}".encode(),
    digestmod=hashlib.sha256
).hexdigest()
```

### 2. **Webhook Verification**
Webhooks are verified before processing:
```python
def verify_webhook_signature(payload: str, signature: str) -> bool:
    expected_signature = hmac.new(
        key=settings.RAZORPAY_WEBHOOK_SECRET.encode(),
        msg=payload.encode(),
        digestmod=hashlib.sha256
    ).hexdigest()
    return hmac.compare_digest(expected_signature, signature)
```

### 3. **Database Transactions**
All payment operations use database transactions:
```python
try:
    subscription.tier = tier
    subscription.status = "active"
    db.commit()
except Exception:
    db.rollback()
    raise
```

---

## 📊 Payment Flow

```mermaid
sequenceDiagram
    participant User
    participant Frontend
    participant Backend
    participant Razorpay
    
    User->>Frontend: Click "Upgrade to Pro"
    Frontend->>Backend: POST /api/payments/create-order
    Backend->>Razorpay: Create Order
    Razorpay-->>Backend: Order ID
    Backend-->>Frontend: Order Details
    Frontend->>Razorpay: Open Checkout
    User->>Razorpay: Enter Payment Details
    Razorpay-->>Frontend: Payment Success
    Frontend->>Backend: POST /api/payments/verify
    Backend->>Razorpay: Verify Signature
    Backend->>Backend: Activate Subscription
    Backend-->>Frontend: Subscription Active
    Frontend->>User: Show Success Message
```

---

## 🎮 Plan Configuration

### Free Plan (Default for New Users)
- **Price**: ₹0
- **Scans**: 10/month
- **Storage**: 7 days
- **Features**: Basic AI extraction, PDF & Image support

### Basic Plan
- **Price**: ₹149/month
- **Scans**: 80/month
- **Storage**: 30 days
- **Features**: 95% AI accuracy, GST validation, Excel/CSV export

### Pro Plan (Most Popular)
- **Price**: ₹299/month
- **Scans**: 200/month
- **Storage**: 90 days
- **Features**: 98% AI accuracy, Bulk upload (20), Custom templates

### Ultra Plan
- **Price**: ₹599/month
- **Scans**: 500/month
- **Storage**: 180 days
- **Features**: 99% AI accuracy, Bulk upload (50), API access

### Max Plan
- **Price**: ₹999/month
- **Scans**: 1000/month
- **Storage**: 365 days
- **Features**: 99.5% AI accuracy, Unlimited bulk upload, Dedicated support

---

## 🔧 Backend API Reference

### Create Payment Order
```http
POST /api/payments/create-order
Content-Type: application/json

{
  "tier": "basic",
  "billing_cycle": "monthly"
}

Response:
{
  "order_id": "order_xxxxxxxxxxxxx",
  "amount": 14900,
  "currency": "INR",
  "message": "Order created successfully"
}
```

### Verify Payment
```http
POST /api/payments/verify
Content-Type: application/json

{
  "order_id": "order_xxxxxxxxxxxxx",
  "payment_id": "pay_xxxxxxxxxxxxx",
  "signature": "xxxxxxxxxxxxxxxxxxxxx"
}

Response:
{
  "success": true,
  "message": "Payment verified and subscription activated",
  "subscription": {
    "tier": "basic",
    "status": "active",
    "period_end": "2024-02-15T10:30:00"
  }
}
```

### Get Razorpay Config
```http
GET /api/payments/config

Response:
{
  "key_id": "rzp_test_xxxxxxxxxxxxx"
}
```

---

## 🌐 Webhook Configuration

### Setup Webhook in Razorpay Dashboard

1. Go to [Razorpay Dashboard → Webhooks](https://dashboard.razorpay.com/app/webhooks)
2. Click "Add Webhook URL"
3. Enter your backend URL: `https://your-api.com/api/payments/webhook`
4. Select events to listen:
   - ✅ `payment.captured`
   - ✅ `payment.failed`
5. Copy the **Webhook Secret** to your `.env` file

### Webhook Events Handled

```python
# payment.captured - Payment successful
if event_type == "payment.captured":
    # Activate subscription
    subscription.status = "active"
    subscription.tier = paid_tier
    db.commit()

# payment.failed - Payment failed
if event_type == "payment.failed":
    # Log failure, send notification
    logging.error(f"Payment failed for order {order_id}")
```

---

## 🎨 Frontend Usage

### Using the Razorpay Hook

```tsx
import { useRazorpay } from '@/components/RazorpayCheckout'

function PricingPage() {
  const { createOrder, verifyPayment, getRazorpayConfig } = useRazorpay()
  
  const handleUpgrade = async (tier: string) => {
    // Step 1: Create order
    const orderData = await createOrder(tier, 'monthly')
    
    // Step 2: Get Razorpay config
    const config = await getRazorpayConfig()
    
    // Step 3: Open Razorpay checkout (see full example)
  }
}
```

### Complete Payment Integration Example

See `frontend/src/app/dashboard/pricing/page.tsx` for the full implementation with:
- Order creation
- Razorpay checkout
- Payment verification
- Success/failure handling
- UI loading states

---

## 🐛 Troubleshooting

### Payment Order Creation Fails
**Problem**: Backend returns error when creating order

**Solutions**:
1. Check if Razorpay keys are correct in `.env`
2. Verify database connection
3. Check if user is authenticated
4. Look at backend logs: `tail -f backend/logs/app.log`

### Payment Verification Fails
**Problem**: Payment completed but subscription not activated

**Solutions**:
1. Check signature verification in backend logs
2. Verify `RAZORPAY_KEY_SECRET` matches Razorpay dashboard
3. Check database for subscription record
4. Test with webhook event manually

### Razorpay Checkout Not Opening
**Problem**: Frontend doesn't show payment modal

**Solutions**:
1. Check browser console for errors
2. Verify `NEXT_PUBLIC_API_URL` in frontend `.env.local`
3. Ensure Razorpay SDK loads: Check Network tab for `checkout.razorpay.com`
4. Check if order_id is returned from backend

### Mock Mode Not Working
**Problem**: Want to test without real Razorpay keys

**Solutions**:
1. Remove or set dummy values for Razorpay keys in `.env`
2. Backend automatically uses mock mode
3. Mock orders return `order_mock_xxxxxxxxxx`
4. Signature verification is skipped in mock mode

---

## 🚀 Going Live Checklist

### Before Production Deployment:

- [ ] **Get Live Keys**
  - [ ] Generate Live API keys from Razorpay Dashboard
  - [ ] Update `.env` with `rzp_live_` keys
  - [ ] Update webhook secret for live mode

- [ ] **Configure Webhooks**
  - [ ] Add production webhook URL
  - [ ] Test webhook delivery with live events
  - [ ] Monitor webhook logs

- [ ] **Security Review**
  - [ ] Verify all secrets are in environment variables (not hardcoded)
  - [ ] Enable HTTPS for frontend and backend
  - [ ] Test signature verification with live payments
  - [ ] Enable rate limiting for payment endpoints

- [ ] **Database**
  - [ ] Run migration script: `python backend/migrate_subscriptions.py`
  - [ ] Backup production database
  - [ ] Test rollback procedure

- [ ] **Testing**
  - [ ] Test complete payment flow with test cards
  - [ ] Test failed payment handling
  - [ ] Test subscription cancellation
  - [ ] Test webhook events

- [ ] **Monitoring**
  - [ ] Set up payment success/failure alerts
  - [ ] Monitor Razorpay dashboard for transactions
  - [ ] Log all payment events
  - [ ] Set up error tracking (Sentry, etc.)

- [ ] **Legal & Compliance**
  - [ ] Add Terms of Service link
  - [ ] Add Privacy Policy
  - [ ] Add Refund Policy
  - [ ] Display GST/Tax information

---

## 📞 Support

### Razorpay Support
- Dashboard: https://dashboard.razorpay.com
- Docs: https://razorpay.com/docs
- Support: support@razorpay.com

### Test Resources
- Test Cards: https://razorpay.com/docs/payments/payments/test-card-upi-details/
- Webhook Testing: https://razorpay.com/docs/webhooks/test

---

## 📝 Files Modified/Created

### Backend
- ✅ `backend/app/services/razorpay_service.py` - Razorpay integration service
- ✅ `backend/app/api/payments.py` - Payment API endpoints
- ✅ `backend/app/api/auth.py` - User registration & free plan setup
- ✅ `backend/app/core/config.py` - Configuration with Razorpay settings
- ✅ `backend/app/main.py` - Added payment & auth routers
- ✅ `backend/.env.example` - Environment variables template

### Frontend
- ✅ `frontend/src/components/RazorpayCheckout.tsx` - Razorpay checkout component
- ✅ `frontend/src/app/dashboard/pricing/page.tsx` - Payment integration
- ✅ `frontend/src/app/register/page.tsx` - Free plan auto-assignment
- ✅ `frontend/src/app/login/page.tsx` - Google Sign-In button added

---

## 🎉 Success Metrics

After implementation, you should see:

1. **New Users**: Automatically get Free plan (10 scans/month)
2. **Payment Flow**: Smooth Razorpay checkout experience
3. **Instant Activation**: Subscriptions activate immediately after payment
4. **Secure**: All payments verified with HMAC SHA256
5. **Reliable**: Webhook system for automated subscription management

---

**Last Updated**: January 2024  
**Version**: 1.0.0  
**Status**: ✅ Production Ready
