# 🔧 SECURITY FIXES - IMPLEMENTATION GUIDE

## Step-by-Step Instructions to Fix Critical Issues

**Time Estimate:** 4-6 hours for all critical fixes  
**Difficulty:** Medium  
**Impact:** Makes system production-ready

---

## FIX #1: Authentication Bypass - PRIORITY #1

### Current Problem
```python
# backend/app/auth.py - WRONG
def get_current_user(authorization: Optional[str] = Header(None)) -> str:
    return "cf0e42f8-109d-4c6f-b52a-eb4ca2c1e590"  # Hardcoded test user!
```

### Fix Implementation

**Step 1: Update `backend/app/auth.py`**

```python
"""
Authentication Utilities - FIXED VERSION
Secure JWT validation with Supabase
"""
from fastapi import Depends, HTTPException, status, Header
from typing import Optional
import jwt
import os
from datetime import datetime

# Import Supabase client
from app.services.supabase_helper import supabase

def get_current_user(authorization: Optional[str] = Header(None)) -> str:
    """
    Extract and validate user ID from Authorization header.
    Validates JWT token with Supabase.
    
    Args:
        authorization: Authorization header (Bearer {token})
    
    Returns:
        Authenticated user ID
    
    Raises:
        HTTPException: If token is invalid or missing
    """
    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing authorization header",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    try:
        # Expected format: "Bearer {jwt_token}"
        scheme, token = authorization.split()
        
        if scheme.lower() != "bearer":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication scheme. Use 'Bearer {token}'",
                headers={"WWW-Authenticate": "Bearer"}
            )
        
        # Validate token with Supabase
        response = supabase.auth.get_user(token)
        
        if not response.user or not response.user.id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired token"
            )
        
        # Return the authenticated user ID
        return response.user.id
        
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authorization header format. Expected: 'Bearer {token}'"
        )
    except HTTPException:
        raise
    except Exception as e:
        print(f"Token validation error: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token validation failed"
        )


def get_current_user_optional(authorization: Optional[str] = Header(None)) -> Optional[str]:
    """
    Optional authentication - returns None if not authenticated.
    Use for endpoints that work for both authenticated and anonymous users.
    """
    if not authorization:
        return None
    
    try:
        return get_current_user(authorization)
    except HTTPException:
        return None
```

**Step 2: Update endpoints to pass Authorization header**

Frontend needs to send JWT in Authorization header:

```typescript
// frontend/src/lib/supabase.ts - ADD THIS
export async function getAuthToken(): Promise<string | null> {
  const { data: { session } } = await supabase.auth.getSession()
  return session?.access_token || null
}

export async function fetchWithAuth(
  url: string,
  options: RequestInit = {}
): Promise<Response> {
  const token = await getAuthToken()
  
  if (!token) {
    throw new Error("Not authenticated")
  }
  
  return fetch(url, {
    ...options,
    headers: {
      ...options.headers,
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json'
    }
  })
}
```

**Step 3: Test the fix**

```python
# backend/test_auth.py - NEW FILE
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_missing_auth_header():
    """Test that missing auth header is rejected"""
    response = client.post("/api/payments/create-order", json={
        "tier": "basic",
        "billing_cycle": "monthly"
    })
    assert response.status_code == 401
    assert "Missing authorization header" in response.json()["detail"]

def test_invalid_token():
    """Test that invalid token is rejected"""
    response = client.post(
        "/api/payments/create-order",
        headers={"Authorization": "Bearer invalid_token"},
        json={"tier": "basic", "billing_cycle": "monthly"}
    )
    assert response.status_code == 401

def test_valid_token():
    """Test that valid token works"""
    # Sign up a test user
    # Get their token
    # Use token in request
    # Verify it works
    pass
```

**Time:** 30 minutes  
**Testing:** CRITICAL

---

## FIX #2: Payment Fraud - PRIORITY #2

