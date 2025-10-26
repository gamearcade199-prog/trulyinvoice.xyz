-- This script verifies and fixes Row Level Security (RLS) on the public.users table.
-- It is designed to be run multiple times safely, as it will remove old policies
-- before creating new ones to prevent conflicts.

-- Step 1: Drop the existing policies to ensure a clean slate.
-- This prevents conflicts if the policies were created incorrectly before.
-- It's safe to run this even if the policies don't exist.
DROP POLICY IF EXISTS "Allow individual users to read their own data" ON public.users;
DROP POLICY IF EXISTS "Allow full access to service_role" ON public.users;

-- Step 2: Ensure RLS is enabled on the table.
-- This is often a missed step, but it's crucial for policies to work.
ALTER TABLE public.users ENABLE ROW LEVEL SECURITY;

-- Step 3: Recreate the policy to allow users to read their own data.
-- This policy allows a logged-in user to view their own record in the public.users table
-- by matching their authentication ID (auth.uid()) with the 'id' column.
CREATE POLICY "Allow individual users to read their own data"
ON public.users
FOR SELECT
USING (auth.uid() = id);

-- Step 4: Recreate the policy for service roles (important for backend functions).
-- This allows internal Supabase services to bypass RLS, which is necessary for
-- administrative tasks.
CREATE POLICY "Allow full access to service_role"
ON public.users
FOR ALL
USING (true)
WITH CHECK (true);

-- After running this script, please refresh your application. The 406 error should be resolved.
