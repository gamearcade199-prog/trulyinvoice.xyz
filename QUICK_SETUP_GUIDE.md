# 🚀 QUICK SETUP GUIDE - New Pricing, Rate Limiting & Authentication

## 📋 Quick Start (5 Minutes)

Follow these steps to activate all the new features:

---

## Step 1: Install Dependencies (if needed)

```bash
cd backend
pip install slowapi pyotp passlib[bcrypt]
```

---

## Step 2: Run Database Migration

```bash
cd backend
python migrate_subscriptions.py
```

**Expected Output:**
```
🔄 Starting database migration for subscriptions table...
  ✓ Running migration 1/14...
  ✓ Running migration 2/14...
  ...
✅ Database migration completed!
```

---

## Step 3: Update Backend Main Application

Edit `backend/app/main.py` and add these imports and configurations:

```python
# Add these imports at the top
from app.api import subscriptions
from app.middleware.rate_limiter import (
    rate_limit_middleware, 
    rate_limit_exception_handler,
    limiter
)
from app.core.advanced_security import SecurityHeaders
from slowapi.errors import RateLimitExceeded
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware

# Add subscription API routes (after other routers)
app.include_router(subscriptions.router)

# Add rate limiting to app state
app.state.limiter = limiter

# Add rate limiting middleware
app.add_middleware(
    BaseHTTPMiddleware,
    dispatch=rate_limit_middleware
)

# Add rate limit exception handler
app.add_exception_handler(RateLimitExceeded, rate_limit_exception_handler)

# Add security headers middleware
@app.middleware("http")
async def add_security_headers_middleware(request: Request, call_next):
    response = await call_next(request)
    return SecurityHeaders.add_security_headers(response)
```

---

## Step 4: Update Authentication Endpoints

Edit `backend/app/api/auth.py` to use new security features:

```python
from app.core.advanced_security import (
    PasswordPolicy,
    hash_password,
    verify_password,
    LoginAttemptTracker,
    get_client_ip
)

# In register endpoint
@router.post("/register")
async def register(
    user_data: UserCreate,
    request: Request,
    db: Session = Depends(get_db)
):
    # Validate password
    is_valid, message = PasswordPolicy.validate(user_data.password)
    if not is_valid:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=message
        )
    
    # Hash password with new method
    hashed_password = hash_password(user_data.password)
    
    # Continue with registration...
    ...


# In login endpoint
@router.post("/login")
async def login(
    credentials: UserLogin,
    request: Request,
    db: Session = Depends(get_db)
):
    client_ip = get_client_ip(request)
    
    # Check for lockout
    is_locked, seconds = LoginAttemptTracker.is_locked_out(credentials.email)
    if is_locked:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=f"Too many failed login attempts. Try again in {seconds} seconds."
        )
    
    # Verify credentials
    user = db.query(User).filter(User.email == credentials.email).first()
    
    if not user or not verify_password(credentials.password, user.hashed_password):
        # Record failed attempt
        LoginAttemptTracker.record_attempt(credentials.email, success=False)
        LoginAttemptTracker.record_attempt(client_ip, success=False)
        
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
    
    # Record successful attempt
    LoginAttemptTracker.record_attempt(credentials.email, success=True)
    LoginAttemptTracker.record_attempt(client_ip, success=True)
    
    # Continue with login...
    ...
```

---

## Step 5: Update Document Upload with Usage Tracking

Edit `backend/app/api/documents.py`:

```python
from app.services.usage_tracker import check_user_quota, increment_user_scans

@router.post("/upload")
async def upload_document(
    file: UploadFile,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Check quota BEFORE processing
    has_quota, message = await check_user_quota(db, current_user.id, 1)
    
    if not has_quota:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={
                "error": "Quota exceeded",
                "message": message,
                "upgrade_link": "/pricing"
            }
        )
    
    # Process file upload...
    result = await process_invoice(file, current_user.id, db)
    
    # Increment scan count AFTER successful processing
    await increment_user_scans(db, current_user.id, 1)
    
    return result


@router.post("/batch-upload")
async def batch_upload(
    files: List[UploadFile],
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    from app.services.usage_tracker import UsageTracker
    
    tracker = UsageTracker(db)
    file_count = len(files)
    
    # Check bulk upload limit
    allowed, message = await tracker.check_bulk_upload_limit(current_user.id, file_count)
    if not allowed:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=message
        )
    
    # Check scan quota
    has_quota, message = await check_user_quota(db, current_user.id, file_count)
    if not has_quota:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=message
        )
    
    # Process batch...
    results = []
    successful_count = 0
    
    for file in files:
        try:
            result = await process_invoice(file, current_user.id, db)
            results.append(result)
            successful_count += 1
        except Exception as e:
            results.append({"error": str(e)})
    
    # Increment by successful count only
    await increment_user_scans(db, current_user.id, successful_count)
    
    return {
        "total": file_count,
        "successful": successful_count,
        "results": results
    }
```

---

## Step 6: Add User Tier to Request State

Update your authentication dependency:

```python
# In backend/app/core/security.py

async def get_current_user(
    request: Request,
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:
    # Verify token and get user...
    user = verify_token_and_get_user(token, db)
    
    # Add user info to request state for rate limiting
    request.state.user_id = user.id
    
    # Get user's tier from subscription
    from app.services.usage_tracker import UsageTracker
    tracker = UsageTracker(db)
    tier = await tracker.get_current_tier(user.id)
    request.state.user_tier = tier
    
    return user
```

