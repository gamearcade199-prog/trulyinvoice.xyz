"""
Authentication API - User Registration and Subscription Setup
Handles user onboarding and free plan assignment
"""
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
from datetime import datetime, timedelta
from typing import Optional

from app.core.database import get_db
from app.models import Subscription

router = APIRouter()

# Request/Response Models
class UserRegistrationRequest(BaseModel):
    """Request to set up a new user's subscription after Supabase auth"""
    user_id: str  # Supabase user ID
    email: EmailStr
    full_name: Optional[str] = None
    company_name: Optional[str] = None

class UserRegistrationResponse(BaseModel):
    """Response after successful user setup"""
    success: bool
    message: str
    subscription: dict

class SubscriptionSetupRequest(BaseModel):
    """Request to manually set up or reset a user's subscription"""
    user_id: str
    tier: str = "free"  # Default to free plan


@router.post("/setup-user", response_model=UserRegistrationResponse)
async def setup_new_user(
    request: UserRegistrationRequest,
    db: Session = Depends(get_db)
):
    """
    Set up a new user with a free subscription plan.
    This should be called from the frontend immediately after Supabase registration.
    
    Workflow:
    1. Frontend registers user with Supabase Auth
    2. Frontend calls this endpoint with user_id
    3. Backend creates free subscription record
    4. User can start using the app with 10 free scans per month
    """
    try:
        # Check if user already has a subscription
        existing_subscription = db.query(Subscription).filter(
            Subscription.user_id == request.user_id
        ).first()
        
        if existing_subscription:
            return UserRegistrationResponse(
                success=True,
                message="User already has a subscription",
                subscription={
                    "tier": existing_subscription.tier,
                    "status": existing_subscription.status,
                    "scans_used": existing_subscription.scans_used_this_period,
                    "period_end": existing_subscription.current_period_end.isoformat()
                }
            )
        
        # Create new free subscription
        now = datetime.utcnow()
        period_end = now + timedelta(days=30)  # 30-day billing cycle
        
        new_subscription = Subscription(
            user_id=request.user_id,
            tier="free",  # Always start with free plan
            status="active",
            scans_used_this_period=0,  # No scans used yet
            current_period_start=now,
            current_period_end=period_end,
            razorpay_order_id=None,  # No payment for free plan
            razorpay_payment_id=None,
            created_at=now,
            updated_at=now
        )
        
        db.add(new_subscription)
        db.commit()
        db.refresh(new_subscription)
        
        return UserRegistrationResponse(
            success=True,
            message=f"Free plan activated! You have 10 scans per month.",
            subscription={
                "tier": new_subscription.tier,
                "status": new_subscription.status,
                "scans_used": new_subscription.scans_used_this_period,
                "scans_limit": 10,  # Free plan limit
                "period_start": new_subscription.current_period_start.isoformat(),
                "period_end": new_subscription.current_period_end.isoformat()
            }
        )
        
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Failed to set up user subscription: {str(e)}"
        )


@router.post("/setup-subscription", response_model=UserRegistrationResponse)
async def setup_subscription(
    request: SubscriptionSetupRequest,
    db: Session = Depends(get_db)
):
    """
    Manually create or reset a user's subscription.
    Useful for admin operations or fixing user accounts.
    """
    try:
        # Check if user already has a subscription
        existing_subscription = db.query(Subscription).filter(
            Subscription.user_id == request.user_id
        ).first()
        
        if existing_subscription:
            # Update existing subscription
            existing_subscription.tier = request.tier
            existing_subscription.status = "active"
            existing_subscription.scans_used_this_period = 0
            existing_subscription.current_period_start = datetime.utcnow()
            existing_subscription.current_period_end = datetime.utcnow() + timedelta(days=30)
            existing_subscription.updated_at = datetime.utcnow()
            
            db.commit()
            db.refresh(existing_subscription)
            
            return UserRegistrationResponse(
                success=True,
                message=f"Subscription updated to {request.tier} plan",
                subscription={
                    "tier": existing_subscription.tier,
                    "status": existing_subscription.status,
                    "scans_used": existing_subscription.scans_used_this_period,
                    "period_end": existing_subscription.current_period_end.isoformat()
                }
            )
        
        # Create new subscription
        now = datetime.utcnow()
        period_end = now + timedelta(days=30)
        
        new_subscription = Subscription(
            user_id=request.user_id,
            tier=request.tier,
            status="active",
            scans_used_this_period=0,
            current_period_start=now,
            current_period_end=period_end,
            created_at=now,
            updated_at=now
        )
        
        db.add(new_subscription)
        db.commit()
        db.refresh(new_subscription)
        
        return UserRegistrationResponse(
            success=True,
            message=f"{request.tier.title()} plan activated",
            subscription={
                "tier": new_subscription.tier,
                "status": new_subscription.status,
                "scans_used": new_subscription.scans_used_this_period,
                "period_end": new_subscription.current_period_end.isoformat()
            }
        )
        
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Failed to set up subscription: {str(e)}"
        )


@router.get("/subscription/{user_id}")
async def get_user_subscription(
    user_id: str,
    db: Session = Depends(get_db)
):
    """
    Get a user's current subscription details.
    Returns subscription info or indicates if user needs setup.
    """
    try:
        subscription = db.query(Subscription).filter(
            Subscription.user_id == user_id
        ).first()
        
        if not subscription:
            return {
                "success": False,
                "message": "User needs subscription setup",
                "subscription": None
            }
        
        # Import plan config to get limits
        from app.config.plans import get_plan_config
        plan_config = get_plan_config(subscription.tier)
        
        return {
            "success": True,
            "subscription": {
                "tier": subscription.tier,
                "status": subscription.status,
                "scans_used": subscription.scans_used_this_period,
                "scans_limit": plan_config["limits"]["scans_per_month"],
                "scans_remaining": max(0, plan_config["limits"]["scans_per_month"] - subscription.scans_used_this_period),
                "period_start": subscription.current_period_start.isoformat(),
                "period_end": subscription.current_period_end.isoformat(),
                "auto_renew": subscription.auto_renew,
                "features": plan_config["features"]
            }
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get subscription: {str(e)}"
        )
