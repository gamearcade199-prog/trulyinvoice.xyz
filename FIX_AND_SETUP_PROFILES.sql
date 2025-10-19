-- This is the complete and final script to fix all user profile and authentication issues.
-- It corrects the database structure and sets up automatic profile creation.

-- Step 1: Fix the public.users table structure.
-- The 'hashed_password' column should not be in this table. It's a security risk
-- and prevents new user profiles from being created. This command removes it.
ALTER TABLE public.users DROP COLUMN IF EXISTS hashed_password;


-- Step 2: Clean up the old, conflicting RLS policies.
-- This removes the redundant SELECT policies to avoid any conflicts.
DROP POLICY IF EXISTS "Users can view own data" ON public.users;
DROP POLICY IF EXISTS "Users can view own profile" ON public.users;
-- We will keep "Allow individual users to read their own data" as the single source of truth.


-- Step 3: Create a function to automatically create a user profile.
-- This function will be triggered whenever a new user signs up. It takes the new
-- user's ID and email from the `auth.users` table and inserts it into `public.users`.
CREATE OR REPLACE FUNCTION public.handle_new_user()
RETURNS TRIGGER AS $$
BEGIN
  INSERT INTO public.users (id, email)
  VALUES (new.id, new.email);
  RETURN new;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;


-- Step 4: Create a trigger that runs the function after a new user is created.
-- This trigger is attached to the `auth.users` table and will fire `AFTER INSERT`,
-- meaning it runs right after a new user successfully signs up.
-- We drop the old trigger first to ensure this script can be run safely multiple times.
DROP TRIGGER IF EXISTS on_auth_user_created ON auth.users;
CREATE TRIGGER on_auth_user_created
  AFTER INSERT ON auth.users
  FOR EACH ROW EXECUTE PROCEDURE public.handle_new_user();


-- Step 5: Manually create a profile for the existing test user.
-- The trigger only works for new sign-ups, so we need to manually create a
-- profile for the user that is already in the system.
-- This command checks if the user already exists before inserting to avoid errors.
INSERT INTO public.users (id, email)
SELECT id, email FROM auth.users WHERE email = 'gamearcade199@gmail.com'
ON CONFLICT (id) DO NOTHING;


-- After running this script, all authentication and profile-related issues
-- should be permanently resolved.