### Current Problem
```python
# Payment endpoint doesn't check if user owns the subscription
@router.post("/create-order")
async def create_payment_order(
    request: CreateOrderRequest,
    current_user: str = Depends(get_current_user),  # Now fixed!
    db: Session = Depends(get_db)
):
    # User COULD be different person - no ownership check!
    order = razorpay_service.create_subscription_order(
        user_id=current_user,  # But what if order was for someone else?
        ...
    )
```

### Fix Implementation

**Step 1: Add ownership check in verify endpoint**

```python
# backend/app/api/payments.py - UPDATE VERIFY ENDPOINT

@router.post("/verify", response_model=VerifyPaymentResponse)
async def verify_payment(
    request: VerifyPaymentRequest,
    current_user: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Verify Razorpay payment and activate subscription.
    NOW WITH OWNERSHIP CHECK.
    """
    try:
        # Step 1: Verify signature
        if not razorpay_service.verify_payment_signature(
            request.razorpay_order_id,
            request.razorpay_payment_id,
            request.razorpay_signature
        ):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid payment signature - possible fraud attempt"
            )
        
        # Step 2: Fetch order and verify ownership
        try:
            order = razorpay_service.client.order.fetch(request.razorpay_order_id)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Could not fetch order details"
            )
        
        # Step 3: CRITICAL - Check user_id in order notes matches current user
        order_user_id = order.get("notes", {}).get("user_id")
        if order_user_id != current_user:
            # FRAUD DETECTED!
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Payment order user_id does not match current user. Fraud detected."
            )
        
        # Step 4: Verify payment was actually captured
        payment = razorpay_service.client.payment.fetch(request.razorpay_payment_id)
        if payment.get("status") != "captured":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Payment not captured. Status: {payment.get('status')}"
            )
        
        # Step 5: Check amount matches
        if payment.get("amount") != order.get("amount"):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Payment amount does not match order amount"
            )
        
        # Step 6: Check if payment already processed (prevent duplicates)
        existing = db.query(Subscription).filter(
            Subscription.razorpay_payment_id == request.razorpay_payment_id
        ).first()
        
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="This payment has already been processed"
            )
        
        # Step 7: Now safe to activate subscription
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
        print(f"Payment verification error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Payment verification failed: {str(e)}"
        )
```

**Time:** 20 minutes

---

## FIX #3: Rate Limiting - PRIORITY #3

### Current Problem
```
No rate limiting on login - attacker can try unlimited passwords
```

### Fix Implementation

**Step 1: Install rate limiting**

```bash
pip install slowapi python-dotenv
```

**Step 2: Add rate limiter**

```python
# backend/app/middleware/rate_limiter.py - NEW FILE
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from fastapi import Request, HTTPException, status
from fastapi.responses import JSONResponse

# Create limiter instance
limiter = Limiter(key_func=get_remote_address)

def rate_limit_error_handler(request: Request, exc: RateLimitExceeded):
    """Custom rate limit error handler"""
    return JSONResponse(
        status_code=status.HTTP_429_TOO_MANY_REQUESTS,
        content={"detail": "Too many requests. Please try again later."}
    )
```

**Step 3: Add to main app**

```python
# backend/app/main.py - ADD THIS
from slowapi import Limiter
from slowapi.util import get_remote_address
from fastapi.middleware.base import BaseHTTPMiddleware

app = FastAPI()

# Add rate limiter
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, rate_limit_error_handler)

# Add CORS
from fastapi.middleware.cors import CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://trulyinvoice.xyz", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

**Step 4: Apply to auth endpoint**

```python
# backend/app/api/auth.py - UPDATE LOGIN ENDPOINT
from app.middleware.rate_limiter import limiter

@router.post("/login")
@limiter.limit("5/minute")  # 5 attempts per minute
async def login(request: LoginRequest, request_obj: Request):
    """Login with rate limiting"""
    try:
        # ... authentication logic ...
    except:
        # Failed attempt counts toward rate limit
        pass
```

**Step 5: Frontend side - Add local attempt tracking**

```typescript
// frontend/src/app/login/page.tsx - UPDATE
'use client'

