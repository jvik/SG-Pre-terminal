-- Add emoji column to categories table
ALTER TABLE "public"."categories" ADD COLUMN IF NOT EXISTS "emoji" TEXT;
