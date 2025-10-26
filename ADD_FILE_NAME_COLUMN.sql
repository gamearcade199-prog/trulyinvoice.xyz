-- =====================================================
-- Add file_name column to documents table
-- =====================================================

-- Add file_name column if it doesn't exist
ALTER TABLE documents ADD COLUMN IF NOT EXISTS file_name TEXT;

-- If you have an old 'filename' column, copy data over and drop it
DO $$ 
BEGIN
    -- Check if old 'filename' column exists
    IF EXISTS (
        SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'documents' AND column_name = 'filename'
    ) THEN
        -- Copy data from old column to new one
        UPDATE documents SET file_name = filename WHERE file_name IS NULL;
        -- Drop the old column
        ALTER TABLE documents DROP COLUMN filename;
    END IF;
END $$;

-- Verify the change
SELECT column_name, data_type 
FROM information_schema.columns 
WHERE table_name = 'documents' 
ORDER BY ordinal_position;
