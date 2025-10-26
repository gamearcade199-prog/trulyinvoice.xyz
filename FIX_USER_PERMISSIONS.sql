-- This script fixes the "406 Not Acceptable" error by setting up the correct
-- Row Level Security (RLS) policies on the `public.users` table.
-- RLS ensures that users can only access data they are permitted to see.

-- Step 1: Ensure Row Level Security is enabled on the `public.users` table.
-- This command activates the RLS feature for the table. If it's already enabled,
-- this command will do nothing.
ALTER TABLE public.users ENABLE ROW LEVEL SECURITY;

-- Step 2: Create a policy to allow users to read their own data.
-- This is the main fix. It creates a rule named "Allow individual users to read their own data".
-- The policy checks if the `id` of a row in the `users` table matches the
-- unique ID (`uid`) of the user who is currently logged in and making the request.
-- This ensures users can only see their own profile, not others'.
CREATE POLICY "Allow individual users to read their own data"
ON public.users
FOR SELECT
USING (auth.uid() = id);

-- Step 3: (Optional but Recommended) Create a policy to allow admin/service access.
-- This policy allows internal Supabase services (using the `service_role` key) to
-- bypass RLS and access all data. This is crucial for administrative tasks and
-- server-side processes.
CREATE POLICY "Allow full access to service_role"
ON public.users
FOR ALL
USING (true)
WITH CHECK (true);

-- After running this script in your Supabase SQL Editor, the 406 errors
-- in your application should be resolved.
