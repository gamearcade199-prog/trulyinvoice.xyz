# ✅ PAYMENT SYSTEM AUDIT - ACTION CHECKLIST

## 🔴 CRITICAL - IMMEDIATE ACTION REQUIRED

### 1. Test Quota Enforcement (HIGHEST PRIORITY)
**Status:** ⏳ PENDING  
**Assigned To:** QA Team / Developer  
**Estimated Time:** 30 minutes  
**Blocker:** Critical fix must be verified before production deploy

**Steps:**
```bash
# Test Case: User with Basic plan (80 scans)
1. Create test user with Basic subscription
2. Upload 85 invoices sequentially
3. Verify first 80 succeed (200 OK)
4. Verify upload #81 fails (429 Too Many Requests)
5. Check error message contains "Monthly scan limit exceeded"
6. Query database: SELECT scans_used_this_period FROM subscriptions WHERE user_id = 'test_user';
7. Verify result shows 80 (not 0)
```

- [ ] Test completed successfully
- [ ] Database confirms scans_used_this_period = 80
- [ ] Error message displays correctly
- [ ] Screenshots captured
- [ ] Verified on staging environment

**Expected Result:**
```
Upload #1-80:  ✅ 200 OK
Upload #81:    ❌ 429 Too Many Requests
Database:      scans_used_this_period = 80 ✅
```

---

### 2. Deploy Quota Fix to Production
**Status:** ⏳ PENDING (waiting for test verification)  
**Assigned To:** DevOps / Lead Developer  
**Estimated Time:** 10 minutes  
**Dependency:** Test quota enforcement first

**Steps:**
- [ ] Verify all tests pass on staging
- [ ] Create backup of current production code
- [ ] Deploy updated `backend/app/api/documents.py`
- [ ] Restart backend service
- [ ] Monitor logs for 30 minutes
- [ ] Check Sentry for errors
- [ ] Verify production database updates correctly

**Rollback Plan:**
```bash
# If issues found:
git revert <commit_hash>
docker restart backend
# Monitor for 10 minutes
```

---

## 🟡 HIGH PRIORITY - THIS WEEK

### 3. Upgrade Rate Limiter to Redis
**Status:** ⏳ TODO  
**Assigned To:** Backend Developer  
**Estimated Time:** 15 minutes  
**Impact:** Required for multi-server production deployment

**File:** `backend/app/middleware/rate_limiter.py`

**Changes Required:**
```python
# BEFORE:
limiter = Limiter(
    key_func=get_remote_address,
    storage_uri="memory://",  # ❌ In-memory (not distributed)
)

# AFTER:
import os
limiter = Limiter(
    key_func=get_remote_address,
    storage_uri=os.getenv("REDIS_URL", "redis://localhost:6379/0"),  # ✅ Redis
)
```

**Checklist:**
- [ ] Update rate_limiter.py with Redis URI
- [ ] Add REDIS_URL to .env file
- [ ] Test rate limiting works across multiple requests
- [ ] Verify limits persist across server restarts
- [ ] Document Redis requirement in deployment docs

---

### 4. Add Webhook Retry Endpoint
**Status:** ⏳ TODO  
**Assigned To:** Backend Developer  
**Estimated Time:** 30 minutes  
**Impact:** Prevents stuck payments from failed webhooks

**File:** `backend/app/api/payments.py`

