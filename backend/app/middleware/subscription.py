from fastapi import Request, HTTPException, status
from app.services.supabase_helper import supabase
from app.config.plans import get_scan_limit, PLAN_LIMITS
from typing import Optional, Tuple, Dict
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
import os

async def check_subscription(user_id: str, db: Optional[Session] = None) -> Tuple[bool, str]:
    """
    Check if user has exceeded their subscription limits.
    Returns dynamically calculated usage based on current month.
    
    Args:
        user_id: User ID to check
        db: Optional database session
    
    Returns:
        Tuple of (allowed: bool, message: str)
    
    Raises:
        HTTPException: If limit exceeded or user not found
    """
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not authenticated"
        )

    try:
        # Get current month dynamically - FIXED
        now = datetime.utcnow()
        current_month = now.strftime("%Y-%m")  # e.g., "2025-10"
        
        print(f"📊 Checking subscription for user {user_id}, month: {current_month}")

        # Get user's subscription and current usage
        # Use execute() and check data array to handle missing subscriptions gracefully
        subscription_response = supabase.table("subscriptions").select("*").eq("user_id", user_id).execute()
        
        if not subscription_response.data or len(subscription_response.data) == 0:
            # No subscription - default to free
            print(f"ℹ️ No subscription found for {user_id}, defaulting to free tier")
            user_tier = "free"
            scans_used = 0
        else:
            subscription = subscription_response.data[0]  # Get first result
            user_tier = subscription.get("tier", "free")
            scans_used = subscription.get("scans_used_this_period", 0)
            
            # Check if subscription is active
            if subscription.get("status") != "active":
                print(f"⚠️ Subscription inactive for user {user_id}")
                user_tier = "free"  # Downgrade to free
                scans_used = 0

        # Get plan limits
        plan_config = PLAN_LIMITS.get(user_tier, PLAN_LIMITS["free"])
        monthly_limit = plan_config["scans_per_month"]

        # Check if limit exceeded
        if scans_used >= monthly_limit:
            print(f"❌ User {user_id} ({user_tier}) has exceeded limit: {scans_used}/{monthly_limit}")
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail=f"Monthly scan limit exceeded. Used: {scans_used}/{monthly_limit}. Upgrade your plan for higher limits."
            )

        print(f"✅ Subscription check passed: {user_tier} - {scans_used}/{monthly_limit} scans used")
        return True, f"User {user_id} ({user_tier}) has {monthly_limit - scans_used} scans remaining"

    except HTTPException:
        raise
    except Exception as e:
        # Log error but don't block requests (fail-open for reliability)
        print(f"⚠️ Subscription check error for user {user_id}: {str(e)}")
        # Allow request to proceed but log the warning
        return True, "Subscription check bypassed due to error"


async def check_and_renew_subscription(user_id: str, db: Optional[Session] = None) -> Dict:
    """
    Check if subscription needs renewal and handle auto-renewal.
    Resets monthly scan count if period expired.
    
    Args:
        user_id: User ID
        db: Optional database session
    
    Returns:
        Subscription renewal status
    """
    try:
        subscription_response = supabase.table("subscriptions").select("*").eq("user_id", user_id).execute()
        
        if not subscription_response.data or len(subscription_response.data) == 0:
            print(f"⚠️ No subscription found for user {user_id}")
            return {"status": "none", "renewed": False}
        
        subscription = subscription_response.data[0]  # Get first result
        now = datetime.utcnow()
        period_end = datetime.fromisoformat(subscription.get("current_period_end"))
        
        # Check if period has ended
        if period_end < now:
            print(f"⏰ Subscription period ended for user {user_id}")
            
            # Check if auto-renewal is enabled
            if subscription.get("auto_renew", False):
                print(f"🔄 Auto-renewing subscription for user {user_id}")
                
                # Calculate new period
                new_period_start = now
                new_period_end = now + timedelta(days=30)
                
                # Reset scan count and renew
                renewal_response = supabase.table("subscriptions").update({
                    "status": "active",
                    "current_period_start": new_period_start.isoformat(),
                    "current_period_end": new_period_end.isoformat(),
                    "scans_used_this_period": 0,
                    "last_renewal_at": now.isoformat()
                }).eq("user_id", user_id).execute()
                
                print(f"✅ Auto-renewal completed for user {user_id}")
                return {"status": "renewed", "renewed": True, "period_end": new_period_end.isoformat()}
            else:
                print(f"❌ Auto-renewal disabled for user {user_id}")
                
                # Mark as expired
                supabase.table("subscriptions").update({
                    "status": "expired"
                }).eq("user_id", user_id).execute()
                
                return {"status": "expired", "renewed": False}
        
        return {"status": "active", "renewed": False}
    
    except Exception as e:
        print(f"⚠️ Renewal check error for user {user_id}: {str(e)}")
        return {"status": "error", "renewed": False, "error": str(e)}


async def increment_usage(user_id: str, amount: int = 1) -> bool:
    """
    Increment scan usage for current month.
    
    Args:
        user_id: User ID
        amount: Number of scans to add (default 1)
    
    Returns:
        True if incremented successfully
    """
    try:
        now = datetime.utcnow()
        current_month = now.strftime("%Y-%m")
        
        # Update scan count
        subscription_response = supabase.table("subscriptions").select("*").eq("user_id", user_id).execute()
        
        if subscription_response.data and len(subscription_response.data) > 0:
            current_scans = subscription_response.data[0].get("scans_used_this_period", 0)
            
            supabase.table("subscriptions").update({
                "scans_used_this_period": current_scans + amount
            }).eq("user_id", user_id).execute()
            
            print(f"📈 Incremented scans for {user_id}: +{amount}")
            return True
        
        return False
        
    except Exception as e:
        print(f"⚠️ Failed to increment usage for {user_id}: {str(e)}")
        return False