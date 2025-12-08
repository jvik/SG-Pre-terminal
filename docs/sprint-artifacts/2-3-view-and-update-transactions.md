# Story 2.3: View and Update Transactions

Status: review

## Story

As a user,
I want to view a list of my past transactions and be able to edit them,
so that I can review my financial history and correct any mistakes.

## Acceptance Criteria

1.  **Given** a user is viewing their transaction history, **when** they select a specific transaction to edit, **then** a form appears pre-filled with the transaction's details.
2.  **When** the user modifies and saves the changes, **then** the transaction is updated in the database and the list is refreshed.

## Tasks / Subtasks

- [x] **Backend: Create API Endpoint for Updating Transactions** (AC: #2)
    - [x] Implement `PUT /api/v1/transactions/{transaction_id}` endpoint in `backend/app/api/v1/endpoints/transactions.py`.
    - [x] Add business logic to `backend/app/crud/transactions.py` to update a transaction by its ID.
    - [x] Ensure the endpoint is protected and requires user authentication.
    - [x] Ensure the query is scoped to the authenticated `user_id` to prevent unauthorized access.
- [x] **Backend: Create API Endpoint for Listing Transactions** (AC: #1)
    - [x] Implement `GET /api/v1/transactions` endpoint in `backend/app/api/v1/endpoints/transactions.py`.
    - [x] Add business logic to `backend/app/crud/transactions.py` to retrieve all transactions for a user.
    - [x] Ensure the endpoint is protected and requires user authentication.
- [x] **Frontend: Create Transaction List Component** (AC: #1, #2)
    - [x] Create a new Svelte component `TransactionList.svelte` in `frontend/src/lib/components/routes/dashboard/`.
    - [x] The component should fetch and display a list of transactions from the `GET /api/v1/transactions` endpoint.
    - [x] Each row in the list should have an "Edit" button.
- [x] **Frontend: Implement Transaction Edit Modal** (AC: #1, #2)
    - [x] Reuse or create a `TransactionForm.svelte` modal component.
    - [x] When the "Edit" button is clicked, the modal should open with the selected transaction's data pre-filled.
    - [x] On form submission, the component should send a `PUT` request to `/api/v1/transactions/{transaction_id}`.
    - [x] After a successful update, the transaction list in the store should be refreshed to reflect the changes.
- [x] **[AI-Review][High] Enable and fix the skipped tests in `excelence/frontend/src/lib/components/shared/TransactionForm.svelte.test.ts`**

## Dev Notes

-   **API Naming:** The endpoint must be `PUT /api/v1/transactions/{transaction_id}`. [Source: `docs/architecture.md#API-Naming`]
-   **Database Naming:** The database table is `transactions` with snake_case columns. [Source: `docs/architecture.md#Database-Naming`]
-   **Error Handling:** The frontend API service should handle potential errors from the API, such as a `404 Not Found` if the transaction ID is invalid. [Source: `docs/architecture.md#Error-Handling`]
-   **Security:** All backend queries MUST be scoped to the `user_id` of the currently authenticated user to ensure data isolation. [Source: `docs/sprint-artifacts/tech-spec-epic-2.md#Security`]

### Project Structure Notes

-   The new frontend component `TransactionList.svelte` should be placed in `frontend/src/lib/components/routes/dashboard/` to align with the established project structure.
-   The backend logic will modify the existing `transactions.py` endpoint file and `crud/transactions.py` file.

### Learnings from Previous Story

**From Story 2.2 (Status: done)**

-   **Pydantic Models**: The previous story's review corrected Pydantic models to use UUIDs. Ensure all models in this story align with that pattern.
-   **Auth Pattern**: A consistent, header-based authentication dependency now exists at `excelence/backend/app/api/deps.py`. This **must** be used to protect the new transaction endpoints.
-   **Frontend Testing**: Frontend component tests are mandatory. A test file must be created for `TransactionList.svelte`.
-   **API Service**: Continue to use and extend the shared `api.ts` service in the frontend for all communication with the backend.

### References

-   [Source: docs/epics.md#Story-2.3-View-and-Update-Transactions]
-   [Source: docs/sprint-artifacts/tech-spec-epic-2.md#APIs-and-Interfaces]
-   [Source: docs/architecture.md#Project-Structure-and-Boundaries]

## Dev Agent Record

### Context Reference

- docs/sprint-artifacts/2-3-view-and-update-transactions.context.xml

### Agent Model Used

{{agent_model_name_version}}

### Debug Log References

### Completion Notes List

### File List
- `excelence/backend/app/api/v1/endpoints/transactions.py` (Modified)
- `excelence/frontend/src/lib/services/api.ts` (Modified)
- `excelence/frontend/src/lib/components/routes/dashboard/TransactionList.svelte` (Created)
- `excelence/frontend/src/lib/components/routes/dashboard/TransactionList.svelte.test.ts` (Created)
- `excelence/frontend/src/lib/components/shared/TransactionForm.svelte` (Modified)
- `excelence/frontend/src/lib/components/shared/TransactionForm.svelte.test.ts` (Modified)

## Senior Developer Review (AI)

- **Reviewer:** BIP
- **Date:** 2025-12-06
- **Outcome:** Changes Requested
- **Summary:** The implementation is functionally correct and meets the acceptance criteria. The backend API is well-implemented with correct security considerations. The frontend components are also correctly implemented. However, the tests for the `TransactionForm.svelte` component have been skipped, which goes against the project's testing standards.

### Key Findings
- **[High]** Tests for `TransactionForm.svelte` are skipped.

### Acceptance Criteria Coverage
| AC# | Description | Status | Evidence |
|---|---|---|---|
| 1 | Edit form appears pre-filled | IMPLEMENTED | `excelence/frontend/src/lib/components/shared/TransactionForm.svelte` |
| 2 | Transaction is updated and list refreshes | IMPLEMENTED | `excelence/frontend/src/lib/components/routes/dashboard/TransactionList.svelte` |

### Task Completion Validation
| Task | Marked As | Verified As | Evidence |
|---|---|---|---|
| Backend: Create API Endpoint for Updating Transactions | [x] | VERIFIED COMPLETE | `excelence/backend/app/api/v1/endpoints/transactions.py` |
| Backend: Create API Endpoint for Listing Transactions | [x] | VERIFIED COMPLETE | `excelence/backend/app/api/v1/endpoints/transactions.py` |
| Frontend: Create Transaction List Component | [x] | VERIFIED COMPLETE | `excelence/frontend/src/lib/components/routes/dashboard/TransactionList.svelte` |
| Frontend: Implement Transaction Edit Modal | [x] | VERIFIED COMPLETE | `excelence/frontend/src/lib/components/routes/dashboard/TransactionList.svelte` |

### Action Items
**Code Changes Required:**
- [x] [High] Enable and fix the skipped tests in `excelence/frontend/src/lib/components/shared/TransactionForm.svelte.test.ts`.

## Change Log
- 2025-12-06: Senior Developer Review notes appended.
- 2025-12-06: Second review complete. Story approved.

## Senior Developer Review (AI) - Round 2

- **Reviewer:** BIP
- **Date:** 2025-12-06
- **Outcome:** Approve
- **Summary:** The previous review's action item has been addressed, and all tests are now passing. The story is fully implemented and meets all acceptance criteria.

### Key Findings
- None.

### Action Items
- None.

