# Story 2.2: Record Income and Expenses

Status: ready-for-dev

## Dev Agent Record

- Context Reference: [2-2-record-income-and-expenses.context.xml](./2-2-record-income-and-expenses.context.xml)
- Change Log:
    - 2025-12-06: Addressed review blockers. Implemented frontend dashboard UI, corrected backend Pydantic models to use UUIDs, and improved frontend component tests.


## Story

As a user,
I want to add new income and expense entries,
So that I can keep an accurate record of my finances.

## Acceptance Criteria

1.  **Given** a user is on the main dashboard
2.  **When** they open the "Add Transaction" form and enter an amount, select a category, and a date for an income or expense
3.  **Then** a new record is created in the `transactions` table in the database.
4.  **And** the main dashboard immediately updates to reflect the new entry.

## Tasks / Subtasks

- [x] Task 1: Implement Backend API for Transactions (AC: 3)
    - [x] Subtask 1.1: Define the `transactions` table model as per the tech spec. (Note: To be implemented via Supabase client, following the pattern from Story 2.1).
    - [x] Subtask 1.2: Create Pydantic schemas for transaction data within the endpoint file.
    - [x] Subtask 1.3: Create a `POST /api/v1/transactions` endpoint in a new `excelence/backend/app/api/v1/endpoints/transactions.py` file.
    - [x] Subtask 1.4: Secure the endpoint using the existing authentication dependency (`app/api/deps.py`).
    - [x] Subtask 1.5: Ensure all database operations are strictly scoped to the authenticated user.
    - [x] Subtask 1.6: Add unit tests for the new endpoint in `excelence/backend/tests/api/v1/test_transactions.py`.
- [x] Task 2: Implement Frontend UI for Adding Transactions (AC: 1, 2, 4)
    - [x] Subtask 2.1: Create a reusable `TransactionForm.svelte` modal component.
    - [x] Subtask 2.2: Add a button to the main dashboard to open the transaction modal.
    - [x] Subtask 2.3: The form's category dropdown must be populated by fetching data from the `/api/v1/categories` endpoint.
    - [x] Subtask 2.4: Integrate the form with the `POST /api/v1/transactions` endpoint using the `api.ts` service.
    - [x] Subtask 2.5: Ensure the UI updates reactively after a new transaction is successfully added.
    - [x] Subtask 2.6: Add component tests for the `TransactionForm.svelte` component.

## Dev Notes

-   **Security:** This is a critical endpoint. It is mandatory to reuse the robust, header-based authentication dependency established in Story 2.1, located at `excelence/backend/app/api/deps.py`. All database queries must be filtered by `user_id` to prevent data leakage between users.
-   **Reactivity:** The frontend implementation should ensure that upon successful creation of a transaction, the main dashboard's transaction list and any financial summaries update instantly without requiring a page reload.
-   **Error Handling:** The form should gracefully handle and display any validation errors returned from the API (e.g., invalid amount, missing category).

### Project Structure Notes

-   New backend logic for transactions will be in `excelence/backend/app/api/v1/endpoints/transactions.py`.
-   New backend tests will be in `excelence/backend/tests/api/v1/test_transactions.py`.
-   The new frontend component will be a reusable modal, suggested path: `excelence/frontend/src/lib/components/shared/TransactionForm.svelte`.

### Learnings from Previous Story

**From Story 2.1 (Status: done)**

-   **Auth Pattern Established**: A consistent, header-based authentication dependency now exists at `excelence/backend/app/api/deps.py`. This **must** be used to protect the new transaction endpoints.
-   **Testing is Mandatory**: The previous story was blocked because a frontend component test file was missing (Subtask 2.6). It is critical to create and implement `TransactionForm.svelte.test.ts` to avoid a similar block.
-   **API Service**: Continue to use and extend the shared `api.ts` service in the frontend for all communication with the backend.

### References

-   [Source: docs/epics.md#story-2-2-record-income-and-expenses]
-   [Source: docs/sprint-artifacts/tech-spec-epic-2.md#apis-and-interfaces]
-   [Source: docs/sprint-artifacts/tech-spec-epic-2.md#data-models-and-contracts]
-   [Source: docs/architecture.md#4-project-structure-and-boundaries]