**Implementation:**
```python
@router.post("/webhook/retry/{payment_id}")
async def retry_webhook_processing(
    payment_id: str,
    admin_key: str = Header(None),
    db: Session = Depends(get_db)
):
    """
    Manual retry for failed webhook processing
    Admin-only endpoint for recovering stuck payments
    """
    # Verify admin authentication
    if admin_key != settings.ADMIN_SECRET_KEY:
        raise HTTPException(403, "Admin access required")
    
    # Fetch payment from Razorpay
    try:
        payment = razorpay_client.payment.fetch(payment_id)
    except Exception as e:
        raise HTTPException(404, f"Payment not found: {str(e)}")
    
    # Verify payment is captured
    if payment["status"] != "captured":
        raise HTTPException(400, f"Payment status is {payment['status']}, must be 'captured'")
    
    # Check if already processed
    existing = db.query(Subscription).filter_by(
        razorpay_payment_id=payment_id
    ).first()
    
    if existing:
        return {
            "status": "already_processed",
            "subscription_id": existing.id,
            "tier": existing.tier,
            "message": "Payment already processed successfully"
        }
    
    # Process payment
    subscription = await razorpay_service.process_successful_payment(
        payment_data=payment,
        db=db
    )
    
    return {
        "status": "processed",
        "subscription_id": subscription.id,
        "tier": subscription.tier,
        "message": "Payment processed successfully via manual retry"
    }
```

**Checklist:**
- [ ] Implement retry endpoint
- [ ] Add ADMIN_SECRET_KEY to .env
- [ ] Test with failed webhook scenario
- [ ] Document usage in admin docs
- [ ] Add to Postman collection

---

### 5. Add Automated Quota Tests
**Status:** ⏳ TODO  
**Assigned To:** Backend Developer  
**Estimated Time:** 1 hour  
**Impact:** Prevents quota bugs in future releases

**File:** `backend/tests/test_quota_enforcement.py`

**Tests to Add:**
```python
def test_quota_increment_after_upload():
    """Ensure scans_used_this_period increments"""
    user = create_test_user(tier="basic")
    response = client.post("/api/documents/upload", files={"file": test_invoice})
    assert response.status_code == 200
    
    subscription = db.query(Subscription).filter_by(user_id=user.id).first()
    assert subscription.scans_used_this_period == 1

def test_quota_enforcement_at_limit():
    """Ensure 81st upload fails for Basic plan"""
    user = create_test_user(tier="basic")
    
    for i in range(80):
        response = client.post("/api/documents/upload", files={"file": test_invoice})
        assert response.status_code == 200
    
    response = client.post("/api/documents/upload", files={"file": test_invoice})
    assert response.status_code == 429
    assert "Monthly scan limit exceeded" in response.json()["detail"]

def test_quota_reset_on_renewal():
    """Ensure scans reset when period ends"""
    user = create_test_user(tier="basic", scans_used=80, period_ended=True)
    
    response = client.post("/api/documents/upload", files={"file": test_invoice})
    assert response.status_code == 200
    
    subscription = db.query(Subscription).filter_by(user_id=user.id).first()
    assert subscription.scans_used_this_period == 1  # Reset + incremented

def test_quota_preserved_on_upgrade():
    """Ensure scans preserved when upgrading mid-period"""
    user = create_test_user(tier="basic", scans_used=40)
    
    # Upgrade to pro
    upgrade_subscription(user.id, "pro")
    
    subscription = db.query(Subscription).filter_by(user_id=user.id).first()
    assert subscription.tier == "pro"
    assert subscription.scans_used_this_period == 40  # Preserved
```

**Checklist:**
- [ ] Create test_quota_enforcement.py
- [ ] Implement all 4 test cases
- [ ] Add to CI/CD pipeline
- [ ] Verify tests pass on staging
- [ ] Document in test suite README

---

## 🟢 MEDIUM PRIORITY - THIS SPRINT

### 6. Post-Payment Confirmation Page
**Status:** ⏳ TODO  
**Assigned To:** Frontend Developer  
**Estimated Time:** 1 hour  
**Impact:** Better UX, reduces support tickets

**File:** `frontend/src/pages/PaymentSuccess.tsx`

**Design Requirements:**
- 🎉 Success icon/animation
- ✅ "Payment Successful" heading
- 📋 Order summary (plan, amount, billing cycle)
- 📊 Subscription details (scans, storage, features)
- 🚀 "Get Started" button (→ /dashboard)
- 📧 "Email receipt sent" confirmation

**Route Change:**
```typescript
// File: frontend/src/hooks/useRazorpay.ts

// BEFORE:
router.push('/dashboard/settings')

// AFTER:
router.push({
  pathname: '/payment-success',
  query: {
    order_id,
    plan: tier,
    amount,
    billing_cycle
  }
})
```

