# 🔧 REGISTRATION FIX - QUICK START

## ❌ Problem
Users see "**Database error saving new user**" when trying to register.

## ✅ Solution
Run the SQL script to fix RLS policies in Supabase.

---

## 📝 STEPS TO FIX

### Step 1: Open Supabase Dashboard
1. Go to https://supabase.com/dashboard
2. Select your project: `ldvwxqluaheuhbycdpwn`
3. Click **SQL Editor** in the left sidebar

### Step 2: Run the Fix Script
1. Click **New Query**
2. Copy the entire contents of `FIX_REGISTRATION_SIMPLE.sql`
3. Paste into the SQL Editor
4. Click **Run** (or press Ctrl+Enter)

### Step 3: Verify Success
You should see output like:
```
✅ RLS POLICIES UPDATED
The service_role (backend) can now:
   ✅ INSERT subscriptions for new users
🎉 Registration should now work!
```

### Step 4: Test Registration
1. Go to http://localhost:3000/register
2. Try registering a new user (use a NEW email)
3. Should redirect to dashboard with FREE plan activated

---

## 🔍 WHAT WAS THE ISSUE?

### Technical Explanation
1. **User fills registration form** → Frontend (React)
2. **Frontend calls Supabase Auth** → Creates user in `auth.users` ✅
3. **Frontend calls backend `/api/auth/setup-user`** → Creates subscription ❌
4. **Backend tries to INSERT into `subscriptions` table** → BLOCKED by RLS policy ❌
5. **User sees error:** "Database error saving new user" ❌

### Root Cause
The `subscriptions` table had RLS (Row Level Security) enabled, but NO policy allowed the **service_role** (backend) to INSERT records.

### The Fix
Added explicit RLS policy:
```sql
CREATE POLICY "Allow service role to insert subscriptions"
ON subscriptions
FOR INSERT
TO service_role
WITH CHECK (true);
```

This tells Supabase: "Let the backend create subscription records for new users."

---

## 🎯 ALTERNATIVE: Python Script (if SQL doesn't work)

If running SQL doesn't work, you can use the Python script approach:

```bash
# For any user who registered but got the error:
python fix_registration.py their-email@example.com
```

This manually creates the subscription record for users who registered but got stuck.

---

## ✅ AFTER THE FIX

### What Happens Now
1. User registers → Creates account in Supabase Auth ✅
2. Backend creates FREE subscription → No error ✅
3. User redirected to dashboard → Can start using app ✅

### Default Plan for New Users
- **Tier:** FREE
- **Scans:** 10/month
- **Storage:** 30 days
- **Status:** Active
- **Valid:** 30 days (renews monthly)

### Users Can Upgrade
After registration, users can go to `/pricing` to upgrade to:
- **BASIC:** ₹99/month - 80 scans
- **PRO:** ₹299/month - 200 scans
- **ULTRA:** ₹499/month - 500 scans
- **MAX:** ₹999/month - 1000 scans

---

## 🚨 IF USERS ALREADY REGISTERED

If users already tried to register and got the error:

### Option 1: They Can Try Again
After running the fix, they can:
1. Try registering with the SAME email again
2. If it says "already registered", they can just login
3. Their account exists, just needs subscription setup

### Option 2: Manual Fix
Run the Python script for each affected user:
```bash
python fix_registration.py user1@example.com
python fix_registration.py user2@example.com
```

---

## 📊 VERIFICATION QUERIES

### Check if fix worked:
```sql
-- See all RLS policies on subscriptions table
SELECT policyname, cmd, roles 
FROM pg_policies 
WHERE tablename = 'subscriptions';
```

### Check existing subscriptions:
```sql
-- See all active subscriptions
SELECT 
    user_id, 
    tier, 
    status, 
    scans_used_this_period,
    current_period_end
FROM subscriptions
WHERE status = 'active';
```

### Find users without subscriptions:
```sql
-- Users who registered but have no subscription
SELECT 
    u.email,
    u.id,
    u.created_at
FROM auth.users u
LEFT JOIN subscriptions s ON u.id = s.user_id
WHERE s.id IS NULL;
```

---

## 📝 FILES CREATED

1. **FIX_REGISTRATION_SIMPLE.sql** - Run this in Supabase SQL Editor
2. **fix_registration.py** - Python script for manual subscription creation
3. **REGISTRATION_FIX_GUIDE.md** - This guide

---

## ✅ SUCCESS CHECKLIST

- [ ] Ran `FIX_REGISTRATION_SIMPLE.sql` in Supabase
- [ ] Saw success message with ✅ checkmarks
- [ ] Tested new registration with a new email
- [ ] User redirected to dashboard successfully
- [ ] User sees "FREE" plan in pricing page
- [ ] No "Database error" message appears

---

## 🆘 IF IT STILL DOESN'T WORK

1. **Check backend logs:**
   ```bash
   # Backend should show:
   INFO: New user registered: a1b2c3d4... (email@example.com)
   ```

2. **Check frontend console:**
   - Open browser DevTools (F12)
   - Look for errors in Console tab
   - Check Network tab for failed `/api/auth/setup-user` requests

3. **Verify Supabase connection:**
   ```bash
   python upgrade_user_simple.py
   # Should connect successfully
   ```

4. **Check service role key:**
   - In `backend/.env`
   - Should have `SUPABASE_SERVICE_KEY=` or `SUPABASE_KEY=`
   - This key must have service_role permissions

---

**Created:** November 3, 2025  
**Status:** ✅ Ready to Deploy  
**Affected:** All new user registrations
