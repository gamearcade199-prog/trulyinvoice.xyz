"""
Subscription API Endpoints
Manages user subscriptions, plans, and upgrades
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime

from app.core.database import get_db
from app.auth import get_current_user
from app.models import Subscription
from app.config.plans import (
    get_all_plans, 
    get_plan_config, 
    upgrade_allowed, 
    downgrade_allowed,
    FEATURE_DESCRIPTIONS,
    PlanTier
)
from app.services.usage_tracker import UsageTracker


router = APIRouter(prefix="/api/subscriptions", tags=["subscriptions"])


# Response Models
class PlanResponse(BaseModel):
    """Plan details response"""
    tier: str
    name: str
    price_monthly: int
    price_yearly: int
    scans_per_month: int
    storage_days: int
    bulk_upload_limit: int
    ai_accuracy: str
    features: List[str]
    feature_descriptions: dict
    rate_limits: dict


class CurrentSubscriptionResponse(BaseModel):
    """Current subscription details"""
    user_id: str
    tier: str
    tier_name: str
    status: str
    scans_used: int
    scans_limit: int
    scans_remaining: int
    usage_percentage: float
    period_start: str
    period_end: str
    bulk_upload_limit: int
    can_upgrade: bool
    can_downgrade: bool
    recommended_upgrade: Optional[str]


class UsageResponse(BaseModel):
    """Usage statistics response"""
    user_id: str
    tier: str
    tier_name: str
    scans_used: int
    scans_limit: int
    scans_remaining: int
    usage_percentage: float
    period_start: str
    period_end: str
    bulk_upload_limit: int


class UpgradeRequest(BaseModel):
    """Request to upgrade/change plan"""
    target_tier: str
    billing_cycle: str = "monthly"  # monthly or yearly


class UpgradeResponse(BaseModel):
    """Response after plan change"""
    success: bool
    message: str
    old_tier: str
    new_tier: str
    effective_date: str


@router.get("/plans", response_model=List[PlanResponse])
async def get_all_pricing_plans():
    """
    Get all available pricing plans
    
    Returns:
        List of all plans with details
    """
    plans = get_all_plans()
    
    response = []
    for tier, plan in plans.items():
        # Get feature descriptions
        feature_descs = {}
        for feature in plan["features"]:
            feature_descs[feature] = FEATURE_DESCRIPTIONS.get(feature, feature)
        
        response.append(PlanResponse(
            tier=tier,
            name=plan["name"],
            price_monthly=plan["price_monthly"],
            price_yearly=plan["price_yearly"],
            scans_per_month=plan["scans_per_month"],
            storage_days=plan["storage_days"],
            bulk_upload_limit=plan["bulk_upload_limit"],
            ai_accuracy=plan["ai_accuracy"],
            features=plan["features"],
            feature_descriptions=feature_descs,
            rate_limits=plan["rate_limits"]
        ))
    
    return response


@router.get("/plans/{tier}", response_model=PlanResponse)
async def get_plan_details(tier: str):
    """
    Get details for a specific plan
    
    Args:
        tier: Plan tier name
    
    Returns:
        Plan details
    """
    try:
        plan = get_plan_config(tier)
        
        # Get feature descriptions
        feature_descs = {}
        for feature in plan["features"]:
            feature_descs[feature] = FEATURE_DESCRIPTIONS.get(feature, feature)
        
        return PlanResponse(
            tier=tier,
            name=plan["name"],
            price_monthly=plan["price_monthly"],
            price_yearly=plan["price_yearly"],
            scans_per_month=plan["scans_per_month"],
            storage_days=plan["storage_days"],
            bulk_upload_limit=plan["bulk_upload_limit"],
            ai_accuracy=plan["ai_accuracy"],
            features=plan["features"],
            feature_descriptions=feature_descs,
            rate_limits=plan["rate_limits"]
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.get("/status", response_model=CurrentSubscriptionResponse)
async def get_subscription_status(
    current_user_id: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get current user's subscription status, usage, and limits
    
    Returns:
        Current subscription information
    """
    tracker = UsageTracker(db)
    
    # Get usage stats
    stats = await tracker.get_usage_stats(current_user_id)
    
    return CurrentSubscriptionResponse(
        user_id=current_user_id,
        tier=stats["tier"],
        tier_name=stats["tier_name"],
        status="active",
        scans_used=stats["scans_used"],
        scans_limit=stats["scans_limit"],
        scans_remaining=stats["scans_remaining"],
        usage_percentage=stats["usage_percentage"],
        period_start=stats["period_start"],
        period_end=stats["period_end"],
        bulk_upload_limit=stats["bulk_upload_limit"],
        can_upgrade=True,
        can_downgrade=stats["tier"] != "free",
        recommended_upgrade=await tracker.get_upgrade_recommendation(current_user_id)
    )

@router.post("/cancel")
async def cancel_subscription(
    current_user_id: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Cancel subscription (revert to free plan)
    
    Returns:
        Cancellation confirmation
    """
    tracker = UsageTracker(db)
    
    # Get current tier
    current_tier = await tracker.get_current_tier(current_user_id)
    
    if current_tier == "free":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You are already on the free plan"
        )
    
    # Downgrade to free
    subscription = await tracker.get_user_subscription(current_user_id)
    
    if subscription:
        subscription.tier = "free"
        subscription.status = "cancelled"
        db.commit()
    
    return {
        "success": True,
        "message": "Subscription cancelled. You have been moved to the free plan",
        "old_tier": current_tier,
        "new_tier": "free",
        "effective_date": datetime.utcnow().isoformat()
    }


@router.get("/history")
async def get_subscription_history(
    current_user_id: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get subscription change history
    
    Returns:
        List of subscription changes
    """
    # TODO: Implement subscription history tracking
    # For now, return current subscription
    
    tracker = UsageTracker(db)
    subscription = await tracker.get_user_subscription(current_user_id)
    
    if not subscription:
        return {"history": []}
    
    return {
        "history": [
            {
                "tier": subscription.tier,
                "status": subscription.status,
                "start_date": subscription.current_period_start.isoformat() if subscription.current_period_start else None,
                "end_date": subscription.current_period_end.isoformat() if subscription.current_period_end else None
            }
        ]
    }


@router.post("/check-quota")
async def check_quota_availability(
    scans_needed: int = 1,
    current_user_id: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Check if user has sufficient quota
    
    Args:
        scans_needed: Number of scans requested
    
    Returns:
        Quota availability status
    """
    tracker = UsageTracker(db)
    has_quota, message = await tracker.check_quota(current_user_id, scans_needed)
    
    if has_quota:
        return {
            "available": True,
            "message": message,
            "scans_needed": scans_needed
        }
    else:
        return {
            "available": False,
            "message": message,
            "scans_needed": scans_needed,
            "upgrade_link": "/pricing"
        }