**Checklist:**
- [ ] Create PaymentSuccess.tsx component
- [ ] Design confirmation UI (Figma)
- [ ] Update useRazorpay hook redirect
- [ ] Add animation (confetti or checkmark)
- [ ] Test on staging
- [ ] Get UX approval

---

### 7. Replace alert() with Toast Notifications
**Status:** ⏳ TODO  
**Assigned To:** Frontend Developer  
**Estimated Time:** 30 minutes  
**Impact:** Professional UX

**Install Toast Library:**
```bash
npm install react-hot-toast
```

**File:** `frontend/src/hooks/useRazorpay.ts`

**Changes:**
```typescript
import toast from 'react-hot-toast';

// BEFORE:
alert('Payment failed: ' + error.description);

// AFTER:
toast.error('Payment failed: ' + error.description, {
  duration: 5000,
  position: 'top-right',
  icon: '❌'
});

// Success case:
toast.success('Payment successful! Your subscription is now active.', {
  duration: 4000,
  icon: '✅'
});
```

**Checklist:**
- [ ] Install react-hot-toast
- [ ] Replace all alert() calls
- [ ] Add toast configuration
- [ ] Test error scenarios
- [ ] Test success scenarios
- [ ] Update error handling docs

---

### 8. Feature Access Middleware
**Status:** ⏳ TODO  
**Assigned To:** Backend Developer  
**Estimated Time:** 2 hours  
**Impact:** Proper tier-based feature enforcement

**File:** `backend/app/middleware/feature_access.py`

**Implementation:**
```python
from functools import wraps
from fastapi import HTTPException, Depends
from app.config.plans import check_feature_access

def require_feature(feature: str):
    """
    Decorator to enforce feature access based on subscription tier
    
    Usage:
        @router.post("/export/custom")
        @require_feature("custom_export_templates")
        async def export_custom(user_id: str):
            ...
    """
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Get user_id from function arguments or request
            user_id = kwargs.get('user_id') or request.state.user_id
            
            # Get user's subscription tier
            subscription = get_subscription(user_id)
            tier = subscription.tier if subscription else "free"
            
            # Check feature access
            has_access = check_feature_access(tier, feature)
            
            if not has_access:
                raise HTTPException(
                    status_code=403,
                    detail={
                        "error": "Feature not available",
                        "message": f"'{feature}' requires a higher plan",
                        "current_tier": tier,
                        "upgrade_url": "/pricing"
                    }
                )
            
            return await func(*args, **kwargs)
        return wrapper
    return decorator
```

**Apply to Endpoints:**
```python
# File: backend/app/api/export.py

@router.post("/export/custom")
@require_feature("custom_export_templates")
async def export_with_custom_template(user_id: str, template_id: str):
    # Only Pro+ users can reach here
    ...

@router.post("/bulk-upload")
@require_feature("bulk_upload_10")
async def bulk_upload(user_id: str, files: List[UploadFile]):
    # Check bulk upload limit
    tier = get_user_tier(user_id)
    limit = get_bulk_upload_limit(tier)
    
    if len(files) > limit:
        raise HTTPException(400, f"Bulk upload limit: {limit} files for {tier} plan")
    ...
```

**Checklist:**
- [ ] Create feature_access.py middleware
- [ ] Implement @require_feature decorator
- [ ] Apply to bulk upload endpoint
- [ ] Apply to custom export endpoint
- [ ] Apply to API access endpoints
- [ ] Add tests for feature blocking
- [ ] Document available features

---

## ⚪ LOW PRIORITY - NEXT SPRINT

### 9. Implement Downgrade Logic
**Status:** ⏳ TODO  
**Estimated Time:** 2 hours  
**Assigned To:** Backend Developer

**Checklist:**
- [ ] Design downgrade flow (immediate vs scheduled)
- [ ] Handle usage exceeded case (block or schedule)
- [ ] Update subscription status
- [ ] Send notification email
- [ ] Add to admin dashboard
- [ ] Test all downgrade scenarios
- [ ] Document in API docs

