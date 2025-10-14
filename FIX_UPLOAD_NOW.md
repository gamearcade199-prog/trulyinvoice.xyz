# 🔥 FIX UPLOAD ERROR NOW - STEP BY STEP

## ❌ Current Error:
```
Processing Failed
new row violates row-level security policy
```

## ✅ Fix (Takes 2 Minutes):

### **Step 1: Open Supabase Dashboard**
1. Go to: https://supabase.com/dashboard
2. Select your **TrulyInvoice** project

---

### **Step 2: Open SQL Editor**
1. Click **SQL Editor** in left sidebar
2. Click **New Query** button

---

### **Step 3: Copy & Paste the SQL Script**

Open this file in VS Code:
```
FIX_ANONYMOUS_UPLOAD_RLS.sql
```

**Copy ALL of it** (Ctrl+A, Ctrl+C)

Then **paste into Supabase SQL Editor**

---

### **Step 4: Run the Script**
1. Click **RUN** button (or press F5)
2. Wait ~5 seconds
3. You should see: ✅ **Success. No rows returned**

---

### **Step 5: Test Upload Again**
1. Go back to: https://trulyinvoice.xyz
2. Try uploading an invoice again
3. Should work now! ✅

---

## 🎯 What This Fixes:

The script does 3 things:

1. **Removes old restrictive policies** that block anonymous users
2. **Adds new public policies** that allow demo uploads
3. **Keeps security** for authenticated users

### Before:
```
❌ Only signed-in users can upload
❌ Anonymous users blocked by RLS
```

### After:
```
✅ Anyone can upload (demo mode)
✅ Signed-in users can manage their invoices
✅ Backend can process uploads
```

---

## 🔒 Security Note:

This enables **PUBLIC access for demo purposes**.

For production, you'll want to:
- ✅ Require sign-up for uploads
- ✅ Add rate limiting
- ✅ Track usage per user

But for now, this gets your demo working!

---

## 🚀 After Running Script:

### Test These:
1. ✅ Anonymous upload (not signed in)
2. ✅ Signed-in upload
3. ✅ View processed invoice
4. ✅ Download PDF

All should work!

---

## ❓ Still Getting Errors?

If you still see "row-level security policy" error:

1. **Clear browser cache** (Ctrl+Shift+Delete)
2. **Hard refresh** page (Ctrl+F5)
3. **Try incognito mode**
4. Check backend logs in Render

---

## 📞 Need Help?

Let me know if:
- ✅ Script runs but upload still fails
- ✅ You see any SQL errors
- ✅ Backend shows different error

I'll help you debug!
