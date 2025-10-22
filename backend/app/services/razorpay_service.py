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
        if not self.client:
            # Return mock order for development
            return {
                "id": f"order_mock_{datetime.utcnow().timestamp()}",
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
            subscription.tier = tier
            subscription.status = "active"
            subscription.billing_cycle = billing_cycle
            subscription.razorpay_order_id = order_id
            subscription.razorpay_payment_id = payment_id
            subscription.current_period_start = current_period_start
            subscription.current_period_end = current_period_end
            subscription.scans_used_this_period = 0  # Reset scans
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
        Handle Razorpay webhook events
        
        Args:
            event: Webhook event data
            signature: Webhook signature
            db: Database session
        
        Returns:
            Tuple of (success: bool, message: str)
        """
        # Verify webhook signature
        webhook_secret = getattr(settings, 'RAZORPAY_WEBHOOK_SECRET', '')
        
        if webhook_secret:
            # Generate signature
            expected_signature = hmac.new(
                webhook_secret.encode('utf-8'),
                str(event).encode('utf-8'),
                hashlib.sha256
            ).hexdigest()
            
            if not hmac.compare_digest(expected_signature, signature):
                return False, "Invalid webhook signature"
        
        # Process event based on type
        event_type = event.get("event")
        
        if event_type == "payment.captured":
            # Payment successful
            payload = event.get("payload", {})
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
                return success, message
        
        elif event_type == "payment.failed":
            # Payment failed - log it
            return True, "Payment failed event logged"
        
        return True, f"Webhook event {event_type} processed"
    
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


# Global instance
razorpay_service = RazorpayService()