---

### 10. Add Refund Handling
**Status:** ⏳ TODO  
**Estimated Time:** 2 hours  
**Assigned To:** Backend Developer

**Checklist:**
- [ ] Create refund endpoint
- [ ] Integrate Razorpay refund API
- [ ] Revert subscription tier
- [ ] Decrement scans_used_this_period
- [ ] Log refund in audit table
- [ ] Send refund confirmation email
- [ ] Add to admin dashboard
- [ ] Document refund policy

---

### 11. Admin Subscription Dashboard
**Status:** ⏳ TODO  
**Estimated Time:** 4 hours  
**Assigned To:** Full-Stack Developer

**Features:**
- [ ] View all subscriptions
- [ ] Filter by tier/status
- [ ] Search by user email
- [ ] Manual subscription update
- [ ] Webhook retry interface
- [ ] Refund processing
- [ ] Usage statistics
- [ ] Revenue reports

---

## 📊 PROGRESS TRACKER

### Overall Completion: 2/11 (18%)

#### Critical (3 items):
- [x] Audit payment system (100%)
- [x] Fix quota enforcement bug (100%)
- [ ] Test quota enforcement (0%)
- [ ] Deploy to production (0%)

#### High Priority (3 items):
- [ ] Upgrade to Redis (0%)
- [ ] Webhook retry endpoint (0%)
- [ ] Automated quota tests (0%)

#### Medium Priority (3 items):
- [ ] Post-payment confirmation (0%)
- [ ] Toast notifications (0%)
- [ ] Feature access middleware (0%)

#### Low Priority (3 items):
- [ ] Downgrade logic (0%)
- [ ] Refund handling (0%)
- [ ] Admin dashboard (0%)

---

## 🎯 SPRINT PLANNING

### Sprint 1 (This Week) - Focus: Critical Fixes
**Goal:** Production-ready payment system  
**Deliverables:**
1. ✅ Quota enforcement verified
2. ✅ Production deployment complete
3. ✅ Redis rate limiter implemented
4. ✅ Webhook retry endpoint added
5. ✅ Automated tests passing

**Effort:** 3-5 hours total

---

### Sprint 2 (Next Week) - Focus: UX Polish
**Goal:** Professional user experience  
**Deliverables:**
1. ✅ Post-payment confirmation page
2. ✅ Toast notifications
3. ✅ Feature access middleware
4. ✅ Documentation updated

**Effort:** 4-6 hours total

---

### Sprint 3 (Week 3) - Focus: Edge Cases
**Goal:** Complete subscription lifecycle  
**Deliverables:**
1. ✅ Downgrade logic
2. ✅ Refund handling
3. ✅ Admin dashboard (basic)

**Effort:** 8-10 hours total

---

## 📝 NOTES

### Testing Environment
- **Staging URL:** https://staging.trulyinvoice.xyz
- **Test Razorpay Keys:** Use test mode keys only
- **Test Cards:** 
  - Success: 4111 1111 1111 1111
  - Failure: 4000 0000 0000 0002

### Monitoring
- **Sentry:** Monitor for payment errors
- **Logs:** Check `/var/log/trulyinvoice/backend.log`
- **Database:** Watch `scans_used_this_period` field

### Rollback Plan
```bash
# If critical issues found:
1. git revert <commit_hash>
2. docker restart backend
3. Verify old behavior restored
4. Investigate issue
5. Fix and redeploy
```

---

## ✅ SIGN-OFF

### Critical Fix Deployed
- [ ] QA Lead Approval: _________________ Date: _______
- [ ] Tech Lead Approval: _________________ Date: _______
- [ ] Product Owner Approval: _________________ Date: _______

### Production Deployment
- [ ] DevOps Approval: _________________ Date: _______
- [ ] Monitoring Confirmed: _________________ Date: _______

---

**Document Version:** 1.0  
**Last Updated:** January 2025  
**Maintained By:** Development Team  
**Review Frequency:** After each sprint
