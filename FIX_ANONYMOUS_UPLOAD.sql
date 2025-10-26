-- FIX FOR ANONYMOUS UPLOAD
-- This script adds Row Level Security policies to the `storage.objects` table
-- to allow anonymous users to upload and view files in a dedicated 'anonymous' folder.
-- This method is used because this Supabase project manages storage policies
-- directly on `storage.objects` instead of using the `storage.policies` table.

-- Policy 1: Allow anonymous users to upload into the 'anonymous' folder.
CREATE POLICY "Anonymous users can upload documents"
ON storage.objects FOR INSERT
TO anon
WITH CHECK (
    bucket_id = 'invoice-documents' AND
    (storage.foldername(name))[1] = 'anonymous'
);

-- Policy 2: Allow anonymous users to view documents within the 'anonymous' folder.
-- This is often necessary for the client-side to confirm a successful upload.
CREATE POLICY "Anonymous users can view documents in anonymous folder"
ON storage.objects FOR SELECT
TO anon
USING (
    bucket_id = 'invoice-documents' AND
    (storage.foldername(name))[1] = 'anonymous'
);
