# 🔄 AUTO-RENEWAL SYSTEM - COMPLETE IMPLEMENTATION GUIDE

**Date:** November 2, 2025  
**System:** TrulyInvoice Subscription Auto-Renewal  
**Status:** Currently ⚠️ MANUAL - Need to Implement Automatic Charging

---

## 📊 CURRENT SITUATION

### What You Have ✅
```python
# backend/app/middleware/subscription.py
async def check_and_renew_subscription(user_id: str):
    """
    ✅ Resets scan count when period expires
    ✅ Checks auto_renew flag
    ⚠️ BUT DOESN'T CHARGE THE CUSTOMER!
    """
    if period_end < now:
        if subscription.get("auto_renew", False):
            # ✅ Resets scans to 0
            # ✅ Extends period by 30 days
            # ❌ DOESN'T CHARGE PAYMENT! ← Problem!
```

### What's Missing ❌
1. **No automatic payment charging** - Only resets usage, doesn't collect money
2. **No webhook handling for recurring payments** - Razorpay sends events, but you don't process them
3. **No scheduled job** - Need cron job to check expired subscriptions daily
4. **No failed payment handling** - If card fails, user keeps access (free service!)

---

## 🎯 TWO APPROACHES TO AUTO-RENEWAL

### Approach 1: Razorpay Subscriptions API (RECOMMENDED) ⭐
**How it works:** Razorpay automatically charges customers every month

**Pros:**
- ✅ Razorpay handles charging automatically
- ✅ Built-in retry logic for failed payments
- ✅ Customer can manage via Razorpay dashboard
- ✅ PCI compliant (Razorpay stores card details)

**Cons:**
- ⚠️ Requires different API (Subscriptions instead of Orders)
- ⚠️ Migration needed for existing customers

---

### Approach 2: Manual Charging + Cron Job (CURRENT PATH)
**How it works:** You store payment method and charge it monthly via cron job

**Pros:**
- ✅ Full control over billing logic
- ✅ Can implement custom proration
- ✅ Works with current Order API

**Cons:**
- ⚠️ You must handle PCI compliance (storing card tokens)
- ⚠️ You handle failed payments manually
- ⚠️ Need infrastructure for cron jobs

---

## 🚀 RECOMMENDED SOLUTION: Razorpay Subscriptions API

Let me show you how to implement proper auto-renewal with Razorpay Subscriptions:

---

## 📝 IMPLEMENTATION STEPS

### Step 1: Update Razorpay Service (Add Subscription Creation)

