# Comprehensive System Test Checklist

## Test Status: Ready for Testing
**Date**: October 22, 2025

---

## ✅ CRITICAL FIXES COMPLETED

### 1. Payment Integration Fix
- ✅ **Fixed**: API route mismatch - Renamed `verify-payment` → `verify` to match hook call
- ✅ **Fixed**: Payment amount now sent in paise (₹999 → 99900 paise)
- ✅ **Fixed**: Processing state only shows on clicked button (not all buttons)

### 2. Code Quality Fixes
- ✅ Fixed 6 bare `except:` blocks in backend
- ✅ Set DEBUG=false default for production
- ✅ Created TypeScript types for Invoice, User, Document
- ✅ Created logger and env validator utilities

### 3. Razorpay Configuration
- ✅ LIVE Key ID: `rzp_live_RUCxZnVyqol9Nv`
- ✅ LIVE Secret: `I4f1ljrMQf5yqTCXSQ0eSM1A`
- ✅ Configured in both frontend and backend `.env` files

---

## 🧪 TESTING WORKFLOW

### Phase 1: Authentication Flow ⏳

#### 1.1 Sign Up (New User)
- [ ] Navigate to `/register`
- [ ] Enter email, password, full name
- [ ] Check email for verification link
- [ ] Click verification link
- [ ] Verify redirect to dashboard
- [ ] Check user created in Supabase `users` table
- [ ] Verify default plan = "free"

#### 1.2 Sign In (Existing User)
- [ ] Navigate to `/login`
- [ ] Enter credentials
- [ ] Verify redirect to dashboard
- [ ] Check session persists on page refresh
- [ ] Test "Remember me" functionality

#### 1.3 Password Reset
- [ ] Click "Forgot Password"
- [ ] Enter email
- [ ] Check email for reset link
- [ ] Set new password
- [ ] Login with new password

---

### Phase 2: Pricing & Payment Flow 💳

#### 2.1 View Pricing Plans
- [ ] Navigate to `/pricing`
- [ ] Verify 5 plans displayed: Free, Basic (₹149), Pro (₹299), Ultra (₹599), Max (₹999)
- [ ] Check Monthly/Yearly toggle works
- [ ] Verify yearly shows 20% discount
- [ ] Check "Popular" badge on Pro plan

#### 2.2 Purchase Plan (Use Test Mode First!)
**WARNING: Currently configured with LIVE keys - Switch to TEST keys first!**

- [ ] Click "Get Started" on Basic plan (₹149)
- [ ] Verify button shows "Processing..."
- [ ] Check Razorpay modal opens
- [ ] Verify amount shows ₹149.00 (not ₹1.49)
- [ ] Enter contact number
- [ ] Select payment method (UPI/Card/NetBanking)
- [ ] Complete test payment
- [ ] Verify success message
- [ ] Check redirect to `/dashboard/settings`

#### 2.3 Verify Subscription Update
- [ ] Check `users` table in Supabase:
  - [ ] `plan` = "basic" (or selected plan)
  - [ ] `subscription_status` = "active"
  - [ ] `plan_expiry_date` = 1 month from now
- [ ] Verify scans_used = 0
- [ ] Check max_scans updated based on plan

---

### Phase 3: Dashboard & Invoice Processing 📄

#### 3.1 Dashboard Overview
- [ ] Navigate to `/dashboard`
- [ ] Verify plan name displays correctly
- [ ] Check scans used/remaining shows
- [ ] Verify expiry date displays
- [ ] Check recent invoices list

#### 3.2 Upload Invoice
- [ ] Click "Upload Invoice"
- [ ] Select PDF/Image file
- [ ] Verify upload progress shows
- [ ] Check file appears in invoices list
- [ ] Verify status = "pending" or "processing"

#### 3.3 AI Processing
- [ ] Wait for processing to complete
- [ ] Verify status changes to "completed"
- [ ] Check extracted fields populated:
  - [ ] Invoice number
  - [ ] Date
  - [ ] Vendor name
  - [ ] Total amount
  - [ ] GST number (if applicable)
  - [ ] Line items
- [ ] Verify confidence scores shown
- [ ] Check scans_used incremented by 1

#### 3.4 View Invoice Details
- [ ] Click on processed invoice
- [ ] Navigate to `/invoices/details/[id]`
- [ ] Verify all extracted data displays
- [ ] Check confidence indicators
- [ ] Verify edit functionality works
- [ ] Save changes and verify update

---

### Phase 4: Export Functionality 📊

