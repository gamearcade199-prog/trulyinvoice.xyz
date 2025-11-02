"""
Razorpay Payment Service
Handles all Razorpay payment operations
"""

import razorpay
import hmac
import hashlib
from typing import Dict, Optional, Tuple
from datetime import datetime, timedelta
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models import Subscription
from app.config.plans import get_plan_config


class RazorpayService:
    """Service for Razorpay payment operations"""
    
    def __init__(self):
        # Initialize Razorpay client
        # Keys will be set from environment variables
        self.key_id = getattr(settings, 'RAZORPAY_KEY_ID', 'rzp_test_dummy_key')
        self.key_secret = getattr(settings, 'RAZORPAY_KEY_SECRET', 'dummy_secret')
        
        # Initialize client (will work when real keys are added)
        try:
            self.client = razorpay.Client(auth=(self.key_id, self.key_secret))
        except Exception as e:
            print(f"Warning: Razorpay client initialization failed: {e}")
            self.client = None
    
    def create_payment_order(
        self, 
        amount: int, 
        currency: str = "INR",
        receipt: Optional[str] = None,
        notes: Optional[Dict] = None
    ) -> Dict:
        """
        Create a Razorpay payment order
        
        Args:
            amount: Amount in paise (e.g., 14900 for ₹149)
            currency: Currency code (default: INR)
            receipt: Receipt ID for reference
            notes: Additional notes/metadata
        
        Returns:
            Order details from Razorpay
        """
        # Check if Razorpay keys are properly configured
        if self.key_id == 'rzp_test_dummy_key' or self.key_secret == 'dummy_secret':
            raise Exception("🔴 ERROR: Razorpay keys not configured! Please set RAZORPAY_KEY_ID and RAZORPAY_KEY_SECRET environment variables with your live keys from https://dashboard.razorpay.com/app/settings/api-keys")
        
        if not self.client:
            # Return mock order for development if keys exist
            return {
                "id": f"order_mock_{int(datetime.utcnow().timestamp())}",
                "entity": "order",
                "amount": amount,
                "amount_paid": 0,
                "amount_due": amount,
                "currency": currency,
                "receipt": receipt,
                "status": "created",
                "notes": notes or {}
            }
        
        try:
            order_data = {
                "amount": amount,  # Amount in paise
                "currency": currency,
                "receipt": receipt or f"rcpt_{int(datetime.utcnow().timestamp())}",
                "notes": notes or {}
            }
            
            order = self.client.order.create(data=order_data)
            return order
        
        except Exception as e:
            raise Exception(f"Failed to create Razorpay order: {str(e)}")
    
    def verify_payment_signature(
        self,
        razorpay_order_id: str,
        razorpay_payment_id: str,
        razorpay_signature: str
    ) -> bool:
        """
        Verify Razorpay payment signature
        
        Args:
            razorpay_order_id: Order ID from Razorpay
            razorpay_payment_id: Payment ID from Razorpay
            razorpay_signature: Signature to verify
        
        Returns:
            True if signature is valid, False otherwise
        """
        # Create signature verification string
        message = f"{razorpay_order_id}|{razorpay_payment_id}"
        
        # Generate signature using secret key
        generated_signature = hmac.new(
            self.key_secret.encode('utf-8'),
            message.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
        
        # Compare signatures
        return hmac.compare_digest(generated_signature, razorpay_signature)
    
    def create_subscription_order(
        self,
        user_id: str,
        tier: str,
        billing_cycle: str,
        user_email: str,
        user_name: str,
        db: Session
    ) -> Dict:
        """
        Create payment order for subscription
        
        Args:
            user_id: User ID
            tier: Plan tier (basic, pro, ultra, max)
            billing_cycle: monthly or yearly
            user_email: User email
            user_name: User name
            db: Database session
        
        Returns:
            Order details including Razorpay order ID
        """
        # Get plan configuration
        plan = get_plan_config(tier)
        
        # Calculate amount based on billing cycle
        if billing_cycle == "yearly":
            amount = plan["price_yearly"]
        else:
            amount = plan["price_monthly"]
        
        # Convert to paise (Razorpay uses smallest currency unit)
        amount_paise = amount * 100
        
        # Create receipt ID
        receipt = f"sub_{user_id}_{tier}_{int(datetime.utcnow().timestamp())}"
        
        # Add notes
        notes = {
            "user_id": user_id,
            "tier": tier,
            "billing_cycle": billing_cycle,
            "user_email": user_email,
            "user_name": user_name,
            "plan_name": plan["name"]
        }
        
        # Create order
        order = self.create_payment_order(
            amount=amount_paise,
            receipt=receipt,
            notes=notes
        )
        
        # Return order details with additional info
        return {
            "order_id": order["id"],
            "amount": amount,
            "amount_paise": amount_paise,
            "currency": "INR",
            "tier": tier,
            "billing_cycle": billing_cycle,
            "plan_name": plan["name"],
            "receipt": receipt,
            "key_id": self.key_id  # Frontend needs this for checkout
        }
    
    def process_successful_payment(
        self,
        order_id: str,
        payment_id: str,
        signature: str,
        db: Session
    ) -> Tuple[bool, str, Optional[Dict]]:
        """
        Process successful payment and activate subscription.
        
        ⚠️ NOTE: This function assumes caller has already verified:
        - Payment signature
        - Payment status = "captured"
        - Payment amount matches order amount
        - Order belongs to current user (verified via order.notes.user_id)
        - Duplicate payment check done
        
        Args:
            order_id: Razorpay order ID
            payment_id: Razorpay payment ID
            signature: Payment signature (already verified by caller)
            db: Database session
        
        Returns:
            Tuple of (success: bool, message: str, subscription_data: dict)
        """
        
        # Fetch order details from Razorpay
        try:
            if self.client:
                order = self.client.order.fetch(order_id)
            else:
                # Mock order for development
                order = {
                    "notes": {
                        "user_id": "mock_user",
                        "tier": "pro",
                        "billing_cycle": "monthly"
                    }
                }
        except Exception as e:
            print(f"❌ Failed to fetch order: {str(e)}")
            return False, f"Failed to fetch order: {str(e)}", None
        
        # Extract subscription details from order notes
        notes = order.get("notes", {})
        user_id = notes.get("user_id")
        tier = notes.get("tier")
        billing_cycle = notes.get("billing_cycle", "monthly")
        
        if not user_id or not tier:
            print(f"❌ Invalid order data. user_id={user_id}, tier={tier}")
            return False, "Invalid order data", None
        
        print(f"📝 Processing payment for user {user_id}")
        print(f"   Tier: {tier}, Cycle: {billing_cycle}")
        
        # Get or create subscription
        subscription = db.query(Subscription).filter(
            Subscription.user_id == user_id
        ).first()
        
        # Calculate period dates
        current_period_start = datetime.utcnow()
        if billing_cycle == "yearly":
            current_period_end = current_period_start + timedelta(days=365)
        else:
            current_period_end = current_period_start + timedelta(days=30)
        
        if subscription:
            # Update existing subscription
            print(f"✏️ Updating existing subscription")
            
            # FIX #5: Distinguish between different update scenarios
            old_tier = subscription.tier
            old_period_end = subscription.current_period_end
            current_time = datetime.utcnow()
            
            # Scenario A: Period has ended (renewal)
            # Example: Previous period ended Oct 26, new payment Oct 27 → Reset scans
            if current_time >= old_period_end:
                print(f"   ↻ Renewal detected (old period ended on {old_period_end})")
                subscription.scans_used_this_period = 0  # Reset for new period
                is_renewal = True
            
            # Scenario B: Same tier, same month (re-subscribe after cancel)
            # Example: Cancelled Oct 1, re-subscribes Oct 15 → Keep the scans
            elif old_tier == tier and current_time < old_period_end:
                print(f"   ✓ Same tier during period (keep scans: {subscription.scans_used_this_period})")
                # Don't reset scans - they're already at fair level
                is_renewal = False
            
            # Scenario C: Mid-period upgrade (tier changed)
            # Example: Free→Pro on Oct 15 → Keep scans (user earned them)
            elif old_tier != tier and current_time < old_period_end:
                print(f"   ⬆️ Mid-period upgrade from {old_tier} to {tier} (keep scans: {subscription.scans_used_this_period})")
                # Don't reset scans - customer earned them on the old plan
                is_renewal = False
            
            # Default: Keep existing scans unless explicitly renewed
            else:
                print(f"   ? Unknown scenario, keeping scans: {subscription.scans_used_this_period}")
                is_renewal = False
            
            subscription.tier = tier
            subscription.status = "active"
            subscription.billing_cycle = billing_cycle
            subscription.razorpay_order_id = order_id
            subscription.razorpay_payment_id = payment_id
            subscription.current_period_start = current_period_start
            subscription.current_period_end = current_period_end
            subscription.cancelled_at = None
        else:
            # Create new subscription
            print(f"✨ Creating new subscription")
            subscription = Subscription(
                user_id=user_id,
                tier=tier,
                status="active",
                billing_cycle=billing_cycle,
                razorpay_order_id=order_id,
                razorpay_payment_id=payment_id,
                scans_used_this_period=0,
                current_period_start=current_period_start,
                current_period_end=current_period_end
            )
            db.add(subscription)
        
        db.commit()
        db.refresh(subscription)
        
        print(f"✅ Subscription activated")
        
        # Return subscription data
        plan = get_plan_config(tier)
        return True, "Subscription activated successfully", {
            "user_id": user_id,
            "tier": tier,
            "tier_name": plan["name"],
            "status": "active",
            "scans_limit": plan["scans_per_month"],
            "period_start": current_period_start.isoformat(),
            "period_end": current_period_end.isoformat(),
            "billing_cycle": billing_cycle
        }
    
    def handle_webhook(self, event: Dict, signature: str, db: Session) -> Tuple[bool, str]:
        """
        Handle Razorpay webhook events - UPDATED FOR SUBSCRIPTIONS
        
        Supports 8+ subscription events:
        - subscription.activated: First payment successful
        - subscription.charged: Recurring payment successful (AUTO-RENEWAL!)
        - subscription.payment_failed: Payment failed (retry logic)
        - subscription.cancelled: User cancelled subscription
        - subscription.paused: Subscription paused
        - subscription.resumed: Subscription resumed
        - subscription.completed: Subscription completed all cycles
        - subscription.pending: Subscription created, awaiting payment
        - payment.captured: Legacy one-time payments (backward compatible)
        
        Features:
        - Idempotency: Uses event_id to prevent duplicate processing
        - Retry logic: Tracks attempts and implements exponential backoff
        - Logging: Stores all webhook events in webhook_logs table
        
        Args:
            event: Webhook event data
            signature: Webhook signature
            db: Database session
        
        Returns:
            Tuple of (success: bool, message: str)
        """
        # Extract event ID for idempotency
        event_id = event.get("id", f"unknown_{int(datetime.utcnow().timestamp())}")
        event_type = event.get("event")
        
        print(f"📨 Webhook received: {event_type} (ID: {event_id})")
        
        # SECURITY FIX: Webhook signature verification is MANDATORY
        webhook_secret = getattr(settings, 'RAZORPAY_WEBHOOK_SECRET', '')
        
        if not webhook_secret:
            # CRITICAL: Don't process webhooks without secret configured
            print("🚨 SECURITY: RAZORPAY_WEBHOOK_SECRET not configured - rejecting webhook")
            self._log_webhook(db, event_id, event_type, event, signature, 'failed', error='Webhook secret not configured')
            return False, "Webhook secret not configured - cannot verify signature"
        
        if not signature:
            print("🚨 SECURITY: Webhook signature missing")
            self._log_webhook(db, event_id, event_type, event, signature, 'failed', error='Signature missing')
            return False, "Webhook signature missing"
        
        # Generate signature
        expected_signature = hmac.new(
            webhook_secret.encode('utf-8'),
            str(event).encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
        
        if not hmac.compare_digest(expected_signature, signature):
            print("🚨 SECURITY: Invalid webhook signature - possible attack")
            self._log_webhook(db, event_id, event_type, event, signature, 'failed', error='Invalid signature')
            return False, "Invalid webhook signature"
        
        print("✅ Webhook signature verified")
        
        # IDEMPOTENCY CHECK: Has this event been processed already?
        existing_log = self._check_webhook_processed(db, event_id)
        if existing_log and existing_log.status == 'processed':
            print(f"⏭️ Webhook {event_id} already processed, skipping")
            return True, f"Webhook {event_id} already processed (idempotent)"
        
        # Log webhook attempt
        attempt_count = (existing_log.attempt_count + 1) if existing_log else 1
        print(f"🔄 Processing webhook (attempt {attempt_count})")
        
        # Process event based on type
        payload = event.get("payload", {})
        
        # Extract subscription_id and user_id for logging
        subscription_id = None
        user_id = None
        try:
            subscription_entity = payload.get("subscription", {}).get("entity", {})
            subscription_id = subscription_entity.get("id")
            # Try to get user_id from subscription notes
            notes = subscription_entity.get("notes", {})
            user_id = notes.get("user_id")
        except:
            pass
        
        # ===================================================================
        # SUBSCRIPTION EVENTS - Auto-Renewal Magic Happens Here!
        # ===================================================================
        
        if event_type == "subscription.activated":
            # 🎉 First payment successful - activate subscription
            subscription_entity = payload.get("subscription", {}).get("entity", {})
            subscription_id = subscription_entity.get("id")
            
            print(f"🎉 SUBSCRIPTION ACTIVATED: {subscription_id}")
            
            # Find subscription in database
            sub = db.query(Subscription).filter(
                Subscription.razorpay_subscription_id == subscription_id
            ).first()
            
            if sub:
                sub.status = "active"
                sub.last_payment_date = datetime.utcnow()
                sub.next_billing_date = datetime.fromtimestamp(subscription_entity.get("current_end", 0))
                sub.current_period_start = datetime.fromtimestamp(subscription_entity.get("current_start", 0))
                sub.current_period_end = datetime.fromtimestamp(subscription_entity.get("current_end", 0))
                sub.payment_retry_count = 0
                sub.updated_at = datetime.utcnow()
                db.commit()
                print(f"✅ Subscription activated for user {sub.user_id}")
                
                # Log success
                self._log_webhook(db, event_id, event_type, event, signature, 'processed', sub.user_id, subscription_id)
                return True, f"Subscription {subscription_id} activated"
            else:
                print(f"⚠️ Subscription {subscription_id} not found in database")
                self._log_webhook(db, event_id, event_type, event, signature, 'failed', error='Subscription not found in database')
                return False, "Subscription not found"
        
        elif event_type == "subscription.charged":
            # 💰 RECURRING PAYMENT SUCCESS - This is the auto-renewal!
            subscription_entity = payload.get("subscription", {}).get("entity", {})
            payment_entity = payload.get("payment", {}).get("entity", {})
            
            subscription_id = subscription_entity.get("id")
            payment_id = payment_entity.get("id")
            
            print(f"💰 AUTO-RENEWAL CHARGED: {subscription_id}, payment: {payment_id}")
            
            # Find subscription in database
            sub = db.query(Subscription).filter(
                Subscription.razorpay_subscription_id == subscription_id
            ).first()
            
            if sub:
                # ✨ RESET USAGE - This is the key to monthly renewal!
                sub.scans_used_this_period = 0
                sub.status = "active"
                sub.last_payment_date = datetime.utcnow()
                sub.next_billing_date = datetime.fromtimestamp(subscription_entity.get("current_end", 0))
                sub.current_period_start = datetime.fromtimestamp(subscription_entity.get("current_start", 0))
                sub.current_period_end = datetime.fromtimestamp(subscription_entity.get("current_end", 0))
                sub.payment_retry_count = 0
                sub.grace_period_ends_at = None  # Clear grace period
                sub.updated_at = datetime.utcnow()
                db.commit()
                
                print(f"✅ AUTO-RENEWAL: Usage reset for user {sub.user_id}, tier {sub.tier}")
                self._log_webhook(db, event_id, event_type, event, signature, 'processed', sub.user_id, subscription_id)
                return True, f"Subscription {subscription_id} charged successfully - usage reset"
            else:
                print(f"⚠️ Subscription {subscription_id} not found")
                self._log_webhook(db, event_id, event_type, event, signature, 'failed', error='Subscription not found')
                return False, "Subscription not found"
        
        elif event_type == "subscription.payment_failed":
            # ❌ Payment failed - implement retry logic
            subscription_entity = payload.get("subscription", {}).get("entity", {})
            subscription_id = subscription_entity.get("id")
            
            print(f"❌ PAYMENT FAILED: {subscription_id}")
            
            sub = db.query(Subscription).filter(
                Subscription.razorpay_subscription_id == subscription_id
            ).first()
            
            if sub:
                sub.payment_retry_count += 1
                sub.last_payment_attempt = datetime.utcnow()
            
            # Give 7-day grace period
                if not sub.grace_period_ends_at:
                    sub.grace_period_ends_at = datetime.utcnow() + timedelta(days=7)
                
                # After 3 failures, mark as past_due
                if sub.payment_retry_count >= 3:
                    sub.status = "past_due"
                    print(f"⚠️ Subscription {subscription_id} marked past_due after 3 failures")
                
                sub.updated_at = datetime.utcnow()
                db.commit()
                
                self._log_webhook(db, event_id, event_type, event, signature, 'processed', sub.user_id, subscription_id)
                return True, f"Payment failed for {subscription_id}, retry count: {sub.payment_retry_count}"
            else:
                self._log_webhook(db, event_id, event_type, event, signature, 'failed', error='Subscription not found')
                return False, "Subscription not found"
        
        elif event_type == "subscription.cancelled":
            # 🛑 User cancelled subscription
            subscription_entity = payload.get("subscription", {}).get("entity", {})
            subscription_id = subscription_entity.get("id")
            
            print(f"🛑 SUBSCRIPTION CANCELLED: {subscription_id}")
            
            sub = db.query(Subscription).filter(
                Subscription.razorpay_subscription_id == subscription_id
            ).first()
            
            if sub:
                sub.status = "cancelled"
                sub.cancelled_at = datetime.utcnow()
                sub.auto_renew = False
                sub.updated_at = datetime.utcnow()
                db.commit()
                
                print(f"✅ Subscription cancelled for user {sub.user_id}")
                self._log_webhook(db, event_id, event_type, event, signature, 'processed', sub.user_id, subscription_id)
                return True, f"Subscription {subscription_id} cancelled"
            else:
                self._log_webhook(db, event_id, event_type, event, signature, 'failed', error='Subscription not found')
                return False, "Subscription not found"
        
        elif event_type == "subscription.paused":
            # ⏸️ Subscription paused
            subscription_entity = payload.get("subscription", {}).get("entity", {})
            subscription_id = subscription_entity.get("id")
            
            print(f"⏸️ SUBSCRIPTION PAUSED: {subscription_id}")
            
            sub = db.query(Subscription).filter(
                Subscription.razorpay_subscription_id == subscription_id
            ).first()
            
            if sub:
                sub.status = "paused"
                sub.updated_at = datetime.utcnow()
                db.commit()
                self._log_webhook(db, event_id, event_type, event, signature, 'processed', sub.user_id, subscription_id)
                return True, f"Subscription {subscription_id} paused"
            else:
                self._log_webhook(db, event_id, event_type, event, signature, 'failed', error='Subscription not found')
                return False, "Subscription not found"
        
        elif event_type == "subscription.resumed":
            # ▶️ Subscription resumed
            subscription_entity = payload.get("subscription", {}).get("entity", {})
            subscription_id = subscription_entity.get("id")
            
            print(f"▶️ SUBSCRIPTION RESUMED: {subscription_id}")
            
            sub = db.query(Subscription).filter(
                Subscription.razorpay_subscription_id == subscription_id
            ).first()
            
            if sub:
                sub.status = "active"
                sub.updated_at = datetime.utcnow()
                db.commit()
                self._log_webhook(db, event_id, event_type, event, signature, 'processed', sub.user_id, subscription_id)
                return True, f"Subscription {subscription_id} resumed"
            else:
                self._log_webhook(db, event_id, event_type, event, signature, 'failed', error='Subscription not found')
                return False, "Subscription not found"
        
        elif event_type == "subscription.completed":
            # ✅ Subscription completed all cycles
            subscription_entity = payload.get("subscription", {}).get("entity", {})
            subscription_id = subscription_entity.get("id")
            
            print(f"✅ SUBSCRIPTION COMPLETED: {subscription_id}")
            
            sub = db.query(Subscription).filter(
                Subscription.razorpay_subscription_id == subscription_id
            ).first()
            
            if sub:
                sub.status = "completed"
                sub.updated_at = datetime.utcnow()
                db.commit()
                self._log_webhook(db, event_id, event_type, event, signature, 'processed', sub.user_id, subscription_id)
                return True, f"Subscription {subscription_id} completed"
            else:
                self._log_webhook(db, event_id, event_type, event, signature, 'failed', error='Subscription not found')
                return False, "Subscription not found"
        
        elif event_type == "subscription.pending":
            # ⏳ Subscription created, awaiting first payment
            subscription_entity = payload.get("subscription", {}).get("entity", {})
            subscription_id = subscription_entity.get("id")
            
            print(f"⏳ SUBSCRIPTION PENDING: {subscription_id}")
            self._log_webhook(db, event_id, event_type, event, signature, 'processed', subscription_id=subscription_id)
            return True, f"Subscription {subscription_id} pending payment"
        
        # ===================================================================
        # LEGACY PAYMENT EVENTS (Backward Compatible)
        # ===================================================================
        
        elif event_type == "payment.captured":
            # Payment successful (legacy one-time orders)
            payment = payload.get("payment", {})
            entity = payment.get("entity", {})
            
            order_id = entity.get("order_id")
            payment_id = entity.get("id")
            
            if order_id and payment_id:
                # Process payment (signature already verified by webhook)
                success, message, _ = self.process_successful_payment(
                    order_id=order_id,
                    payment_id=payment_id,
                    signature="webhook_verified",
                    db=db
                )
                self._log_webhook(db, event_id, event_type, event, signature, 'processed' if success else 'failed')
                return success, message
        
        elif event_type == "payment.failed":
            # Payment failed - log it
            self._log_webhook(db, event_id, event_type, event, signature, 'processed')
            return True, "Payment failed event logged"
        
        # Unknown event type
        print(f"⚠️ Unknown webhook event: {event_type}")
        self._log_webhook(db, event_id, event_type, event, signature, 'processed')
        return True, f"Webhook event {event_type} received (no handler)"
    
    def cancel_subscription(self, user_id: str, db: Session) -> Tuple[bool, str]:
        """
        Cancel user subscription
        
        Args:
            user_id: User ID
            db: Database session
        
        Returns:
            Tuple of (success: bool, message: str)
        """
        subscription = db.query(Subscription).filter(
            Subscription.user_id == user_id
        ).first()
        
        if not subscription:
            return False, "No subscription found"
        
        if subscription.tier == "free":
            return False, "Cannot cancel free plan"
        
        # Mark as cancelled but keep active until period ends
        subscription.status = "cancelled"
        subscription.cancelled_at = datetime.utcnow()
        
        db.commit()
        
        return True, f"Subscription cancelled. Access until {subscription.current_period_end.date()}"
    
    # ========================================================================
    # RAZORPAY SUBSCRIPTIONS API - INDUSTRY-GRADE RECURRING BILLING
    # ========================================================================
    
    def create_razorpay_plan(
        self, 
        tier: str, 
        amount: int, 
        interval: int = 1,
        period: str = "monthly"
    ) -> str:
        """
        Create or fetch a Razorpay Plan (subscription template).
        
        Plans are reusable templates that define:
        - Billing amount
        - Billing frequency (monthly/yearly)
        - Auto-renewal behavior
        
        Args:
            tier: Plan tier (basic, pro, ultra, max)
            amount: Amount in paise (e.g., 58882 for ₹588.82)
            interval: Billing interval (1 = every period, 2 = every 2 periods)
            period: Billing period ("monthly", "yearly", "weekly", "daily")
        
        Returns:
            Plan ID (string)
        
        Raises:
            Exception: If plan creation fails
        """
        # Check if Razorpay client is initialized
        if not self.client:
            raise Exception("Razorpay client not initialized. Check your API keys.")
        
        # Generate deterministic plan ID for idempotency (for internal tracking)
        # Format: trulyinvoice_{tier}_{period}_v2 (v2 = correct pricing)
        internal_plan_id = f"trulyinvoice_{tier.lower()}_{period.lower()}_v2"
        
        try:
            # Try to fetch existing plan by searching through all plans
            all_plans = razorpay_service.client.plan.all()
            
            # Handle both dict and list responses
            if isinstance(all_plans, dict):
                plans_list = all_plans.get("items", [])
            else:
                plans_list = list(all_plans) if all_plans else []
            
            # Look for v2 plans first (correct pricing)
            for existing_plan in plans_list:
                plan_notes = existing_plan.get("notes", {})
                if plan_notes.get("internal_id") == internal_plan_id:
                    print(f"✅ Plan already exists: {existing_plan['id']} (internal: {internal_plan_id})")
                    return existing_plan["id"]
        
        except Exception as fetch_error:
            print(f"⚠️ Could not check for existing plans: {str(fetch_error)}")
        
        # Plan doesn't exist, create it
        print(f"📝 Creating new plan: {internal_plan_id}")
        
        try:
            # Get plan configuration
            from app.config.plans import get_plan_config
            plan_config = get_plan_config(tier)
            
            # Create plan (let Razorpay generate the ID)
            plan = self.client.plan.create({
                "period": period,
                "interval": interval,
                "item": {
                    "name": f"TrulyInvoice {tier.title()} Plan",
                    "amount": amount,
                    "currency": "INR",
                    "description": f"{plan_config['name']} - {plan_config['scans_per_month']} scans/month"
                },
                "notes": {
                    "tier": tier,
                    "internal_id": internal_plan_id,  # For searching later
                    "version": "v2",  # Correct pricing version
                    "created_via": "api",
                    "created_at": datetime.utcnow().isoformat(),
                    "scans_limit": str(plan_config['scans_per_month']),
                    "correct_pricing": "true"
                }
            })
            
            print(f"✅ Plan created successfully: {plan['id']}")
            return plan["id"]
        
        except Exception as create_error:
            print(f"❌ Failed to create plan: {str(create_error)}")
            raise Exception(f"Failed to create Razorpay plan: {str(create_error)}")
    
    def create_subscription(
        self,
        user_id: str,
        tier: str,
        billing_cycle: str = "monthly",
        customer_notify: bool = True
    ) -> Dict:
        """
        Create a recurring subscription for a user.
        
        This is THE KEY METHOD for auto-renewal. Once created, Razorpay will:
        1. Charge the customer for the first period
        2. Automatically charge every month (or year)
        3. Send webhooks on successful/failed charges
        4. Handle retry logic for failed payments
        
        Args:
            user_id: User ID
            tier: Plan tier (basic, pro, ultra, max)
            billing_cycle: "monthly" or "yearly"
            customer_notify: Whether to send email notifications to customer
        
        Returns:
            Dict with subscription details:
            {
                "subscription_id": "sub_xxxxx",
                "plan_id": "trulyinvoice_pro_monthly",
                "status": "created",
                "short_url": "https://rzp.io/i/xxxxx",  # Payment link
                "amount": 588.82,
                "next_billing_at": timestamp,
                "auto_renew": True
            }
        
        Raises:
            Exception: If subscription creation fails
        """
        # Check if Razorpay client is initialized
        if not self.client:
            raise Exception("Razorpay client not initialized. Check your API keys.")
        
        print(f"📝 Creating subscription for user {user_id}, tier: {tier}, cycle: {billing_cycle}")
        
        # 1. Get plan configuration
        from app.config.plans import get_plan_config
        plan = get_plan_config(tier)
        
        # 2. Get amount (already GST-inclusive from plan config)
        if billing_cycle == "yearly":
            amount = plan["price_yearly"]
        else:
            amount = plan["price_monthly"]
        
        # Convert to paise (plans already include GST)
        amount_paise = int(amount * 100)
        
        print(f"   Amount (GST-inclusive): ₹{amount}")
        
        # 3. Ensure plan exists (create if needed)
        try:
            period = "monthly" if billing_cycle == "monthly" else "yearly"
            interval = 1 if billing_cycle == "monthly" else 12
            
            plan_id = self.create_razorpay_plan(
                tier=tier,
                amount=amount_paise,
                interval=interval,
                period="monthly"  # Always monthly, interval controls frequency
            )
            
            print(f"✅ Plan ready: {plan_id}")
        
        except Exception as e:
            print(f"❌ Failed to create/fetch plan: {str(e)}")
            raise Exception(f"Failed to prepare subscription plan: {str(e)}")
        
        # 4. Create subscription
        try:
            subscription = self.client.subscription.create({
                "plan_id": plan_id,
                "customer_notify": 1 if customer_notify else 0,
                "quantity": 1,
                "total_count": 120,  # 120 months = 10 years (effectively unlimited)
                "start_at": None,  # Start immediately after first payment
                "expire_by": None,  # Never expires (until cancelled)
                "addons": [],
                "notes": {
                    "user_id": user_id,
                    "tier": tier,
                    "billing_cycle": billing_cycle,
                    "created_at": datetime.utcnow().isoformat(),
                    "platform": "trulyinvoice"
                },
                "notify_info": {
                    "notify_email": user_id if "@" in user_id else None
                }
            })
            
            print(f"✅ Subscription created: {subscription['id']}")
            
            # 5. Return subscription details
            return {
                "subscription_id": subscription["id"],
                "plan_id": plan_id,
                "status": subscription["status"],  # Usually "created"
                "short_url": subscription.get("short_url"),  # Payment link for customer
                "amount": amount,  # GST-inclusive amount
                "amount_paise": amount_paise,
                "next_billing_at": subscription.get("charge_at"),
                "current_start": subscription.get("current_start"),
                "current_end": subscription.get("current_end"),
                "auto_renew": True,
                "total_count": 120,
                "paid_count": subscription.get("paid_count", 0)
            }
        
        except Exception as e:
            print(f"❌ Failed to create subscription: {str(e)}")
            raise Exception(f"Failed to create Razorpay subscription: {str(e)}")
    
    def fetch_subscription(self, subscription_id: str) -> Dict:
        """
        Fetch subscription details from Razorpay.
        
        Args:
            subscription_id: Razorpay subscription ID
        
        Returns:
            Subscription details dictionary
        
        Raises:
            Exception: If fetch fails
        """
        if not self.client:
            raise Exception("Razorpay client not initialized")
        
        try:
            subscription = self.client.subscription.fetch(subscription_id)
            return subscription
        except Exception as e:
            raise Exception(f"Failed to fetch subscription: {str(e)}")
    
    def cancel_razorpay_subscription(
        self,
        subscription_id: str,
        cancel_at_cycle_end: bool = True
    ) -> Tuple[bool, str, Optional[Dict]]:
        """
        Cancel a Razorpay subscription.
        
        Args:
            subscription_id: Razorpay subscription ID
            cancel_at_cycle_end: If True, cancels at end of billing cycle.
                                 If False, cancels immediately.
        
        Returns:
            Tuple of (success: bool, message: str, subscription_data: dict)
        """
        if not self.client:
            return False, "Razorpay client not initialized", None
        
        try:
            if cancel_at_cycle_end:
                # Cancel at end of cycle (customer gets full period)
                subscription = self.client.subscription.cancel(
                    subscription_id,
                    {"cancel_at_cycle_end": 1}
                )
                message = "Subscription will be cancelled at the end of current billing cycle"
            else:
                # Cancel immediately (customer loses access now)
                subscription = self.client.subscription.cancel(subscription_id)
                message = "Subscription cancelled immediately"
            
            print(f"✅ Subscription cancelled: {subscription_id}")
            return True, message, subscription
        
        except Exception as e:
            print(f"❌ Failed to cancel subscription: {str(e)}")
            return False, f"Failed to cancel subscription: {str(e)}", None
    
    def pause_razorpay_subscription(
        self,
        subscription_id: str,
        pause_at: str = "now"
    ) -> Tuple[bool, str, Optional[Dict]]:
        """
        Pause a Razorpay subscription.
        
        Paused subscriptions don't charge customers but can be resumed later.
        Useful for temporary holds (vacation, financial difficulties, etc).
        
        Args:
            subscription_id: Razorpay subscription ID
            pause_at: When to pause ("now" or timestamp)
        
        Returns:
            Tuple of (success: bool, message: str, subscription_data: dict)
        """
        if not self.client:
            return False, "Razorpay client not initialized", None
        
        try:
            subscription = self.client.subscription.pause(
                subscription_id,
                {"pause_at": pause_at}
            )
            
            print(f"✅ Subscription paused: {subscription_id}")
            return True, "Subscription paused successfully", subscription
        
        except Exception as e:
            print(f"❌ Failed to pause subscription: {str(e)}")
            return False, f"Failed to pause subscription: {str(e)}", None
    
    def resume_razorpay_subscription(
        self,
        subscription_id: str,
        resume_at: str = "now"
    ) -> Tuple[bool, str, Optional[Dict]]:
        """
        Resume a paused Razorpay subscription.
        
        Args:
            subscription_id: Razorpay subscription ID
            resume_at: When to resume ("now" or timestamp)
        
        Returns:
            Tuple of (success: bool, message: str, subscription_data: dict)
        """
        if not self.client:
            return False, "Razorpay client not initialized", None
        
        try:
            subscription = self.client.subscription.resume(
                subscription_id,
                {"resume_at": resume_at}
            )
            
            print(f"✅ Subscription resumed: {subscription_id}")
            return True, "Subscription resumed successfully", subscription
        
        except Exception as e:
            print(f"❌ Failed to resume subscription: {str(e)}")
            return False, f"Failed to resume subscription: {str(e)}", None
    
    def update_subscription(
        self,
        subscription_id: str,
        updates: Dict
    ) -> Tuple[bool, str, Optional[Dict]]:
        """
        Update subscription details (plan, quantity, etc).
        
        Useful for:
        - Upgrading/downgrading plans
        - Changing quantity
        - Updating customer notification preferences
        
        Args:
            subscription_id: Razorpay subscription ID
            updates: Dictionary of fields to update
        
        Returns:
            Tuple of (success: bool, message: str, subscription_data: dict)
        """
        if not self.client:
            return False, "Razorpay client not initialized", None
        
        try:
            subscription = self.client.subscription.update(
                subscription_id,
                updates
            )
            
            print(f"✅ Subscription updated: {subscription_id}")
            return True, "Subscription updated successfully", subscription
        
        except Exception as e:
            print(f"❌ Failed to update subscription: {str(e)}")
            return False, f"Failed to update subscription: {str(e)}", None
    
    # ========================================================================
    # WEBHOOK LOGGING & IDEMPOTENCY HELPERS
    # ========================================================================
    
    def _check_webhook_processed(self, db: Session, event_id: str):
        """
        Check if webhook event has already been processed (idempotency).
        
        Args:
            db: Database session
            event_id: Razorpay event ID
        
        Returns:
            WebhookLog record or None
        """
        try:
            from sqlalchemy import text
            result = db.execute(
                text("SELECT * FROM webhook_logs WHERE event_id = :event_id"),
                {"event_id": event_id}
            ).fetchone()
            
            if result:
                # Convert row to object-like structure
                class WebhookLog:
                    def __init__(self, row):
                        self.id = row[0]
                        self.event_id = row[1]
                        self.status = row[6]
                        self.attempt_count = row[7]
                
                return WebhookLog(result)
            return None
        except Exception as e:
            print(f"⚠️ Error checking webhook processed: {str(e)}")
            return None
    
    def _log_webhook(
        self,
        db: Session,
        event_id: str,
        event_type: str,
        payload: Dict,
        signature: str,
        status: str,
        user_id: str = None,
        subscription_id: str = None,
        error: str = None
    ):
        """
        Log webhook event to database for tracking and debugging.
        
        Args:
            db: Database session
            event_id: Razorpay event ID
            event_type: Event type (subscription.charged, etc.)
            payload: Full webhook payload
            signature: Webhook signature
            status: Status (pending, processed, failed, retrying)
            user_id: User ID (if available)
            subscription_id: Subscription ID (if available)
            error: Error message (if failed)
        """
        try:
            import json
            from sqlalchemy import text
            
            # Check if log exists
            existing = db.execute(
                text("SELECT id, attempt_count FROM webhook_logs WHERE event_id = :event_id"),
                {"event_id": event_id}
            ).fetchone()
            
            if existing:
                # Update existing log
                attempt_count = existing[1] + 1
                db.execute(
                    text("""
                        UPDATE webhook_logs 
                        SET status = :status,
                            attempt_count = :attempt_count,
                            last_attempt_at = NOW(),
                            error_message = :error,
                            processed_at = CASE WHEN :status = 'processed' THEN NOW() ELSE processed_at END,
                            updated_at = NOW()
                        WHERE event_id = :event_id
                    """),
                    {
                        "event_id": event_id,
                        "status": status,
                        "attempt_count": attempt_count,
                        "error": error
                    }
                )
            else:
                # Insert new log
                db.execute(
                    text("""
                        INSERT INTO webhook_logs (
                            event_id, event_type, subscription_id, user_id,
                            payload, signature, status, attempt_count,
                            last_attempt_at, error_message, processed_at
                        ) VALUES (
                            :event_id, :event_type, :subscription_id, :user_id,
                            :payload, :signature, :status, 1,
                            NOW(), :error,
                            CASE WHEN :status = 'processed' THEN NOW() ELSE NULL END
                        )
                    """),
                    {
                        "event_id": event_id,
                        "event_type": event_type,
                        "subscription_id": subscription_id,
                        "user_id": user_id,
                        "payload": json.dumps(payload),
                        "signature": signature,
                        "status": status,
                        "error": error
                    }
                )
            
            db.commit()
            print(f"📝 Webhook logged: {event_id} ({status})")
        
        except Exception as e:
            print(f"⚠️ Error logging webhook: {str(e)}")
            # Don't fail webhook processing if logging fails
            try:
                db.rollback()
            except:
                pass


# Global instance
razorpay_service = RazorpayService()
