"""
Payment API Endpoints
Handles Razorpay payment operations
"""

from fastapi import APIRouter, Depends, HTTPException, status, Request, Header
from sqlalchemy.orm import Session
from typing import Optional
from pydantic import BaseModel

from app.database import get_db
from app.services.razorpay_service import razorpay_service
from app.auth import get_current_user


router = APIRouter()


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


@router.post("/create-order", response_model=CreateOrderResponse)
async def create_payment_order(
    request: CreateOrderRequest,
    current_user: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Create Razorpay payment order for subscription
    
    Args:
        request: Order creation request with tier and billing cycle
        current_user: Current authenticated user
        db: Database session
    
    Returns:
        Order details including Razorpay order ID
    """
    try:
        # Validate tier
        valid_tiers = ["basic", "pro", "ultra", "max"]
        if request.tier not in valid_tiers:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid tier. Must be one of: {valid_tiers}"
            )
        
        # Validate billing cycle
        if request.billing_cycle not in ["monthly", "yearly"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="billing_cycle must be 'monthly' or 'yearly'"
            )
        
        # Create order
        order = razorpay_service.create_subscription_order(
            user_id=current_user.id,
            tier=request.tier,
            billing_cycle=request.billing_cycle,
            user_email=current_user.email,
            user_name=current_user.full_name or current_user.email,
            db=db
        )
        
        return CreateOrderResponse(**order)
    
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
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
    Verify Razorpay payment and activate subscription
    
    Args:
        request: Payment verification details
        current_user: Current authenticated user
        db: Database session
    
    Returns:
        Verification result and subscription details
    """
    try:
        # Process payment
        success, message, subscription_data = razorpay_service.process_successful_payment(
            order_id=request.razorpay_order_id,
            payment_id=request.razorpay_payment_id,
            signature=request.razorpay_signature,
            db=db
        )
        
        if not success:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=message
            )
        
        return VerifyPaymentResponse(
            success=True,
            message=message,
            subscription=subscription_data
        )
    
    except HTTPException:
        raise
    except Exception as e:
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
    Handle Razorpay webhook events
    
    Args:
        request: FastAPI request object
        db: Database session
        x_razorpay_signature: Webhook signature from headers
    
    Returns:
        Success response
    """
    try:
        # Get webhook body
        body = await request.json()
        
        # Get signature from header
        signature = x_razorpay_signature or ""
        
        # Process webhook
        success, message = razorpay_service.handle_webhook(
            event=body,
            signature=signature,
            db=db
        )
        
        if not success:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=message
            )
        
        return {
            "status": "success",
            "message": message
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Webhook processing failed: {str(e)}"
        )


@router.get("/config")
async def get_payment_config():
    """
    Get Razorpay configuration for frontend
    
    Returns:
        Razorpay key ID for checkout
    """
    return {
        "key_id": razorpay_service.key_id,
        "currency": "INR",
        "description": "TrulyInvoice Subscription",
        "image": "/logo.png"  # Your logo URL
    }


@router.post("/cancel-subscription")
async def cancel_subscription(
    current_user: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Cancel user's subscription
    
    Args:
        current_user: Current authenticated user
        db: Database session
    
    Returns:
        Cancellation confirmation
    """
    try:
        success, message = razorpay_service.cancel_subscription(
            user_id=current_user.id,
            db=db
        )
        
        if not success:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=message
            )
        
        return {
            "success": True,
            "message": message
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Cancellation failed: {str(e)}"
        )