import { useState, useEffect } from 'react'
import Link from 'next/link'
import { useRouter } from 'next/navigation'
import { FileText, Mail, Lock, ArrowRight, Loader2 } from 'lucide-react'
import { supabase } from '@/lib/supabase'
import { linkTempInvoicesToUser } from '@/lib/invoiceUpload'

export default function LoginPage() {
  const router = useRouter()
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState('')
  const [loginAttempts, setLoginAttempts] = useState(0)
  const [isLocked, setIsLocked] = useState(false)
  const [lockoutSeconds, setLockoutSeconds] = useState(0)
  
  const [formData, setFormData] = useState({
    email: '',
    password: ''
  })

  // Lockout timer
  useEffect(() => {
    if (lockoutSeconds > 0) {
      const timer = setTimeout(() => {
        setLockoutSeconds(lockoutSeconds - 1)
      }, 1000)
      return () => clearTimeout(timer)
    } else if (isLocked && lockoutSeconds === 0) {
      setIsLocked(false)
    }
  }, [lockoutSeconds, isLocked])

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError('')
    
    // Check if locked out
    if (isLocked) {
      setError(`Too many failed attempts. Try again in ${lockoutSeconds} seconds.`)
      return
    }
    
    // Check attempt count
    if (loginAttempts >= 5) {
      setIsLocked(true)
      setLockoutSeconds(300) // 5 minutes
      setError('Too many failed attempts. Account locked for 5 minutes.')
      return
    }

    setIsLoading(true)

    try {
      // Sign in with Supabase Auth
      const { data, error: authError } = await supabase.auth.signInWithPassword({
        email: formData.email,
        password: formData.password
      })

      if (authError) throw authError

      // Success - reset counter
      setLoginAttempts(0)
      setIsLocked(false)

      // Link any temporary invoices to the logged-in user
      if (data.user) {
        await linkTempInvoicesToUser(data.user.id)
      }

      // Redirect to dashboard
      window.location.href = '/dashboard'
    } catch (err: any) {
      // Increment failed attempts
      const newAttempts = loginAttempts + 1
      setLoginAttempts(newAttempts)
      
      setError(err.message || 'Login failed. Please check your credentials.')
      
      if (newAttempts >= 5) {
        setIsLocked(true)
        setLockoutSeconds(300)
        setError('Too many failed attempts. Account locked for 5 minutes.')
      }
      
      setIsLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50 flex items-center justify-center p-4">
      <div className="w-full max-w-md">
        {/* ... existing code ... */}
        
        {error && (
          <div className={`${isLocked ? 'bg-red-50 border-red-200 text-red-700' : 'bg-yellow-50 border-yellow-200 text-yellow-700'} border px-4 py-3 rounded-lg mb-4`}>
            {error}
          </div>
        )}
        
        <form onSubmit={handleSubmit} className="space-y-5">
          {/* ... existing fields ... */}
          
          <button
            type="submit"
            disabled={isLoading || isLocked}
            className="w-full bg-gradient-to-r from-blue-600 to-blue-700 text-white py-3 rounded-lg font-semibold hover:shadow-lg transition-all flex items-center justify-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {isLoading ? (
              <>
                <Loader2 className="w-5 h-5 animate-spin" />
                Signing in...
              </>
            ) : isLocked ? (
              `Locked (${lockoutSeconds}s)`
            ) : (
              <>
                Sign In <ArrowRight className="w-5 h-5" />
              </>
            )}
          </button>
        </form>
      </div>
    </div>
  )
}
```

**Time:** 40 minutes

---

## FIX #4: Session Timeout - PRIORITY #4

### Current Problem
```
Sessions persist forever - no automatic logout
```

### Fix Implementation

**Step 1: Update Supabase client**

```typescript
// frontend/src/lib/supabase.ts - REPLACE
import { createClient } from '@supabase/supabase-js'

const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL!
const supabaseAnonKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!

