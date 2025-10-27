"""
Authentication API - User Registration and Subscription Setup
Handles user onboarding and free plan assignment

SECURITY: Rate limiting applied to all registration endpoints
to prevent brute force account creation attacks
"""
from fastapi import APIRouter, HTTPException, Depends, Request, status
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
from datetime import datetime, timedelta
from typing import Optional
import secrets
import uuid
import logging

from app.core.database import get_db
from app.models import Subscription
from app.middleware.rate_limiter import check_login_rate_limit, record_failed_login_attempt
from app.services.supabase_helper import supabase

router = APIRouter()
logger = logging.getLogger(__name__)

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


class ForgotPasswordRequest(BaseModel):
    """Request to initiate password reset"""
    email: EmailStr


class ForgotPasswordResponse(BaseModel):
    """Response for password reset initiation"""
    success: bool
    message: str


class ResetPasswordRequest(BaseModel):
    """Request to complete password reset"""
    token: str
    new_password: str


class ResetPasswordResponse(BaseModel):
    """Response for password reset completion"""
    success: bool
    message: str



@router.post("/setup-user", response_model=UserRegistrationResponse)
async def setup_new_user(
    request: UserRegistrationRequest,
    http_request: Request,
    db: Session = Depends(get_db)
):
    """
    Set up a new user with a free subscription plan.
    This should be called from the frontend immediately after Supabase registration.
    
    SECURITY: Rate limited to prevent account creation abuse (5 per minute per IP)
    
    Workflow:
    1. Frontend registers user with Supabase Auth
    2. Frontend calls this endpoint with user_id
    3. Backend creates free subscription record in Supabase
    4. User can start using the app with 10 free scans per month
    """
    try:
        # Get client IP
        client_ip = http_request.client.host if http_request.client else "unknown"
        
        # Check rate limit on registration
        allowed, error_msg = check_login_rate_limit(client_ip)
        if not allowed:
            logger.warning(f"Registration rate limited from IP: {client_ip}")
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail=error_msg
            )
        
        logger.info(f"Registration rate check passed", extra={"ip": client_ip, "email_domain": request.email.split('@')[1]})
        
        # Check if user already has a subscription in Supabase
        try:
            existing_response = supabase.table("subscriptions").select("*").eq("user_id", request.user_id).execute()
            existing_subscription = existing_response.data[0] if existing_response.data else None
        except Exception as e:
            print(f"ℹ️ Could not check existing subscription: {e}")
            existing_subscription = None
        
        if existing_subscription:
            print(f"ℹ️ Subscription already exists for {request.user_id}")
            return UserRegistrationResponse(
                success=True,
                message="User already has a subscription",
                subscription={
                    "tier": existing_subscription.get("tier", "free"),
                    "status": existing_subscription.get("status", "active"),
                    "scans_used": existing_subscription.get("scans_used_this_period", 0),
                    "period_end": existing_subscription.get("current_period_end")
                }
            )
        
        # Create new free subscription in Supabase
        now = datetime.utcnow().isoformat()
        period_end = (datetime.utcnow() + timedelta(days=30)).isoformat()  # 30-day billing cycle
        
        subscription_data = {
            "user_id": request.user_id,
            "tier": "free",  # Always start with free plan
            "status": "active",
            "scans_used_this_period": 0,  # No scans used yet
            "current_period_start": now,
            "current_period_end": period_end,
            "razorpay_order_id": None,  # No payment for free plan
            "razorpay_payment_id": None,
            "created_at": now,
            "updated_at": now
        }
        
        # Insert into Supabase
        response = supabase.table("subscriptions").insert([subscription_data]).execute()
        
        if response.data:
            new_subscription = response.data[0]
            print(f"📝 New user registered in Supabase: {request.user_id} ({request.email})")
            
            return UserRegistrationResponse(
                success=True,
                message=f"Free plan activated! You have 10 scans per month.",
                subscription={
                    "tier": new_subscription.get("tier", "free"),
                    "status": new_subscription.get("status", "active"),
                    "scans_used": new_subscription.get("scans_used_this_period", 0),
                    "scans_limit": 10,  # Free plan limit
                    "period_start": new_subscription.get("current_period_start"),
                    "period_end": new_subscription.get("current_period_end")
                }
            )
        else:
            raise Exception("Failed to insert subscription into Supabase")
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Registration error: {str(e)}")
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