#### 4.1 Export Single Invoice
- [ ] From invoice details page:
  - [ ] Click "Export to Excel"
  - [ ] Verify .xlsx file downloads
  - [ ] Open file and check data accuracy
  - [ ] Click "Export to CSV"
  - [ ] Verify .csv file downloads
  - [ ] Click "Export to PDF"
  - [ ] Verify .pdf file downloads

#### 4.2 Bulk Export
- [ ] From invoices list:
  - [ ] Select multiple invoices (checkbox)
  - [ ] Click "Export Selected to Excel"
  - [ ] Verify all invoices in file
  - [ ] Check data integrity

#### 4.3 Export Template Preference
- [ ] Go to `/dashboard/settings`
- [ ] Change export template preference
- [ ] Export invoice
- [ ] Verify correct template used

---

### Phase 5: Billing & Settings ⚙️

#### 5.1 Settings Page - Billing Tab
- [ ] Navigate to `/dashboard/settings`
- [ ] Click "Billing" tab
- [ ] Verify current plan displays
- [ ] Check **real-time scans used** counter
- [ ] Verify scans remaining calculation
- [ ] Check plan expiry date
- [ ] Verify subscription status

#### 5.2 Plan Upgrade/Downgrade
- [ ] Click "Change Plan"
- [ ] Select different tier
- [ ] Complete payment
- [ ] Verify plan updated
- [ ] Check scans reset/adjusted
- [ ] Verify billing reflects change

#### 5.3 Subscription Cancellation
- [ ] Click "Cancel Subscription"
- [ ] Confirm cancellation
- [ ] Verify status = "cancelled"
- [ ] Check access until expiry date
- [ ] Verify no auto-renewal

---

### Phase 6: Quota & Rate Limiting 🚦

#### 6.1 Free Plan Quota Test
- [ ] Use Free plan (10 scans/month)
- [ ] Upload and process 10 invoices
- [ ] Verify scans_used = 10
- [ ] Try 11th upload
- [ ] Verify quota exceeded message
- [ ] Check upgrade prompt

#### 6.2 Paid Plan Quota Test
- [ ] Upgrade to Basic (80 scans)
- [ ] Verify max_scans = 80
- [ ] Upload multiple invoices
- [ ] Check real-time counter updates
- [ ] Verify no limit until quota reached

---

### Phase 7: Anonymous Upload (Free Tier) 🔓

#### 7.1 Anonymous Processing
- [ ] Navigate to `/` (homepage)
- [ ] Upload invoice without login
- [ ] Verify processing works
- [ ] Check limited features
- [ ] Verify export not available
- [ ] Check signup prompt

---

### Phase 8: Edge Cases & Error Handling ⚠️

#### 8.1 Payment Failures
- [ ] Initiate payment
- [ ] Close Razorpay modal
- [ ] Verify processing state resets
- [ ] Try payment with insufficient funds
- [ ] Verify error handling

#### 8.2 File Upload Errors
- [ ] Upload non-PDF/non-image file
- [ ] Verify error message
- [ ] Upload file > 10MB
- [ ] Check size limit error
- [ ] Upload corrupted PDF
- [ ] Verify graceful handling

#### 8.3 Session Management
- [ ] Login and stay idle
- [ ] Verify no auto-logout (removed feature)
- [ ] Check session persists
- [ ] Manually logout
- [ ] Verify redirect to login

---

## 🔧 ENVIRONMENT VARIABLES CHECKLIST

### Frontend (.env.local)
```bash
✅ NEXT_PUBLIC_SUPABASE_URL
✅ NEXT_PUBLIC_SUPABASE_ANON_KEY
✅ NEXT_PUBLIC_API_URL
✅ NEXT_PUBLIC_RAZORPAY_KEY_ID=rzp_live_RUCxZnVyqol9Nv
✅ RAZORPAY_KEY_SECRET=I4f1ljrMQf5yqTCXSQ0eSM1A
```

### Backend (.env)
```bash
✅ SUPABASE_URL
✅ SUPABASE_SERVICE_ROLE_KEY
✅ GOOGLE_APPLICATION_CREDENTIALS
✅ GEMINI_API_KEY
✅ RAZORPAY_KEY_ID=rzp_live_RUCxZnVyqol9Nv
✅ RAZORPAY_KEY_SECRET=I4f1ljrMQf5yqTCXSQ0eSM1A
✅ DEBUG=false
```

---

## 📊 DATABASE SCHEMA VERIFICATION

