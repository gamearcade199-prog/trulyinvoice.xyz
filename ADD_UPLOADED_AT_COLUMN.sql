-- Add uploaded_at column to documents table
ALTER TABLE documents
ADD COLUMN uploaded_at TIMESTAMPTZ DEFAULT NOW();