```python
# backend/app/services/razorpay_service.py

class RazorpayService:
    """Enhanced with Razorpay Subscriptions API"""
    
    def create_recurring_subscription(
        self,
        user_id: str,
        tier: str,
        billing_cycle: str,
        user_email: str,
        user_name: str,
        db: Session
    ) -> Dict:
        """
        Create Razorpay recurring subscription (auto-renewal enabled)
        
        This uses Razorpay Subscriptions API instead of one-time Orders.
        Customer is charged automatically every month.
        
        Args:
            user_id: User ID
            tier: Plan tier (basic, pro, ultra, max)
            billing_cycle: monthly or yearly
            user_email: User email
            user_name: User name
            db: Database session
        
        Returns:
            Subscription details including subscription ID
        """
        # Get plan configuration
        plan = get_plan_config(tier)
        
        # Calculate amount based on billing cycle
        if billing_cycle == "yearly":
            amount = plan["price_yearly"]
            interval = 12  # 12 months
        else:
            amount = plan["price_monthly"]
            interval = 1  # 1 month
        
        # Convert to paise
        amount_paise = amount * 100
        
        # Step 1: Create Razorpay Plan (if not exists)
        plan_id = self._get_or_create_razorpay_plan(
            tier=tier,
            amount=amount_paise,
            interval=interval,
            billing_cycle=billing_cycle
        )
        
        # Step 2: Create Razorpay Subscription
        try:
            subscription = self.client.subscription.create({
                "plan_id": plan_id,
                "customer_notify": 1,  # Send email to customer
                "quantity": 1,
                "total_count": 12 if billing_cycle == "yearly" else 120,  # 10 years max
                "start_at": int((datetime.utcnow() + timedelta(days=30)).timestamp()),  # Start in 30 days
                "notes": {
                    "user_id": user_id,
                    "tier": tier,
                    "user_email": user_email,
                    "user_name": user_name
                },
                "addons": []
            })
            
            print(f"✅ Razorpay subscription created: {subscription['id']}")
            
            return {
                "subscription_id": subscription["id"],
                "plan_id": plan_id,
                "status": subscription["status"],  # "created"
                "short_url": subscription["short_url"],  # Payment link
                "amount": amount,
                "interval": interval,
                "next_billing": subscription.get("start_at")
            }
            
        except Exception as e:
            print(f"❌ Failed to create subscription: {str(e)}")
            raise Exception(f"Subscription creation failed: {str(e)}")
    
    def _get_or_create_razorpay_plan(
        self,
        tier: str,
        amount: int,
        interval: int,
        billing_cycle: str
    ) -> str:
        """
        Get or create Razorpay Plan (product definition)
        
        Razorpay Plans are like product SKUs - create once, reuse many times.
        
        Args:
            tier: Plan tier (basic, pro, etc.)
            amount: Amount in paise
            interval: Billing interval (1 for monthly, 12 for yearly)
            billing_cycle: "monthly" or "yearly"
        
        Returns:
            Razorpay plan_id
        """
        # Plan ID convention: trulyinvoice_basic_monthly
        plan_id = f"trulyinvoice_{tier}_{billing_cycle}"
        
        try:
            # Try to fetch existing plan
            existing_plan = self.client.plan.fetch(plan_id)
            print(f"✅ Using existing Razorpay plan: {plan_id}")
            return existing_plan["id"]
        
        except Exception:
            # Plan doesn't exist, create it
            print(f"📝 Creating new Razorpay plan: {plan_id}")
            
            plan_config = get_plan_config(tier)
            
            new_plan = self.client.plan.create({
                "id": plan_id,  # Custom ID
                "period": "monthly",  # Always monthly (even for yearly, we use interval)
                "interval": interval,  # 1 = monthly, 12 = yearly
                "item": {
                    "name": f"{plan_config['name']} Plan",
                    "amount": amount,
                    "currency": "INR",
                    "description": f"{plan_config['scans_per_month']} scans/month"
                },
                "notes": {
                    "tier": tier,
                    "billing_cycle": billing_cycle
                }
            })
            
            print(f"✅ Razorpay plan created: {new_plan['id']}")
            return new_plan["id"]
    
    def activate_subscription_from_webhook(
        self,
        subscription_id: str,
        payment_id: str,
        db: Session
    ) -> Tuple[bool, str]:
        """
        Activate subscription when first payment succeeds (via webhook)
        
        This is called by webhook handler when subscription.activated event fires.
        
        Args:
            subscription_id: Razorpay subscription ID
            payment_id: Razorpay payment ID
            db: Database session
        
        Returns:
            Tuple of (success: bool, message: str)
        """
        try:
            # Fetch subscription details from Razorpay
            razorpay_subscription = self.client.subscription.fetch(subscription_id)
            
            # Extract user details from notes
            notes = razorpay_subscription.get("notes", {})
            user_id = notes.get("user_id")
            tier = notes.get("tier")
            
            if not user_id or not tier:
                return False, "Invalid subscription data"
            
            # Calculate period dates
            current_period_start = datetime.utcnow()
            current_period_end = current_period_start + timedelta(days=30)
            
            # Get or create subscription in our database
            subscription = db.query(Subscription).filter(
                Subscription.user_id == user_id
            ).first()
            
            if subscription:
                # Update existing
                subscription.tier = tier
                subscription.status = "active"
                subscription.razorpay_subscription_id = subscription_id
                subscription.razorpay_payment_id = payment_id
                subscription.auto_renew = True  # ✅ Auto-renewal enabled
                subscription.current_period_start = current_period_start
                subscription.current_period_end = current_period_end
                subscription.scans_used_this_period = 0
            else:
                # Create new
                subscription = Subscription(
                    user_id=user_id,
                    tier=tier,
                    status="active",
                    razorpay_subscription_id=subscription_id,
                    razorpay_payment_id=payment_id,
                    auto_renew=True,
                    scans_used_this_period=0,
                    current_period_start=current_period_start,
                    current_period_end=current_period_end
                )
                db.add(subscription)
            
            db.commit()
            print(f"✅ Subscription activated for user {user_id}")
            
            return True, "Subscription activated successfully"
            
        except Exception as e:
            print(f"❌ Subscription activation failed: {str(e)}")
            return False, f"Activation failed: {str(e)}"
    
    def handle_recurring_payment(
        self,
        subscription_id: str,
        payment_id: str,
        db: Session
    ) -> Tuple[bool, str]:
        """
        Handle automatic recurring payment (monthly charge)
        
        Called by webhook when subscription.charged event fires.
        This happens automatically every month by Razorpay.
        
        Args:
            subscription_id: Razorpay subscription ID
            payment_id: Razorpay payment ID
            db: Database session
        
        Returns:
            Tuple of (success: bool, message: str)
        """
        try:
            # Find subscription in our database
            subscription = db.query(Subscription).filter(
                Subscription.razorpay_subscription_id == subscription_id
            ).first()
            
            if not subscription:
                return False, "Subscription not found in database"
            
            # Reset usage for new billing period
            subscription.scans_used_this_period = 0
            subscription.current_period_start = datetime.utcnow()
            subscription.current_period_end = datetime.utcnow() + timedelta(days=30)
            subscription.status = "active"
            subscription.razorpay_payment_id = payment_id  # Update to latest payment
            
            db.commit()
            
            print(f"✅ Recurring payment processed for user {subscription.user_id}")
            return True, "Recurring payment processed successfully"
            
        except Exception as e:
            print(f"❌ Recurring payment processing failed: {str(e)}")
            return False, f"Processing failed: {str(e)}"
    
    def handle_payment_failed(
        self,
        subscription_id: str,
        db: Session
    ) -> Tuple[bool, str]:
        """
        Handle failed recurring payment
        
        Called when subscription.payment_failed webhook fires.
        Razorpay will auto-retry, but we should notify user.
        
        Args:
            subscription_id: Razorpay subscription ID
            db: Database session
        
        Returns:
            Tuple of (success: bool, message: str)
        """
        try:
            subscription = db.query(Subscription).filter(
                Subscription.razorpay_subscription_id == subscription_id
            ).first()
            
            if not subscription:
                return False, "Subscription not found"
            
            # Mark as payment_failed (but keep active for grace period)
            subscription.status = "payment_failed"
            db.commit()
            
            # TODO: Send email notification to user
            # send_payment_failed_email(subscription.user_id, db)
            
            print(f"⚠️ Payment failed for user {subscription.user_id}")
            return True, "Payment failure recorded"
            
        except Exception as e:
            print(f"❌ Failed payment handling error: {str(e)}")
            return False, f"Error: {str(e)}"
```

