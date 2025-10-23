"""
API Endpoint for Storage Cleanup
Allows manual triggering of storage cleanup via API
"""

from fastapi import APIRouter, Depends, HTTPException, status
from typing import Dict, Any
from pydantic import BaseModel

from app.auth import get_current_user
from app.services.storage_cleanup import (
    cleanup_user_storage,
    cleanup_all_storage,
    cleanup_anonymous_storage,
    get_user_storage_stats
)

router = APIRouter()


class CleanupResponse(BaseModel):
    """Response for cleanup operations"""
    success: bool
    message: str
    details: Dict[str, Any]


class StorageStatsResponse(BaseModel):
    """Response for storage statistics"""
    success: bool
    stats: Dict[str, Any]


@router.post("/cleanup/user", response_model=CleanupResponse)
async def cleanup_user_data(
    current_user: str = Depends(get_current_user)
):
    """
    Clean up old data for the current user based on their subscription tier
    
    Security: Only authenticated users can cleanup their own data
    
    Args:
        current_user: Current authenticated user (from JWT token)
    
    Returns:
        Cleanup results
    """
    try:
        # Get user's subscription tier
        from app.services.supabase_helper import supabase
        
        subscription = supabase.table("subscriptions").select("tier").eq("user_id", current_user).execute()
        
        if not subscription.data or len(subscription.data) == 0:
            tier = "free"
        else:
            tier = subscription.data[0].get("tier", "free")
        
        # Perform cleanup
        result = cleanup_user_storage(current_user, tier)
        
        return CleanupResponse(
            success=True,
            message="Storage cleanup completed",
            details=result
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Cleanup failed: {str(e)}"
        )


@router.get("/storage/stats", response_model=StorageStatsResponse)
async def get_storage_statistics(
    current_user: str = Depends(get_current_user)
):
    """
    Get storage statistics for the current user
    
    Security: Only authenticated users can view their own stats
    
    Args:
        current_user: Current authenticated user (from JWT token)
    
    Returns:
        Storage statistics
    """
    try:
        stats = get_user_storage_stats(current_user)
        
        return StorageStatsResponse(
            success=True,
            stats=stats
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get stats: {str(e)}"
        )


# Admin endpoints (would need admin authentication in production)
@router.post("/cleanup/all", response_model=CleanupResponse)
async def cleanup_all_users():
    """
    Clean up old data for all users based on their subscription tiers
    
    Security: This should be restricted to admin users or run via cron job
    TODO: Add admin authentication
    
    Returns:
        Cleanup results for all users
    """
    try:
        result = cleanup_all_storage()
        
        return CleanupResponse(
            success=True,
            message="All users storage cleanup completed",
            details=result
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Cleanup failed: {str(e)}"
        )


@router.post("/cleanup/anonymous", response_model=CleanupResponse)
async def cleanup_anonymous_data():
    """
    Clean up anonymous uploads older than 24 hours
    
    Security: This should be restricted to admin users or run via cron job
    TODO: Add admin authentication
    
    Returns:
        Cleanup results for anonymous uploads
    """
    try:
        result = cleanup_anonymous_storage()
        
        return CleanupResponse(
            success=True,
            message="Anonymous uploads cleanup completed",
            details=result
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Cleanup failed: {str(e)}"
        )
