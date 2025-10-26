-- Check all RLS policies and table status for invoices and documents

-- 1. Show RLS status for invoices and documents tables
SELECT tablename, rowsecurity as rls_enabled
FROM pg_tables
WHERE schemaname = 'public'
  AND tablename IN ('invoices', 'documents');

-- 2. List all RLS policies for invoices and documents
SELECT tablename, policyname, cmd, roles, qual, with_check
FROM pg_policies
WHERE schemaname = 'public'
  AND tablename IN ('invoices', 'documents');

-- 3. Show table structure for invoices and documents
SELECT table_name, column_name, data_type, is_nullable, column_default
FROM information_schema.columns
WHERE table_schema = 'public'
  AND table_name IN ('invoices', 'documents')
ORDER BY table_name, ordinal_position;

-- 4. Show foreign key constraints for invoices and documents
SELECT tc.constraint_name, tc.table_name, kcu.column_name, ccu.table_name AS foreign_table_name, ccu.column_name AS foreign_column_name
FROM information_schema.table_constraints AS tc
JOIN information_schema.key_column_usage AS kcu
  ON tc.constraint_name = kcu.constraint_name
  AND tc.table_schema = kcu.table_schema
JOIN information_schema.constraint_column_usage AS ccu
  ON ccu.constraint_name = tc.constraint_name
  AND ccu.table_schema = tc.table_schema
WHERE tc.constraint_type = 'FOREIGN KEY'
  AND tc.table_schema = 'public'
  AND tc.table_name IN ('invoices', 'documents');

-- 5. Try a test insert (replace <category_id> and <document_id> with real values)
-- INSERT INTO invoices (category_id, document_id) VALUES ('<category_id>', '<document_id>');
