"""
Payment API Endpoints - Production Grade
Handles Razorpay payment operations with full security checks
"""

from fastapi import APIRouter, Depends, HTTPException, status, Request, Header
from sqlalchemy.orm import Session
from typing import Optional
from pydantic import BaseModel
from datetime import datetime
from slowapi import Limiter
from slowapi.util import get_remote_address

from app.core.database import get_db
from app.services.razorpay_service import razorpay_service
from app.auth import get_current_user, verify_user_ownership

# Config, rate limiter and caching helpers
from app.core.config import settings
from app.core.redis_limiter import get_rate_limiter, get_tier_limit
from app.core.caching import get_redis_client


router = APIRouter()

# Rate limiter for payment endpoints
limiter = Limiter(key_func=get_remote_address)


# Request/Response Models
class CreateOrderRequest(BaseModel):
    """Request to create payment order"""
    tier: str
    billing_cycle: str = "monthly"


class CreateOrderResponse(BaseModel):
    """Payment order details"""
    order_id: str
    amount: int
    amount_paise: int
    currency: str
    tier: str
    billing_cycle: str
    plan_name: str
    key_id: str


class VerifyPaymentRequest(BaseModel):
    """Request to verify payment"""
    razorpay_order_id: str
    razorpay_payment_id: str
    razorpay_signature: str


class VerifyPaymentResponse(BaseModel):
    """Payment verification response"""
    success: bool
    message: str
    subscription: Optional[dict]
    # FIX #4: Add feature confirmation fields
    features: Optional[dict] = None
    tier: Optional[str] = None
    plan_name: Optional[str] = None
    scan_limit: Optional[int] = None
    storage_days: Optional[int] = None