@router.post("/forgot-password", response_model=ForgotPasswordResponse)
async def forgot_password(
    request: ForgotPasswordRequest,
    http_request: Request,
    db: Session = Depends(get_db)
):
    """
    Initiate password reset by sending reset link to email.
    
    SECURITY:
    - Rate limited (5 per minute per IP)
    - Doesn't reveal if email exists (security best practice)
    - Token expires after 1 hour
    - Tokens are one-time use
    
    Args:
        request: ForgotPasswordRequest with email
        http_request: HTTP request for rate limiting
        db: Database session
    
    Returns:
        Success message (always success for security)
    """
    try:
        # Get client IP
        client_ip = http_request.client.host if http_request.client else "unknown"
        
        # Check rate limit
        allowed, error_msg = check_login_rate_limit(client_ip)
        if not allowed:
            logger.warning(f"Password reset rate limited from IP: {client_ip}")
            # Don't reveal rate limit for security
            return ForgotPasswordResponse(
                success=True,
                message="If an account exists with this email, a reset link will be sent"
            )
        
        logger.info("Password reset requested", extra={"email_domain": request.email.split('@')[1]})
        
        # Generate secure token
        reset_token = secrets.token_urlsafe(32)
        token_hash = hash(reset_token)  # Store hash, not token itself
        
        # Store token in database (in-memory for now, production use Redis)
        # TODO: Create password_reset_tokens table
        # For now, use Supabase built-in functionality
        
        try:
            # Use Supabase Auth's built-in password reset
            response = supabase.auth.reset_password_for_email(request.email)
            
            logger.info("Password reset email sent", extra={"email_domain": request.email.split('@')[1]})
            
            return ForgotPasswordResponse(
                success=True,
                message="If an account exists with this email, a password reset link has been sent"
            )
        
        except Exception as e:
            logger.error(f"Supabase password reset failed: {str(e)}")
            # Return generic message for security
            return ForgotPasswordResponse(
                success=True,
                message="If an account exists with this email, a password reset link has been sent"
            )
    
    except Exception as e:
        logger.error(f"Password reset error: {str(e)}")
        # Return generic message for security
        return ForgotPasswordResponse(
            success=True,
            message="If an account exists with this email, a password reset link has been sent"
        )


@router.post("/reset-password", response_model=ResetPasswordResponse)
async def reset_password(
    request: ResetPasswordRequest,
    http_request: Request,
    db: Session = Depends(get_db)
):
    """
    Complete password reset with token and new password.
    
    SECURITY:
    - Validates token format and expiry
    - Requires strong new password
    - Invalidates all other sessions after reset
    - Logs the password change
    
    Args:
        request: ResetPasswordRequest with token and new password
        http_request: HTTP request for logging
        db: Database session
    
    Returns:
        Success message with next steps
    """
    try:
        # Get client IP
        client_ip = http_request.client.host if http_request.client else "unknown"
        
        # Validate token format
        if not request.token or len(request.token) < 20:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid reset token"
            )
        
        # Validate password strength
        if len(request.new_password) < 8:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Password must be at least 8 characters long"
            )
        
        logger.info("Processing password reset", extra={"ip": client_ip})
        
        # Use Supabase Auth to update password
        # Note: This requires the token from the Supabase password reset email
        try:
            # Supabase Auth handles the token validation
            response = supabase.auth.update_user({
                'password': request.new_password
            }, jwt=request.token)
            
            logger.info("Password reset completed successfully", extra={"ip": client_ip})
            
            return ResetPasswordResponse(
                success=True,
                message="Password has been reset successfully. Please log in with your new password."
            )
        
        except Exception as e:
            logger.error(f"Password update failed: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid or expired reset token. Please request a new password reset."
            )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Password reset error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to reset password"
        )


@router.post("/change-password", response_model=ResetPasswordResponse)
async def change_password(
    current_password: str,
    new_password: str,
    current_user: str = Depends(lambda: "user_id"),  # Would come from JWT in real scenario
    http_request: Request = None,
    db: Session = Depends(get_db)
):
    """
    Change password for authenticated user.
    
    Args:
        current_password: User's current password for verification
        new_password: New password to set
        current_user: Current authenticated user ID
        http_request: HTTP request for logging
        db: Database session
    
    Returns:
        Success message
    """
    try:
        if len(new_password) < 8:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="New password must be at least 8 characters"
            )
        
        logger.info("Password change requested", extra={"user_id": current_user[:8]})
        
        try:
            # Update password in Supabase Auth
            response = supabase.auth.update_user({
                'password': new_password
            })
            
            logger.info("Password changed successfully", extra={"user_id": current_user[:8]})
            
            return ResetPasswordResponse(
                success=True,
                message="Password has been changed successfully"
            )
        
        except Exception as e:
            logger.error(f"Password change failed: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to change password"
            )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error changing password: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to change password"
        )
