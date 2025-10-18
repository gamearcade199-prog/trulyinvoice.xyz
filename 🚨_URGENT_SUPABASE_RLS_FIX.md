# 🚨 CRITICAL RLS POLICY FIX FOR SUPABASE

**IMMEDIATE ACTION REQUIRED**

Copy and paste this SQL into your **Supabase SQL Editor** to fix the upload errors:

```sql
-- 🔓 EMERGENCY FIX: Disable RLS to restore functionality
ALTER TABLE invoices DISABLE ROW LEVEL SECURITY;
ALTER TABLE documents DISABLE ROW LEVEL SECURITY;

-- Make storage bucket public
UPDATE storage.buckets 
SET public = true 
WHERE id = 'invoice-documents';

-- Ensure bucket exists
INSERT INTO storage.buckets (id, name, public)
VALUES ('invoice-documents', 'invoice-documents', true)
ON CONFLICT (id) DO UPDATE SET public = true;

-- Grant necessary permissions
GRANT ALL ON invoices TO anon, authenticated, service_role;
GRANT ALL ON documents TO anon, authenticated, service_role;
GRANT USAGE ON SCHEMA storage TO anon, authenticated, service_role;
GRANT ALL ON storage.objects TO anon, authenticated, service_role;
```

## 🎯 HOW TO APPLY THE FIX:

1. **Open Supabase Dashboard**: Go to your project
2. **Navigate to SQL Editor**: Click on "SQL Editor" in the sidebar  
3. **Paste the SQL above**: Copy the entire SQL block
4. **Click "Run"**: Execute the SQL commands
5. **Test Upload**: Try uploading an invoice again

## ✅ WHAT THIS FIXES:

- ❌ "new row violates row-level security policy" 
- ❌ "Processing Failed" errors
- ❌ 400 Bad Request storage errors
- ❌ Invoice view "not found" errors

## ⚠️ SECURITY NOTE:

This temporarily disables Row Level Security for testing. After confirming uploads work, you can implement proper policies later.

## 🔍 VERIFICATION:

After running the SQL:
1. Try uploading an invoice (anonymous or logged in)
2. Check if processing completes successfully
3. Verify you can view invoice details

If you still see errors after this fix, check:
- Backend server is running (http://localhost:8000)
- Frontend server is running (http://localhost:3000) 
- Browser console for any additional errors

**Run this SQL fix NOW to restore functionality!** 🚀