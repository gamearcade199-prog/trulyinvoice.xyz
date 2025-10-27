"""
API Endpoint for Storage Cleanup
Allows manual triggering of storage cleanup via API
"""

from fastapi import APIRouter, Depends, HTTPException, status, Request
from typing import Dict, Any
from pydantic import BaseModel
from slowapi import Limiter
from slowapi.util import get_remote_address

from app.auth import get_current_user
from app.services.storage_cleanup import (
    cleanup_user_storage,
    get_user_storage_stats
)

router = APIRouter()
limiter = Limiter(key_func=get_remote_address)


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
@limiter.limit("5/hour")
async def cleanup_user_data(
    request: Request,
    current_user: str = Depends(get_current_user)
):
    """
    Clean up old data for the current user based on their subscription tier
    
    Security: Only authenticated users can cleanup their own data
    Rate Limited: 5 requests per hour to prevent abuse
    
    Args:
        request: HTTP request (for rate limiting)
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
    Rate Limited: 30 requests per minute
    
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


# Admin endpoints REMOVED for security
# These operations should only be run via scheduled cron jobs or backend scripts
# NOT exposed as public API endpoints to prevent unauthorized data deletion
#
# To run cleanup manually:
# 1. SSH into server
# 2. Run: python -c "from app.services.storage_cleanup import cleanup_all_storage; cleanup_all_storage()"
#
# Or set up a cron job in Render dashboard to run cleanup_script.py daily
