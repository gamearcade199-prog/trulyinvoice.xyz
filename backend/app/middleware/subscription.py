from fastapi import Request, HTTPException
from app.services.supabase_helper import supabase
from app.config.plans import get_scan_limit, PLAN_LIMITS
from app.services.usage_tracker import UsageTracker
from sqlalchemy.orm import Session
from app.core.database import get_db
from typing import Optional
import os

async def check_subscription(user_id: str, db: Optional[Session] = None):
    """
    Check if user has exceeded their subscription limits
    """
    if not user_id:
        raise HTTPException(status_code=401, detail="User not authenticated")

    # Get database session
    if db is None:
        db = next(get_db())

    # Use usage tracker for proper plan and quota checking
    tracker = UsageTracker(db)

    # Check if user has quota for 1 scan
    has_quota, message = await tracker.check_quota(user_id, 1)

    if not has_quota:
        raise HTTPException(status_code=403, detail=f"Subscription limit exceeded: {message}")

    return True