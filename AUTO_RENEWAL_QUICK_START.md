# ⚡ AUTO-RENEWAL QUICK START

## 🎯 THE PROBLEM

**Current System:**
```python
# ❌ What you have now:
def check_and_renew_subscription():
    if period_expired:
        subscription.scans_used = 0  # ✅ Resets usage
        subscription.period_end = now + 30 days  # ✅ Extends period
        # ❌ BUT DOESN'T CHARGE THE CUSTOMER!
```

**Result:** Users get free service after first month! 💸

---

## ✅ THE SOLUTION

Use **Razorpay Subscriptions API** - Let Razorpay charge customers automatically every month.

---

## 🚀 5-STEP IMPLEMENTATION (5 Hours Total)

### Step 1: Add Subscription Creation (2 hours)

```python
# backend/app/services/razorpay_service.py

def create_recurring_subscription(self, user_id, tier, billing_cycle, db):
    """Create auto-renewing subscription"""
    
    # 1. Get plan details
    plan = get_plan_config(tier)
    amount = plan["price_monthly"] * 100  # Convert to paise
    
    # 2. Create Razorpay Plan (do once per tier)
    plan_id = f"trulyinvoice_{tier}_monthly"
    try:
        razorpay_plan = self.client.plan.fetch(plan_id)
    except:
        razorpay_plan = self.client.plan.create({
            "id": plan_id,
            "period": "monthly",
            "interval": 1,
            "item": {
                "name": f"{plan['name']} Plan",
                "amount": amount,
                "currency": "INR"
            }
        })
    
    # 3. Create Subscription
    subscription = self.client.subscription.create({
        "plan_id": plan_id,
        "customer_notify": 1,
        "total_count": 120,  # 10 years
        "notes": {
            "user_id": user_id,
            "tier": tier
        }
    })
    
    return {
        "subscription_id": subscription["id"],
        "short_url": subscription["short_url"]  # ← Redirect customer here
    }
```

---

### Step 2: Handle Webhooks (1 hour)

```python
# backend/app/services/razorpay_service.py

def handle_webhook(self, event, signature, db):
    # ... existing signature verification ...
    
    event_type = event.get("event")
    
    # NEW: Handle subscription events
    if event_type == "subscription.charged":
        # 🎉 AUTOMATIC MONTHLY CHARGE!
        subscription_id = event["payload"]["subscription"]["entity"]["id"]
        payment_id = event["payload"]["payment"]["entity"]["id"]
        
        # Find subscription in DB
        sub = db.query(Subscription).filter(
            Subscription.razorpay_subscription_id == subscription_id
        ).first()
        
        # Reset usage for new month
        sub.scans_used_this_period = 0
        sub.current_period_start = datetime.utcnow()
        sub.current_period_end = datetime.utcnow() + timedelta(days=30)
        sub.razorpay_payment_id = payment_id
        
        db.commit()
        
        return True, "Renewal successful"
```

---

### Step 3: Add API Endpoint (30 min)

```python
# backend/app/api/payments.py

@router.post("/create-subscription")
async def create_subscription(
    request: CreateOrderRequest,
    current_user: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create auto-renewing subscription"""
    
    subscription_data = razorpay_service.create_recurring_subscription(
        user_id=current_user,
        tier=request.tier,
        billing_cycle=request.billing_cycle,
        db=db
    )
    
    return {
        "subscription_id": subscription_data["subscription_id"],
        "short_url": subscription_data["short_url"]  # Redirect here
    }
```

---

### Step 4: Update Frontend (1 hour)

```typescript
// frontend/src/components/RazorpayCheckout.tsx

export function useRazorpay() {
  const createSubscription = async (tier: string) => {
    const response = await fetch('/api/payments/create-subscription', {
      method: 'POST',
      body: JSON.stringify({ tier, billing_cycle: 'monthly' })
    })
    
    const data = await response.json()
    
    // Redirect to Razorpay hosted page
    window.location.href = data.short_url
  }
  
  return { createSubscription }
}
```

---

### Step 5: Test (30 min)

1. Create test subscription
2. Complete first payment
3. Check webhook receives `subscription.activated`
4. Simulate next month (Razorpay allows date override in test mode)
5. Verify webhook receives `subscription.charged`
6. Check database - scans reset to 0

---

## 📊 HOW IT WORKS

