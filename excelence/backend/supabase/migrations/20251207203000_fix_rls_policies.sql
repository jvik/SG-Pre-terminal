-- Drop existing policies
DROP POLICY IF EXISTS "Users can view their own categories" ON "public"."categories";
DROP POLICY IF EXISTS "Users can insert their own categories" ON "public"."categories";
DROP POLICY IF EXISTS "Users can update their own categories" ON "public"."categories";
DROP POLICY IF EXISTS "Users can delete their own categories" ON "public"."categories";

DROP POLICY IF EXISTS "Users can view their own transactions" ON "public"."transactions";
DROP POLICY IF EXISTS "Users can insert their own transactions" ON "public"."transactions";
DROP POLICY IF EXISTS "Users can update their own transactions" ON "public"."transactions";
DROP POLICY IF EXISTS "Users can delete their own transactions" ON "public"."transactions";

-- Create new policies for categories that work with service_role
CREATE POLICY "Enable read access for users" ON "public"."categories"
    FOR SELECT USING (
        auth.uid() = user_id OR 
        auth.jwt()->>'role' = 'service_role'
    );

CREATE POLICY "Enable insert for users" ON "public"."categories"
    FOR INSERT WITH CHECK (
        auth.uid() = user_id OR 
        auth.jwt()->>'role' = 'service_role'
    );

CREATE POLICY "Enable update for users" ON "public"."categories"
    FOR UPDATE USING (
        auth.uid() = user_id OR 
        auth.jwt()->>'role' = 'service_role'
    ) WITH CHECK (
        auth.uid() = user_id OR 
        auth.jwt()->>'role' = 'service_role'
    );

CREATE POLICY "Enable delete for users" ON "public"."categories"
    FOR DELETE USING (
        auth.uid() = user_id OR 
        auth.jwt()->>'role' = 'service_role'
    );

-- Create new policies for transactions
CREATE POLICY "Enable read access for users" ON "public"."transactions"
    FOR SELECT USING (
        auth.uid() = user_id OR 
        auth.jwt()->>'role' = 'service_role'
    );

CREATE POLICY "Enable insert for users" ON "public"."transactions"
    FOR INSERT WITH CHECK (
        auth.uid() = user_id OR 
        auth.jwt()->>'role' = 'service_role'
    );

CREATE POLICY "Enable update for users" ON "public"."transactions"
    FOR UPDATE USING (
        auth.uid() = user_id OR 
        auth.jwt()->>'role' = 'service_role'
    ) WITH CHECK (
        auth.uid() = user_id OR 
        auth.jwt()->>'role' = 'service_role'
    );

CREATE POLICY "Enable delete for users" ON "public"."transactions"
    FOR DELETE USING (
        auth.uid() = user_id OR 
        auth.jwt()->>'role' = 'service_role'
    );