### Users Table Fields
- [ ] id (UUID)
- [ ] email
- [ ] full_name
- [ ] plan (free/basic/pro/ultra/max)
- [ ] subscription_status (active/cancelled/expired)
- [ ] scans_used (integer)
- [ ] max_scans (integer)
- [ ] plan_expiry_date (timestamp)
- [ ] export_template (preference)
- [ ] created_at
- [ ] updated_at

### Invoices Table Fields
- [ ] id
- [ ] user_id (FK to users)
- [ ] file_name
- [ ] file_url
- [ ] status (pending/processing/completed/failed)
- [ ] extracted_data (JSONB)
- [ ] confidence_scores (JSONB)
- [ ] uploaded_at
- [ ] processed_at

---

## ⚠️ KNOWN ISSUES & WARNINGS

### 1. Razorpay LIVE Mode Active
**STATUS**: ⚠️ **CRITICAL - LIVE KEYS CONFIGURED**
- Currently using LIVE Razorpay keys
- **ACTION REQUIRED**: Switch to TEST keys before testing payments
- Test Key ID: `rzp_test_...` (obtain from Razorpay dashboard)
- Test Secret: `...` (obtain from Razorpay dashboard)

### 2. TypeScript Version Warning
**STATUS**: ⚠️ Minor
- Using TypeScript 5.9.3 (officially supported: <5.5.0)
- Working fine but may cause ESLint warnings
- No immediate action needed

### 3. React Hooks Warnings
**STATUS**: ⚠️ Minor
- 2 ESLint warnings for missing dependencies
- Files: `invoices/details/page.tsx`, `RazorpayCheckout.tsx`
- Non-blocking, can be fixed with useCallback

---

## 🚀 TESTING SEQUENCE (RECOMMENDED ORDER)

1. **Environment Setup** (5 min)
   - Verify all env variables
   - Start backend server
   - Start frontend server

2. **Authentication** (10 min)
   - Sign up new user
   - Verify email
   - Login/logout

3. **Free Plan Testing** (15 min)
   - Upload invoice
   - Verify AI processing
   - Test exports
   - Check quota limit

4. **Payment Flow** (20 min)
   - **SWITCH TO TEST KEYS FIRST!**
   - View pricing page
   - Purchase Basic plan
   - Verify payment success
   - Check subscription update

5. **Paid Plan Features** (20 min)
   - Upload multiple invoices
   - Test bulk export
   - Verify higher quota
   - Check real-time counter

6. **Settings & Billing** (10 min)
   - View billing details
   - Check scans used display
   - Test plan change
   - Verify updates

7. **Edge Cases** (15 min)
   - Test error scenarios
   - Verify error messages
   - Check graceful degradation

---

## 📝 TEST RESULTS TEMPLATE

### Authentication Flow
- Sign Up: [ PASS / FAIL / SKIP ]
- Sign In: [ PASS / FAIL / SKIP ]
- Password Reset: [ PASS / FAIL / SKIP ]

### Payment Flow
- Pricing Display: [ PASS / FAIL / SKIP ]
- Payment Processing: [ PASS / FAIL / SKIP ]
- Subscription Update: [ PASS / FAIL / SKIP ]

### Invoice Processing
- Upload: [ PASS / FAIL / SKIP ]
- AI Extraction: [ PASS / FAIL / SKIP ]
- Export: [ PASS / FAIL / SKIP ]

### Billing & Settings
- Scans Counter: [ PASS / FAIL / SKIP ]
- Plan Display: [ PASS / FAIL / SKIP ]
- Real-time Updates: [ PASS / FAIL / SKIP ]

---

## 🎯 SUCCESS CRITERIA

✅ **All tests pass** with no critical errors
✅ **Payment flow** works with correct amounts (in paise)
✅ **Real-time scans counter** updates accurately in billing
✅ **Subscription status** reflects correctly in database
✅ **AI processing** extracts data with >90% confidence
✅ **Exports** download successfully with accurate data
✅ **Quota limits** enforced correctly per plan

---

## 📞 SUPPORT & DEBUGGING

### If Payment Fails:
1. Check browser console for errors
2. Verify Razorpay keys in `.env` files
3. Check backend logs: `backend/app/api/payments.py`
4. Verify amount is in paise (multiply by 100)

### If AI Processing Fails:
1. Check Gemini API key
2. Verify Vision API enabled
3. Check file format (PDF/JPG/PNG)
4. Review backend logs

### If Billing Counter Not Updating:
1. Check `scans_used` in Supabase users table
2. Verify API call to increment counter
3. Check frontend polling/refresh logic
4. Review `/dashboard/settings` data fetching

---

**READY TO TEST!** 🚀

**IMPORTANT**: Before testing payments, switch Razorpay to TEST mode!