@router.post("/create-order", response_model=CreateOrderResponse)
@limiter.limit("10/minute")  # Rate limit: 10 order creations per minute per IP
async def create_payment_order(
    request_obj: Request,  # Changed from 'request' to avoid conflict
    create_request: CreateOrderRequest,
    current_user: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Create Razorpay payment order for subscription.
    
    Security: Only authenticated users can create orders for themselves.
    Rate Limited: 10 requests per minute per IP to prevent abuse.
    
    Args:
        request_obj: FastAPI request object
        create_request: Order creation request with tier and billing cycle
        current_user: Current authenticated user (from JWT token)
        db: Database session
    
    Returns:
        Order details including Razorpay order ID
    """
    try:
        print(f"🔒 Creating order for user {current_user}")
        
        # Validate tier
        valid_tiers = ["free", "basic", "pro", "ultra", "max"]
        if create_request.tier.lower() not in valid_tiers:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid tier '{create_request.tier}'. Valid tiers: {valid_tiers}"
            )
        
        # Validate billing cycle
        if create_request.billing_cycle not in ["monthly", "yearly"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="billing_cycle must be 'monthly' or 'yearly'"
            )
        
        # Check if free tier (can't create order for free)
        if create_request.tier.lower() == "free":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot create payment order for free tier"
            )

        # FIX #2: Fetch user email and name from Supabase auth
        from app.services.supabase_helper import supabase
        try:
            auth_user = supabase.auth.admin.get_user(current_user)
            user_email = getattr(auth_user.user, 'email', 'user@example.com') if auth_user.user else 'user@example.com'
            # Try to get user metadata for full name
            user_metadata = getattr(auth_user.user, 'user_metadata', {}) if auth_user.user else {}
            user_name = user_metadata.get('full_name', user_metadata.get('name', 'User')) if user_metadata else 'User'
        except Exception as e:
            print(f"⚠️ Could not fetch user details from Supabase: {str(e)}")
            user_email = 'user@example.com'
            user_name = 'User'
        
        # RATE LIMIT: Use Redis rate limiter per-user based on their current tier
        try:
            rate_limiter = get_rate_limiter()
            # Determine user tier (fallback to free)
            try:
                from app.models import Subscription
                sub = db.query(Subscription).filter(Subscription.user_id == current_user).order_by(Subscription.id.desc()).first()
                user_tier = getattr(sub, 'tier', 'free') if sub else 'free'
            except Exception:
                user_tier = 'free'

            limit, window = get_tier_limit(user_tier, 'scan')
            allowed, info = rate_limiter.is_allowed(current_user, 'create_order', limit=limit if limit else 10, window_seconds=60)
            if not allowed:
                retry_after = info.get('retry_after') if isinstance(info, dict) else None
                raise HTTPException(status_code=status.HTTP_429_TOO_MANY_REQUESTS, detail=f"Rate limit exceeded. Retry after {retry_after or 'some'} seconds")
        except Exception as e:
            # If rate limiter fails, continue but log warning
            print(f"⚠️ Rate limiter check failed: {e}")

        # Create order with user_id in notes (for verification later)
        order = razorpay_service.create_subscription_order(
            user_id=current_user,
            tier=create_request.tier.lower(),
            billing_cycle=create_request.billing_cycle,
            user_email=user_email,
            user_name=user_name,
            db=db
        )

        print(f"✅ Order created: {order['order_id']}")
        return CreateOrderResponse(**order)
    
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        print(f"❌ Error creating order: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create order: {str(e)}"
        )


@router.post("/verify", response_model=VerifyPaymentResponse)
async def verify_payment(
    request: VerifyPaymentRequest,
    current_user: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Verify Razorpay payment and activate subscription.
    
    Security: 
    - Validates JWT token
    - Checks payment signature
    - Verifies payment amount matches order
    - Confirms user_id in order notes matches current user
    - Prevents duplicate payment processing
    
    Args:
        request: Payment verification details (order_id, payment_id, signature)
        current_user: Current authenticated user (from JWT token)
        db: Database session
    
    Returns:
        Verification result and subscription details
    """
    try:
        print(f"🔒 Verifying payment for user {current_user}")
        print(f"   Order: {request.razorpay_order_id}")
        print(f"   Payment: {request.razorpay_payment_id}")
        
        # RATE LIMIT: Protect verify endpoint per-user
        try:
            rate_limiter = get_rate_limiter()
            try:
                from app.models import Subscription
                sub = db.query(Subscription).filter(Subscription.user_id == current_user).order_by(Subscription.id.desc()).first()
                user_tier = getattr(sub, 'tier', 'free') if sub else 'free'
            except Exception:
                user_tier = 'free'

            vlimit, vwindow = get_tier_limit(user_tier, 'scan')
            allowed_v, info_v = rate_limiter.is_allowed(current_user, 'verify_payment', limit=vlimit if vlimit else 20, window_seconds=60)
            if not allowed_v:
                retry_after = info_v.get('retry_after') if isinstance(info_v, dict) else None
                raise HTTPException(status_code=status.HTTP_429_TOO_MANY_REQUESTS, detail=f"Rate limit exceeded. Retry after {retry_after or 'some'} seconds")
        except HTTPException:
            raise
        except Exception as e:
            print(f"⚠️ Rate limiter (verify) failed: {e}")

        # Step 1: Verify payment signature
        if not razorpay_service.verify_payment_signature(
            request.razorpay_order_id,
            request.razorpay_payment_id,
            request.razorpay_signature
        ):
            print(f"❌ Invalid payment signature")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid payment signature - possible fraud attempt"
            )
        print(f"✅ Signature verified")
        
        # Step 2: Fetch order and verify it exists
        try:
            order = razorpay_service.client.order.fetch(request.razorpay_order_id)
        except Exception as e:
            print(f"❌ Could not fetch order: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Could not fetch order details from payment provider"
            )
        
        # Step 3: CRITICAL SECURITY CHECK - Verify order belongs to current user
        order_notes = order.get("notes", {})
        order_user_id = order_notes.get("user_id")
        
        if order_user_id != current_user:
            print(f"❌ FRAUD DETECTED: Order user_id {order_user_id} != current user {current_user}")
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Payment order does not belong to current user - fraud detected"
            )
        print(f"✅ Order ownership verified")
        
        # Step 4: Fetch payment details
        try:
            payment = razorpay_service.client.payment.fetch(request.razorpay_payment_id)
        except Exception as e:
            print(f"❌ Could not fetch payment: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Could not fetch payment details"
            )
        
        # Step 5: Verify payment was actually captured
        payment_status = payment.get("status")
        if payment_status != "captured":
            print(f"❌ Payment not captured. Status: {payment_status}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Payment not captured. Status: {payment_status}"
            )
        print(f"✅ Payment captured")
        
        # Step 6: Verify payment amount matches order amount
        payment_amount = payment.get("amount")
        order_amount = order.get("amount")
        
        if payment_amount != order_amount:
            print(f"❌ Amount mismatch: paid {payment_amount} vs order {order_amount}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Payment amount does not match order amount"
            )
        print(f"✅ Amount verified: {payment_amount} paise")
        
        # Step 7: Check if payment was already processed (prevent duplicates)
        from app.models import Subscription
        existing = db.query(Subscription).filter(
            Subscription.razorpay_payment_id == request.razorpay_payment_id
        ).first()
        
        if existing:
            print(f"⚠️ Payment already processed for {existing.user_id}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="This payment has already been processed"
            )
        print(f"✅ No duplicate payment")
        
        # Step 8: NOW SAFE - Process payment with transaction isolation (FIX #1)
        # Use db.begin_nested() to create a SAVEPOINT for atomicity
        try:
            savepoint = db.begin_nested()
            
            success, message, subscription_data = razorpay_service.process_successful_payment(
                order_id=request.razorpay_order_id,
                payment_id=request.razorpay_payment_id,
                signature=request.razorpay_signature,
                db=db
            )
            
            if not success:
                print(f"❌ Payment processing failed: {message}")
                savepoint.rollback()  # Rollback the savepoint
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=message
                )
            
            # FIX #1: Flush writes to ensure subscription is committed
            # This forces the DB to execute the INSERT/UPDATE but doesn't COMMIT yet
            db.flush()
            print(f"✅ Subscription changes flushed to database")
            
            # Now commit the savepoint (atomic transaction)
            savepoint.commit()
            print(f"✅ Transaction committed successfully")
            
        except Exception as e:
            print(f"❌ Transaction error: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Payment processing transaction failed: {str(e)}"
            )
        
        print(f"✅ Payment verified and processed successfully")
        
        # Log successful payment
        log_payment_event(current_user, request.razorpay_order_id, "success", db)
        
        # FIX #4: Build feature confirmation response
        from app.config.plans import get_plan_config
        tier = subscription_data.get('tier') if subscription_data else 'free'
        plan = get_plan_config(tier)
        
        features_dict = {
            "invoice_processing": True,
            "csv_export": True,
            "excel_export": True,
            "pdf_export": True,
            "api_access": tier != "free"
        }
        
        return VerifyPaymentResponse(
            success=True,
            message=message,
            subscription=subscription_data,
            # FIX #4: Add feature confirmation fields so frontend knows immediately
            features=features_dict,
            tier=tier,
            plan_name=plan.get('name'),
            scan_limit=plan.get('scans_per_month'),
            storage_days=plan.get('storage_days')
        )
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Payment verification error: {str(e)}")
        # Log failed payment
        log_payment_event(current_user, request.razorpay_order_id, "failed", db, str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Payment verification failed: {str(e)}"
        )


