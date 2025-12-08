# Sprint Change Proposal: Technology Stack Realignment

**Date:** 2025-12-02
**Author:** Bob (Scrum Master)
**Status:** Proposed

---

## 1. Issue Summary

A strategic technical misalignment was identified requiring a course correction. The project's implementation needs to be updated to fully align with the architectural decisions and to standardize the development environment.

**Core Problems:**

1.  **Database Mismatch:** The backend was initialized using a template that relies on **SQLAlchemy** for database interaction. However, the `architecture.md` specifies **Supabase** as the chosen database platform. This change aligns the live implementation with the architectural blueprint.
2.  **Environment Inconsistency:** The project uses Python, but the method of running commands and managing packages is not standardized. All Python-related operations must be unified under the **`uv`** toolchain for performance and consistency.
3.  **Migration & Type Generation:** There is a need to formally define how database migrations and client-side type generation will be handled within the Supabase ecosystem.

---

## 2. Impact Analysis

The proposed changes are foundational and primarily affect the backend data layer and developer tooling.

### 2.1. Epic and Story Impact

The goals of the epics remain unchanged, but the implementation details for several stories will be significantly modified.

-   **Epic 1: Project Foundation & User Authentication:**
    -   **Story 1.2 (Implement User Registration):** The user creation logic will be rewritten to use the `supabase.auth.sign_up()` method instead of SQLAlchemy CRUD operations.
    -   **Story 1.3 (Implement User Login and Logout):** The authentication logic will use `supabase.auth.sign_in()` and `supabase.auth.sign_out()` instead of custom token generation with a database lookup.

-   **Epic 2: Core Financial Management:**
    -   **All Stories (2.1, 2.2, 2.3, 2.4):** All database CRUD (Create, Read, Update, Delete) operations for Categories and Transactions will be rewritten to use the `supabase-py` client library for interacting with Supabase tables.

-   **Epic 3: Dashboard, Visualization & Data Export:**
    -   **Stories 3.1, 3.2, 3.3:** The backend endpoints that serve data for the dashboard and exports will be modified to query Supabase for the necessary information.

### 2.2. Artifact Conflict and Impact

This change resolves existing conflicts and necessitates updates to tooling configurations.

-   **Architecture Document:** **RESOLVED CONFLICT.** The change brings the implementation into alignment with the document's decision to use Supabase. The document will be updated to include specific implementation patterns for the `supabase-py` client.
-   **PRD & UX Specification:** No impact. These documents are technology-agnostic.
-   **`justfile`:** This file will be updated to ensure all Python commands (e.g., `run`, `pip install`) are executed exclusively via `uv`.
-   **Backend Dependencies (`pyproject.toml` / `requirements.txt`):**
    -   **REMOVE:** `sqlalchemy`, `psycopg2-binary` (or other Postgres drivers).
    -   **ADD:** `supabase`, `gotrue`.

---

## 3. Recommended Approach

The recommended path forward is a **Direct Adjustment** of the current implementation.

-   **Rationale:** This is a necessary correction to build upon the correct technical foundation. It avoids future rework and technical debt. While it requires a one-time, medium-effort refactoring of the backend, it aligns the project with its documented architecture and modernizes the development environment. The MVP scope and project timeline are not expected to change.
-   **Risk:** Low. Supabase is a well-documented and robust platform. The changes are contained within the backend data access layer.

---

## 4. Detailed Change Proposals

### 4.1. Backend Refactoring: SQLAlchemy to Supabase

1.  **Dependency Update:** Modify backend dependencies to remove SQLAlchemy and add the Supabase client.
2.  **Database Connection:** Remove the SQLAlchemy database session management (`database.py`) and replace it with a Supabase client initialized with the project's URL and key from `.env` variables.
3.  **CRUD Operations:** Refactor all functions in the `backend/app/crud/` directory. All database queries will be rewritten from SQLAlchemy ORM syntax to Supabase's Python client syntax (e.g., `supabase.table('users').select('*').execute()`).
4.  **Authentication:** Rework the endpoints in `backend/app/api/v1/endpoints/auth.py` to use the Supabase `gotrue` client for user registration and login, leveraging the built-in JWT management.

### 4.2. Tooling Standardization: `uv`

1.  **`justfile` Update:** Audit and update all recipes in the `justfile`. Any instance of `python` or `pip` will be replaced with `uv run` and `uv pip` respectively to ensure consistent, high-performance execution.

### 4.3. Database Migrations and Type Generation

1.  **Migrations:** We will adopt the standard Supabase workflow for database migrations. Migrations will be written as plain `.sql` files and managed using the Supabase CLI. This ensures version-controlled, repeatable database schema changes.
2.  **Type Generation:** Supabase can automatically generate an OpenAPI (Swagger) specification for the database tables. We will use this feature to generate TypeScript interfaces for the frontend, ensuring type safety between the backend data and the SvelteKit application.

---

## 5. Implementation Handoff

-   **Recipient:** Development Team (AI Agent)
-   **Responsibilities:**
    1.  Execute the backend dependency changes.
    2.  Refactor the backend code as detailed above.
    3.  Update the `justfile` to standardize on `uv`.
    4.  Proceed with the implementation of Epic 1 stories using the new Supabase data layer.

This proposal outlines a clear path to correct the project's technical foundation. Upon approval, I will proceed with these changes.
