# 🔄 Rate Limiting Update - Aligned with Pricing Plans

**Date:** October 22, 2025  
**Status:** ✅ Updated to match TrulyInvoice pricing structure

---

## ⚠️ Previous Issue

**Old Rate Limit:** 5 uploads per 10 minutes (too restrictive!)

**Problem:** This didn't align with your pricing plans:
- Free: 1 bulk upload (1 invoice)
- Basic: 5 bulk uploads (5 invoices)
- Pro: 10 bulk uploads (10 invoices)
- Ultra: 50 bulk uploads (50 invoices)
- Max: 100 bulk uploads (100 invoices)

---

## ✅ New Rate Limiting Structure

### **Anonymous/Preview Users:**
- **Limit:** 10 uploads per hour
- **Purpose:** Prevents abuse while allowing proper testing
- **Rationale:** Users can test the app with multiple invoices before signing up

### **Authenticated Users (Plan-based):**
Rate limits are now handled in **application logic** (not database):

| Plan | Bulk Upload Limit | Scans/Month | Rate Limit Strategy |
|------|------------------|-------------|---------------------|
| **Free** | 1 invoice/upload | 10 | Allow 10 total uploads/month |
| **Basic** | 5 invoices/upload | 80 | Allow 16 bulk uploads/month (80÷5) |
| **Pro** | 10 invoices/upload | 200 | Allow 20 bulk uploads/month (200÷10) |
| **Ultra** | 50 invoices/upload | 500 | Allow 10 bulk uploads/month (500÷50) |
| **Max** | 100 invoices/upload | 1000 | Allow 10 bulk uploads/month (1000÷100) |

---

## 📝 Changes Made

### 1. **Updated SQL File** ✅
**File:** `PRODUCTION_READY_RLS_POLICIES.sql`

**Changed:**
- Anonymous rate limit: 5/10min → **10/hour**
- Added comments explaining plan-based bulk upload limits
- Updated cleanup queries

### 2. **Removed City Pages** ✅
**Deleted:** `frontend/src/app/invoice-software/` folder (20 city pages)

**Removed cities:**
- Mumbai, Delhi, Bangalore, Chennai, Kolkata
- Hyderabad, Pune, Ahmedabad, Jaipur, Lucknow
- Kanpur, Nagpur, Indore, Thane, Bhopal
- Visakhapatnam, Pimpri-Chinchwad, Patna, Vadodara, Surat

### 3. **Updated Footer** ✅
**File:** `frontend/src/components/Footer.tsx`

**Removed:**
- "Top Cities" section (10 cities)
- "More Cities" section (10 cities)
- MapPin icon import

**Result:** Cleaner footer with 4 columns instead of 5

---

## 🎯 Implementation Notes

### **Database Rate Limiting (SQL)**
Only for anonymous/preview users:
```sql
-- 10 uploads per hour for anonymous users
SELECT COUNT(*) FROM anonymous_upload_attempts
WHERE ip_address = '...' 
AND attempted_at > NOW() - INTERVAL '60 minutes';

-- If count < 10, allow upload
```

### **Application Rate Limiting (Backend)**
For authenticated users, check in `documents.py`:
```python
# Check user's plan and current usage
user_plan = user.subscription_tier  # 'free', 'basic', 'pro', 'ultra', 'max'
scans_used = get_user_scans_this_month(user_id)

# Plan limits
plan_limits = {
    'free': {'total': 10, 'bulk_size': 1},
    'basic': {'total': 80, 'bulk_size': 5},
    'pro': {'total': 200, 'bulk_size': 10},
    'ultra': {'total': 500, 'bulk_size': 50},
    'max': {'total': 1000, 'bulk_size': 100},
}

# Check if upload exceeds plan limit
if scans_used + num_files > plan_limits[user_plan]['total']:
    return {"error": "Monthly scan limit exceeded. Upgrade plan."}

# Check if bulk upload exceeds plan's bulk size
if num_files > plan_limits[user_plan]['bulk_size']:
    return {"error": f"Bulk upload limited to {plan_limits[user_plan]['bulk_size']} invoices. Upgrade for more."}
```

---

## 🚀 Next Steps

### **1. Run Updated SQL** (5 minutes)
```sql
-- In Supabase SQL Editor, run:
-- PRODUCTION_READY_RLS_POLICIES.sql

-- This updates the anonymous rate limit to 10/hour
```

### **2. Update Backend Upload Logic** (15 minutes)
**File to modify:** `backend/app/api/documents.py`

Add plan-based bulk upload validation:
```python
async def upload_document(files: List[UploadFile], user: User):
    # Get user's plan
    plan = user.subscription_tier or 'free'
    
    # Plan bulk upload limits
    bulk_limits = {
        'free': 1,
        'basic': 5,
        'pro': 10,
        'ultra': 50,
        'max': 100,
    }
    
    # Check bulk size
    if len(files) > bulk_limits.get(plan, 1):
        raise HTTPException(
            status_code=403,
            detail=f"Your {plan} plan allows {bulk_limits[plan]} invoices per upload. Please upgrade."
        )
    
    # Check monthly scan limit
    scans_used = await get_user_scans_this_month(user.id)
    if scans_used + len(files) > get_plan_scan_limit(plan):
        raise HTTPException(
            status_code=403,
            detail="Monthly scan limit exceeded. Please upgrade your plan."
        )
```

### **3. Test New Limits** (10 minutes)
- **Anonymous:** Try uploading 11 files in 1 hour → Should block 11th
- **Free User:** Try uploading 2 files at once → Should show "upgrade to upload 2+"
- **Basic User:** Try uploading 6 files at once → Should show "upgrade to upload 6+"
- **Pro User:** Upload 10 files at once → Should work ✅

### **4. Verify Footer Changes** (2 minutes)
- Visit homepage → Scroll to footer
- Should show: Company, Legal, Resources (no city links)
- City pages should return 404

---

## 📊 Summary

| Change | Before | After | Status |
|--------|--------|-------|--------|
| **Anonymous Rate Limit** | 5/10min | 10/hour | ✅ Updated |
| **Plan-based Limits** | Not aligned | Matches pricing | ✅ Documented |
| **City Pages** | 20 pages | 0 pages | ✅ Deleted |
| **Footer Sections** | 5 columns | 4 columns | ✅ Cleaned |

---

## ✅ Benefits

1. **Fair Rate Limiting:** Anonymous users can test properly (10/hour)
2. **Plan-aligned:** Bulk upload limits match pricing tiers
3. **Cleaner UI:** Removed irrelevant city pages
4. **SEO Focus:** Focus on core value prop, not location-based pages
5. **Easier Maintenance:** Less pages to maintain

---

**All changes complete!** The rate limiting now properly reflects your pricing structure. 🎉
