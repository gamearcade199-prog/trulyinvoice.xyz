-- Question 1: How many invoices exist?
SELECT COUNT(*) as total_invoices FROM invoices;

-- Question 2: Show me ALL invoice IDs
SELECT id, vendor_name, total_amount FROM invoices ORDER BY created_at DESC LIMIT 20;

-- Question 3: Show me the FIRST/LAST invoice in full detail
SELECT * FROM invoices ORDER BY created_at DESC LIMIT 1;

-- Question 4: Check if documents table has data
SELECT COUNT(*) as total_documents FROM documents;

-- Question 5: Show all documents
SELECT id, file_name, user_id, created_at FROM documents ORDER BY created_at DESC LIMIT 20;

-- Question 6: Are invoices linked to documents?
SELECT 
  i.id as invoice_id,
  i.vendor_name,
  i.document_id,
  d.file_name,
  CASE WHEN d.id IS NULL THEN 'NOT LINKED' ELSE 'LINKED' END as status
FROM invoices i
LEFT JOIN documents d ON i.document_id = d.id
LIMIT 20;

-- Question 7: Are users created?
SELECT id, email FROM users LIMIT 20;

-- Question 8: Do invoices have user_id?
SELECT 
  COUNT(*) as total,
  COUNT(CASE WHEN user_id IS NULL THEN 1 END) as no_user_id,
  COUNT(CASE WHEN user_id IS NOT NULL THEN 1 END) as has_user_id
FROM invoices;