---

### Step 2: Update Webhook Handler

```python
# backend/app/services/razorpay_service.py

def handle_webhook(self, event: Dict, signature: str, db: Session) -> Tuple[bool, str]:
    """
    Enhanced webhook handler with subscription events
    """
    # ... existing signature verification code ...
    
    event_type = event.get("event")
    payload = event.get("payload", {})
    
    # Handle one-time payment events (existing)
    if event_type == "payment.captured":
        # ... existing code ...
        pass
    
    # ✅ NEW: Handle subscription events
    elif event_type == "subscription.activated":
        """
        Fired when customer completes first payment of subscription.
        This is when we activate their plan.
        """
        subscription_entity = payload.get("subscription", {}).get("entity", {})
        payment_entity = payload.get("payment", {}).get("entity", {})
        
        subscription_id = subscription_entity.get("id")
        payment_id = payment_entity.get("id")
        
        if subscription_id and payment_id:
            success, message = self.activate_subscription_from_webhook(
                subscription_id=subscription_id,
                payment_id=payment_id,
                db=db
            )
            return success, message
    
    elif event_type == "subscription.charged":
        """
        Fired every month when Razorpay automatically charges the customer.
        This is the AUTO-RENEWAL event! 🎉
        """
        subscription_entity = payload.get("subscription", {}).get("entity", {})
        payment_entity = payload.get("payment", {}).get("entity", {})
        
        subscription_id = subscription_entity.get("id")
        payment_id = payment_entity.get("id")
        
        if subscription_id and payment_id:
            success, message = self.handle_recurring_payment(
                subscription_id=subscription_id,
                payment_id=payment_id,
                db=db
            )
            return success, message
    
    elif event_type == "subscription.payment_failed":
        """
        Fired when monthly charge fails (insufficient funds, expired card, etc.)
        """
        subscription_entity = payload.get("subscription", {}).get("entity", {})
        subscription_id = subscription_entity.get("id")
        
        if subscription_id:
            success, message = self.handle_payment_failed(
                subscription_id=subscription_id,
                db=db
            )
            return success, message
    
    elif event_type == "subscription.cancelled":
        """
        Fired when subscription is cancelled (by user or after failed payments)
        """
        subscription_entity = payload.get("subscription", {}).get("entity", {})
        subscription_id = subscription_entity.get("id")
        
        if subscription_id:
            subscription = db.query(Subscription).filter(
                Subscription.razorpay_subscription_id == subscription_id
            ).first()
            
            if subscription:
                subscription.status = "cancelled"
                subscription.auto_renew = False
                subscription.cancelled_at = datetime.utcnow()
                db.commit()
                
                return True, "Subscription cancelled"
    
    elif event_type == "subscription.paused":
        """
        Fired when subscription is paused
        """
        subscription_entity = payload.get("subscription", {}).get("entity", {})
        subscription_id = subscription_entity.get("id")
        
        if subscription_id:
            subscription = db.query(Subscription).filter(
                Subscription.razorpay_subscription_id == subscription_id
            ).first()
            
            if subscription:
                subscription.status = "paused"
                db.commit()
                
                return True, "Subscription paused"
    
    return True, f"Webhook event {event_type} processed"
```

