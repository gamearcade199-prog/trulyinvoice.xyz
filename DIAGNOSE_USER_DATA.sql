-- This is a diagnostic script to help debug the "406 Not Acceptable" error.
-- It does not make any changes to your database.
-- Please run this query in your Supabase SQL Editor and share the results from all three queries.

-- Query 1: Get the ID of the currently logged-in user.
-- This helps us confirm the user ID that the security policies are using.
SELECT auth.uid() as current_user_id;

-- Query 2: Check for a matching user in the public.users table.
-- This will show if a public profile exists for the logged-in user.
-- If this returns no rows, it is the cause of the 406 error.
SELECT * FROM public.users WHERE id = auth.uid();

-- Query 3: List all Row Level Security policies on the public.users table.
-- This will show us exactly which security policies are active on the table.
SELECT
    policyname,
    permissive,
    cmd,
    qual,
    with_check
FROM
    pg_policies
WHERE
    schemaname = 'public' AND tablename = 'users';
