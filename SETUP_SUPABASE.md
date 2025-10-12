# Supabase Setup Guide

## Step 1: Execute Database Schema (3 minutes)

### 1.1 Open Supabase Dashboard
1. Go to https://app.supabase.com
2. Login to your account
3. Select your project

### 1.2 Run SQL Schema
1. Click **SQL Editor** in the left sidebar
2. Click **+ New Query** button
3. Open the file `SUPABASE_SCHEMA.sql` in this project
4. **Copy ALL contents** (500+ lines)
5. **Paste** into the SQL Editor
6. Click **Run** button (or press Ctrl+Enter)
7. Wait for success message: "Success. No rows returned"

### 1.3 Verify Tables Created
1. Click **Table Editor** in left sidebar
2. You should see 6 tables:
   - ✓ users
   - ✓ subscriptions
   - ✓ documents
   - ✓ invoices
   - ✓ categories
   - ✓ usage_logs

---

## Step 2: Create Storage Bucket (2 minutes)

### 2.1 Open Storage
1. Click **Storage** in left sidebar
2. Click **Create a new bucket** button

### 2.2 Configure Bucket
1. **Name**: `invoice-documents`
2. **Public bucket**: **OFF** (Keep it Private)
3. **Allowed MIME types**: Leave empty (allow all)
4. **File size limit**: 50 MB (default)
5. Click **Create bucket**

### 2.3 Set Storage Policies
1. Click on the `invoice-documents` bucket
2. Click **Policies** tab
3. Click **New Policy**
4. Select **For full customization**
5. Add these policies:

#### Policy 1: Allow Authenticated Upload
```sql
-- Policy Name: Users can upload their own files
-- Target: INSERT

CREATE POLICY "Users can upload their own files"
ON storage.objects FOR INSERT
TO authenticated
WITH CHECK (
  bucket_id = 'invoice-documents' AND
  (storage.foldername(name))[1] = auth.uid()::text
);
```

#### Policy 2: Allow Authenticated Read
```sql
-- Policy Name: Users can read their own files
-- Target: SELECT

CREATE POLICY "Users can read their own files"
ON storage.objects FOR SELECT
TO authenticated
USING (
  bucket_id = 'invoice-documents' AND
  (storage.foldername(name))[1] = auth.uid()::text
);
```

#### Policy 3: Allow Authenticated Delete
```sql
-- Policy Name: Users can delete their own files
-- Target: DELETE

CREATE POLICY "Users can delete their own files"
ON storage.objects FOR DELETE
TO authenticated
USING (
  bucket_id = 'invoice-documents' AND
  (storage.foldername(name))[1] = auth.uid()::text
);
```

---

## Step 3: Verify Setup

### 3.1 Check Database
1. Go to **Table Editor**
2. Click on `users` table - should be empty
3. Click on `categories` table - should be empty (will populate when first user registers)
4. Click on `subscriptions` table - should be empty

### 3.2 Check Storage
1. Go to **Storage**
2. Click on `invoice-documents` bucket
3. Should be empty
4. Verify **Public** is OFF

### 3.3 Check Policies
1. Go to **Authentication** → **Policies**
2. Should see RLS policies for all 6 tables:
   - users (2 policies: SELECT, UPDATE)
   - subscriptions (1 policy: SELECT)
   - documents (2 policies: SELECT, INSERT)
   - invoices (3 policies: SELECT, INSERT, UPDATE)
   - categories (3 policies: SELECT, INSERT, UPDATE)
   - usage_logs (1 policy: INSERT)

---

## Step 4: Test Database Connection

### From Backend Server
Once your backend is running, test the database:

1. Start backend server: `.\START_BACKEND.ps1`
2. Open browser: http://localhost:8000/docs
3. Try the **POST /auth/register** endpoint:
   ```json
   {
     "email": "test@example.com",
     "password": "testpassword123",
     "full_name": "Test User",
     "company_name": "Test Company"
   }
   ```
4. Should get success response with user ID (UUID format)
5. Go to Supabase Table Editor → `users` → Should see the new user
6. Check `categories` table → Should see 10 default categories created automatically
7. Check `subscriptions` table → Should see 1 starter subscription created automatically

---

## Troubleshooting

### Error: "relation does not exist"
**Solution**: SQL schema not executed. Go back to Step 1.2 and run the SQL.

### Error: "permission denied"
**Solution**: RLS policies not created. Check Step 1.2 - make sure you ran the COMPLETE schema file.

### Error: "bucket not found"
**Solution**: Storage bucket not created. Go back to Step 2 and create the bucket.

### Error: "uuid_generate_v4() function not found"
**Solution**: UUID extension not enabled. Run this SQL:
```sql
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
```

### Storage uploads fail
**Solution**: Storage policies not set. Go back to Step 2.3 and add the policies.

---

## ✅ Setup Complete Checklist

Before proceeding to test the application:

- [ ] Executed `SUPABASE_SCHEMA.sql` in SQL Editor
- [ ] Verified 6 tables exist in Table Editor
- [ ] Created `invoice-documents` storage bucket
- [ ] Set bucket to Private (not public)
- [ ] Added 3 storage policies (upload, read, delete)
- [ ] Verified RLS policies exist for all tables
- [ ] Tested database connection with user registration

---

## Next Steps

After Supabase setup is complete:

1. **Fix Frontend** - Run `.\FIX_FRONTEND.ps1` to resolve SWC issue
2. **Start Backend** - Run `.\START_BACKEND.ps1` (http://localhost:8000)
3. **Start Frontend** - Run `npm run dev` in frontend folder (http://localhost:3000)
4. **Test Complete Flow**:
   - Register new user
   - Login
   - Upload invoice (PDF/JPG/PNG)
   - Verify AI extraction
   - Check data in Supabase Dashboard

---

**Need Help?**
- Supabase Docs: https://supabase.com/docs
- Check `DIAGNOSTIC_REPORT.md` for detailed troubleshooting
- Review backend logs for database connection errors
