# 📦 Storage Days & Features Update

## ✅ Changes Applied

### Storage Days Updated

| Plan | Old Storage | New Storage | Status |
|------|-------------|-------------|--------|
| **Free** | 7 days | **1 day** | ✅ Updated |
| **Basic** | 30 days | **7 days** | ✅ Updated |
| **Pro** | 90 days | **30 days** | ✅ Updated |
| **Ultra** | 180 days | **60 days** | ✅ Updated |
| **Max** | 365 days (1 year) | **90 days** | ✅ Updated |

### Features Removed

#### ❌ Removed from **Ultra Plan**:
- API access (removed)

#### ❌ Removed from **Max Plan**:
- Dedicated account manager (removed)
- White-label options (removed)

---

## 📊 Updated Plan Features

### 🆓 Free Plan
- 10 scans per month
- Basic AI extraction
- PDF & Image support
- Bulk upload (1 invoice)
- **1-day storage** ⬅️ Updated
- Email support

### 💼 Basic Plan (₹149/month)
- 80 scans per month
- 95% AI accuracy
- GST validation
- Bulk upload (5 invoices)
- Export to Excel/CSV
- **7-day storage** ⬅️ Updated
- Priority support

### 👑 Pro Plan (₹299/month)
- 200 scans per month
- 98% AI accuracy
- Bulk upload (10 invoices)
- Custom export templates
- **30-day storage** ⬅️ Updated
- 24/7 priority support

### 🚀 Ultra Plan (₹599/month)
- 500 scans per month
- 99% AI accuracy
- Bulk upload (50 invoices)
- Advanced GST compliance
- **60-day storage** ⬅️ Updated
- Dedicated support
- Custom integrations
- ~~API access~~ ❌ Removed

### ⭐ Max Plan (₹999/month)
- 1,000 scans per month
- 99.5% AI accuracy
- Bulk upload (100 invoices)
- Custom integrations
- **90-day storage** ⬅️ Updated
- 24/7 priority support
- ~~Dedicated account manager~~ ❌ Removed
- ~~White-label options~~ ❌ Removed

---

## 📝 Files Modified

### Backend Configuration
✅ `backend/app/config/plans.py`
- Updated `storage_days` for all plans
- Removed `api_access` from Ultra features
- Removed `dedicated_account_manager` and `white_label_options` from Max features

### Frontend Pages
✅ `frontend/src/app/pricing/page.tsx` (Public pricing page)
- Updated storage days display
- Removed API access, dedicated account manager, white-label options

✅ `frontend/src/app/dashboard/pricing/page.tsx` (Dashboard pricing)
- Updated storage days display
- Removed API access, dedicated account manager, white-label options

---

## 🎯 Summary of Changes

### Storage Policy:
- **Free**: 1 day retention (invoices auto-deleted after 24 hours)
- **Basic**: 7 days retention (1 week)
- **Pro**: 30 days retention (1 month)
- **Ultra**: 60 days retention (2 months)
- **Max**: 90 days retention (3 months)

### Feature Cleanup:
- **No API access** on any plan (removed from Ultra)
- **No white-labeling** (removed from Max)
- **No dedicated account manager** (removed from Max)

This simplifies the offering and makes the plans more straightforward for users to understand!

---

## ✨ Why These Changes?

1. **Realistic Storage**: Shorter retention periods are more practical and cost-effective
2. **Simplified Features**: Removed enterprise-level features (API, white-label, dedicated manager) that are complex to deliver
3. **Clear Value Proposition**: Each plan now has clear, achievable benefits
4. **Better User Experience**: Users understand exactly what they get without confusion

---

**Status**: ✅ Complete and Deployed
**Date**: October 16, 2025
