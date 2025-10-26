-- =====================================================
-- TrulyInvoice - Supabase Storage Bucket Setup
-- =====================================================
-- This creates the storage bucket for invoice documents
-- Run this in Supabase Dashboard > SQL Editor
-- =====================================================

-- Note: Storage buckets in Supabase are created via the Dashboard UI, 
-- but you can also create them with SQL using the storage schema

-- =====================================================
-- CREATE STORAGE BUCKET
-- =====================================================

-- Insert the bucket into storage.buckets table
INSERT INTO storage.buckets (id, name, public, file_size_limit, allowed_mime_types)
VALUES (
    'invoice-documents',  -- Bucket ID
    'invoice-documents',  -- Bucket name
    false,                -- NOT public (private bucket)
    52428800,            -- 50 MB file size limit (in bytes)
    ARRAY[
        'application/pdf',
        'image/jpeg',
        'image/jpg',
        'image/png',
        'image/webp'
    ]
)
ON CONFLICT (id) DO NOTHING;

-- =====================================================
-- STORAGE POLICIES (Row Level Security)
-- =====================================================

-- Policy 1: Users can upload their own documents
-- Files are stored in folders named by user_id: /user_id/filename
CREATE POLICY "Users can upload own documents"
ON storage.objects FOR INSERT
TO authenticated
WITH CHECK (
    bucket_id = 'invoice-documents' AND
    (storage.foldername(name))[1] = auth.uid()::text
);

-- Policy 2: Users can view/download their own documents
CREATE POLICY "Users can view own documents"
ON storage.objects FOR SELECT
TO authenticated
USING (
    bucket_id = 'invoice-documents' AND
    (storage.foldername(name))[1] = auth.uid()::text
);

-- Policy 3: Users can update their own documents
CREATE POLICY "Users can update own documents"
ON storage.objects FOR UPDATE
TO authenticated
USING (
    bucket_id = 'invoice-documents' AND
    (storage.foldername(name))[1] = auth.uid()::text
);

-- Policy 4: Users can delete their own documents
CREATE POLICY "Users can delete own documents"
ON storage.objects FOR DELETE
TO authenticated
USING (
    bucket_id = 'invoice-documents' AND
    (storage.foldername(name))[1] = auth.uid()::text
);

-- =====================================================
-- VERIFICATION QUERIES
-- =====================================================

-- Check if bucket was created
SELECT * FROM storage.buckets WHERE id = 'invoice-documents';

-- Check storage policies
SELECT * FROM pg_policies WHERE tablename = 'objects' AND policyname LIKE '%own documents%';

-- =====================================================
-- WHY PRIVATE BUCKET? (Security Reasons)
-- =====================================================

