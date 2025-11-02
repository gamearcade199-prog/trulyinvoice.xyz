"""
Usage Tracker Service
Tracks and enforces scan limits based on subscription tier
"""

from datetime import datetime, timedelta
from typing import Dict, Optional, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import func, and_

from app.models import Subscription, Invoice
from app.config.plans import get_scan_limit, get_bulk_upload_limit, PLAN_LIMITS


class UsageTracker:
    """Service for tracking and enforcing usage limits"""
    
    def __init__(self, db: Session):
        self.db = db
    
    async def get_user_subscription(self, user_id: str) -> Optional[Subscription]:
        """
        Get user's active subscription
        
        Args:
            user_id: User ID
        
        Returns:
            Subscription object or None
        """
        subscription = self.db.query(Subscription).filter(
            and_(
                Subscription.user_id == user_id,
                Subscription.status == 'active'
            )
        ).first()
        
        return subscription
    
    async def get_current_tier(self, user_id: str) -> str:
        """
        Get user's current subscription tier
        
        Args:
            user_id: User ID
        
        Returns:
            Tier name (free, basic, pro, ultra, max)
        """
        subscription = await self.get_user_subscription(user_id)
        
        if subscription:
            return subscription.tier
        
        return "free"  # Default to free plan
    
    async def get_usage_stats(self, user_id: str) -> Dict:
        """
        Get usage statistics for a user
        
        Args:
            user_id: User ID
        
        Returns:
            Dictionary with usage stats
        """
        tier = await self.get_current_tier(user_id)
        scan_limit = get_scan_limit(tier)
        
        subscription = await self.get_user_subscription(user_id)
        
        if not subscription:
            # Create a default free plan subscription
            subscription = Subscription(
                user_id=user_id,
                tier='free',
                status='active',
                scans_used_this_period=0,
                current_period_start=datetime.utcnow(),
                current_period_end=datetime.utcnow() + timedelta(days=30)
            )
            self.db.add(subscription)
            self.db.commit()
            self.db.refresh(subscription)
        
        scans_used = subscription.scans_used_this_period or 0
        scans_remaining = max(0, scan_limit - scans_used)
        usage_percentage = (scans_used / scan_limit * 100) if scan_limit > 0 else 0
        
        # Check if period has ended
        period_ended = datetime.utcnow() > subscription.current_period_end
        
        return {
            "user_id": user_id,
            "tier": tier,
            "tier_name": PLAN_LIMITS[tier]["name"],
            "scans_used": scans_used,
            "scans_limit": scan_limit,
            "scans_remaining": scans_remaining,
            "usage_percentage": round(usage_percentage, 2),
            "period_start": subscription.current_period_start.isoformat(),
            "period_end": subscription.current_period_end.isoformat(),
            "period_ended": period_ended,
            "bulk_upload_limit": get_bulk_upload_limit(tier)
        }
    
    async def check_quota(self, user_id: str, scans_needed: int = 1) -> Tuple[bool, str]:
        """
        Check if user has remaining quota
        
        Args:
            user_id: User ID
            scans_needed: Number of scans requested
        
        Returns:
            Tuple of (has_quota: bool, message: str)
        """
        stats = await self.get_usage_stats(user_id)
        
        # Reset quota if period has ended
        if stats["period_ended"]:
            await self.reset_monthly_quota(user_id)
            stats = await self.get_usage_stats(user_id)
        
        if stats["scans_remaining"] >= scans_needed:
            return True, "Quota available"
        
        shortage = scans_needed - stats["scans_remaining"]
        message = f"Insufficient quota. Need {scans_needed} scans, but only {stats['scans_remaining']} remaining. Short by {shortage} scans."
        
        return False, message
    
    async def check_and_increment_atomic(self, user_id: str, count: int = 1) -> Tuple[bool, str]:
        """
        SECURITY FIX: Atomically check quota and increment if allowed
        Prevents race conditions where multiple requests bypass quota
        
        Args:
            user_id: User ID
            count: Number of scans to add
        
        Returns:
            Tuple of (success: bool, message: str)
        """
        # Use database transaction with row-level locking
        try:
            # Get subscription with FOR UPDATE lock (prevents concurrent modifications)
            subscription = self.db.query(Subscription).filter(
                and_(
                    Subscription.user_id == user_id,
                    Subscription.status == 'active'
                )
            ).with_for_update().first()
            
            if not subscription:
                # Create default free subscription
                subscription = Subscription(
                    user_id=user_id,
                    tier='free',
                    status='active',
                    scans_used_this_period=0,
                    current_period_start=datetime.utcnow(),
                    current_period_end=datetime.utcnow() + timedelta(days=30)
                )
                self.db.add(subscription)
                self.db.commit()
                self.db.refresh(subscription)
                
                # Re-acquire lock
                subscription = self.db.query(Subscription).filter(
                    Subscription.user_id == user_id
                ).with_for_update().first()
            
            # Check if period ended (while holding lock)
            if datetime.utcnow() > subscription.current_period_end:
                subscription.scans_used_this_period = 0
                subscription.current_period_start = datetime.utcnow()
                subscription.current_period_end = datetime.utcnow() + timedelta(days=30)
            
            # Get limit
            scan_limit = get_scan_limit(subscription.tier)
            current_usage = subscription.scans_used_this_period or 0
            
            # Check quota
            if current_usage + count > scan_limit:
                shortage = (current_usage + count) - scan_limit
                message = f"Quota exceeded: {current_usage + count}/{scan_limit} (over by {shortage})"
                self.db.rollback()  # Release lock
                return False, message
            
            # Increment atomically
            subscription.scans_used_this_period = current_usage + count
            self.db.commit()
            
            remaining = scan_limit - subscription.scans_used_this_period
            return True, f"Success: {subscription.scans_used_this_period}/{scan_limit} used ({remaining} remaining)"
        
        except Exception as e:
            self.db.rollback()
            return False, f"Error checking quota: {str(e)}"
    
    async def increment_scan_count(self, user_id: str, count: int = 1) -> bool:
        """
        Increment user's scan count
        
        Args:
            user_id: User ID
            count: Number of scans to add
        
        Returns:
            True if successful, False otherwise
        """
        subscription = await self.get_user_subscription(user_id)
        
        if not subscription:
            return False
        
        subscription.scans_used_this_period = (subscription.scans_used_this_period or 0) + count
        self.db.commit()
        
        return True
    
    async def decrement_scan_count(self, user_id: str, count: int = 1) -> bool:
        """
        Decrement user's scan count (for refunds/deletions)
        
        Args:
            user_id: User ID
            count: Number of scans to remove
        
        Returns:
            True if successful, False otherwise
        """
        subscription = await self.get_user_subscription(user_id)
        
        if not subscription:
            return False
        
        subscription.scans_used_this_period = max(0, (subscription.scans_used_this_period or 0) - count)
        self.db.commit()
        
        return True
    
    async def reset_monthly_quota(self, user_id: str) -> bool:
        """
        Reset user's monthly scan quota
        
        Args:
            user_id: User ID
        
        Returns:
            True if successful, False otherwise
        """
        subscription = await self.get_user_subscription(user_id)
        
        if not subscription:
            return False
        
        # Reset scan count
        subscription.scans_used_this_period = 0
        
        # Update period dates
        subscription.current_period_start = datetime.utcnow()
        subscription.current_period_end = datetime.utcnow() + timedelta(days=30)
        
        self.db.commit()
        
        return True
    
    async def check_bulk_upload_limit(self, user_id: str, file_count: int) -> Tuple[bool, str]:
        """
        Check if user can upload the requested number of files
        
        Args:
            user_id: User ID
            file_count: Number of files to upload
        
        Returns:
            Tuple of (allowed: bool, message: str)
        """
        tier = await self.get_current_tier(user_id)
        bulk_limit = get_bulk_upload_limit(tier)
        
        if file_count <= bulk_limit:
            return True, f"Bulk upload allowed ({file_count}/{bulk_limit} files)"
        
        excess = file_count - bulk_limit
        message = f"Bulk upload limit exceeded. Your plan allows {bulk_limit} files at once, but you're trying to upload {file_count} files (excess: {excess})"
        
        return False, message
    
    async def get_usage_history(self, user_id: str, days: int = 30) -> Dict:
        """
        Get historical usage data
        
        Args:
            user_id: User ID
            days: Number of days to look back
        
        Returns:
            Dictionary with usage history
        """
        start_date = datetime.utcnow() - timedelta(days=days)
        
        # Count documents uploaded in the period
        documents = self.db.query(Invoice).filter(
            and_(
                Invoice.user_id == user_id,
                Invoice.uploaded_at >= start_date
            )
        ).all()
        
        # Group by date
        daily_usage = {}
        for doc in documents:
            date_key = doc.uploaded_at.date().isoformat()
            daily_usage[date_key] = daily_usage.get(date_key, 0) + 1
        
        total_scans = len(documents)
        avg_daily = total_scans / days if days > 0 else 0
        
        return {
            "user_id": user_id,
            "period_days": days,
            "total_scans": total_scans,
            "avg_daily_scans": round(avg_daily, 2),
            "daily_breakdown": daily_usage
        }
    
    async def enforce_storage_limit(self, user_id: str) -> int:
        """
        Enforce storage retention policy
        Deletes documents older than the plan's storage limit
        
        Args:
            user_id: User ID
        
        Returns:
            Number of documents deleted
        """
        tier = await self.get_current_tier(user_id)
        storage_days = PLAN_LIMITS[tier]["storage_days"]
        
        if storage_days <= 0:
            return 0  # Unlimited storage
        
        cutoff_date = datetime.utcnow() - timedelta(days=storage_days)
        
        # Find old documents
        old_documents = self.db.query(Invoice).filter(
            and_(
                Invoice.user_id == user_id,
                Invoice.uploaded_at < cutoff_date
            )
        ).all()
        
        count = len(old_documents)
        
        # Delete old documents
        for doc in old_documents:
            self.db.delete(doc)
        
        self.db.commit()
        
        return count
    
    async def get_upgrade_recommendation(self, user_id: str) -> Optional[str]:
        """
        Recommend plan upgrade if user is hitting limits
        
        Args:
            user_id: User ID
        
        Returns:
            Recommended tier or None
        """
        stats = await self.get_usage_stats(user_id)
        
        # If usage is over 80%, recommend upgrade
        if stats["usage_percentage"] >= 80:
            current_tier = stats["tier"]
            tier_hierarchy = ["free", "basic", "pro", "ultra", "max"]
            
            try:
                current_index = tier_hierarchy.index(current_tier)
                if current_index < len(tier_hierarchy) - 1:
                    return tier_hierarchy[current_index + 1]
            except (ValueError, IndexError):
                pass
        
        return None


# Helper functions for quick access
async def check_user_quota(db: Session, user_id: str, scans_needed: int = 1) -> Tuple[bool, str]:
    """Quick check if user has quota"""
    tracker = UsageTracker(db)
    return await tracker.check_quota(user_id, scans_needed)


async def check_and_increment_atomic(db: Session, user_id: str, count: int = 1) -> Tuple[bool, str]:
    """SECURITY FIX: Atomically check and increment quota (prevents race conditions)"""
    tracker = UsageTracker(db)
    return await tracker.check_and_increment_atomic(user_id, count)


async def increment_user_scans(db: Session, user_id: str, count: int = 1) -> bool:
    """Quick increment of user's scan count"""
    tracker = UsageTracker(db)
    return await tracker.increment_scan_count(user_id, count)


async def get_user_usage(db: Session, user_id: str) -> Dict:
    """Quick get user usage stats"""
    tracker = UsageTracker(db)
    return await tracker.get_usage_stats(user_id)
