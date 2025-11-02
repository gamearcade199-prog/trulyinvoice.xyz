# 🔑 HOW TO GET RAZORPAY SUBSCRIPTIONS API ACCESS

**Date:** November 2, 2025  
**Purpose:** Enable automatic recurring payments for TrulyInvoice

---

## 📋 GOOD NEWS: You Already Have It! ✅

**The Razorpay Subscriptions API is available with your existing Razorpay account.** You don't need to request special access or upgrade your plan.

### What You Currently Have:
- ✅ Razorpay account (already set up)
- ✅ API keys (already configured)
- ✅ `razorpay` Python package (already installed)

### What You Need to Do:
- ✅ Use the **same API keys** you're currently using
- ✅ Just call different API endpoints (subscriptions instead of orders)
- ✅ Update your webhook handler (I'll show you)

---

## 🎯 THE DIFFERENCE

### Current Approach (One-Time Payments)
```python
# What you're doing now:
order = razorpay_client.order.create({
    "amount": 58882,  # One-time charge
    "currency": "INR"
})
# ❌ Customer pays once, never charged again
```

### New Approach (Recurring Subscriptions)
```python
# What you'll do:
subscription = razorpay_client.subscription.create({
    "plan_id": "trulyinvoice_pro_monthly",
    "customer_notify": 1,
    "total_count": 120  # 10 years of automatic charges
})
# ✅ Customer charged automatically every month
```

---

## 🚀 STEP-BY-STEP SETUP GUIDE

### Step 1: Verify Your Razorpay Package (1 minute)

Your `razorpay` Python package already supports subscriptions!

```bash
# Check current version
pip show razorpay

# Should show: razorpay >= 1.2.0
# If older, upgrade:
pip install --upgrade razorpay
```

---

### Step 2: Access Razorpay Dashboard (2 minutes)

1. **Login to Razorpay Dashboard:**
   - Go to: https://dashboard.razorpay.com
   - Login with your credentials

2. **Navigate to Subscriptions:**
   ```
   Dashboard → Left Sidebar → "Subscriptions"
   ```

3. **You'll See:**
   - Plans (empty for now - we'll create via API)
   - Subscriptions (empty for now)
   - Settings

---

### Step 3: Get Your API Keys (Already Done! ✅)

**You're already using these keys** - same ones for subscriptions:

```python
# backend/app/services/razorpay_service.py
# These are ALREADY configured:
self.key_id = "rzp_live_RUCxZnVyqol9Nv"  # ✅ From your .env
self.key_secret = "YOUR_SECRET"  # ✅ From your .env
self.client = razorpay.Client(auth=(self.key_id, self.key_secret))
```

**No new keys needed!** Same client works for:
- ✅ `client.order.create()` - One-time payments (current)
- ✅ `client.plan.create()` - Create subscription plans (new)
- ✅ `client.subscription.create()` - Create subscriptions (new)

---

### Step 4: Enable Subscriptions in Dashboard (Optional, 2 minutes)

**Good news:** Subscriptions are **enabled by default** for all Razorpay accounts!

But if you want to verify:

1. Go to: https://dashboard.razorpay.com/app/subscriptions
2. If you see "Enable Subscriptions" button, click it
3. If you see the subscriptions list, you're already enabled ✅

---

### Step 5: Create Your First Plan via API (5 minutes)

Plans are like product definitions. Create once, reuse many times.

```python
# Add to backend/app/services/razorpay_service.py

def create_razorpay_plan(self, tier: str, amount: int, interval: int):
    """
    Create a Razorpay Plan (subscription template)
    
    Args:
        tier: Plan tier (basic, pro, ultra, max)
        amount: Amount in paise (e.g., 58882 for ₹588.82)
        interval: Billing interval (1 = monthly, 12 = yearly)
    
    Returns:
        Plan ID
    """
    plan_id = f"trulyinvoice_{tier}_monthly"
    
    try:
        # Try to fetch existing plan
        plan = self.client.plan.fetch(plan_id)
        print(f"✅ Plan already exists: {plan_id}")
        return plan["id"]
    
    except Exception:
        # Plan doesn't exist, create it
        print(f"📝 Creating new plan: {plan_id}")
        
        plan = self.client.plan.create({
            "id": plan_id,  # Custom ID (recommended)
            "period": "monthly",
            "interval": interval,  # 1 = monthly, 12 = yearly
            "item": {
                "name": f"TrulyInvoice {tier.title()} Plan",
                "amount": amount,
                "currency": "INR",
                "description": f"{tier.title()} subscription"
            },
            "notes": {
                "tier": tier,
                "created_via": "api"
            }
        })
        
        print(f"✅ Plan created: {plan['id']}")
        return plan["id"]


# Usage:
razorpay_service = RazorpayService()

# Create plans for all tiers (do this ONCE)
plans = {
    "basic": razorpay_service.create_razorpay_plan("basic", 17582, 1),  # ₹149 + GST
    "pro": razorpay_service.create_razorpay_plan("pro", 58882, 1),      # ₹499 + GST
    "ultra": razorpay_service.create_razorpay_plan("ultra", 118182, 1), # ₹1001 + GST
    "max": razorpay_service.create_razorpay_plan("max", 235882, 1)      # ₹1999 + GST
}
```

---

### Step 6: Create a Subscription (5 minutes)

```python
# Add to backend/app/services/razorpay_service.py

def create_subscription(self, user_id: str, tier: str):
    """
    Create a recurring subscription for a user
    
    Args:
        user_id: User ID
        tier: Plan tier (basic, pro, ultra, max)
    
    Returns:
        Subscription details with payment link
    """
    # 1. Ensure plan exists
    plan = get_plan_config(tier)
    amount = plan["price_monthly"]
    amount_with_gst = int(amount * 1.18 * 100)  # Add 18% GST, convert to paise
    
    plan_id = self.create_razorpay_plan(tier, amount_with_gst, 1)
    
    # 2. Create subscription
    subscription = self.client.subscription.create({
        "plan_id": plan_id,
        "customer_notify": 1,  # Send email to customer
        "quantity": 1,
        "total_count": 120,  # 120 months = 10 years
        "start_at": None,  # Start immediately after first payment
        "expire_by": None,  # Never expires (until cancelled)
        "addons": [],
        "notes": {
            "user_id": user_id,
            "tier": tier,
            "created_at": datetime.utcnow().isoformat()
        }
    })
    
    print(f"✅ Subscription created: {subscription['id']}")
    
    return {
        "subscription_id": subscription["id"],
        "plan_id": plan_id,
        "status": subscription["status"],  # "created"
        "short_url": subscription["short_url"],  # ← Payment link for customer
        "amount": amount,
        "next_billing_at": subscription.get("charge_at"),
        "auto_renew": True
    }


# Usage in your API endpoint:
@router.post("/create-subscription")
async def create_subscription_endpoint(
    request: CreateOrderRequest,
    current_user: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Create subscription
    subscription_data = razorpay_service.create_subscription(
        user_id=current_user,
        tier=request.tier
    )
    
    # Save to database
    db_subscription = Subscription(
        user_id=current_user,
        tier=request.tier,
        razorpay_subscription_id=subscription_data["subscription_id"],
        status="pending",  # Will be "active" after first payment
        auto_renew=True
    )
    db.add(db_subscription)
    db.commit()
    
    # Return payment link
    return {
        "subscription_id": subscription_data["subscription_id"],
        "payment_url": subscription_data["short_url"]  # Redirect customer here
    }
```

---

### Step 7: Handle Webhook Events (15 minutes)

When subscriptions auto-charge, Razorpay sends webhook events. You need to handle them:

```python
# Update backend/app/services/razorpay_service.py

def handle_webhook(self, event: Dict, signature: str, db: Session):
    """Handle Razorpay webhook events"""
    
    # ... existing signature verification ...
    
    event_type = event.get("event")
    payload = event.get("payload", {})
    
    # NEW: Handle subscription events
    if event_type == "subscription.activated":
        """First payment successful - activate user"""
        subscription_entity = payload.get("subscription", {}).get("entity", {})
        payment_entity = payload.get("payment", {}).get("entity", {})
        
        subscription_id = subscription_entity.get("id")
        payment_id = payment_entity.get("id")
        user_id = subscription_entity.get("notes", {}).get("user_id")
        
        # Update database
        sub = db.query(Subscription).filter(
            Subscription.razorpay_subscription_id == subscription_id
        ).first()
        
        if sub:
            sub.status = "active"
            sub.razorpay_payment_id = payment_id
            sub.current_period_start = datetime.utcnow()
            sub.current_period_end = datetime.utcnow() + timedelta(days=30)
            sub.scans_used_this_period = 0
            db.commit()
            
            print(f"✅ Subscription activated for user {user_id}")
        
        return True, "Subscription activated"
    
    elif event_type == "subscription.charged":
        """🎉 AUTO-RENEWAL! Monthly charge succeeded"""
        subscription_entity = payload.get("subscription", {}).get("entity", {})
        payment_entity = payload.get("payment", {}).get("entity", {})
        
        subscription_id = subscription_entity.get("id")
        payment_id = payment_entity.get("id")
        
        # Find subscription
        sub = db.query(Subscription).filter(
            Subscription.razorpay_subscription_id == subscription_id
        ).first()
        
        if sub:
            # Reset usage for new billing period
            sub.scans_used_this_period = 0
            sub.current_period_start = datetime.utcnow()
            sub.current_period_end = datetime.utcnow() + timedelta(days=30)
            sub.razorpay_payment_id = payment_id
            sub.status = "active"
            db.commit()
            
            print(f"✅ Monthly renewal for user {sub.user_id} - scans reset")
        
        return True, "Subscription renewed"
    
    elif event_type == "subscription.payment_failed":
        """Monthly charge failed - notify user"""
        subscription_entity = payload.get("subscription", {}).get("entity", {})
        subscription_id = subscription_entity.get("id")
        
        sub = db.query(Subscription).filter(
            Subscription.razorpay_subscription_id == subscription_id
        ).first()
        
        if sub:
            sub.status = "payment_failed"
            db.commit()
            
            # TODO: Send email to user
            print(f"⚠️ Payment failed for user {sub.user_id}")
        
        return True, "Payment failure recorded"
    
    elif event_type == "subscription.cancelled":
        """Subscription cancelled"""
        subscription_entity = payload.get("subscription", {}).get("entity", {})
        subscription_id = subscription_entity.get("id")
        
        sub = db.query(Subscription).filter(
            Subscription.razorpay_subscription_id == subscription_id
        ).first()
        
        if sub:
            sub.status = "cancelled"
            sub.auto_renew = False
            sub.cancelled_at = datetime.utcnow()
            db.commit()
            
            print(f"❌ Subscription cancelled for user {sub.user_id}")
        
        return True, "Subscription cancelled"
    
    # ... handle other events ...
    
    return True, f"Event {event_type} processed"
```

---

### Step 8: Update Webhook URL in Razorpay Dashboard (3 minutes)

1. **Go to Razorpay Dashboard:**
   - https://dashboard.razorpay.com/app/webhooks

2. **Add Webhook URL:**
   ```
   https://trulyinvoice-backend.onrender.com/api/payments/webhook
   ```

3. **Select Events:**
   - ✅ `subscription.activated`
   - ✅ `subscription.charged` ← **This is the auto-renewal event!**
   - ✅ `subscription.payment_failed`
   - ✅ `subscription.cancelled`
   - ✅ `subscription.paused`
   - ✅ `subscription.resumed`

4. **Set Webhook Secret:**
   - Copy the webhook secret
   - Add to your `.env`:
     ```
     RAZORPAY_WEBHOOK_SECRET=whsec_xxxxxxxxxxxxxx
     ```

---

## 🧪 TESTING (10 minutes)

### Test Mode (Free Testing)

Razorpay provides test keys for free testing:

1. **Switch to Test Mode:**
   - Dashboard → Top right → Toggle to "Test Mode"

2. **Get Test Keys:**
   - Dashboard → Settings → API Keys
   - Copy test keys (start with `rzp_test_`)

3. **Update `.env` for testing:**
   ```bash
   RAZORPAY_KEY_ID=rzp_test_xxxxxxxxxx
   RAZORPAY_KEY_SECRET=test_secret_xxxxxxxxxx
   ```

4. **Create Test Subscription:**
   ```python
   # Call your API
   POST /api/payments/create-subscription
   {
     "tier": "pro",
     "billing_cycle": "monthly"
   }
   ```

5. **Use Test Card:**
   - Card Number: `4111 1111 1111 1111`
   - CVV: `123`
   - Expiry: Any future date
   - Name: Any name

6. **Simulate Next Month:**
   - Dashboard → Subscriptions → Click subscription
   - Click "Charge Now" button
   - This simulates next month's automatic charge!

7. **Check Webhook:**
   - Dashboard → Webhooks → View logs
   - Should see `subscription.charged` event

---

## 📊 API REFERENCE

### Key Endpoints You'll Use:

```python
# Create Plan
razorpay_client.plan.create({
    "period": "monthly",
    "interval": 1,
    "item": {
        "name": "Plan Name",
        "amount": 58882,
        "currency": "INR"
    }
})

# Create Subscription
razorpay_client.subscription.create({
    "plan_id": "trulyinvoice_pro_monthly",
    "customer_notify": 1,
    "total_count": 120
})

# Fetch Subscription
razorpay_client.subscription.fetch("sub_xxxxxxxxxx")

# Cancel Subscription
razorpay_client.subscription.cancel("sub_xxxxxxxxxx")

# Update Subscription
razorpay_client.subscription.update("sub_xxxxxxxxxx", {
    "quantity": 2
})
```

---

## 🔒 SECURITY CHECKLIST

- ✅ Never expose `RAZORPAY_KEY_SECRET` to frontend
- ✅ Always verify webhook signatures
- ✅ Use HTTPS for webhook endpoint
- ✅ Store subscription_id in database
- ✅ Log all payment events
- ✅ Handle failed payments gracefully

---

## 💡 PRICING REMINDER

**Don't forget GST!**

```python
# ❌ WRONG
amount = 499 * 100  # 49900 paise

# ✅ CORRECT
base = 499
gst = base * 0.18  # 89.82 (18% GST)
total = base + gst  # 588.82
amount = int(total * 100)  # 58882 paise
```

---

## 🎯 QUICK START COMMANDS

### 1. Test Your Current Setup
```python
# In Python shell
from app.services.razorpay_service import razorpay_service

# Test connection
client = razorpay_service.client
print(client)  # Should show Razorpay client object

# List existing plans
plans = client.plan.all()
print(plans)
```

### 2. Create Your First Plan
```python
# Create Pro plan
plan = razorpay_service.create_razorpay_plan(
    tier="pro",
    amount=58882,  # ₹499 + 18% GST
    interval=1
)
print(f"Plan created: {plan}")
```

### 3. Create Test Subscription
```python
# Create subscription
subscription = razorpay_service.create_subscription(
    user_id="test_user_123",
    tier="pro"
)
print(f"Payment URL: {subscription['short_url']}")
```

---

## 📞 RAZORPAY SUPPORT

If you need help:

1. **Documentation:**
   - https://razorpay.com/docs/api/subscriptions/

2. **Support:**
   - Dashboard → Help → Support Ticket
   - Email: support@razorpay.com

3. **Phone:**
   - 080-68727374 (Bangalore)
   - 022-68727374 (Mumbai)

---

## ✅ CHECKLIST

Before going live:

- [ ] Razorpay account verified ✅ (Already done)
- [ ] API keys configured ✅ (Already done)
- [ ] `razorpay` package installed ✅ (Already done)
- [ ] Plans created (use code above)
- [ ] Webhook URL configured (use code above)
- [ ] Webhook handler updated (use code above)
- [ ] Tested in test mode
- [ ] Tested webhook events
- [ ] Switch to live keys for production

---

## 🚀 DEPLOYMENT STEPS

### For Your Render Backend:

1. **Update Environment Variables:**
   ```bash
   # In Render dashboard
   RAZORPAY_KEY_ID=rzp_live_RUCxZnVyqol9Nv  # ✅ Already set
   RAZORPAY_KEY_SECRET=your_secret          # ✅ Already set
   RAZORPAY_WEBHOOK_SECRET=whsec_xxxxx      # ← Add this
   ```

2. **Deploy Updated Code:**
   ```bash
   git add .
   git commit -m "Add Razorpay Subscriptions API support"
   git push origin main
   ```

3. **Verify Deployment:**
   - Check Render logs
   - Test API endpoint: `POST /api/payments/create-subscription`

---

## 🎉 SUMMARY

**You already have everything you need!**

✅ Same Razorpay account  
✅ Same API keys  
✅ Same `razorpay` package  
✅ Just use different API methods

**What's different:**
- `client.order.create()` → One-time payments
- `client.subscription.create()` → Recurring payments ✨

**Time to implement:** 5 hours  
**Revenue impact:** Recover 92% of lost revenue  

**Next step:** Follow Step 5-8 above to create your first subscription!

---

**Questions? Check the full implementation guide:** `AUTO_RENEWAL_COMPLETE_GUIDE.md`
