# Supabase Development Workflow

This document outlines the standard procedures for managing the Supabase database, including migrations and client-side type generation.

## Database Migrations

All database schema changes (e.g., creating tables, adding columns) MUST be managed via Supabase's built-in migration system. This ensures a version-controlled and repeatable process.

### Workflow

1.  **Install the Supabase CLI:** If you haven't already, install the CLI following the [official documentation](https://supabase.com/docs/guides/cli).

2.  **Link the Project:** Link your local repository to your Supabase project. You will only need to do this once.
    ```bash
    supabase link --project-ref <your-project-ref>
    ```

3.  **Create a New Migration:** To create a new migration file for a schema change, use the following command. This will generate a new `.sql` file in the `supabase/migrations` directory.
    ```bash
    supabase migration new <migration_name>
    ```

4.  **Develop Locally:** Use `supabase start` to run a local instance of Supabase in Docker. This is highly recommended for development to avoid breaking the remote database.

5.  **Apply Migrations:** To apply local migrations to your remote Supabase project, run:
    ```bash
    supabase db push
    ```

## Client-Side Type Generation

To ensure type safety between the backend database and the frontend application, we will use Supabase's ability to generate an OpenAPI specification.

### Workflow

1.  **Generate Types:** Use the Supabase CLI to generate TypeScript types from your database schema.
    ```bash
    supabase gen types typescript --project-id <your-project-ref> --schema public > ../frontend/src/lib/types/supabase.ts
    ```

2.  **Frequency:** This command should be run whenever there is a change to the database schema (i.e., after running `supabase db push`) to keep the frontend types in sync with the database.