export const supabase = createClient(supabaseUrl, supabaseAnonKey, {
  auth: {
    persistSession: true,
    autoRefreshToken: true,
    detectSessionInUrl: true,
    flowType: 'pkce'  // More secure flow
  },
  global: {
    headers: {
      'X-Client-Info': 'trulyinvoice-web',
    },
  },
})

// Session timeout management
let inactivityTimer: NodeJS.Timeout | null = null
const INACTIVITY_TIMEOUT = 30 * 60 * 1000 // 30 minutes

export function resetInactivityTimer() {
  // Clear existing timer
  if (inactivityTimer) {
    clearTimeout(inactivityTimer)
  }
  
  // Set new timeout
  inactivityTimer = setTimeout(async () => {
    console.log('Session expired due to inactivity')
    await supabase.auth.signOut()
    window.location.href = '/login?reason=session-expired&message=Your%20session%20expired%20due%20to%20inactivity'
  }, INACTIVITY_TIMEOUT)
}

export function clearInactivityTimer() {
  if (inactivityTimer) {
    clearTimeout(inactivityTimer)
  }
}

// Initialize activity tracking
if (typeof window !== 'undefined') {
  const resetTimer = () => resetInactivityTimer()
  
  document.addEventListener('click', resetTimer)
  document.addEventListener('keypress', resetTimer)
  document.addEventListener('mousemove', resetTimer)
  document.addEventListener('scroll', resetTimer)
  document.addEventListener('touchstart', resetTimer)
  
  // Clear timer on page unload
  window.addEventListener('beforeunload', () => {
    clearInactivityTimer()
  })
  
  // Initial timer
  resetInactivityTimer()
}

export function validateSession(): boolean {
  const session = localStorage.getItem('supabase.auth.token')
  return session !== null
}
```

**Step 2: Add session timeout notification**

```typescript
// frontend/src/components/SessionTimeoutWarning.tsx - NEW FILE
'use client'

import { useEffect, useState } from 'react'
import { supabase, resetInactivityTimer } from '@/lib/supabase'
import { AlertTriangle } from 'lucide-react'

export default function SessionTimeoutWarning() {
  const [showWarning, setShowWarning] = useState(false)
  const [secondsRemaining, setSecondsRemaining] = useState(300)
  
  const WARNING_TIME = 5 * 60 * 1000 // Warn 5 minutes before expiry
  const INACTIVITY_TIMEOUT = 30 * 60 * 1000 // 30 minutes total

  useEffect(() => {
    let warningTimer: NodeJS.Timeout
    let countdownTimer: NodeJS.Timeout

    const resetWarning = () => {
      setShowWarning(false)
      setSecondsRemaining(300)
      
      clearTimeout(warningTimer)
      clearTimeout(countdownTimer)
      
      // Set new warning timer
      warningTimer = setTimeout(() => {
        setShowWarning(true)
        setSecondsRemaining(300)
        
        // Countdown timer
        countdownTimer = setInterval(() => {
          setSecondsRemaining(prev => {
            if (prev <= 1) {
              clearInterval(countdownTimer)
              return 0
            }
            return prev - 1
          })
        }, 1000)
      }, INACTIVITY_TIMEOUT - WARNING_TIME)
    }

    const events = ['click', 'keypress', 'mousemove', 'scroll', 'touchstart']
    
    events.forEach(event => {
      document.addEventListener(event, resetWarning)
    })

    resetWarning()

    return () => {
      clearTimeout(warningTimer)
      clearInterval(countdownTimer)
      events.forEach(event => {
        document.removeEventListener(event, resetWarning)
      })
    }
  }, [])

  if (!showWarning) return null

  return (
    <div className="fixed bottom-4 right-4 bg-yellow-50 border-l-4 border-yellow-400 p-4 rounded shadow-lg max-w-sm z-50">
      <div className="flex items-start gap-3">
        <AlertTriangle className="w-5 h-5 text-yellow-600 flex-shrink-0 mt-0.5" />
        <div>
          <h3 className="font-semibold text-yellow-800">Session Expiring Soon</h3>
          <p className="text-sm text-yellow-700 mt-1">
            Your session will expire in {secondsRemaining} seconds due to inactivity.
          </p>
          <button
            onClick={() => {
              resetInactivityTimer()
              setShowWarning(false)
            }}
            className="mt-2 px-3 py-1 bg-yellow-600 text-white rounded text-sm font-medium hover:bg-yellow-700"
          >
            Stay Logged In
          </button>
        </div>
      </div>
    </div>
  )
}
```

**Step 3: Add to layout**

```typescript
// frontend/src/components/DashboardLayout.tsx - ADD THIS
import SessionTimeoutWarning from './SessionTimeoutWarning'

