# 🚨 404 FIX - ADVANCED DIAGNOSIS

## What I See From Your Screenshot

✅ **Invoices ARE showing in the list**
- "WhatsApp Image 2025-10-13 at 11.18.36..." visible
- Amount: ₹0.00
- Status: Pending
- Confidence: 9/10

❌ **But clicking eye icon shows 404**
- Console shows multiple 404 errors
- IDs like `8507ec01-5117-4148-8858-eeb2584e2863` → NOT FOUND
- Another: `357a0e56-f383-4564-8e03-8808948a25d1` → NOT FOUND

---

## 🎯 MOST LIKELY CAUSE

The issue is **user_id filtering**:

1. **Frontend** fetches invoices for logged-in user → Works ✅
2. **Frontend** stores invoice IDs locally → Shows in list ✅
3. **Backend** queries invoices by ID → But applies user_id filter → 404 ❌

### Why?

The backend endpoint might have user authentication that filters invoices by the **current logged-in user**, and there could be a mismatch:
- User A uploads invoice
- Invoice saved with user A's ID
- User B logs in
- Clicks eye icon on User A's invoice
- Backend filters: "WHERE id = X AND user_id = [logged in user]"
- Returns 404 because user IDs don't match

---

## 🔧 EXACT SQL TO RUN - FOCUSED ON USER_ID

Copy and run this in Supabase SQL Editor:

```sql
-- =====================================================
-- FOCUSED USER_ID DEBUG
-- =====================================================

-- 1. Show all users in system
SELECT 'Users in System' as section, id, email, created_at
FROM users
LIMIT 20;

-- 2. Show invoices with their user associations
SELECT 'All Invoices with User Info' as section,
  i.id as invoice_id,
  i.user_id,
  i.vendor_name,
  i.invoice_number,
  u.email as user_email
FROM invoices i
LEFT JOIN users u ON i.user_id = u.id
LIMIT 50;

-- 3. Count invoices per user
SELECT 'Invoice Count Per User' as section,
  u.id,
  u.email,
  COUNT(i.id) as invoice_count
FROM users u
LEFT JOIN invoices i ON u.id = i.user_id
GROUP BY u.id, u.email
ORDER BY COUNT(i.id) DESC;

-- 4. Show invoices with NULL user_id (anonymous)
SELECT 'Invoices with NULL user_id' as section,
  COUNT(*) as anonymous_invoice_count
FROM invoices
WHERE user_id IS NULL;

-- 5. Show current auth users (from Supabase auth_users table if exists)
SELECT 'Auth Table Check' as section,
  id,
  email,
  created_at
FROM auth.users
LIMIT 10;

-- 6. See if auth.users and public.users match
SELECT 'User ID Mismatch Check' as section,
  a.id as auth_user_id,
  a.email as auth_email,
  p.id as public_user_id,
  p.email as public_email
FROM auth.users a
LEFT JOIN public.users p ON a.id::text = p.id::text
LIMIT 20;

-- 7. Copy ONE invoice ID from earlier and test
-- Replace UUID_HERE with actual invoice ID from your list
SELECT 'Direct Invoice Query Test' as section,
  id,
  vendor_name,
  user_id,
  created_at
FROM invoices
WHERE id = 'UUID_HERE'
LIMIT 1;

-- 8. Show auth session if possible
SELECT 'Current Session Check' as section,
  current_user as session_user,
  session_user as session_info,
  current_database() as db_name;
```

---

## 📱 EXACT STEPS

1. **Go to:** https://app.supabase.com
2. **Select project:** trulyinvoice.xyz
3. **Click:** SQL Editor
4. **Click:** New Query
5. **Paste** the SQL above
6. **Click:** Run
7. **Copy ALL output** and share with me

---

## 🔍 WHAT TO LOOK FOR

### Section 1 - Users in System
Shows all users. If you only see 1-2 users, that's normal.

### Section 2 - All Invoices with User Info
**KEY INSIGHT:** Look at `user_id` column:
```
✅ If filled with UUIDs → user_id is being saved
❌ If shows NULL for all → user_id is NOT being saved
```

### Section 3 - Invoice Count Per User
**Shows:** Which user created which invoices
```
✅ If shows "email: john@example.com | count: 5" → Normal
❌ If shows "email: NULL | count: 50" → Big problem (anonymous)
```

### Section 5 - Auth Users
Shows Supabase internal auth table. Should match your users.

### Section 6 - User ID Mismatch
**CRITICAL:** Checks if auth.users IDs match public.users IDs
```
✅ If auth_user_id matches public_user_id → Good
❌ If they don't match → FOUND THE BUG!
```

### Section 7 - Direct Query Test
Replace `UUID_HERE` with an actual invoice ID from the list:
```
If returns 1 row with user_id:        Invoice exists ✅
If returns 1 row with NULL user_id:   Invoice is anonymous ⚠️
If returns 0 rows:                     Invoice not in DB ❌
```

---

## 🎯 POTENTIAL FIXES

### If Section 6 shows ID mismatch:

The user IDs don't match between auth.users and public.users tables.

**Fix in backend** (`backend/app/services/document_processor.py`):

Change this line (around line 381):
```python
'user_id': document.get('user_id'),  # ← Current (might be wrong format)
```

To this:
```python
'user_id': str(document.get('user_id')),  # ← Convert to string if UUID
```

Or this (if using auth):
```python
'user_id': document.get('user_id') or auth.uid,  # ← Use auth context
```

---

### If Section 3 shows many NULL user_id:

Invoices are being created as anonymous (no user associated).

**Fix:** Ensure document creation includes user_id:

In `backend/app/api/documents.py` or upload endpoint:
```python
# When creating document, must include user_id
document = {
    'user_id': current_user.id,  # ← MUST NOT BE NULL
    'file_name': filename,
    'storage_path': path,
    ...
}
```

---

## 🚀 QUICK FIX: BYPASS USER_ID CHECK

**Temporary fix** - Query invoices WITHOUT user_id filter:

In `backend/app/api/invoices.py` line ~35:

Change:
```python
invoices = supabase.select("invoices", filters={"id": invoice_id})
```

To:
```python
# Don't filter by user_id - just get by invoice ID
invoices = supabase.select("invoices", filters={"id": invoice_id})
# This already doesn't filter by user_id, so that's good
```

Actually this is already correct! So the issue must be with **how the invoice is being saved**.

---

## 📊 FINAL DIAGNOSIS COMMAND

If you want to see EVERYTHING about why 404 happens:

```sql
-- Find an invoice ID that shows 404
-- Replace with actual ID from browser console error
SELECT 
  'COMPLETE 404 ANALYSIS' as analysis,
  i.id as invoice_id,
  i.user_id,
  i.document_id,
  i.vendor_name,
  i.total_amount,
  i.created_at,
  d.id as doc_id,
  d.file_name,
  d.user_id as doc_user_id,
  u.id as user_id,
  u.email
FROM invoices i
LEFT JOIN documents d ON i.document_id = d.id
LEFT JOIN users u ON i.user_id = u.id
WHERE i.id = '8507ec01-5117-4148-8858-eeb2584e2863'  -- Replace with actual ID
LIMIT 1;
```

---

## 📞 AFTER RUNNING SQL

Share:
1. **Complete SQL output** (all sections)
2. **Specific invoice IDs** that show 404
3. **Result of the "Final Diagnosis Command"**

Then I'll know **EXACTLY** what's wrong and how to fix it! 🎯

