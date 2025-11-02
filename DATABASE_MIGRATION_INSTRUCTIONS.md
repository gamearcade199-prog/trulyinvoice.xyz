# 📋 DATABASE MIGRATION INSTRUCTIONS

**Task:** Phase 1.1.3 - Add Subscription Columns to Supabase  
**Time Required:** 5 minutes  
**Difficulty:** Easy (just copy-paste SQL)

---

## 🎯 STEPS TO EXECUTE

### Step 1: Open Supabase SQL Editor

Click this link: **https://supabase.com/dashboard/project/ldvwxqluaheuhbycdpwn/sql**

Or manually navigate:
1. Go to https://supabase.com/dashboard
2. Select your project: `ldvwxqluaheuhbycdpwn`
3. Click "SQL Editor" in left sidebar

---

### Step 2: Copy the SQL Script

The SQL script is in: **`SUPABASE_MIGRATION.sql`** (in your project root)

Or copy from here:
```sql
[See SUPABASE_MIGRATION.sql file]
```

---

### Step 3: Execute the SQL

1. Paste the SQL into the SQL Editor
2. Click the green **"RUN"** button (bottom right)
3. Wait for execution (should take 2-3 seconds)

---

### Step 4: Verify Success

You should see messages like:
```
✅ Added column: razorpay_plan_id
✅ Added column: next_billing_date
✅ Added column: last_payment_date
✅ Added column: payment_retry_count
✅ Added column: last_payment_attempt
✅ Added column: grace_period_ends_at
============================================
MIGRATION VERIFICATION
============================================
New columns found: 6 / 6
✅ ALL COLUMNS ADDED SUCCESSFULLY!
============================================
```

---

### Step 5: Confirm Completion

Once you see the success messages, tell me:
- **"migration done"** or
- **"database updated"** or
- **"columns added"**

And I'll immediately continue with Phase 1.1.4 (API endpoint updates).

---

## ⚠️ IF YOU SEE ERRORS

### Error: "column already exists"
✅ **This is fine!** The script is safe to run multiple times. Just means columns were already there.

### Error: "permission denied"
❌ You need admin access to your Supabase project. Make sure you're logged in as the project owner.

### Error: "relation does not exist"
❌ The subscriptions table doesn't exist yet. The script will create it automatically.

---

## 🔍 WHAT THIS MIGRATION DOES

Adds 6 new columns to track subscription state:

| Column | Purpose |
|--------|---------|
| `razorpay_plan_id` | Which Razorpay plan is active |
| `next_billing_date` | When next charge will happen |
| `last_payment_date` | Last successful payment time |
| `payment_retry_count` | How many retries after failure |
| `last_payment_attempt` | Last retry timestamp |
| `grace_period_ends_at` | When grace period expires |

Plus creates indexes for fast queries.

---

## ✅ AFTER MIGRATION

Once done, we'll move to:
- ✅ Phase 1.1.4: Update API endpoints (30 min)
- ✅ Phase 1.1.5: Update frontend (1 hour)
- ✅ Phase 1.2: Webhook handlers (2 hours)

**Total remaining:** ~4 hours to complete Phase 1

---

**Ready?** Go execute the SQL in Supabase, then let me know when it's done! 🚀