---

### Step 3: Update Frontend - Switch to Subscription Flow

```typescript
// frontend/src/components/RazorpayCheckout.tsx

export function useRazorpay() {
  const createSubscription = async (tier: string, billingCycle: 'monthly' | 'yearly') => {
    try {
      // Call new endpoint to create Razorpay subscription
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/payments/create-subscription`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        credentials: 'include',
        body: JSON.stringify({
          tier,
          billing_cycle: billingCycle
        })
      })
      
      if (!response.ok) {
        const error = await response.json()
        throw new Error(error.detail || 'Failed to create subscription')
      }
      
      const data = await response.json()
      
      // Redirect user to Razorpay hosted page for subscription
      window.location.href = data.short_url
      
      return data
    } catch (error) {
      console.error('Error creating subscription:', error)
      throw error
    }
  }
  
  return {
    createSubscription,
    // ... existing functions ...
  }
}
```

---

### Step 4: Add New API Endpoint

```python
# backend/app/api/payments.py

@router.post("/create-subscription")
async def create_recurring_subscription(
    request: CreateOrderRequest,
    current_user: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Create Razorpay recurring subscription (auto-renewal enabled)
    
    This replaces create-order for customers who want auto-renewal.
    Razorpay will automatically charge them every month.
    
    Args:
        request: Subscription creation request
        current_user: Current authenticated user
        db: Database session
    
    Returns:
        Subscription details with payment link
    """
    try:
        print(f"🔄 Creating recurring subscription for user {current_user}")
        
        # Validate tier
        valid_tiers = ["basic", "pro", "ultra", "max"]
        if request.tier.lower() not in valid_tiers:
            raise HTTPException(400, f"Invalid tier: {request.tier}")
        
        # Get user details
        user_email = "user@example.com"  # TODO: Fetch from DB
        user_name = "User"  # TODO: Fetch from DB
        
        # Create subscription
        subscription_data = razorpay_service.create_recurring_subscription(
            user_id=current_user,
            tier=request.tier.lower(),
            billing_cycle=request.billing_cycle,
            user_email=user_email,
            user_name=user_name,
            db=db
        )
        
        print(f"✅ Subscription created: {subscription_data['subscription_id']}")
        
        return {
            "success": True,
            "subscription_id": subscription_data["subscription_id"],
            "short_url": subscription_data["short_url"],  # ← Redirect here
            "amount": subscription_data["amount"],
            "next_billing": subscription_data["next_billing"]
        }
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Subscription creation error: {str(e)}")
        raise HTTPException(500, f"Subscription creation failed: {str(e)}")
```

---

## 🔧 ALTERNATIVE: If You Can't Use Razorpay Subscriptions

If Razorpay Subscriptions API doesn't work for you, here's the **manual cron job approach**:

### Step 1: Create Renewal Cron Job

```python
# backend/app/cron/subscription_renewal.py

"""
Subscription Renewal Cron Job
Run this daily to charge expired subscriptions
"""

from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.models import Subscription
from app.services.razorpay_service import razorpay_service

def renew_expired_subscriptions():
    """
    Check all subscriptions and renew expired ones
    Run this daily via cron job
    """
    db: Session = SessionLocal()
    
    try:
        now = datetime.utcnow()
        
        # Find subscriptions that expired in last 24 hours
        expired_subscriptions = db.query(Subscription).filter(
            Subscription.status == "active",
            Subscription.auto_renew == True,
            Subscription.current_period_end < now,
            Subscription.current_period_end > now - timedelta(days=1)
        ).all()
        
        print(f"📋 Found {len(expired_subscriptions)} subscriptions to renew")
        
        for subscription in expired_subscriptions:
            try:
                print(f"🔄 Renewing subscription for user {subscription.user_id}")
                
                # Get plan details
                from app.config.plans import get_plan_config
                plan = get_plan_config(subscription.tier)
                
                # Calculate amount
                if subscription.billing_cycle == "yearly":
                    amount = plan["price_yearly"]
                else:
                    amount = plan["price_monthly"]
                
                amount_paise = amount * 100
                
                # Create payment order
                order = razorpay_service.create_payment_order(
                    amount=amount_paise,
                    receipt=f"renewal_{subscription.user_id}_{int(now.timestamp())}",
                    notes={
                        "user_id": subscription.user_id,
                        "tier": subscription.tier,
                        "type": "renewal"
                    }
                )
                
                # TODO: Charge stored payment method
                # This requires saving card token after first payment
                # payment = razorpay_service.charge_saved_card(
                #     order_id=order["id"],
                #     token=subscription.payment_token
                # )
                
                # For now, send payment link to customer
                # send_renewal_payment_link_email(
                #     email=subscription.user_email,
                #     order_id=order["id"],
                #     amount=amount
                # )
                
                print(f"✅ Renewal initiated for {subscription.user_id}")
                
            except Exception as e:
                print(f"❌ Failed to renew {subscription.user_id}: {str(e)}")
                
                # Mark subscription as expired after 3 failed attempts
                if not hasattr(subscription, 'renewal_attempts'):
                    subscription.renewal_attempts = 0
                
                subscription.renewal_attempts += 1
                
                if subscription.renewal_attempts >= 3:
                    subscription.status = "expired"
                    subscription.auto_renew = False
                    print(f"⏰ Subscription expired for {subscription.user_id}")
                
                db.commit()
        
        print("✅ Renewal cron job complete")
        
    except Exception as e:
        print(f"❌ Renewal cron job failed: {str(e)}")
    
    finally:
        db.close()

if __name__ == "__main__":
    renew_expired_subscriptions()
```

### Step 2: Schedule Cron Job

**Option A: Render.com Cron Jobs**
```yaml
# render.yaml
services:
  - type: cron
    name: subscription-renewal
    env: python
    schedule: "0 0 * * *"  # Daily at midnight
    buildCommand: "pip install -r requirements.txt"
    startCommand: "python backend/app/cron/subscription_renewal.py"
    envVars:
      - key: DATABASE_URL
        fromDatabase:
          name: trulyinvoice-db
          property: connectionString
```

**Option B: External Cron Service (cron-job.org)**
1. Create endpoint: `POST /api/cron/renew-subscriptions`
2. Add authentication: Check API key in header
3. Schedule daily call from cron-job.org

---

## 📊 COMPARISON TABLE

| Feature | Razorpay Subscriptions API | Manual Cron Job |
|---------|---------------------------|-----------------|
| **Auto-Charging** | ✅ Automatic by Razorpay | ❌ You handle manually |
| **Retry Logic** | ✅ Built-in (3 retries) | ❌ You implement |
| **PCI Compliance** | ✅ Razorpay handles | ⚠️ You must handle token storage |
| **Setup Complexity** | 🟢 Low (API changes only) | 🔴 High (cron + token storage) |
| **Reliability** | ✅ 99.9% uptime | ⚠️ Depends on your cron |
| **Failed Payment UI** | ✅ Razorpay hosted page | ❌ Build yourself |
| **Customer Control** | ✅ Razorpay dashboard | ❌ Build yourself |
| **Recommendation** | ⭐ **USE THIS** | ⚠️ Only if API unavailable |

---

## 🎯 RECOMMENDED NEXT STEPS

### This Week (Critical):
1. ✅ Implement `create_recurring_subscription()` method (2 hours)
2. ✅ Update webhook handler for subscription events (1 hour)
3. ✅ Add `/create-subscription` API endpoint (30 min)
4. ✅ Test with Razorpay test mode (1 hour)

### Next Week:
1. ✅ Update frontend to use subscription flow (1 hour)
2. ✅ Add email notifications for renewals (1 hour)
3. ✅ Test failed payment scenarios (30 min)
4. ✅ Go live with production keys

---

## ✅ TESTING CHECKLIST

- [ ] Create test subscription in Razorpay dashboard
- [ ] Verify webhook receives `subscription.activated` event
- [ ] Check database - subscription status should be "active"
- [ ] Wait 30 days (or use Razorpay date override) for renewal
- [ ] Verify webhook receives `subscription.charged` event
- [ ] Check database - scans_used reset to 0
- [ ] Test failed payment - temporarily block card
- [ ] Verify webhook receives `subscription.payment_failed` event
- [ ] Check customer receives email notification
- [ ] Test cancellation flow
- [ ] Verify `subscription.cancelled` webhook works

---

## 🔒 SECURITY NOTES

1. ✅ **Always verify webhook signatures** (already implemented)
2. ✅ **Never store card numbers** - Use Razorpay tokens only
3. ✅ **Log all payment events** for audit trail
4. ✅ **Rate limit webhook endpoint** to prevent DDoS
5. ✅ **Use HTTPS** for all payment communications

---

## 💰 PRICING REMINDER

Make sure to charge correctly:
```python
# ❌ WRONG
amount = 499  # Base price

# ✅ CORRECT (With 18% GST)
base = 499
gst = base * 0.18  # 89.82
total = base + gst  # 588.82
amount_paise = int(total * 100)  # 58882 paise
```

---

## 📞 SUMMARY

**Current State:** You have auto-renewal **logic** (resets scans), but no auto-**charging**

**Recommended Solution:** Use Razorpay Subscriptions API
- Razorpay charges customers automatically every month
- You just handle webhooks to update database
- Total implementation time: ~5 hours

**Alternative:** Manual cron job + stored payment tokens
- More complex, less reliable
- Only if Razorpay Subscriptions API unavailable

**Next Action:** Implement Step 1-4 above using Razorpay Subscriptions API

---

**Questions? Need help implementing? Let me know!** 🚀