```
┌─────────────────────────────────────────────────────────┐
│                    AUTO-RENEWAL FLOW                     │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  Day 1: User subscribes                                 │
│  ├─ You: Create Razorpay subscription                  │
│  ├─ User: Pays ₹588.82 (₹499 + ₹89.82 GST)            │
│  └─ Webhook: subscription.activated → Activate user    │
│                                                          │
│  Day 30: First renewal (AUTOMATIC)                      │
│  ├─ Razorpay: Charges card ₹588.82                     │
│  ├─ Webhook: subscription.charged → Reset scans        │
│  └─ User: Gets email receipt                           │
│                                                          │
│  Day 60: Second renewal (AUTOMATIC)                     │
│  ├─ Razorpay: Charges card ₹588.82                     │
│  ├─ Webhook: subscription.charged → Reset scans        │
│  └─ User: Gets email receipt                           │
│                                                          │
│  ... Repeats every 30 days automatically ...            │
│                                                          │
│  If payment fails:                                       │
│  ├─ Razorpay: Auto-retries 3 times                     │
│  ├─ Webhook: subscription.payment_failed               │
│  ├─ You: Send email to user                            │
│  └─ Razorpay: Cancels after 3 failures                 │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

---

## ✅ WHAT RAZORPAY HANDLES FOR YOU

- ✅ Stores card details securely (PCI compliant)
- ✅ Charges automatically every month
- ✅ Retries failed payments (3 attempts)
- ✅ Sends receipts to customers
- ✅ Handles 3D Secure / OTP
- ✅ Provides customer dashboard
- ✅ Manages refunds

---

## ❌ WHAT YOU DON'T NEED

- ❌ Cron jobs to check expired subscriptions
- ❌ Storing card tokens
- ❌ Manual charging logic
- ❌ Retry mechanism for failed payments
- ❌ PCI compliance certification

---

## 🎯 KEY WEBHOOK EVENTS

| Event | When | What To Do |
|-------|------|------------|
| `subscription.activated` | First payment succeeds | Activate user's plan |
| `subscription.charged` | Monthly auto-renewal | Reset scans to 0 |
| `subscription.payment_failed` | Charge fails | Email user |
| `subscription.cancelled` | User cancels or 3 failures | Downgrade to free |

---

## 💡 MIGRATION STRATEGY

**For Existing One-Time Customers:**

```python
# Option 1: Keep one-time payments for existing users
# Only use subscriptions for new signups

# Option 2: Migrate existing customers
def migrate_to_subscription(user_id):
    """Convert one-time payment to subscription"""
    
    # 1. Get user's current tier
    user = db.query(Subscription).filter(user_id=user_id).first()
    
    # 2. Create subscription starting next billing date
    subscription = razorpay_service.create_recurring_subscription(
        user_id=user_id,
        tier=user.tier,
        start_at=user.current_period_end  # Start when current period ends
    )
    
    # 3. Update database
    user.razorpay_subscription_id = subscription["subscription_id"]
    db.commit()
```

---

## 🚨 IMPORTANT: PRICING

Don't forget to include GST!

```python
# ❌ WRONG
amount = 499  # You lose ₹89.82

# ✅ CORRECT
base = 499
gst = base * 0.18  # ₹89.82 (18% GST)
total = base + gst  # ₹588.82
amount_paise = int(total * 100)  # 58882 paise
```

---

## 📞 COMPARISON

| Feature | Current System | With Auto-Renewal |
|---------|----------------|-------------------|
| Month 1 | ✅ User pays ₹588 | ✅ User pays ₹588 |
| Month 2 | ❌ FREE (no charge!) | ✅ Auto-charge ₹588 |
| Month 3 | ❌ FREE | ✅ Auto-charge ₹588 |
| Your Revenue | ₹588 (1 month) | ₹7,056 (12 months) |
| **Revenue Loss** | **₹6,468/year** 💸 | **₹0** ✅ |

**Without auto-renewal:** You lose 92% of potential revenue!

---

## 🎯 BOTTOM LINE

**Current Problem:** Users pay once, get lifetime free service  
**Solution:** Razorpay Subscriptions API (5 hours to implement)  
**Result:** Automatic monthly charges, no cron jobs needed  
**Revenue Impact:** Recover 92% of lost revenue  

**Next Step:** Implement Step 1-5 above

---

**Full guide:** See `AUTO_RENEWAL_COMPLETE_GUIDE.md`  
**Date:** November 2, 2025  
**Status:** Ready to implement 🚀