export default function DashboardLayout({ children }: DashboardLayoutProps) {
  return (
    <div>
      {/* ... existing layout ... */}
      <SessionTimeoutWarning />
      {/* ... rest of layout ... */}
    </div>
  )
}
```

**Time:** 35 minutes

---

## FIX #5: Hardcoded Month - PRIORITY #5

### Current Problem
```python
current_month = "2025-10"  # TODO: Get current month dynamically
```

### Fix Implementation

```python
# backend/app/middleware/subscription.py - UPDATE

from datetime import datetime
from fastapi import Request, HTTPException
from app.services.supabase_helper import supabase
from app.config.plans import get_scan_limit, PLAN_LIMITS
from typing import Optional

async def check_subscription(user_id: str, db: Optional[Session] = None):
    """
    Check if user has exceeded their subscription limits
    FIXED: Now uses dynamic month
    """
    if not user_id:
        raise HTTPException(status_code=401, detail="User not authenticated")

    try:
        # Get current month dynamically
        now = datetime.now()
        current_month = now.strftime("%Y-%m")  # e.g., "2025-10"
        
        print(f"Checking subscription for {user_id}, month: {current_month}")

        # Query usage from Supabase
        usage_response = supabase.table("usage_tracking").select("scan_count").eq("user_id", user_id).eq("month", current_month).execute()

        current_usage = 0
        if usage_response.data:
            current_usage = usage_response.data[0].get("scan_count", 0)

        # Get user's plan (default to free)
        user_response = supabase.table("users").select("subscription_tier").eq("id", user_id).execute()
        user_tier = "free"
        if user_response.data:
            user_tier = user_response.data[0].get("subscription_tier", "free")

        # Get plan limits
        plan_limits = PLAN_LIMITS.get(user_tier, PLAN_LIMITS["free"])
        monthly_limit = plan_limits["scans_per_month"]

        if current_usage >= monthly_limit:
            raise HTTPException(
                status_code=403,
                detail=f"Monthly scan limit exceeded. Used: {current_usage}/{monthly_limit}. Upgrade your plan for higher limits."
            )

        return True

    except HTTPException:
        raise
    except Exception as e:
        # If subscription check fails, allow the request but log the error
        print(f"Warning: Subscription check failed for user {user_id}: {str(e)}")
        return True
```

**Time:** 10 minutes

---

## Summary

| Fix | Time | Priority |
|-----|------|----------|
| Authentication bypass | 30 min | 🔴 CRITICAL |
| Payment fraud | 20 min | 🔴 CRITICAL |
| Rate limiting | 40 min | 🔴 CRITICAL |
| Session timeout | 35 min | 🟠 HIGH |
| Hardcoded month | 10 min | 🟠 HIGH |
| **TOTAL** | **135 min** | **~2.5 hours** |

---

## Testing Checklist

After implementing fixes:

- [ ] Test login with multiple users
- [ ] Verify sessions are isolated
- [ ] Test payment with each user
- [ ] Verify payment ownership check works
- [ ] Test rate limiting (try 6 failed logins)
- [ ] Test session timeout (wait 30+ minutes)
- [ ] Test month rollover (next month)
- [ ] Verify no cross-user data access