@router.post("/webhook")
async def razorpay_webhook(
    request: Request,
    db: Session = Depends(get_db),
    x_razorpay_signature: Optional[str] = Header(None)
):
    """
    Handle Razorpay webhook events.
    
    Note: Webhooks don't have user context, so we verify signature and extract
    user_id from order notes.
    
    Args:
        request: FastAPI request object
        db: Database session
        x_razorpay_signature: Webhook signature from Razorpay header
    
    Returns:
        Success response
    """
    try:
        # Get webhook body (raw json payload)
        body = await request.json()

        # Signature must be present and webhook secret must be configured
        signature = x_razorpay_signature or ""
        webhook_secret = getattr(settings, 'RAZORPAY_WEBHOOK_SECRET', '')
        if not webhook_secret:
            print("🚨 RAZORPAY_WEBHOOK_SECRET not configured - rejecting webhook")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Webhook secret not configured")

        if not signature:
            print("🚨 Webhook signature header missing")
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Missing webhook signature header")

        # Idempotency: prevent duplicate processing of same payment
        try:
            redis_client = get_redis_client()
        except Exception:
            redis_client = None

        payment_id = None
        try:
            event_payload = body.get('payload', {})
            payment = event_payload.get('payment', {})
            entity = payment.get('entity', {})
            payment_id = entity.get('id')
        except Exception:
            payment_id = None

        if payment_id and redis_client:
            processed_key = f"processed_payment:{payment_id}"
            try:
                # SETNX semantics: only set if not exists
                set_ok = redis_client.set(processed_key, '1', nx=True, ex=60*60*24)
                if not set_ok:
                    # Already processed
                    print(f"⚠️ Webhook already processed for payment {payment_id}")
                    return {"status": "success", "message": "Already processed"}
            except Exception as e:
                print(f"⚠️ Redis idempotency check failed: {e}")

        # Process webhook (service will verify signature using webhook secret)
        success, message = razorpay_service.handle_webhook(
            event=body,
            signature=signature,
            db=db
        )
        
        if not success:
            print(f"⚠️ Webhook processing failed: {message}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=message
            )
        
        print(f"✅ Webhook processed: {message}")
        return {
            "status": "success",
            "message": message
        }
    
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Webhook error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Webhook processing failed: {str(e)}"
        )


@router.get("/config")
async def get_payment_config():
    """
    Get Razorpay configuration for frontend.
    
    Returns:
        Razorpay key ID and other config for checkout
    """
    return {
        "key_id": razorpay_service.key_id,
        "currency": "INR",
        "description": "TrulyInvoice Subscription",
        "image": "/logo.png"
    }


@router.post("/cancel-subscription")
async def cancel_subscription(
    current_user: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Cancel user's subscription.
    
    Args:
        current_user: Current authenticated user (from JWT token)
        db: Database session
    
    Returns:
        Cancellation confirmation
    """
    try:
        print(f"🔒 Cancelling subscription for user {current_user}")
        
        success, message = razorpay_service.cancel_subscription(
            user_id=current_user,
            db=db
        )
        
        if not success:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=message
            )
        
        print(f"✅ Subscription cancelled")
        log_payment_event(current_user, "cancel", "cancelled", db)
        
        return {
            "success": True,
            "message": message
        }
    
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Cancellation error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Cancellation failed: {str(e)}"
        )


def log_payment_event(user_id: str, order_id: str, status: str, db: Session, error: str = None):
    """
    Log payment events for audit trail.
    
    Args:
        user_id: User ID
        order_id: Razorpay order ID
        status: Payment status (success, failed, cancelled)
        db: Database session
        error: Optional error message
    """
    try:
        # TODO: Create payment_logs table and log here
        print(f"📝 Payment event logged: user={user_id}, order={order_id}, status={status}")
    except Exception as e:
        print(f"⚠️ Failed to log payment event: {str(e)}")
