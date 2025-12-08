-- Create categories table
CREATE TABLE IF NOT EXISTS "public"."categories" (
    "id" uuid DEFAULT extensions.uuid_generate_v4() NOT NULL,
    "created_at" timestamp with time zone DEFAULT timezone('utc'::text, now()) NOT NULL,
    "name" character varying NOT NULL,
    "user_id" uuid NOT NULL,
    CONSTRAINT "categories_pkey" PRIMARY KEY ("id")
);

-- Create transactions table
CREATE TABLE IF NOT EXISTS "public"."transactions" (
    "id" uuid DEFAULT extensions.uuid_generate_v4() NOT NULL,
    "created_at" timestamp with time zone DEFAULT timezone('utc'::text, now()) NOT NULL,
    "amount" numeric NOT NULL,
    "type" character varying NOT NULL,
    "date" date NOT NULL,
    "description" text,
    "category_id" uuid NOT NULL,
    "user_id" uuid NOT NULL,
    CONSTRAINT "transactions_pkey" PRIMARY KEY ("id")
);

-- Add foreign keys
ALTER TABLE ONLY "public"."categories"
    ADD CONSTRAINT "categories_user_id_fkey" FOREIGN KEY ("user_id") REFERENCES "auth"."users"("id") ON DELETE CASCADE;

ALTER TABLE ONLY "public"."transactions"
    ADD CONSTRAINT "transactions_user_id_fkey" FOREIGN KEY ("user_id") REFERENCES "auth"."users"("id") ON DELETE CASCADE;

ALTER TABLE ONLY "public"."transactions"
    ADD CONSTRAINT "transactions_category_id_fkey" FOREIGN KEY ("category_id") REFERENCES "public"."categories"("id") ON DELETE RESTRICT;

-- Enable Row Level Security
ALTER TABLE "public"."categories" ENABLE ROW LEVEL SECURITY;
ALTER TABLE "public"."transactions" ENABLE ROW LEVEL SECURITY;

-- Create policies for categories
CREATE POLICY "Users can view their own categories" ON "public"."categories"
    FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users can insert their own categories" ON "public"."categories"
    FOR INSERT WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update their own categories" ON "public"."categories"
    FOR UPDATE USING (auth.uid() = user_id) WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can delete their own categories" ON "public"."categories"
    FOR DELETE USING (auth.uid() = user_id);

-- Create policies for transactions
CREATE POLICY "Users can view their own transactions" ON "public"."transactions"
    FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users can insert their own transactions" ON "public"."transactions"
    FOR INSERT WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update their own transactions" ON "public"."transactions"
    FOR UPDATE USING (auth.uid() = user_id) WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can delete their own transactions" ON "public"."transactions"
    FOR DELETE USING (auth.uid() = user_id);

-- Grant permissions
GRANT ALL ON TABLE "public"."categories" TO "anon";
GRANT ALL ON TABLE "public"."categories" TO "authenticated";
GRANT ALL ON TABLE "public"."categories" TO "service_role";

GRANT ALL ON TABLE "public"."transactions" TO "anon";
GRANT ALL ON TABLE "public"."transactions" TO "authenticated";
GRANT ALL ON TABLE "public"."transactions" TO "service_role";
