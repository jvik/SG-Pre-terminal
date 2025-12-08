# Story 3.3: Export Budget Data

Status: done

## Story

As a user,
I want to export my transaction data to a CSV file,
So that I can perform my own analysis or keep a local backup.

## Acceptance Criteria

1.  **Given** a user is on their dashboard, **when** they click an "Export to CSV" button, **then** a `.csv` file is generated and downloaded by their browser.
2.  **And** the file contains all their income and expense transactions, including columns for date, description, category, and amount.

## Tasks / Subtasks

-   [x] **Backend: Create Export Endpoint** (AC: #1, #2)
    -   [ ] Create `backend/app/api/v1/endpoints/export.py`.
    -   [ ] Implement `GET /api/v1/export/csv` endpoint.
    -   [ ] Fetch all transactions for the authenticated user (joined with categories).
    -   [ ] Use Python's `csv` module to generate CSV content in memory.
    -   [ ] Return `StreamingResponse` with `media_type="text/csv"` and header `Content-Disposition: attachment; filename="export.csv"`.
    -   [ ] **Testing**: Add integration test in `backend/tests/api/v1/test_export.py` verifying status 200, headers, and CSV content structure.
-   [x] **Frontend: Add Export Button** (AC: #1)
    -   [ ] In `frontend/src/routes/dashboard/+page.svelte`, add an "Export to CSV" button.
    -   [ ] Implement the button click handler to trigger the download using `fetch` with the `Authorization` header.
    -   [ ] Handle the response as a `Blob`, create an object URL, and trigger a download via a hidden `<a>` tag.
    -   [ ] **Testing**: Update `dashboard/+page.svelte` tests to verify button presence and click interaction.

## Dev Notes

-   **Authentication for Download**: Since we use JWT in headers (`Authorization: Bearer ...`), a simple `<a href="...">` will NOT work because it doesn't send the header. The frontend MUST use `fetch` (or the API service wrapper) to get the file as a `Blob`, then create a temporary object URL (`URL.createObjectURL`) and trigger a download via a hidden `<a>` tag.
-   **CSV Format**:
    -   Headers: `Date`, `Description`, `Category`, `Amount`, `Type` (Income/Expense).
    -   Date format: ISO 8601 (`YYYY-MM-DD`).
    -   Amount: Decimal/Float.
-   **Performance**: For MVP, generating in memory is fine. If transactions > 5000, consider streaming from DB cursor to response.

### Project Structure Notes

-   New endpoint file: `backend/app/api/v1/endpoints/export.py`.
-   Register new router in `backend/app/api/v1/api.py`.

### Learnings from Previous Story

**From Story 3.2 (Status: done)**

-   **Reactivity**: While not strictly needed for the export *button*, remember that dashboard data is in Svelte stores.
-   **Database Aggregation**: (Not directly applicable here, but good to remember for efficiency).
-   **Testing**: Ensure backend tests validate the *content* of the CSV, not just the success status.
-   **Security**: Scoping to `user_id` is critical.

### References

-   [Source: docs/epics.md#Story-3.3-Export-Budget-Data]
-   [Source: docs/sprint-artifacts/tech-spec-epic-3.md#Detailed-Design]
-   [Source: docs/architecture.md#Architectural-Decisions]

## Dev Agent Record

### Context Reference

- docs/sprint-artifacts/3-3-export-budget-data.context.xml

### Agent Model Used

{{agent_model_name_version}}

### Debug Log References

### Completion Notes List

- ✅ Implemented Backend Export Endpoint (`GET /api/v1/export/csv`) with CSV generation and Supabase join.
- ✅ Implemented Frontend Export Button on Dashboard with Blob handling.
- ✅ Added comprehensive tests for backend endpoint and frontend button interaction.
- ✅ Verified all regression tests pass.

### File List

- excelence/backend/app/api/v1/endpoints/export.py
- excelence/backend/main.py
- excelence/backend/tests/api/v1/test_export.py
- excelence/frontend/src/lib/services/api.ts
- excelence/frontend/src/routes/dashboard/+page.svelte
- excelence/frontend/src/routes/dashboard/dashboard.test.ts

### Change Log
- 2025-12-07: Implemented backend export endpoint and frontend button.
- 2025-12-07: Senior Developer Review notes appended.

## Senior Developer Review (AI)

### Reviewer: BIP
### Date: Sunday, December 7, 2025
### Outcome: Approve

### Summary
The implementation delivers the requested CSV export functionality with a clean separation of concerns. The backend handles the data aggregation and streaming response correctly, while the frontend manages the secure download process. Code quality is consistent with the project's standards, and tests provide adequate coverage.

### Key Findings

- **[Low]** Hardcoded filename: The backend uses `filename="export.csv"`. It would be better to include a timestamp in the filename (e.g., `export_YYYY-MM-DD.csv`) to prevent overwrites and help users organize backups.
- **[Low]** Error Handling: The frontend `handleExport` function uses `alert()` for errors. A more integrated toast notification would be better for UX, though `alert` is acceptable for MVP.
- **[Low]** Performance: The current implementation iterates over all transactions in memory. While noted in Dev Notes as acceptable for MVP, large datasets will eventually require streaming from the database cursor directly to the response stream.

### Acceptance Criteria Coverage

| AC# | Description | Status | Evidence |
| :--- | :--- | :--- | :--- |
| 1 | Clicking "Export to CSV" generates and downloads a .csv file | **IMPLEMENTED** | `frontend/src/routes/dashboard/+page.svelte:44` (Button), `frontend/src/lib/services/api.ts:108` (Blob handling), `backend/app/api/v1/endpoints/export.py:46` (StreamingResponse) |
| 2 | File contains all transactions with correct columns (Date, Description, Category, Amount) | **IMPLEMENTED** | `backend/app/api/v1/endpoints/export.py:24` (Header row), `backend/app/api/v1/endpoints/export.py:38` (Data rows) |

**Summary:** 2 of 2 acceptance criteria fully implemented.

### Task Completion Validation

| Task | Marked As | Verified As | Evidence |
| :--- | :--- | :--- | :--- |
| Backend: Create Export Endpoint | **[x]** | **VERIFIED COMPLETE** | `backend/app/api/v1/endpoints/export.py` exists and implements logic. |
| Frontend: Add Export Button | **[x]** | **VERIFIED COMPLETE** | `frontend/src/routes/dashboard/+page.svelte` contains button and handler. |

**Summary:** 2 of 2 completed tasks verified.

### Test Coverage and Gaps
- **Backend:** `backend/tests/api/v1/test_export.py` covers happy path, empty state, and unauthorized access. It mocks the Supabase response structure correctly, including the joined category data.
- **Frontend:** `frontend/src/routes/dashboard/dashboard.test.ts` verifies the button renders and triggers the service call.

### Architectural Alignment
- Follows the API design pattern (endpoints in `api/v1/endpoints`).
- Uses SvelteKit stores and services correctly.
- Adheres to the security requirement of scoping data to `user_id`.

### Security Notes
- **Authorization:** correctly checks `get_current_user` dependency.
- **Data Isolation:** `eq('user_id', str(user_id))` ensures users can only export their own data.

### Best-Practices and References
- [FastAPI StreamingResponse](https://fastapi.tiangolo.com/advanced/custom-response/#streamingresponse) used correctly.
- [MDN: Blob](https://developer.mozilla.org/en-US/docs/Web/API/Blob) used correctly for client-side file creation.

### Action Items

**Code Changes Required:**
- (None)

**Advisory Notes:**
- Note: Consider adding a timestamp to the exported filename (e.g., `export_{date}.csv`) for better user experience.
- Note: For future scaling, refactor the backend to stream data directly from the DB cursor to the response iterator to avoid loading all transactions into memory.

