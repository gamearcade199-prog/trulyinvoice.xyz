"""
Redis-Based Rate Limiting
CRITICAL FIX #3: Persistent Rate Limiting Across Restarts

Install: pip install redis fastapi-limiter2

This replaces the in-memory rate limiter with Redis for persistence.
"""

import redis
import time
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
from typing import Optional, Dict, Tuple

load_dotenv()

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")


class RedisRateLimiter:
    """Rate limiter using Redis backend"""
    
    def __init__(self, redis_url: str = REDIS_URL):
        """Initialize Redis connection"""
        try:
            self.redis = redis.from_url(redis_url, decode_responses=True)
            self.redis.ping()
            print("✅ Redis connected successfully")
        except Exception as e:
            print(f"⚠️  Redis connection failed: {e}")
            print("   Rate limiting will use in-memory fallback")
            self.redis = None
            self.in_memory_limits = {}
    
    def is_allowed(
        self, 
        user_id: str, 
        operation: str,
        limit: int,
        window_seconds: int = 3600
    ) -> Tuple[bool, Dict]:
        """
        Check if operation is allowed for user within time window
        
        Args:
            user_id: User identifier
            operation: Operation name (scan, export, upload)
            limit: Max operations per window
            window_seconds: Time window in seconds
        
        Returns:
            (is_allowed: bool, info: dict with remaining, reset_time)
        """
        
        if not self.redis:
            return self._in_memory_check(user_id, operation, limit, window_seconds)
        
        key = f"rate_limit:{user_id}:{operation}"
        current_time = int(time.time())
        window_start = current_time - window_seconds
        
        try:
            # Remove old entries outside window
            self.redis.zremrangebyscore(key, 0, window_start)
            
            # Count requests in current window
            count = self.redis.zcard(key)
            
            # Add current request
            if count < limit:
                self.redis.zadd(key, {str(current_time): current_time})
                self.redis.expire(key, window_seconds + 10)
                
                remaining = limit - count - 1
                reset_time = datetime.fromtimestamp(
                    current_time + window_seconds
                )
                
                return True, {
                    "limit": limit,
                    "remaining": remaining,
                    "reset_time": reset_time.isoformat(),
                    "window_seconds": window_seconds
                }
            else:
                # Get oldest request timestamp
                oldest = self.redis.zrange(key, 0, 0, withscores=True)
                if oldest:
                    reset_time = oldest[0][1] + window_seconds
                    return False, {
                        "limit": limit,
                        "remaining": 0,
                        "reset_time": datetime.fromtimestamp(reset_time).isoformat(),
                        "retry_after": int(reset_time - current_time)
                    }
                
        except Exception as e:
            print(f"⚠️  Redis error: {e}, using fallback")
            return self._in_memory_check(user_id, operation, limit, window_seconds)
        
        return False, {"error": "Rate limit exceeded"}
    
    def _in_memory_check(
        self,
        user_id: str,
        operation: str,
        limit: int,
        window_seconds: int
    ) -> Tuple[bool, Dict]:
        """Fallback in-memory rate limiting"""
        
        key = f"{user_id}:{operation}"
        current_time = time.time()
        
        if key not in self.in_memory_limits:
            self.in_memory_limits[key] = {
                "count": 0,
                "window_start": current_time
            }
        
        entry = self.in_memory_limits[key]
        
        # Reset if window expired
        if current_time - entry["window_start"] > window_seconds:
            entry["count"] = 0
            entry["window_start"] = current_time
        
        if entry["count"] < limit:
            entry["count"] += 1
            remaining = limit - entry["count"]
            reset_time = datetime.fromtimestamp(
                entry["window_start"] + window_seconds
            )
            
            return True, {
                "limit": limit,
                "remaining": remaining,
                "reset_time": reset_time.isoformat(),
                "backend": "memory"
            }
        
        return False, {"error": "Rate limit exceeded", "backend": "memory"}
    
    def get_user_limits(self, user_id: str) -> Dict:
        """Get all rate limits for a user"""
        
        if not self.redis:
            return {}
        
        limits = {}
        pattern = f"rate_limit:{user_id}:*"
        
        for key in self.redis.scan_iter(match=pattern):
            operation = key.split(":")[-1]
            count = self.redis.zcard(key)
            limits[operation] = count
        
        return limits
    
    def reset_user_limits(self, user_id: str):
        """Reset all rate limits for a user (admin function)"""
        
        if not self.redis:
            # Clear in-memory
            keys_to_delete = [
                k for k in self.in_memory_limits.keys()
                if k.startswith(f"{user_id}:")
            ]
            for k in keys_to_delete:
                del self.in_memory_limits[k]
            return
        
        pattern = f"rate_limit:{user_id}:*"
        for key in self.redis.scan_iter(match=pattern):
            self.redis.delete(key)
    
    def health_check(self) -> Dict:
        """Check rate limiter health"""
        
        if not self.redis:
            return {"status": "fallback", "backend": "in-memory"}
        
        try:
            info = self.redis.info()
            return {
                "status": "healthy",
                "backend": "redis",
                "connected_clients": info.get("connected_clients"),
                "used_memory": info.get("used_memory_human")
            }
        except Exception as e:
            return {"status": "error", "backend": "redis", "error": str(e)}


# Global rate limiter instance
_rate_limiter: Optional[RedisRateLimiter] = None


def get_rate_limiter() -> RedisRateLimiter:
    """Get or create global rate limiter instance"""
    global _rate_limiter
    if _rate_limiter is None:
        _rate_limiter = RedisRateLimiter()
    return _rate_limiter


# Tier-specific rate limits
TIER_LIMITS = {
    "free": {
        "scan": (5, 3600),           # 5 scans per hour
        "export": (3, 86400),         # 3 exports per day
        "upload": (10, 3600),         # 10 uploads per hour
    },
    "basic": {
        "scan": (50, 3600),           # 50 scans per hour
        "export": (20, 86400),        # 20 exports per day
        "upload": (50, 3600),         # 50 uploads per hour
    },
    "pro": {
        "scan": (200, 3600),          # 200 scans per hour
        "export": (100, 86400),       # 100 exports per day
        "upload": (200, 3600),        # 200 uploads per hour
    },
    "ultra": {
        "scan": (500, 3600),          # 500 scans per hour
        "export": (300, 86400),       # 300 exports per day
        "upload": (500, 3600),        # 500 uploads per hour
    },
    "max": {
        "scan": (2000, 3600),         # 2000 scans per hour
        "export": (1000, 86400),      # 1000 exports per day
        "upload": (2000, 3600),       # 2000 uploads per hour
    }
}


def get_tier_limit(tier: str, operation: str) -> Tuple[int, int]:
    """Get rate limit for tier and operation"""
    tier_config = TIER_LIMITS.get(tier, TIER_LIMITS["free"])
    return tier_config.get(operation, (5, 3600))