---

## Step 7: Test the Setup

### Test 1: Check Pricing API

```bash
curl http://localhost:8000/api/subscriptions/plans
```

**Expected:** JSON array with all 5 plans

### Test 2: Check Current Subscription

```bash
curl http://localhost:8000/api/subscriptions/current \
  -H "Authorization: Bearer YOUR_TOKEN"
```

**Expected:** Your current subscription details

### Test 3: Test Rate Limiting

```bash
# Run this multiple times quickly
for i in {1..15}; do
  curl http://localhost:8000/api/documents/upload \
    -H "Authorization: Bearer YOUR_TOKEN" \
    -F "file=@test.pdf"
  sleep 0.1
done
```

**Expected:** After your tier's limit, you should get:
```json
{
  "error": "Rate limit exceeded",
  "message": "Too many requests. Limit: 10 requests per minute",
  "retry_after_seconds": 60
}
```

### Test 4: Test Password Policy

Try registering with weak password:
```bash
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "weak",
    "full_name": "Test User"
  }'
```

**Expected:**
```json
{
  "detail": "Password must be at least 8 characters long"
}
```

### Test 5: Test Quota Enforcement

Upload more than your plan allows:
```bash
# For free plan (10 scans), try uploading 15 files
# Should succeed for first 10, then fail
```

**Expected after limit:**
```json
{
  "error": "Quota exceeded",
  "message": "Insufficient quota. Need 1 scans, but only 0 remaining.",
  "upgrade_link": "/pricing"
}
```

---

## Step 8: Frontend Integration (Optional)

### Display Usage in Dashboard

Edit `frontend/src/app/dashboard/page.tsx`:

```tsx
'use client'

import { useEffect, useState } from 'react'

export default function DashboardPage() {
  const [usage, setUsage] = useState(null)
  
  useEffect(() => {
    fetchUsage()
  }, [])
  
  async function fetchUsage() {
    const response = await fetch('/api/subscriptions/usage', {
      headers: {
        'Authorization': `Bearer ${getToken()}`
      }
    })
    const data = await response.json()
    setUsage(data)
  }
  
  return (
    <div>
      {/* Usage Stats Card */}
      <div className="bg-white rounded-lg p-6 shadow">
        <h3 className="font-bold text-lg mb-4">Your Usage</h3>
        
        {usage && (
          <>
            <div className="mb-4">
              <div className="flex justify-between mb-2">
                <span>Scans Used</span>
                <span className="font-bold">
                  {usage.scans_used} / {usage.scans_limit}
                </span>
              </div>
              
              {/* Progress Bar */}
              <div className="w-full bg-gray-200 rounded-full h-2">
                <div 
                  className="bg-blue-600 h-2 rounded-full"
                  style={{ width: `${usage.usage_percentage}%` }}
                />
              </div>
            </div>
            
            <p className="text-sm text-gray-600">
              Current Plan: <span className="font-semibold">{usage.tier_name}</span>
            </p>
            
            {usage.usage_percentage > 80 && (
              <a 
                href="/dashboard/pricing"
                className="text-blue-600 text-sm mt-2 inline-block"
              >
                Upgrade for more scans →
              </a>
            )}
          </>
        )}
      </div>
    </div>
  )
}
```

---

## 🎯 Verification Checklist

- [ ] Database migration ran successfully
- [ ] Backend server starts without errors
- [ ] `/api/subscriptions/plans` returns all plans
- [ ] Rate limiting works (429 error after limit)
- [ ] Password policy enforced on registration
- [ ] Login attempts tracked and locked after 5 failures
- [ ] Usage tracking works (quota enforced)
- [ ] Security headers present in responses
- [ ] Frontend pricing pages show new plans

---

## 🐛 Troubleshooting

### Issue: Import Errors

**Solution:** Install missing dependencies
```bash
pip install slowapi pyotp passlib[bcrypt]
```

### Issue: Database Migration Fails

**Solution:** Check database connection
```bash
# Check if database is running
# Verify DATABASE_URL in .env file
```

### Issue: Rate Limiting Not Working

**Solution:** Ensure middleware is added to app
```python
# In main.py
app.add_middleware(BaseHTTPMiddleware, dispatch=rate_limit_middleware)
```

### Issue: Security Headers Not Present

**Solution:** Add security headers middleware
```python
@app.middleware("http")
async def add_security_headers_middleware(request: Request, call_next):
    response = await call_next(request)
    return SecurityHeaders.add_security_headers(response)
```

---

## 📞 Need Help?

All features are documented in:
- `NEW_PRICING_RATE_LIMITING_AUTH_COMPLETE.md` - Complete documentation
- `backend/app/config/plans.py` - Plan configuration
- `backend/app/middleware/rate_limiter.py` - Rate limiting
- `backend/app/core/advanced_security.py` - Authentication security
- `backend/app/services/usage_tracker.py` - Usage tracking
- `backend/app/api/subscriptions.py` - Subscription API

---

## ✅ You're All Set!

Your application now has:
- ✅ **5 pricing tiers** with proper limits
- ✅ **Robust rate limiting** based on subscription tier
- ✅ **Industry-grade authentication** with MFA support
- ✅ **Usage tracking** and quota enforcement
- ✅ **Security headers** (OWASP compliant)
- ✅ **Password policies** (OWASP compliant)
- ✅ **Brute force protection**
- ✅ **Session management**

**Start the backend and test the new features!** 🚀
