-- Disable Row Level Security on categories and transactions tables
-- The backend handles authentication and authorization
ALTER TABLE "public"."categories" DISABLE ROW LEVEL SECURITY;
ALTER TABLE "public"."transactions" DISABLE ROW LEVEL SECURITY;

-- Drop all existing policies since they're no longer needed
DROP POLICY IF EXISTS "Enable read access for users" ON "public"."categories";
DROP POLICY IF EXISTS "Enable insert for users" ON "public"."categories";
DROP POLICY IF EXISTS "Enable update for users" ON "public"."categories";
DROP POLICY IF EXISTS "Enable delete for users" ON "public"."categories";

DROP POLICY IF EXISTS "Enable read access for users" ON "public"."transactions";
DROP POLICY IF EXISTS "Enable insert for users" ON "public"."transactions";
DROP POLICY IF EXISTS "Enable update for users" ON "public"."transactions";
DROP POLICY IF EXISTS "Enable delete for users" ON "public"."transactions";