/*
 * PRIVATE BUCKET (public = false) - RECOMMENDED ✅
 * ================================================
 * 
 * 1. SECURITY & PRIVACY:
 *    - Invoice documents contain sensitive business data (vendor info, amounts, GST numbers)
 *    - Only authenticated users can access files
 *    - Each user can ONLY see their own documents
 *    - No one can guess URLs and access other users' files
 * 
 * 2. COMPLIANCE:
 *    - GDPR compliance: User data is protected
 *    - Indian data protection laws: Business financial data is secured
 *    - Prevents data leaks and unauthorized access
 * 
 * 3. ROW LEVEL SECURITY (RLS):
 *    - Storage policies enforce user_id matching
 *    - Files stored as: /user_id/filename.pdf
 *    - Policy checks: (storage.foldername(name))[1] = auth.uid()::text
 *    - Users can't access files outside their folder
 * 
 * 4. ACCESS CONTROL:
 *    - Files require authentication token to access
 *    - Backend validates user permissions before serving files
 *    - Prevents direct URL sharing (security risk)
 * 
 * 5. BUSINESS LOGIC:
 *    - You can track who accesses what (usage logs)
 *    - You can implement download limits per subscription tier
 *    - You can add watermarks or processing before serving
 * 
 * 
 * PUBLIC BUCKET (public = true) - NOT RECOMMENDED ❌
 * =================================================
 * 
 * Issues with public buckets:
 * - Anyone with URL can download files
 * - No authentication required
 * - Sensitive invoice data exposed
 * - Can't track or limit access
 * - Violates data privacy regulations
 * - Risk of data scraping/theft
 * 
 * 
 * HOW PRIVATE BUCKET WORKS:
 * =========================
 * 
 * Upload Flow:
 * 1. User authenticated → Gets JWT token
 * 2. Frontend sends file with auth token
 * 3. Backend verifies user identity
 * 4. File saved to: invoice-documents/user_id/filename.pdf
 * 5. Storage policy checks if folder name matches user_id
 * 6. Only allows if match = secure upload ✅
 * 
 * Download Flow:
 * 1. User requests file
 * 2. Backend checks ownership in database
 * 3. Generates signed URL (temporary, time-limited)
 * 4. User can download for limited time (e.g., 60 seconds)
 * 5. URL expires → Can't be reused or shared
 * 
 * 
 * SIGNED URLs (for private buckets):
 * ==================================
 * 
 * Example in your backend code:
 * 
 *   from supabase import create_client
 *   
 *   # Create signed URL (valid for 60 seconds)
 *   signed_url = supabase.storage.from_('invoice-documents').create_signed_url(
 *       f"{user_id}/{filename}",
 *       expires_in=60
 *   )
 *   
 *   # This URL can be used once, then expires
 *   return {"download_url": signed_url}
 * 
 * 
 * FOLDER STRUCTURE:
 * =================
 * 
 * invoice-documents/
 * ├── 550e8400-e29b-41d4-a716-446655440000/  (user 1's UUID)
 * │   ├── invoice_001.pdf
 * │   ├── receipt_002.jpg
 * │   └── bill_003.png
 * ├── 660e8400-e29b-41d4-a716-446655440001/  (user 2's UUID)
 * │   ├── invoice_abc.pdf
 * │   └── receipt_xyz.jpg
 * └── 770e8400-e29b-41d4-a716-446655440002/  (user 3's UUID)
 *     └── invoice_test.pdf
 * 
 * Each user has their own folder (named by their UUID)
 * RLS policies ensure users can't access other folders
 * 
 * 
 * SUBSCRIPTION TIER BENEFITS:
 * ===========================
 * 
 * With private bucket, you can enforce:
 * - Starter: 30 scans, 30-day retention → Auto-delete old files
 * - Pro: 200 scans, 90-day retention → Keep files longer
 * - Business: Unlimited retention → Never delete
 * 
 * This wouldn't be possible with public buckets!
 */

-- =====================================================
-- FILE RETENTION POLICY (Optional - Advanced)
-- =====================================================

-- Function to delete old files based on subscription tier
CREATE OR REPLACE FUNCTION delete_expired_documents()
RETURNS void AS $$
DECLARE
    rec RECORD;
    retention_days INTEGER;
BEGIN
    -- Loop through all users and their subscription tiers
    FOR rec IN 
        SELECT u.id as user_id, s.tier
        FROM users u
        JOIN subscriptions s ON u.id = s.user_id
    LOOP
        -- Set retention days based on tier
        retention_days := CASE
            WHEN rec.tier = 'starter' THEN 30
            WHEN rec.tier = 'pro' THEN 90
            WHEN rec.tier = 'business' THEN 36500  -- ~100 years (unlimited)
        END;
        
        -- Delete documents older than retention period
        DELETE FROM documents
        WHERE user_id = rec.user_id
        AND created_at < NOW() - (retention_days || ' days')::INTERVAL;
        
        -- Note: This only deletes database records
        -- Storage files should be deleted via backend API
    END LOOP;
END;
$$ LANGUAGE plpgsql;

-- Schedule this function to run daily (optional)
-- You can use Supabase Edge Functions or pg_cron for scheduling

-- =====================================================
-- COMPLETED!
-- =====================================================
-- Your storage bucket is now configured with:
-- ✅ Private access (secure)
-- ✅ File size limits (50 MB)
-- ✅ MIME type restrictions (PDF, JPG, PNG only)
-- ✅ Row Level Security policies
-- ✅ User folder isolation
-- 
-- Next: Test by uploading a file via your application!
-- =====================================================
